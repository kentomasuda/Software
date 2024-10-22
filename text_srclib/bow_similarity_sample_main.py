# -*- coding: utf-8 -*-
"""
Bag-of-words similarity sample main

@author: MURAKAMI Tamotsu
@date: 2023-11-15
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from xml.etree import ElementTree

# Library
from container_srclib.bag import Bag
from edr_lib.edr import Edr
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_lib.word_phrase import Word
from text_srclib.simplepos import SimplePos
from text_srclib.text_similarity import TextSimilarity

"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-11-15
"""

if __name__ == '__main__':
    
    print('* Start *')
    
    meaning_id = Edr.ID # EDR

    # Bow の作り方1: 文を bow に変換。
    sen = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><sen><s><n>自動車</n></s>が<v><v>走る</v></v>。</sen></jpn>'))
    Meaning.fill_meaning(sen, meaning_id=meaning_id, suggest=sys.stdout)
    bow1 = sen.bag_of_words()
    print('Bow1 =', bow1)
    
    # Bow の作り方2: 語リストを bow に変換。
    words1 = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><n>自動車</n><av eng="fast">速く</av><v>走る</v></jpn>'))
    Meaning.fill_meaning(words1, meaning_id=meaning_id, suggest=sys.stdout)
    bow2 = Bag(elems=words1)
    print('Bow2 =', bow2)
    
    # Bow の作り方3: 語リストを bow に変換。
    w21 = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><aj>赤い</aj></jpn>'))
    w22 = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><n>自動車</n></jpn>'))
    w23 = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><v>走る</v></jpn>'))
    words2 = [w21, w22, w23]
    Meaning.fill_meaning(words2, meaning_id, suggest=sys.stdout)
    bow3 = Bag(elems=words2)
    print('Bow3 =', bow3)
    
    # Bow の作り方4: 語リストを bow に変換。
    w31 = Word(pos=SimplePos.ADJ, text='白い', lang=Lang.JPN)
    w32 = Word(pos=SimplePos.N, text='自動車', lang=Lang.JPN)
    w33 = Word(pos=SimplePos.ADV, text='fast', lang=Lang.ENG)
    w34 = Word(pos=SimplePos.V, text='走る', lang=Lang.JPN)
    words3 = [w31, w32, w33, w34]
    Meaning.fill_meaning(words3, meaning_id=meaning_id, suggest=sys.stdout)
    bow4 = Bag(elems=words3)
    print('Bow4 =', bow4)
    
    # Bow の作り方5: 名詞句を bow に変換。
    np = Text_.xml_parse_tree(ElementTree.fromstring('<jpn><np><m><av eng="fast">速く</av><v>走る</v></m><n>自動車</n></np></jpn>'))
    Meaning.fill_meaning(np, meaning_id=meaning_id, suggest=sys.stdout)
    bow5 = sen.bag_of_words()
    print('Bow5 =', bow5)
    
    print(TextSimilarity.word_sim.__doc__)

    print(TextSimilarity.bag_sim.__doc__)
    
    # Word の類似度計算に使用する関数。
    wsimf = lambda w1, w2: TextSimilarity.word_sim(w1,
                                                   w2,
                                                   meaning_id = meaning_id)
    
    bows = (bow1, bow2, bow3, bow4, bow5)
    n = len(bows)
    for i in range(n):
        bowi = bows[i]
        for j in range(i + 1, n):
            bowj = bows[j]
            sim = TextSimilarity.bag_sim(bowi, bowj, simf=wsimf, scalar=True, pairs=False)
            print('sim({}, {}) = {}'.format(i + 1, j + 1, sim))
    
    # Asymmetric
    print('* Asymmetric')
    bows = (bow1, bow2, bow3, bow4, bow5)
    n = len(bows)
    for i in range(n):
        bowi = bows[i]
        for j in range(i + 1, n):
            bowj = bows[j]
            sim_ij = Bag.calc_sim_asym(bowi, bowj, simf=wsimf, scalar=True, pairs=False)
            sim_ji = Bag.calc_sim_asym(bowj, bowi, simf=wsimf, scalar=True, pairs=False)
            print('sim({}, {}) = {}, {}'.format(i + 1, j + 1, sim_ij, sim_ji))
    
    print('* End *')
    
# End of file