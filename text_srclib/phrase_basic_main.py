# -*- coding: utf-8 -*-
"""
Phrase（句） basic sample

@author: MURAKAMI Tamotsu
@date: 2022-02-08
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from xml.etree import ElementTree

# Library
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.text_similarity import TextSimilarity

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-02-08
"""

if __name__ == "__main__":
    print('* Start *')

    # Select concept dictionary to handle meaning
    # meaning_id = Edr.ID # EDR
    # meaning_id = WordNet.ID # WordNet
    # meaning_id = (Edr.ID, WordNet.ID) # EDR and WordNet

    """    
    Phrase
    """
    
    print(Text_.xml_parse_tree.__doc__)
    
    # tagging1 = '<jpn><n>警察</n></jpn>'
    # tagging2 = '<jpn><n>犬</n></jpn>'

    tagging1 = '<jpn><n>警察</n></jpn>'
    tagging2 = '<jpn><n>猫</n></jpn>'

    # tagging1 = '<jpn><np><m><n>警察</n></m><n>犬</n></np></jpn>'
    # tagging2 = '<jpn><np><m><n>犬</n></m><n>小屋</n></np></jpn>'

    # tagging1 = '<jpn><n>犬</n></jpn>'
    # tagging2 = '<jpn><np><m><n>犬</n></m><n>小屋</n></np></jpn>'

    # tagging1 = '<jpn><np><m><n>犬</n></m><n>小屋</n></np></jpn>'
    # tagging2 = '<jpn><np><m><n>犬</n></m><n>小屋</n></np></jpn>'

    # tagging1 = '<jpn><np><m><n>照明</n></m><n>器具</n></np></jpn>'
    # tagging2 = '<jpn><n>懐中電灯</n></jpn>'

    ph1 = Text_.xml_parse_tree(ElementTree.fromstring(tagging1))
    Meaning.fill_meaning(ph1, suggest=sys.stdout)
    print(ph1)

    ph2 = Text_.xml_parse_tree(ElementTree.fromstring(tagging2))
    Meaning.fill_meaning(ph2, suggest=sys.stdout)
    print(ph2)
    
    # 通常は主辞同士、修飾語同士の類似度の平均を計算する。
    # cross は句の主辞と修飾語の交差比較（主辞1と修飾語2、主辞2と修飾語1）を加える際の重み
    
    # 省略時は cross = 0
    print(TextSimilarity.phrase_sim(ph1, ph2))

    cross = 0
    print((cross, TextSimilarity.phrase_sim(ph1, ph2, cross=cross)))

    cross = 0.25
    print((cross, TextSimilarity.phrase_sim(ph1, ph2, cross=cross)))

    cross = 0.5
    print((cross, TextSimilarity.phrase_sim(ph1, ph2, cross=cross)))

    """
    PhraseLm (language map)
    """

    plm1 = Text_.xml_parse_tree(ElementTree.fromstring('<lm><jpn><np><m><aj>白い</aj></m><n>列車</n></np></jpn><eng><np><t>a</t><m><aj>white</aj></m><n>train</n></np></eng></lm>'))
    Meaning.fill_meaning(plm1, suggest=sys.stdout)
    print(plm1)

    plm2 = Text_.xml_parse_tree(ElementTree.fromstring('<lm><jpn><np><m><aj>黒い</aj></m><n>列車</n></np></jpn><eng><np><t>a</t><m><aj>black</aj></m><n>train</n></np></eng></lm>'))
    Meaning.fill_meaning(plm2, suggest=sys.stdout)
    print(plm2)

    print(TextSimilarity.phraselm_sim.__doc__)

    simlm12 = TextSimilarity.phraselm_sim(plm1, plm2)
    print(simlm12)

    print('* End *')
    
# End of file