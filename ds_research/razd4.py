import pandas as pd

def grazd4(smeta, proccessed, df):
    out_df = pd.DataFrame(columns=['num', 'id', 'kpgz', 'spgz', 'count', 'ei', 'amount', 'sum', 'address']) 
    for sect, rows in proccessed.items():
        for row in rows:
            pos =  row[1]
            address = ""
            if(next(filter(lambda x: x["name"] == sect, smeta["sections"]))["address"]):
                address = next(filter(lambda x: x["name"] == sect, smeta["sections"]))["address"]
            else:
                address = smeta["address"]
            address = address.__str__()
            ID = "".__str__()
            
            number = pos["num"].__str__()
            
            code = pos["code"].__str__()
            
            name = pos["name"].__str__()
            
            spgz = set([pos["fasttext_spgz"], pos["key_phrases_spgz"]]).__str__()
            
            kpgz = df[df.СПГЗ == pos["fasttext_spgz"]].iloc[0].КПГЗ.__str__()
            
            ei = pos["ei"].__str__()
            
            amount = pos["amount"]
            
            summ = pos["sum"]
                    
            count = pos["count"]
            
            if(count>=1):
                if(amount>summ):
                    amount, summ = summ, amount
            else:
                if(amount<summ):
                    amount, summ = summ, amount 
            buf_df = pd.DataFrame({'num':[number], 'id':[ID], 'kpgz':[kpgz], 'spgz':[spgz], 'count':[count], 'ei':[ei], 'amount':[amount], 'sum':[summ], 'address':[address]})
            out_df = pd.concat([out_df, buf_df], axis = 0)
    return out_df
