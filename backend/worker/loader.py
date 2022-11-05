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

def _get_instanse_with_type_update(model: object, type_update:str, data: dict, *args, **kwargs)->object:
    if type_update == 'full':
        instance, created = model.objects.update_or_create(defaults=data, *args, **kwargs)
    else:
        instance, created = model.objects.get_or_create(defaults=data, *args, **kwargs)
    return (instance, created)

def load_sn(path: str, type_update:str)-> None:
    from parser.smeta import Parse
    logger.info(f"Start parsing file: {path}")
    sn = Parse(path)[0]
    sections = sn.pop('sections')
    o_sn, created = _get_instanse_with_type_update(model=SN, 
        type_update=type_update, 
        data={
            "type_ref" : str(sn['type_ref'] if sn['type_ref']!='null' else ''), 
            "advance" :  str(sn['advance'] if sn['advance']!='null' else ''),
            "coef_ref" : str(sn['coef_ref'] if sn['coef_ref']!='null' else ''),
            "coef_date" : sn['coef_date'],
            "sum" : float(sn['sum'] if sn['sum'] is not None else 0),
            "tax" : float(sn['tax'] if sn['tax'] is not None else 0),
            "sum_with_tax" : float(sn['sum_with_tax']  if sn['sum_with_tax'] is not None else 0),
            "sum_with_ko" : float(sn['sum_with_ko'] if sn['sum_with_ko'] is not None else 0)}, 
        type_ref = str(sn['type_ref'] if sn['type_ref']!='null' else ''))
    for section in sections:
        subsections = section.pop('subsections')
        o_section, created = _get_instanse_with_type_update(model=SNSection,
            type_update=type_update,
            data={
                "name" :  str(section['name'] if section['name']!='null' else ''),
                "sum": float(section['sum']  if section['sum'] is not None else 0),
                "sn": o_sn
            },
            name=str(section['name'] if section['name']!='null' else ''))
        for subsection in subsections:
            rows = subsection.pop('rows')
            o_subsection, created = _get_instanse_with_type_update(model=SNSubsection,
                type_update=type_update,
                data={
                    "name" :  str(subsection['name'] if subsection['name']!='null' else ''),
                    "sum": float(subsection['sum']  if subsection['sum'] is not None else 0),
                    "sn_section": o_section
                },
                name=str(subsection['name'] if subsection['name']!='null' else ''))
            for row in rows:
                subrows = row.pop('subrows')
                ei = row.pop('ei')
                o_row, created = _get_instanse_with_type_update(model=SNRow, 
                    type_update=type_update,
                    data = {
                        "sn_subsection" : o_subsection,
                        "code" : str(row['code'] if row['code']!='null' else ''),
                        "num" : int(row['num'] if row['num'] is not None else 0),
                        "name" : str(row['name'] if row['name']!='null' else ''),
                        "ei" : OKEI.objects.filter(short_name=ei).first(),
                        "count" : float(row['count'] if row['count'] is not None else 0),
                        "sum" : float(row['sum'] if row['sum'] is not None else 0)
                    }, 
                    code = str(row['code'] if row['code']!='null' else ''))
                for subrow in subrows:
                    o_subrow, created = _get_instanse_with_type_update(model=SNSubRow,
                    type_update=type_update,
                    data = {
                        "sn_row" : o_row,
                        "name" : str(subrow['name'] if subrow['name']!='null' else ''),
                        "ei" : OKEI.objects.filter(short_name=ei).first(),
                        "count" : float(subrow.get('count') if subrow.get('count') is not None else 0),
                        "amount" : float(subrow.get('amount') if subrow.get('amount') is not None else 0),
                        "coef_correct" : float(subrow.get('coef_correct') if subrow.get('coef_correct') is not None else 0),
                        "coef_winter" : float(subrow.get('coef_winter') if subrow.get('coef_winter') is not None else 0),
                        "coef_recalc" : float(subrow.get('coef_recalc') if subrow.get('coef_recalc') is not None else 0),
                        "sum_basic" : float(subrow.get('sum_basic') if subrow.get('sum_basic') is not None else 0),
                        "sum_current" : float(subrow.get('sum_current') if subrow.get('sum_current') is not None else 0)
                    }, name = str(subrow['name'] if subrow['name']!='null' else ''))
    logger.info('SN/TSN file updated.')


def load_spgz(path: str, type_update:str) -> None:
    from parser.spgz import Parse
    for row in Parse(path):
        row['kpgz'], created = KPGZ.objects.get_or_create(code=row['kpgz'], defaults={"code":row['kpgz'], "name": row['kpgz_name'].capitalize()})
        row.pop('kpgz_name')
        row['okpd'] = OKPD.objects.filter(code=row['okpd']).first()
        row['okpd2'] = OKPD2.objects.filter(code=row['okpd2']).first()
        eis = row.pop('ei')
        if type_update == 'full':
            spgz, created = SPGZ.objects.update_or_create(defaults=row, id=row['id'])
        else:
            spgz, created = SPGZ.objects.get_or_create(defaults=row, id=row['id']) 
        if created:
            for ei in eis:
                ei_o = OKEI.objects.filter(name=ei).first() if ei is not None else None
                if ei_o:
                    spgz.ei.add(ei_o) 
        spgz.save()
    logger.info('SPGZ file updated.')

def load_tz(path: str, type_update:str) -> None:
    from parser.tz import Parse
    for row in Parse(path):
        tz, created = TZ.objects.get_or_create(name=row['name'].capitalize(), defaults={"name": row['name'].capitalize()})
        if created:
            for kpgz_spgz in row['rows']:
                kpgz = KPGZ.objects.filter(pk=kpgz_spgz['kpgz_id']).first()
                spgz = SPGZ.objects.filter(pk=int(kpgz_spgz['spgz_id'])).first()
                if kpgz and spgz:
                    tz_row = TZRow(kpgz=kpgz, spgz=spgz, tz=tz)
                    tz_row.save()
        tz=None
    logger.info('TZ file updated.')

def load_from_file(type_data: str, path: str, type_update: str) -> None:
    threads = []
    match type_data:
        case 'sn': 
            t = threading.Thread(target=load_sn, args=[path, type_update])
            t.start()
            threads.append(t)
        case 'spgz':
            t = threading.Thread(target=load_spgz, args=[path, type_update])
            t.start()
            threads.append(t)
        case 'tz':
            t = threading.Thread(target=load_tz, args=[path, type_update])
            t.start()
            threads.append(t)
    return None

def callback(ch, method, properties, body):
    message = json.loads(body)
    logger.info(f"Incomming message: {message}")

    type_data = message['type_data']
    source = message['source']
    path = message.get('path', None)
    type_update = message.get('type_update', None)

    if source == SOURCE_INTERNET:
        load_from_internet(type_data)
    else:
        load_from_file(type_data, path, type_update)

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