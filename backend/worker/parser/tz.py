import pandas as pd

def Parse(path: str)-> dict:
    df = pd.read_excel(path)
    df =df.dropna()
    df.sort_values(by='Наименование шаблона ТЗ')
    result = {"name": "", "rows":[]}
    last_name = None
    for index, row in df.iterrows():
        name = row['Наименование шаблона ТЗ']
        kpgz_id = row['КПГЗ'].split(' ')[0]
        spgz_id = row['ID']
        if last_name is None: 
            last_name = name
        result["name"] = name
        result["rows"].append({
            "kpgz_id": kpgz_id,
            "spgz_id": spgz_id
        })
        if last_name != name:
            yield result
        last_name = name

if __name__ == '__main__':
    path = r'C:\Users\ruha\Downloads\Telegram Desktop\Исходные данные\Шаблон ТЗ.xlsx'
    for i in Parse(path):
        print(i)
