import pandas as pd
import regex as re
from tqdm import tqdm
import Levenshtein
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import fasttext.util
import pymorphy2
from pathlib import Path
nltk.download("stopwords")
class Keyphrases():
    def __init__(self, d_spgz: dict):
        self.morph = pymorphy2.MorphAnalyzer()
        cc_path = str(Path(Path(__file__).parent, 'cc.ru.100.bin'))
        self.ft = fasttext.load_model(cc_path)
        self.ref_s = {} 
        self.df = pd.DataFrame(d_spgz)
        self.key_ph = self.df["Ключевые слова"].dropna().apply(lambda s: re.sub("[^а-яА-Я]"," ",s).lower()).str.split()
        self.vectorizers = {}
         
    def load_vectorizers(self, spravochn, name):
        corpus = []
        for sect in spravochn["sections"]:
            for pos in sect["rows"]:
                corpus.append(self.normalize_sent(pos["name"]))

        vectorizer = TfidfVectorizer()
        vectorizer.fit(corpus)
        self.vectorizers[name] = vectorizer
        self.ref_s[name] = spravochn 
            
    def process_smeta(self, smeta: dict):
        if(not self.vectorizers):
            print("No available vectorizers, please run load_vectorizers at least once")
            return None
        len_pos = sum([sum([len(x["rows"]) for x in sect["subsections"]]) for sect in smeta["sections"]])
        bar1 = tqdm(total = len_pos*2)
        for sect_ind, sect in enumerate(smeta["sections"]):
            for subs_ind, subs in enumerate(sect["subsections"]):
                for pos_ind, pos in enumerate(subs["rows"]):
                    poss_matches = []
                    for ind, phrs in self.key_ph.items():
                        try:
                            pos["name"]
                        except Exception as e:
                            print(f"Exception {e} but who cares?")
                            continue
                        matched = 0
                        for phr in phrs:
                            if(phr in pos["name"].lower()):
                                matched+=1
                        poss_matches.append({"phrase_ind":ind,
                                             "phrase":phrs,
                                             "match_amount": matched,
                                             "match_ratio": matched/len(phrs),
                                             "levenst_ratio":Levenshtein.ratio(pos["name"].lower(), self.df.iloc[ind].СПГЗ)})
                    poss_matches = sorted(poss_matches,key=lambda x: (-x["match_ratio"],-x["levenst_ratio"]))
                    poss_matches = poss_matches[:20]

                    smeta["sections"][sect_ind]\
                         ["subsections"][subs_ind]\
                         ["rows"][pos_ind]["poss_matches"] = poss_matches
                    bar1.update()
        positions = {}
        dyn_thrsh = {}
        thrs = 0.5
        for sect_ind, sect in enumerate(smeta["sections"]):
            positions[sect["name"]] = []
            dyn_thrsh[sect["name"]] = []
            for subs_ind, subs in enumerate(sect["subsections"]):
                for pos_ind, pos in enumerate(subs["rows"]):
                    try:
                        sim = self.match_best_fasttext( pos["name"], [self.df.iloc[poss_match["phrase_ind"]].СПГЗ for poss_match in pos["poss_matches"]])
                        poss_match = pos["poss_matches"][sim[0][2]]
                        pos["fasttext_percent"] = sim[0][0][0]
                        pos["fasttext_spgz"] = sim[0][1]
                        if(self.get_file_for(pos, self.ref_s)):
                            pos["word_importance"] = self.get_words_importance(pos['name'], self.vectorizers[self.get_file_for(pos, self.ref_s)[0]])
                        else:
                            pos["word_importance"] = [("",0)]
                        pos["key_phrases_spgz"] = self.df.iloc[poss_match["phrase_ind"]].СПГЗ
                        pos["match_ratio"] = pos["poss_matches"][sim[0][2]]["match_ratio"]
                        pos["levenst_ratio"] = pos["poss_matches"][sim[0][2]]["levenst_ratio"]
                        pos["is_key_coof"] = (pos["match_ratio"]+pos["levenst_ratio"]+pos["fasttext_percent"]+max([x[1] for x in pos["word_importance"]]))/4
                        positions[sect["name"]].append((pos["sum"], pos))
                        dyn_thrsh[sect["name"]].append(pos["is_key_coof"])
                        sim = None
                        bar1.update()
                    except:
                        pos["fasttext_percent"] = 0
                        pos["fasttext_spgz"] = 0
                        pos["key_phrases_spgz"] = 0
                        pos["match_ratio"] = 0
                        pos["levenst_ratio"] = 0
                        pos["is_key_coof"] = 0
            positions[sect["name"]] = sorted(positions[sect["name"]], key = lambda x: x[0], reverse=True)
        word_importance_coof = 0.8
        for sect, position_list in positions.items():
            max_per_pos = max([__[0] for __ in position_list])
            for pos_ind, position in enumerate(position_list):
                positions[sect][pos_ind][1]["is_key_coof"] = position[1]["is_key_coof"]*(word_importance_coof)  + position[0]/max_per_pos*(1-word_importance_coof)
        
        for sect, position_list in positions.items():
            real_thr = max(thrs, np.mean(dyn_thrsh[sect]))
            #print(sect, real_thr)
            for pos_ind, position in enumerate(position_list):
                positions[sect][pos_ind][1]["is_key"] = False
                if(position[1]["is_key_coof"]>=real_thr):
                    positions[sect][pos_ind][1]["is_key"] = True     
        return positions
        
    def normalize_sent(self, s):
        stops = nltk.corpus.stopwords.words("russian")
        s = re.sub("[^а-я]"," ", s.lower())
        s = " ".join(filter(lambda x: True if(x not in stops and len(x)>3) else False,s.split()))
        return " ".join([self.morph.parse(name)[0].normal_form for name in s.split()])

    def get_words_importance(self, sentence, vectorizer=None):
        if(not vectorizer):
            return []
        names = vectorizer.get_feature_names_out()
        x = vectorizer.transform([self.normalize_sent(sentence)])[0]
        items = sorted(list(zip(names[x.indices], x.data)),key = lambda x: -x[1])
        return items

    def match_best_fasttext(self, to_match, corpus):
        vecs = []
        for sent in corpus:
            vecs.append(self.ft.get_sentence_vector(self.normalize_sent(sent)))
        vecs = np.array(vecs)
        sent_vec = self.ft.get_sentence_vector(self.normalize_sent(to_match))
        sent_vec = sent_vec.reshape(1,*sent_vec.shape)
        similarity = cosine_similarity(vecs, sent_vec)
        return sorted([(sim, corpus[ind], ind) for ind, sim in enumerate(similarity) ], reverse=True)

    def get_file_for(self, pos, ref_s):
        for key, ref in self.ref_s.items():
            for sect_ind, sect in enumerate(ref["sections"]):
                for z_ind, z in enumerate(sect["rows"]):
                    if(pos["code"].lower() in z["code"].lower()):
                        return (key,z)

        for key, ref in self.ref_s.items():
            for sect_ind, sect in enumerate(ref["sections"]):
                for z_ind, z in enumerate(sect["rows"]):
                    if(pos["name"].lower() in z["name"].lower()):
                        return (key,z)
        return None
