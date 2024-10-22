# -*- coding: utf-8 -*-
"""
Check word similarity

@author: MURAKAMI Tamotsu
@date: 2022-10-13
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.edr import Edr
from math_srclib.calc_type import CalcType
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet
    
Edr.load_simple_dict()
WordNet.load_synlink_dict()

def check_sim(words):
    """
    @author: MURAKAMI Tamotsu
    @date: 2020-07-15
    """
    
    meaning_id = Edr.ID
    #meaning_id = WordNet.ID
    #meaning_id = (Edr.ID, WordNet.ID)

    n = len(words)
    for i in range(n):
        w1 = words[i]
        for j in range(i + 1, n):
            w2 = words[j]
            sims = []
            for wsimtype in (CalcType.MAX_COMBI, CalcType.MEAN_MAX_1_TO_M, CalcType.MEAN_COMBI):
                sims.append(Similarity.wordlm_sim(w1, w2, meaning_id, wsimtype = wsimtype, msimtype = CalcType.MAX))
            print('{}, {}: {}'.format(w1.get_text(), w2.get_text(), sims))
    print()

if __name__ == '__main__':

    print('* Test start *')
   
    #meaning_id = Edr.ID
    #meaning_id = WordNet.ID
    meaning_id = (Edr.ID, WordNet.ID)
    
#    w = Text_.xml_parse_string('<lm><eng><av jpn="常に">anytime</av></eng></lm>')
#    Meaning.fill_meaning(w, meaning_id)
#    print(w)

    # Word
    
    print(Similarity.wordlm_sim.__doc__)
    
    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>display</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>photograph</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>illustration</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>transfer</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>sound</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><av>far</av></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><av>remotely</av></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><av jpn="常に">anytime</av></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><av>anywhere</av></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>record</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>photograph</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>motion picture</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)
    
    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>record</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><aj jpn="多い">many</aj></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>data</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><aj>rear</aj></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>photograph</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>display</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>train</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>bus</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>timetable</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>item</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>simulate</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>shoulder</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>neck</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>measure</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>body</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>fat</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>find</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>food</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>cuisine</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>cut</v></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>find</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>food</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>cuisine</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>display</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>photograph</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>convert</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>sound</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><aj>electrical</aj></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>signal</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)
    
    words = []
    
    for w in (Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>cut</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>food</n></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><v>deliver</v></eng></lm>'),
              Text_.xml_parse_string('<lm><eng><n>home</n></eng></lm>')):
        Meaning.fill_meaning(w, meaning_id)
        words.append(w)

    check_sim(words)

    print('* Test end *')
    
# End of file