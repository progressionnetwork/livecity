
data = {
    "type_ref": "",
    "advance": "",
    "coef_ref": "1",
    "type_ref": "1",
    "coef_date": "2",
    "sum": "3000",
    "tax": "12",
    "sum_with_tax": "",
    "sum_with_ko": "",
    "sections": [{
            "name": "NAME_1",
            "sum": "3000",
            "subsections": [{
                "name": "SUBNAME_1",
                "sum": "1500",
                "rows": [{
                    "code": "432213",
                    "num": "1",
                    "name": "ROW_NAME1",
                    'ei': "1",
                    "count": "2",
                    "sum": "432213",
                    "subrows": [{
                        "name": "SUBROW_1",
                        "ei": "2",
                        "count": "2",
                        "amount": "2",
                        "coef_correct": "2",
                        "coef_winter": "2",
                        "coef_recalc": "2",
                        "sum_basic": "2",
                        "sum_current": "2",
                    }]
                }]
             }]
        }     
    ]
}


for section in data["sections"]:
    print(f"Name: {section['name']}, sum: {section['sum']}")
    try:
        for subsec in section["subsections"]:
            print(f"Subsection Name: {subsec['name']}, Subsection sum: {subsec['sum']}") 
            try:
                for row in subsec["rows"]:
                        print(f"Row Name: {row['name']}, row sum: {row['sum']}, row code: {row['code']}") 
                        try:
                            for subrow in row["subrows"]:
                                print(f"Subrow Name: {row['name']}, Subrow count: {row['count']}") 
                        except: print("No subrows")
            except: print("No rows")
    except: print("No subsections")