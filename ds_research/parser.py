import pandas as pd
import numpy as np
import openpyxl
import sys,os
filename = r'D:\Projects\lct_8\Исходные данные\Исходные данные\СН-ТСН\СН-2012\Глава 3. Мосты, путепроводы, эстакады.xlsx'

wb = openpyxl.load_workbook(filename)
sheet = wb.active
sheet_size = 180 #sheet.max_row
c_max = 'C'+str(sheet_size)

for rowOfCellObjects in sheet['C1':c_max]:
        for cellObj in rowOfCellObjects:
               if cellObj.value != None and '-' in cellObj.value:
                   #print(cellObj.coordinate, cellObj.value)
                   d = str(cellObj.coordinate)[1:]
                   delta = int(d)
                   id = sheet['A'+d].value
                   number = sheet['C'+d].value
                   work_name = sheet['E'+d].value
                   unit = sheet['G'+d].value
                   amount = sheet['H'+d].value
                   zp_ppu = sheet['J'+str(delta+1)].value                 
                   em_ppu = sheet['J'+str(delta+2)].value                 
                   zpm_ppu = sheet['J'+str(delta+3)].value                 
                   mp_ppu = sheet['J'+str(delta+4)].value                 
                   np_zp = sheet['H'+str(delta+5)].value                 
                   sp_zp = sheet['H'+str(delta+6)].value                 
                   np_sp_zpm = sheet['H'+str(delta+7)].value                 
                   ztr_amount = sheet['H'+str(delta+9)].value                 
                   total_price = sheet['O'+str(delta+11)].value                 
                    
                   print("id", id)
                   print("number", number)
                   print("work_name", work_name)
                   print("unit", unit)
                   print("amount", amount)
                   print("zp_ppu", zp_ppu)
                   print("em_ppu", em_ppu)
                   print("zpm_ppu", zpm_ppu)
                   print("mp_ppu", mp_ppu)
                   print("np_zp", np_zp)
                   print("sp_zp", sp_zp)
                   print("np_sp_zpm", np_sp_zpm)
                   print("ztr_amount", ztr_amount)
                   print("total_price", total_price)
                   print('==='*20)

sys.exit()
delta = 15
for i in range(1, 100):
    
    
    d = str(delta)
    id = sheet['A'+d].value
    number = sheet['C'+d].value
    work_name = sheet['E'+d].value
    unit = sheet['G'+d].value
    amount = sheet['H'+d].value
    ppu = sheet['J'+d].value
    
    print('A'+d)
    
    print(id, number, work_name, unit, amount, ppu)
    
    delta += 15

sys.exit()

df = pd.read_excel(filename,
                   #sheet_name='', 
                    skiprows=range(1, 26),  # header
                   #usecols = "A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R"
                   )
# df.columns = ['id','empty','code','work_name','spec','count','price_per_one',
#                           'fix_coeff','winter_coeff','re_coeff','price','total_count']

# df.dropna(how='all', inplace=True)
# df.ffill(inplace=True)

for index, row in df.iterrows():
    print(row)
    # if '/' in marker and '-' in marker:      
    # if type(row[4]) != float:  
    #     id = row[2]
    #     name = row[4]
    #     print(id, name)
    #     if 'ЗП' in name:
    #         zp = row[4]
    #         xuy1 = row[9]
    #         xuy2 = row[10]
    #         xuy3 = row[12]
    #         xuy4 = row[13]
    #         xuy5 = row[13]
    #         print(zp, xuy1, xuy2, xuy3, xuy4, xuy5)
    
    if index > 50:
        break

print(df.head(20))

