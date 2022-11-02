import pandas as pd

def Parse(path: str)-> dict:
    df = pd.read_excel(path)
    for index, row in df.iterrows():
        id = row['ID'] if pd.notna(row['ID']) else 0
        kpgz = row['КПГЗ'].split(' ')[0] if pd.notna(row['КПГЗ']) else None
        name = row['Наименование СПГЗ'].strip() if pd.notna(row['Наименование СПГЗ']) else ''
        ei = row['Единицы измерения'].lower() if pd.notna(row['Единицы измерения']) else None
        okpd = row['ОКПД'] if pd.notna(row['ОКПД'])  else None
        okpd2 = row['ОКПД 2'] if pd.notna(row['ОКПД 2']) else None
        if ei is not None:
            ei = ei.split(',')
            if len(ei) == 1:
                ei = ei[0].split(';')
        yield {
            "id": id,
            "kpgz": kpgz,
            "name": name,
            "ei": ei,
            "okpd": okpd,
            "okpd2": okpd2
        }


if __name__ == '__main__':
    path = r'C:\Users\ruha\Downloads\Telegram Desktop\Исходные данные\Список СПГЗ 27_5_2022.xlsx'
    for i in Parse(path):
        print(i)
