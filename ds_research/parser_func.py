import pandas as pd
import string
import os
from glob import glob
import random
import json
import regex as re
from IPython.display import JSON,display,display_json
from tqdm import tqdm


path_to_SN2012_folder = "./"

class WrongSmeta(Exception):
        pass

possible_types = {"SN-2012": [[("№"),],
                              [("шифр"),],
                              [("наименовани",)],
                              [("ед","изм"),],
                              [("кол","во","ед"),],
                              [("цена", "ед"),],
                              [("коэф", "поправоч"),],
                              [("коэф", "зимн"),],
                              [("коэф", "пересч"),],
                              [("всего",)],
                              [("справ", "зтр", "ед", "стоим"), ("справ", "зтр", "ед", "ст", "ть")]],
                 "TSN-2001": [[("№"),],
                              [("шифр"),],
                              [("наименовани",)],
                              [("ед","изм"),],
                              [("кол","во","ед"),],
                              [("цена", "ед"),],
                              [("коэф", "поправоч"),],
                              [("коэф", "зимн"),],
                              [("всего", "цен", "базис"),("всего", "затр", "базис"), ("всего", "ценах", "на"),],
                              [("коэф","пересч"),],
                              [("всего", "цен", "текущ"),]]}

def check_change_type(col_type, value):
    if(type(value) is col_type):
        return value
    if(col_type is float):
        value = re.sub("[^0-9|\.|,]","",value)
        try:
            return float(value)
        except Exception as e:
            if("," in value and "." not in value):
                try:
                    value = re.sub(",",".",value)
                    return float(value)
                except Exception as e:
                    try:
                        float_part = value.split(".")[-1]
                        int_part = "".join(value.split(".")[:-1])
                        return float(f"{int_part}.{float_part}")
                    except:
                        print(value)
                        raise ValueError()

column_names = {"SN-2012":{1:"num",
                            2:"code",
                            3:"name",
                            4:"ei",
                            5:"count",
                            6:"amount",
                            7:"coef_correct",
                            8:"coef_winter",
                            9:"coef_recalc",
                            10:"sum",
                            11:"additional"}}

column_types = {"SN-2012":{1:float,
                         2:str,
                         3:str,
                         4:str,
                         5:float,
                         6:float,
                         7:float,
                         8:float,
                         9:float,
                         10:float,
                         11:float}}

def contains(pattern: str or tuple, s: str, lower = True, to_delete = ['-','\n']):
    #print(pattern, s)
    if(to_delete):
        s = re.sub('|'.join(to_delete),"", s)
    if(lower):
        pattern = tuple(map(lambda x:x.lower(), pattern))
        s = s.lower()
    if(type(pattern) is str):
        return pattern in s
    flag = True
    for val in pattern:
        flag *= val in s
    return flag

def load_and_check(excel_file, choosen_name):
    
    #df = pd.read_excel(sheet,header=None)
    df = excel_file.parse(sheet_name=choosen_name,header=None)
    df = df.dropna(how="all").dropna(axis=1,how="all")
    df = df.astype(str)
    df = df.reset_index(drop=True)
    df.columns = range(df.columns.size)

    #Определение начала таблицы
    one2elvn = [str(_) for _ in range(1,12)]
    for index, row in df.iterrows():
        if(series_startswith(row, one2elvn)):
            #print(index)
            table_title = index
            break
    # Маппинг номеров колонок таблицы в случае объединенных excel ячеек
    column_map = {}
    index = 1
    for ind, val in enumerate(df.iloc[table_title]):
        if(val == str(index)):
            column_map[index] = ind
            index+=1

    columns_mask = list(column_map.values())

    # Проверка соответствия колонок по СН-2012
    ser = df.iloc[table_title-1][columns_mask].apply(lambda x: "" if x == "nan" else x)[::]
    for index, row in df[:table_title-1][::-1].iterrows():
        ser += row[columns_mask].apply(lambda x: "" if x == "nan" else x)
        if("№" in ser[0]):
            break

    smeta_type = None
    for key, col_phrs in possible_types.items():
        for col, phr in enumerate(col_phrs):
            or_flag = False
            for sub_phr in phr:
                or_flag = or_flag or contains(sub_phr, ser[column_map[col+1]])
            if(not or_flag):
                break
        else:
            smeta_type = key
            break
    if(smeta_type):
        #print(f"Структура сметы подходит под {smeta_type}")
        return {"ok":True,
                "choosen_name":choosen_name,
                "smeta_type":smeta_type,
                "column_map":column_map,
                "column_mask":columns_mask,
                "table_title":table_title}
    else:
        #raise WrongSmeta("Формат сметы не распознан") 
        return {"ok":False,
                "choosen_name":choosen_name} 

#Определение начала таблицы
def series_startswith(ser, pattern):
    index = 0
    for val in ser:
        if(val == pattern[index]):
            index+=1
        elif(val == 'nan'):
            continue
        else:
            return False
        if(index == len(pattern)):
            return True
    return False

def Parse(sheet):
    out_dict = {
        "type_ref": "",
        "advance": "",
        "coef_ref": None,
        "coef_date": None,
        "sum": None,
        "tax": "",
        "sum_with_tax": None,
        "sum_with_ko": None,
        "sections": [{
                "name": "",
                "sum": None,
                "subsections": [{
                    "name": "",
                    "sum": None,
                    "rows": [{
                        "code":"",             #Шифр
                        "num":"",              #Номер
                        "name":"",             #Имя
                        'ei':"",               #Единица измерения
                        "count": None,         #Количество
                        "sum_basic":None,      #Цена в базисе
                        "sum_current":None,     #Цена
                        "amount":None,         #Цена за единицу
                        "additioanl":"",       #Дополнительно
                        "subrows": [{
                            "category":"",          #Категория material or expanse
                            "name":"",              #Имя
                            "unit":"",              #Единица измерения
                            "count":None,           #Количество
                            "amount":None,          #Цена за единицу
                            "coef_correct":None,    #Коэф коррект
                            "coef_winter":None,     #Коэф зимний
                            "coef_recalc":None,     #Коэф пересчета
                            "sum_basic":None,       #Цена в базисе
                            "sum_current":None,     #Цена
                            "additioanl":"",        #Дополнительно
                        }]
                    }]
                }]
            }]
    }


    out_dict = {
        "type_ref": "",
        "advance": "",
        "coef_ref": None,
        "coef_date": None,
        "sum": None,
        "tax": "",
        "sum_with_tax": None,
        "sum_with_ko": None,
        "sections": []
        }
    #Поиск листов со сметами
    success = [sheet, []]
    error = [sheet, []]
    excel_file = pd.ExcelFile(sheet)
    for choosen_name in excel_file.sheet_names:
        result = {"ok":False,
                  "choosen_name":choosen_name}
        try:
            result = load_and_check(excel_file, choosen_name)
            if(result["ok"]):
                success[1].append(result)
        except Exception as e:
            error[1].append(result)
            #print(sheet)
            #print(e)
    if(success[1]):
        del error
    if(not success[1]):
        raise WrongSmeta("Структура сметы не распознана")
    
    lists = []
     
    for page_info  in success[1]:
        column_map = page_info["column_map"]
        column_mask = page_info["column_mask"]
        choosen_name = page_info["choosen_name"]
        table_title = page_info["table_title"]
        smeta_type = page_info["smeta_type"]

        out_dict["type_ref"] = smeta_type

        excel_file = pd.ExcelFile(sheet)
        df = excel_file.parse(sheet_name=choosen_name,header=None)
        df = df.dropna(how="all").dropna(axis=1,how="all")
        df = df.astype(str)
        df = df.reset_index(drop=True)
        df.columns = range(df.columns.size)

        # Определение разделов и подразделов
        current_section = None
        current_subsection = None
        current_item = 0
        
        item_indices = {0:[None,None,None,None]} # Началный индекс, Конечный индекс, раздел, подраздел
        #Границы записей явлеяются отрезком [], учитывать при использовании slice

        for index, row in tqdm(df[table_title+1:].iterrows()):
            # Определения разделов и подразделов
            if(row.str.lower().str.contains("подраздел").any()):
                if((row.str.lower().str.contains("подраздел") * row.str.lower().str.contains("итог")).any()):
                    #print(f"    Конец {current_subsection}")
                    current_subsection = None
                    item_indices[current_item][1] = index-1
                else:
                    # Иногда в одной линии два раза встречается подраздел
                    for cell in row:
                        if(cell!="nan" and "подраздел" in cell.lower()):
                            current_subsection = cell
                            break
                            
                    #print(f"    Начало {current_subsection}")
            elif(row.str.lower().str.contains("раздел").any()):
                if((row.str.lower().str.contains("раздел") * row.str.lower().str.contains("итог")).any()):
                    #print(f"Конец {current_section}")
                    current_section = None
                    item_indices[current_item][1] = index-1
                else:
                    # Иногда в одной линии два раза встречается раздел
                    for cell in row:
                        if(cell!="nan" and "раздел" in cell.lower()):
                            current_section = cell
                            break
                    
                    #print(f"Начало {current_section}")
            elif(row.str.lower().str.contains("смет").any() * \
                 row.str.lower().str.contains("итог").any()):
                if(item_indices[current_item][1] is None):
                    item_indices[current_item][1] = index-1
                 
            # Определение номера и границ записи
            if( row[column_map[1]].isnumeric() and row[column_map[1]] == str(current_item+1)):
                if(item_indices[current_item][1] is None):
                    item_indices[current_item][1] = index-1
                current_item += 1
                #print(f"****Запись**** At index {index} found new item num. {current_item}")
                item_indices[current_item] = [index,None,current_section,current_subsection]

        #0 запись исскуственная
        del item_indices[0]

        assert item_indices, "No items were found. Cannot continue"

        value_mask = list(map(lambda x: x[1],filter(lambda x: x[0]>3, column_map.items())))
            
        all_items = []
        for item_to_parse in range(1, len(item_indices)+1):
            zap = df.iloc[item_indices[item_to_parse][0]:item_indices[item_to_parse][1]+1].reset_index(drop=True)
            #Парсинг отдельной записи
            main_work_dict = {}
            for col in range(1, 12):
                if(zap.iloc[0][column_map[col]] != "nan"):
                    main_work_dict[column_names[smeta_type][col]] = check_change_type(column_types[smeta_type][col],zap.iloc[0][column_map[col]])

            main_work_dict["Sub_works"] = []
            main_work_dict["Related_works"] = []

            for index, row in zap[1:].iterrows():
                if(len(set(row[value_mask])) == 1 and row[value_mask[0]] == "nan"):
                    continue
                if(row[column_map[3]] == 'nan'):
                    continue
                if(row.str.lower().str.contains("итого").any()):
                    continue
                
                if(row[column_map[1]] != 'nan' or row[column_map[2]] != 'nan'):
                    related_work_dict = {}
                    for col in range(1, 12):
                        if(row[column_map[col]] != "nan"):
                            related_work_dict[column_names[smeta_type][col]] = check_change_type(column_types[smeta_type][col],row[column_map[col]])
                    main_work_dict["Related_works"].append(related_work_dict)
                else:
                    sub_work_dict = {}
                    for col in range(1, 12):
                        if(row[column_map[col]] != "nan"):
                            sub_work_dict[column_names[smeta_type][col]] = check_change_type(column_types[smeta_type][col],row[column_map[col]])
                    main_work_dict["Sub_works"].append(sub_work_dict)
                
            for index, row in zap[::-1].iterrows():
                first = None
                second = None
                for val in row[::-1]:
                    if(val != 'nan'):
                        if(second):
                            first = val
                            break
                        else:
                            second = val
                if(first and second and re.search('[a-zA-Zа-яА-Я]', first+second) is None):
                    main_work_dict["sum"] = check_change_type(float,first)
                    main_work_dict["amount"] = check_change_type(float,second)
                    break 
                    
            main_work_dict["subrows"] = []
            for ind, pos in enumerate(main_work_dict["Sub_works"]):
                pos["type"] = "expanse"
                main_work_dict["subrows"].append(pos)

            for ind, pos in enumerate(main_work_dict["Related_works"]):
                pos["type"] = "material"
                main_work_dict["subrows"].append(pos)

            del main_work_dict["Sub_works"]
            del main_work_dict["Related_works"]
            
            sect = item_indices[item_to_parse][2] 
            sub_sect= item_indices[item_to_parse][3]
            
            if("code" not in main_work_dict.keys()):
                main_work_dict["code"] = ""
            

            if(sect not in [x["name"] for x in out_dict["sections"]]):
                out_dict["sections"].append({"name":sect,
                                             "sum":None,
                                             "subsections":[]})
                out_dict["sections"][-1]["subsections"].append({"name":sub_sect,
                                                                 "sum":None,
                                                                 "rows":[]})
            elif(sub_sect not in [sub_x["name"] for sub_x in \
                    list(filter(lambda x: x["name"] == sect,
                           out_dict["sections"]))[0]["subsections"]]):
                for ind,section in enumerate(out_dict["sections"]):
                    if(section["name"] == sect):
                        out_dict["sections"][ind]["subsections"].append({"name":sub_sect,
                                                                         "sum":None,
                                                                         "rows":[]})
                        break


            for ind, section in enumerate(out_dict["sections"]):
                if(section["name"] == sect):
                    for sub_ind, sub_section in enumerate(out_dict["sections"][ind]["subsections"]):
                        if(sub_section["name"] == sub_sect):
                            out_dict["sections"][ind]["subsections"][sub_ind]["rows"].append(main_work_dict)
            
            
            all_items.append(main_work_dict)        

        lists.append(all_items)
    return out_dict

