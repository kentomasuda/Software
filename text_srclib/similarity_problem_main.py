# -*- coding: utf-8 -*-
"""
Text similarity problem

@author: MURAKAMI Tamotsu
@date: 2019-10-29
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Library
from edr_lib.edr import Edr
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet

# Library


 
"""
Test

@author: MURAKAMI Tamotsu
@date: 2019-10-29
"""

if __name__ == '__main__':

    print('* Test start *')
    
    
#    SUGGEST = None
    SUGGEST = sys.stdout
    
    SIMMIN = 0.3
    
    PATTERN = False
    
    meaning_id = Edr.ID
#    meaning_id = WordNet.ID
#    meaning_id = (Edr.ID, WordNet.ID)
    
    items = [
            # 「違う方法で」
#            '<eng><sen><s><n>I</n></s> <v><v>do</v></v> <a><av>differently</av></a>.</sen></eng>',
#            '<eng><sen><s><n>I</n></s> <v><v>do</v></v> <a>in <np><m><aj>different</aj></m> <n>way</n></np></a>.</sen></eng>',
            # 「冷やす」
#            '<eng><sen><s><n>I</n></s> <v><v>cool</v></v> <o><n>object</n></o>.</sen></eng>',
#            '<eng><sen><s><n>I</n></s> <v><v>make</v></v> <o><n>object</n></o> <c><aj>cool</aj></c>.</sen></eng>',
            # 「えさをやる」
            '<eng><sen><s><n>I</n></s> <v><v>feed</v></v> <o><n>animal</n></o>.</sen></eng>',
            '<eng><sen><s><n>I</n></s> <v><v>give</v></v> <o><n>animal</n></o> <oi><n>food</n></oi>.</sen></eng>',
            # 「写真を撮る」
#            '<eng><sen><s><n>I</n></s> <v><v>take</v></v> <o><np><m><n>product</n></m> <n>picture</n></np></o>.</sen></eng>',
#            '<eng><sen><s><n>I</n></s> <v><v>take</v></v> <o><np><n>picture</n> <m>of <n>product</n></m></np></o>.</sen></eng>',
#            '<eng><sen><s><n>I</n></s> <v><v>photograph</v></v> <o><n>product</n></o>.</sen></eng>',
            ]
    
    n = len(items)
    
    for i in range(n):
        words = []
        sen1 = Text_.xml_parse_string(items[i], words)
        Meaning.fill_meaning(sen1, meaning_id=meaning_id, suggest=SUGGEST, simmin=SIMMIN)
        print('sen1 = ', sen1)
        for j in range(i + 1, n):
            words = []
            sen2 = Text_.xml_parse_string(items[j], words)
            Meaning.fill_meaning(sen2, meaning_id=meaning_id, suggest=SUGGEST, simmin=SIMMIN)
            print('sen2 = ', sen2)
            sim = Similarity.sentence_sim(sen1, sen2, meaning_id=meaning_id, pattern=PATTERN)
            print('{}, {}: {}'.format(i, j, sim))

    print('* Test end *')
    
# End of file