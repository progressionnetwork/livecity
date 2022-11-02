from slugify import slugify # pip install python-slugify
from rutermextract import TermExtractor
from thefuzz import fuzz# pip install thefuzz[speedup]
from thefuzz import process

smets = {}

smets['1.1-3101-6-1/1'] = 'Погрузка грунта вручную в автомобили-самосвалы с выгрузкой'
smets['2.49-3401-1-1/1'] = 'Перевозка грунта автосамосвалами грузоподъемностью до 10 т на расстояние 1 км'
smets['2.49-3401-1-2/1'] = 'Перевозка грунта автосамосвалами грузоподъемностью до 10 т - добавляется на каждый последующий 1 км до 100 км'
smets['5.3-5202-3-3/1'] = 'Устройство вручную набивных дорожек и площадок с добавлением щебня слоем 20 см (подушки под столбы)'
smets['5.3-5202-2-1/1'] = 'Устройство основания из песка толщиной 10 см для дорожек и площадок вручную (подушки под столбы)'
smets['1.2-3103-2-15/1'] = 'Устройство фундаментных плит железобетонных плоских'
smets['21.3-1-83'] = 'Смеси бетонные, БСГ, тяжелого бетона на гранитном щебне, фракция 5-20'

def clean_text(text):
    text = text.lower()
    text = text.replace(' т ', '')  
    return text

# lemmatize text 
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(tokens)    
    
    return text
	
new_features = []

for smet in smets:
    #smet_hash = hashlib.sha256(smet.encode('utf-8')).hexdigest()
    #print(smet, '-', smets[smet], ':', smet_hash)
    new_features.append(smets[smet])


for idx, smet in enumerate(new_features):    
    score = fuzz.partial_ratio(smet, 'Перевозка грунта автосамосвалами грузоподъемностью до 10 т - добавляется на каждый последующий 1 км до 100 км')
    print(smet, ':', score)

# term_extractor = TermExtractor()
# for smet in smets:
#     feature_set = ''
#     #print(smet, '-', smets[smet])
#     for term in term_extractor(smets[smet]):
#         feature = slugify(term.normalized, separator='_') + '_'
#         feature_set += feature
#     feature_set = feature_set[:-1]
#     print (smet, feature_set)
#     #new_features.append(feature)