# -*- coding: utf-8 -*-
"""
Test similarity sample main

@author: MURAKAMI Tamotsu
@date: 2024-05-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_srclib.edr_ginza_parser import EdrGinzaParser
from ginza_srclib.ginza_ import Ginza_
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_

"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-05-03
"""

if __name__ == '__main__':
    
    print('* Main starts *')
    
    texts = [
        "共産主義",
        "収支",
        "未熟",
        "赤",
        "青",
        "黒",
        "性",
        "LGBT"
    ]
    
    n = len(texts)
    
    parsed_texts = [EdrGinzaParser.parse_text(text) for text in texts]
    print('parsed_texts =', parsed_texts)
    # それぞれ、形態素解析の結果が語（dict一つのみを要素とするlist）になっていることを前提としています。
    
    words = [parsed_text[0] for parsed_text in parsed_texts]
    words_cids = EdrGinzaParser.add_conceptids(words)
    print('words =', words)
    
    lemmas = [words_cid[Ginza_.KEY_LEMMA] for words_cid in words_cids]
    print('lemmas =', lemmas)
    
    sims_edr_lev = []
    sims_edr_st = []
    sims_st = []
    for i in range(n):
        word_cid_i = words_cids[i]
        lemma_i = lemmas[i]
        for j in range(i + 1, n):
            word_cid_j = words_cids[j]
            lemma_j = lemmas[j]
            # EDR + Levenshtein
            sim_edr_lev = EdrGinzaParser.calc_word_sim_old(word_cid_i, word_cid_j)
            sims_edr_lev.append((lemma_i, lemma_j, sim_edr_lev))
            # EDR + SentenceTransformer
            sim_edr_st = EdrGinzaParser.calc_word_sim(word_cid_i, word_cid_j)
            sims_edr_st.append((lemma_i, lemma_j, sim_edr_st))
            # SentenceTransformer only
            sim_st = SentenceTransformers_.calc_sim(lemma_i, lemma_j)
            sims_st.append((lemma_i, lemma_j, sim_st))
    
    print('EDR + Levenshtein')
    for sim_edr_lev in sorted(sims_edr_lev):
        print(sim_edr_lev)
    
    print('EDR + SentenceTransformer')
    for sim_edr_st in sorted(sims_edr_st):
        print(sim_edr_st)
    
    print('SentenceTransformer only')
    for sim_st in sorted(sims_st):
        print(sim_st)

    print('* Main ends *')
        
# End of file