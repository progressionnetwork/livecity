import pandas as pd

def Parse(path: str)-> dict:
    df = pd.read_excel(path)
    df =df.dropna()
    for index, row in df.iterrows():
        kpgz_id = row['КПГЗ'].split(' ')[0]
        spgz = row['СПГЗ'].split(',')[0].strip()
        key = row['Ключевые слова']
        yield {
            "kpgz_id": kpgz_id,
            "spgz": spgz,
            "key": key
        }


if __name__ == '__main__':
    path = r'C:\Users\ruha\Downloads\Telegram Desktop\Исходные данные\Ключевые фразы по СПГЗ.xlsx'
    for i in Parse(path):
        print(i)
