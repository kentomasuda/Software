# -*- coding: utf-8 -*-
"""
EDR relevance of concepts

This will be discontinued.
Use EdrRelation.

@author: MURAKAMI Tamotsu
@date: 2020-02-24
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import statistics

# Library
from edr_lib.edr import Edr
from edr_lib.relation import Relation, RelLabel
from misc_srclib.time_ import Time_
from text_lib.lang import Lang

class DegreeOfRelation:
    """
    Degree of relation （関係度）
    
    @author: MURAKAMI Tamotsu
    @date: 2020-02-24
    """
    
    @staticmethod
    def deg_of_rel(step: int
                   ): # -> number
        """
        定義域[0, ∞) → 値域(0, 1]
        
        @author: MURAKAMI Tamotsu
        @date: 2020-02-24
        """
        
        if step is None:
            return 0
        else:
            return 1 / step

    @staticmethod
    def word_relation(word1: str,
                      word2: str,
                      lang: Lang,
                      lang2: Lang = None,
                      model: str = 'MAX' # 'MEAN' or 'MEDIAN' or 'MAX' 
                      ): # -> number
        """
        Must be w1 != w2.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-02-24
        """
        
        SIMPLE_POS = True
        
        if lang2 is None:
            lang2 = lang
            
        cids1 = Edr.headword_conceptid(word1, lang=lang, simplepos=SIMPLE_POS)
        cids2 = Edr.headword_conceptid(word2, lang=lang2, simplepos=SIMPLE_POS)
        
        degrels = []
        for cid1 in cids1:
            for cid2 in cids2:
                step = Relation.shortest_relation_chain_step(cid1, cid2)
                degrels.append(DegreeOfRelation.deg_of_rel(step))
        
        if model == 'MEDIAN':
            return statistics.median(degrels)
        elif model == 'MEAN':
            return statistics.mean(degrels)
        elif model == 'MAX':
            return max(degrels)
        else:
            print("Unknown model: '{}'".format(model))
        
"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-02-25
"""

if __name__ == '__main__':
    print('* Test start *')
    
    LANG = Lang.JPN
    SIMPLE_POS = True

    words = (
            '日本',
            '土産',
            '寒い',
            '快適だ'
            )
    
    for word in words:
        cids = Edr.headword_conceptid(word, lang=LANG, simplepos=SIMPLE_POS)
        print('"{}":{}'.format(word, cids))
    
    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            rel = DegreeOfRelation.word_relation(words[i], words[j], lang = Lang.JPN, model = 'MAX')
            print('rel({}, {})={}'.format(words[i], words[j], rel))

    print('* Test end *')
        
# End of file