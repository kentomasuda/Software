# -*- coding: utf-8 -*-
"""
EDR similarity sample main

@author: MURAKAMI Tamotsu
@date: 2022-10-19
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import pprint
from xml.etree import ElementTree

# Library
from edr_lib.concept import Concept
from edr_lib.edr import Edr
from math_srclib.calc_type import CalcType
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.text_similarity import TextSimilarity

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-10-19
"""

if __name__ == '__main__':
    
    print('* Main starts *')

    meaning_id = Edr.ID
    
    print('多義性そのままで類似度を計算')
    
    text1 = '緑'
    word1 = Text_.xml_parse_tree(ElementTree.fromstring('<n>{}</n>'.format(text1)), lang=Lang.JPN)
    print('word1 =', word1)

    Meaning.fill_meaning(word1, meaning_id=meaning_id)
    print('word1 =', word1)
   
    cids = word1.get_edr_conceptids()
    expls = Concept.concept_expl(cids)
    pprint.pprint(expls)

    text2 = '赤'
    word2 = Text_.xml_parse_tree(ElementTree.fromstring('<n>{}</n>'.format(text2)), lang=Lang.JPN)
    print('word2 =', word2)

    Meaning.fill_meaning(word2, meaning_id=meaning_id)
    print('word2 =', word2)
   
    cids = word2.get_edr_conceptids()
    expls = Concept.concept_expl(cids)
    pprint.pprint(expls)
    
    sim = TextSimilarity.word_sim(word1,
                                  word2,
                                  meaning_id=meaning_id,
                                  wsimtype=CalcType.MEDIAN_MAX_1_TO_M)
    print('sim =', sim)

    print('意味を手動で限定して類似度を計算')
    
    text1 = '緑'
    word1 = Text_.xml_parse_tree(ElementTree.fromstring('<n cid="107a8d,3bfb4e">{}</n>'.format(text1)), lang=Lang.JPN)
    print('word1 =', word1)

    cids = word1.get_edr_conceptids()
    expls = Concept.concept_expl(cids)
    pprint.pprint(expls)
    
    text2 = '赤'
    word2 = Text_.xml_parse_tree(ElementTree.fromstring('<n cid="1f8697">{}</n>'.format(text2)), lang=Lang.JPN)
    print('word2 =', word2)

    cids = word2.get_edr_conceptids()
    expls = Concept.concept_expl(cids)
    pprint.pprint(expls)

    sim = TextSimilarity.word_sim(word1,
                                  word2,
                                  meaning_id=meaning_id,
                                  wsimtype=CalcType.MEDIAN_MAX_1_TO_M)
    print('sim =', sim)

    print('* Main ends *')
        
# End of file