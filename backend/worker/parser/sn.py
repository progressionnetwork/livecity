import pandas as pd
from glob import glob
import json
import regex as re
from tqdm import tqdm


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

column_names = {1:"Number",
                2:"Code",
                3:"Name",
                4:"Unit",
                5:"Amount",
                6:"Price_per_unit",
                7:"Correction_coof",
                8:"Winter_coof",
                9:"Recalc_coof",
                10:"Total",
                11:"Additional"}

column_types = {1:float,
                 2:str,
                 3:str,
                 4:str,
                 5:float,
                 6:float,
                 7:float,
                 8:float,
                 9:float,
                 10:float,
                 11:float}

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
        return True
    else:
        #raise WrongSmeta("Формат сметы не распознан") 
        return False

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
    #Поиск листов со сметами
    success = [sheet, []]
    error = [sheet, []]
    excel_file = pd.ExcelFile(sheet)
    for choosen_name in excel_file.sheet_names:
        try:
            result = load_and_check(excel_file, choosen_name)
            if(result):
                success[1].append(choosen_name)
        except Exception as e:
            error[1].append(choosen_name)
            #print(sheet)
            #print(e)
    if(success[1]):
        del error
    if(not success[1]):
        raise WrongSmeta("Структура сметы не распознана")
    
    lists = []
     
    for choosen_name in success[1]:
        excel_file = pd.ExcelFile(sheet)
        df = excel_file.parse(sheet_name=choosen_name,header=None)
        df = df.dropna(how="all").dropna(axis=1,how="all")
        df = df.astype(str)
        df = df.reset_index(drop=True)
        df.columns = range(df.columns.size)
        one2elvn = [str(_) for _ in range(1,12)]
        for index, row in df.iterrows():
            if(series_startswith(row, one2elvn)):
                print(index)
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
                    print(key, sub_phr)
                    break
            else:
                smeta_type = key
                break
        if(smeta_type):
            print(f"Структура сметы подходит под {smeta_type}")
        else:
            raise WrongSmeta("Формат сметы не распознан")       

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

        columns_mask = list(column_map.values())
        value_mask = list(map(lambda x: x[1],filter(lambda x: x[0]>3, column_map.items())))
            
        all_items = []

        for item_to_parse in range(1, len(item_indices)+1):
            zap = df.iloc[item_indices[item_to_parse][0]:item_indices[item_to_parse][1]+1].reset_index(drop=True)
            #Парсинг отдельной записи
            main_work_dict = {}
            for col in range(1, 12):
                if(zap.iloc[0][column_map[col]] != "nan"):
                    main_work_dict[column_names[col]] = check_change_type(column_types[col],zap.iloc[0][column_map[col]])

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
                            related_work_dict[column_names[col]] = check_change_type(column_types[col],row[column_map[col]])
                    main_work_dict["Related_works"].append(related_work_dict)
                else:
                    sub_work_dict = {}
                    for col in range(1, 12):
                        if(row[column_map[col]] != "nan"):
                            sub_work_dict[column_names[col]] = check_change_type(column_types[col],row[column_map[col]])
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
                    main_work_dict["Total"] = check_change_type(float,first)
                    main_work_dict["Unit_cost_with_additions"] = check_change_type(float,second)
                    break
                    
            main_work_dict["Section"] = item_indices[item_to_parse][2] 
            main_work_dict["Sub_section"] = item_indices[item_to_parse][3]
            
            if("Code" not in main_work_dict.keys()):
                main_work_dict["Code"] = ""
            
            all_items.append(main_work_dict)        

        lists.append(all_items)
    return lists
