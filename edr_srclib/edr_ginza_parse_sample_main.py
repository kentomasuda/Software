# -*- coding: utf-8 -*-
"""
EDR Ginza parse sample main

@author: MURAKAMI Tamotsu
@date: 2023-12-02
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import statistics

# Library
from edr_srclib.edr_ginza_parser import EdrGinzaParser
from edr_srclib.jwpos import JwPos
from ginza_srclib.udpos import UdPos


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-12-02
"""
if __name__ == '__main__':
    print('* Main starts *')
    
    text_list = ['白い自動車が走る。', '白い自動車が速く走る。', '白い車が疾走する。', '赤い自動車が走る。']
    n = len(text_list)
    
    lemma_pos_cids_seq_list = []
    
    for i in range(n):
        lemma_pos_seq = EdrGinzaParser.parse_text(text_list[i])
        print('lemma_pos_seq({}) = {}'.format(i, lemma_pos_seq))
        lemma_pos_cids_seq = EdrGinzaParser.add_conceptids(lemma_pos_seq)
        print('lemma_pos_cids_seq({}) = {}'.format(i, lemma_pos_cids_seq))
        lemma_pos_cids_seq_list.append(lemma_pos_cids_seq)

    print()
    
    for i in range(n):
        wordsi = lemma_pos_cids_seq_list[i]
        texti = text_list[i]
        for j in range(i + 1, n):
            wordsj = lemma_pos_cids_seq_list[j]
            textj = text_list[j]
            simij = EdrGinzaParser.calc_sim(wordsi, wordsj)
            simji = EdrGinzaParser.calc_sim(wordsj, wordsi)
            sim = EdrGinzaParser.calc_sim(wordsj, wordsi, symmetricfn=statistics.mean)
            print('sim=({}, {}, {}) between "{}" and "{}".'.format(simij, simji, sim, texti, textj))

    print()

    # 名詞、動詞のみを比較する    
    jwpos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
            JwPos.JVE |\
            JwPos.JN1_JVE
    udpos = UdPos.NOUN | UdPos.PROPN | UdPos.VERB

    for i in range(n):
        wordsi = lemma_pos_cids_seq_list[i]
        texti = text_list[i]
        for j in range(i + 1, n):
            wordsj = lemma_pos_cids_seq_list[j]
            textj = text_list[j]
            simij = EdrGinzaParser.calc_sim(wordsi, wordsj, jwpos=jwpos, udpos=udpos)
            simji = EdrGinzaParser.calc_sim(wordsj, wordsi, jwpos=jwpos, udpos=udpos)
            sim = EdrGinzaParser.calc_sim(wordsj, wordsi, jwpos=jwpos, udpos=udpos, symmetricfn=statistics.mean)
            print('sim=({}, {}, {}) between "{}" and "{}".'.format(simij, simji, sim, texti, textj))

    print('* Main ends *')

# End of file