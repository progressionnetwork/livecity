import pandas as pd
import json

def Parse(path: str)-> dict:
    df = pd.read_excel(path)
    df =df.dropna()
    df.sort_values(by='Наименование шаблона ТЗ')
    # print(f"Количество шаблонов: {df['Наименование шаблона ТЗ'].unique().shape[0]}")
    templates = df['Наименование шаблона ТЗ'].unique()
    for template in templates:
        result={"name": template, "rows":[]}
        df_rows = df[(df['Наименование шаблона ТЗ'] == template)]
        for index, row in df_rows.iterrows():
            result['rows'].append({
                "kpgz_id": str(row['КПГЗ'].split(' ')[0]),
                "spgz_id": int(row['ID'])
            })
        yield result

if __name__ == '__main__':
    path = r'C:\Users\ruha\Downloads\Telegram Desktop\Исходные данные\Шаблон ТЗ.xlsx'
    for index, i in  enumerate(Parse(path)):
        print(json.dumps(i))
        print(",")
        # break
    print("]")    
    