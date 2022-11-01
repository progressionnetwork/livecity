import sys, os, json, time
import logging
import django
import pika
import threading
from pathlib import Path
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# add django project and models
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livecity.settings')
django.setup()
from core.models import *

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE_INTERNET='internet'
SOURCE_FILE='file'

def model_mapper(type_data: str, data: dict, source: str)-> object | None:
    # fix mapper for file
    if data is None:
        return None
    try:
        match type_data:
            case 'KPGZ': 
                return KPGZ.objects.update_or_create(
                    defaults={  'code' : data.get('kpgzCode',''), 
                                'name' : data.get('kpgzName','').capitalize()},
                    code=data.get('kpgzCode',''))
            case 'OKEI':
                return OKEI.objects.update_or_create(
                    defaults={  'code' : data.get('CODE',''), 
                                'name' : data.get('NAME','').capitalize(),
                                'short_name' : data.get('NATIONAL','').lower()},
                    code=data.get('CODE',''))
            case 'OKPD':
                return OKPD.objects.update_or_create(
                    defaults={  'code' : data.get('Kod',''), 
                                'name' : data.get('Name','').capitalize()},
                    code=data.get('Kod',''))
            case 'OKPD2':
                return OKPD2.objects.update_or_create(
                    defaults={  'code' : data.get('Kod',''), 
                                'name' : data.get('Name','').capitalize()},
                    code=data.get('CODE',''))
            case _: return None
    except Exception as error:
        logger.error(str(error))
        
        return None

def count_rows_from_internet(type_data: str) -> int:
    session = Session()
    match type_data:
        case 'KPGZ': url=f"https://apidata.mos.ru/v1/datasets/2586/count?api_key=486cbf89d2ca71bde32fa9b559ad5956"
        case 'OKEI': url=f"https://apidata.mos.ru/v1/datasets/2744/count?api_key=486cbf89d2ca71bde32fa9b559ad5956"
        case 'OKPD': url=f"https://apidata.mos.ru/v1/datasets/2313/count?api_key=486cbf89d2ca71bde32fa9b559ad5956"
        case 'OKPD2': url=f"https://apidata.mos.ru/v1/datasets/2752/count?api_key=486cbf89d2ca71bde32fa9b559ad5956"
        case _: return None
    try:
        logger.info(f"Send request to {url}")
        response = session.get(url=url)
        data = int(response.text)
        return data if data else 0
    except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        logger.error(f'{e=}')
        return 0

def load_chunk_from_internet(type_data: str, limit: int, offset: int) -> None:
    session = Session()
    match type_data:
        case 'KPGZ': url=f"https://apidata.mos.ru/v1/datasets/2586/rows?$orderby=global_id&api_key=486cbf89d2ca71bde32fa9b559ad5956&$top={limit}&$skip={offset}"
        case 'OKEI': url=f"https://apidata.mos.ru/v1/datasets/2744/rows?$orderby=global_id&api_key=486cbf89d2ca71bde32fa9b559ad5956&$top={limit}&$skip={offset}&$filter=Cells/CODE ne ''"
        case 'OKPD': url=f"https://apidata.mos.ru/v1/datasets/2313/rows?$orderby=global_id&api_key=486cbf89d2ca71bde32fa9b559ad5956&$top={limit}&$skip={offset}"
        case 'OKPD2': url=f"https://apidata.mos.ru/v1/datasets/2752/rows?$orderby=global_id&api_key=486cbf89d2ca71bde32fa9b559ad5956&$top={limit}&$skip={offset}"
        case _: return None
    try:
        logger.info(f"Send request to {url}")
        response = session.get(url=url)
        data = json.loads(response.text)
        # logger.info(f"Get response: {data}")
        for row in data: 
            if isinstance(row, str):
                time.sleep(5)
                logger.error(f"Error receive information from {url}")
                load_chunk_from_internet(type_data, limit, offset)
            if isinstance(row, dict):
                model_mapper(type_data, row.get('Cells', None), 'internet')
        logger.info(f"Received all data from {url}")
    except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        logger.error(f'{e=}')
        return None

def load_from_internet(type_data: str, chunk_size: int = 1000) -> None:
    count = count_rows_from_internet(type_data)
    threads = []
    for offset in range(0, count, chunk_size):
        thread = threading.Thread(target=load_chunk_from_internet, args=(
            type_data, chunk_size, offset
            ))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def load_sn(path: str)-> None:
    from parser.sn import Parse
    logger.info(f"Start parsing file: {path}")
    l = Parse(path)
    logger.info(l[:1][:5])


def load_from_file(type_data: str, path: str) -> None:
    threads = []
    match type_data:
        case 'SN': 
            t = threading.Thread(target=load_sn, args=[path])
            t.start()
            threads.append(t)
    return None

def callback(ch, method, properties, body):
    message = json.loads(body)
    logger.info(f"Incomming message: {message}")

    type_data = message['type_data']
    source = message['source']
    path = message.get('path', None)

    if source == SOURCE_INTERNET:
        load_from_internet(type_data)
    else:
        load_from_file(type_data, path)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info("ACK sended")


def start_worker(queue: str):
    connection = pika.BlockingConnection(parameters=pika.URLParameters(os.getenv('RABBITMQ_URL')))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(on_message_callback=callback, queue=queue)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_worker(queue=sys.argv[1])