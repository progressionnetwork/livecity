from slugify import slugify # pip install python-slugify
from rutermextract import TermExtractor

smets = {}

smets['1.1-3101-6-1/1'] = 'Погрузка грунта вручную в автомобили-самосвалы с выгрузкой'
smets['2.49-3401-1-1/1'] = 'Перевозка грунта автосамосвалами грузоподъемностью до 10 т на расстояние 1 км'
smets['2.49-3401-1-2/1'] = 'Перевозка грунта автосамосвалами грузоподъемностью до 10 т - добавляется на каждый последующий 1 км до 100 км'
smets['5.3-5202-3-3/1'] = 'Устройство вручную набивных дорожек и площадок с добавлением щебня слоем 20 см (подушки под столбы)'
smets['5.3-5202-2-1/1'] = 'Устройство основания из песка толщиной 10 см для дорожек и площадок вручную (подушки под столбы)'
smets['1.2-3103-2-15/1'] = 'Устройство фундаментных плит железобетонных плоских'
smets['21.3-1-83'] = 'Смеси бетонные, БСГ, тяжелого бетона на гранитном щебне, фракция 5-20'
	
new_features = []

term_extractor = TermExtractor()
for smet in smets:
    feature_set = ''
    #print(smet, '-', smets[smet])
    for term in term_extractor(smets[smet]):
        feature = slugify(term.normalized, separator='_') + '_'
        feature_set += feature
    feature_set = feature_set[:-1]
    print (smet, feature_set)
    #new_features.append(feature)