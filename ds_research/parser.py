import pandas as pd
import numpy as np
import openpyxl
import sys,os


filenames = [r'D:\Projects\lct_8\Исходные данные\Исходные данные\Список СПГЗ 27_5_2022.xlsx',
            r'D:\Projects\lct_8\Исходные данные\Исходные данные\СН-2012 с СПГЗ.xlsx']
result_names = ['Список СПГЗ 27_5_2022.csv', 'СН-2012 с СПГЗ.csv']

for idx, f in enumerate(filenames):
    df = pd.read_excel(filenames[idx],
                    )
    # for index, row in df.iterrows():
    #     print(row)

    print(df.head(20))

    df.to_csv(result_names[idx])

