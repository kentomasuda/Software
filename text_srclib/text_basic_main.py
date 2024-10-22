# -*- coding: utf-8 -*-
"""
Text library basic sample

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
from misc_srclib.time_ import Time_
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.simple_pos import SimplePos
from text_lib.text import Text_
from text_lib.word_phrase import Word
from text_lib.wordlm import WordLm
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet

print('* Start *')

# Select concept dictionary to handle meaning
# meaning_id = Edr.ID # EDR
# meaning_id = WordNet.ID # WordNet
meaning_id = (Edr.ID, WordNet.ID) # EDR and WordNet

# Word

print(Word.__doc__)

print(Word.__init__.__doc__)

we1 = Word(text='heavy', lang=Lang.ENG, pos=SimplePos.ADJ)

print(Meaning.fill_meaning.__doc__)

Meaning.fill_meaning(we1, meaning_id)
print(we1)

print(Text_.xml_parse_string.__doc__)

we2 = Text_.xml_parse_string('<eng><aj>big</aj></eng>')
Meaning.fill_meaning(we2, meaning_id)
print(we2)

wj1 = Word(text='重い', lang=Lang.JPN, pos=SimplePos.ADJ)
Meaning.fill_meaning(wj1, meaning_id)
print(wj1)

wj2 = Text_.xml_parse_string('<jpn><aj>大きい</aj></jpn>')
Meaning.fill_meaning(wj2, meaning_id)
print(wj2)

print(Similarity.word_sim.__doc__)

sim1 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MAX_COMBI)
sim2 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MEAN_COMBI)
sim3 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MEAN_MAX_1_TO_M)
print((sim1, sim2, sim3))

print(Meaning.meaning_json_string.__doc__)

print(Meaning.meaning_json_string(wj2, meaning_id))

# You can reduce polysemy by manually specifying EDR concept id's and WordNet synsets.
wj2 = Text_.xml_parse_string('<jpn><aj cid="3cf941,0e7b01" syn="00624576-a,02385102-a,01210854-a,01382086-a,01386883-a,01389170-a">大きい</aj></jpn>')
Meaning.fill_meaning(wj2, meaning_id)
print(wj2)
print(Meaning.meaning_json_string(wj2, meaning_id))

sim1 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MAX_COMBI)
sim2 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MEAN_COMBI)
sim3 = Similarity.word_sim(wj1, wj2, meaning_id, wsimtype = CalcType.MEAN_MAX_1_TO_M)
print((sim1, sim2, sim3))

wj3 = Text_.xml_parse_string('<jpn><aj>白い</aj></jpn>')
Meaning.fill_meaning(wj3, meaning_id)

wj4 = Text_.xml_parse_string('<jpn><n>自動車</n></jpn>')
Meaning.fill_meaning(wj4, meaning_id)

wj5 = Text_.xml_parse_string('<jpn><aj>軽い</aj></jpn>')
Meaning.fill_meaning(wj5, meaning_id)

wj6 = Text_.xml_parse_string('<jpn><n>車</n></jpn>')
Meaning.fill_meaning(wj6, meaning_id)

wj7 = Text_.xml_parse_string('<jpn><aj jpn="きれいだ">きれい</aj>な</jpn>')
Meaning.fill_meaning(wj7, meaning_id)
print(wj7)
print(Meaning.meaning_json_string(wj7, meaning_id))

wj8 = Text_.xml_parse_string('<jpn><aj>速い</aj></jpn>')
Meaning.fill_meaning(wj8, meaning_id)

wj9 = Text_.xml_parse_string('<jpn><aj>小さい</aj></jpn>')
Meaning.fill_meaning(wj9, meaning_id)

"""
['白い', '大きい', '重い', '自動車']
と
['軽い', '車', 'きれい', '速い', '小さい']
の類似度を計算すると、後者を
['きれい', '小さい', '軽い', '車']
の順に前者に対応させた場合に、類似度の合計が最大になることが求まる。
"""

sim1 = Similarity.word_sim(wj3, wj5, meaning_id)
sim2 = Similarity.word_sim(wj2, wj6, meaning_id)
sim3 = Similarity.word_sim(wj1, wj7, meaning_id)
sim4 = Similarity.word_sim(wj4, wj8, meaning_id)
print((sim1, sim2, sim3, sim4))

start = Time_.time_now()
result = Similarity.word_col_sim([wj3, wj2, wj1, wj4],
                                 [wj5, wj6, wj7, wj8, wj9],
                                 meaning_id,
                                 pairs = True)
time = Time_.time_now(start)
print('sim=', result[0])
print('order1=', tuple(w.text for w in result[1]))
print('order2=', tuple(w.text for w in result[2]))
print('time=', time)

# WordLm

print(WordLm.__doc__)

print(WordLm.__init__.__doc__)

wlm3 = WordLm(wj3)

we3 = Word(text='white', lang=Lang.ENG, pos=SimplePos.ADJ)

print(WordLm.set_elem.__doc__)

wlm3.set_elem(we3)
Meaning.fill_meaning(wlm3, meaning_id)
print(wlm3)

wlm1 = Text_.xml_parse_string('<lm><eng><aj cid="0c11a8,0c119b,3cfe13,0c11af" syn="01184932-a,01188491-a">heavy</aj></eng><jpn><aj>重い</aj></jpn></lm>')
Meaning.fill_meaning(wlm1, meaning_id)

wlm2 = Text_.xml_parse_string('<lm><eng><aj>big</aj></eng><jpn><aj>大きい</aj></jpn></lm>')
Meaning.fill_meaning(wlm2, meaning_id)

wlm4 = Text_.xml_parse_string('<lm><eng><n>automobile</n></eng><jpn><n>自動車</n></jpn></lm>')
Meaning.fill_meaning(wlm4, meaning_id)

wlm5 = Text_.xml_parse_string('<lm><eng><aj cid="262793,262792,2627a6" syn="01191876-a,01190993-a,01186408-a,01188186-a">light</aj></eng><jpn><aj>軽い</aj></jpn></lm>')
Meaning.fill_meaning(wlm5, meaning_id)

wlm6 = Text_.xml_parse_string('<lm><eng><n>car</n></eng><jpn><n>車</n></jpn></lm>')
Meaning.fill_meaning(wlm6, meaning_id)

wlm7 = Text_.xml_parse_string('<lm><eng><aj>beautiful</aj></eng><jpn><aj jpn="きれいだ">きれい</aj>な</jpn></lm>')
Meaning.fill_meaning(wlm7, meaning_id)

wlm8 = Text_.xml_parse_string('<lm><eng><aj cid="3cf251,3cfaa0,0bc6ea,0bc6e0,0bc6d5,0f3413" syn="00976508-a,00981818-a">fast</aj></eng><jpn><aj>速い</aj></jpn></lm>')
Meaning.fill_meaning(wlm8, meaning_id)

wlm9 = Text_.xml_parse_string('<lm><eng><aj>little</aj></eng><jpn><aj>小さい</aj></jpn></lm>')
Meaning.fill_meaning(wlm9, meaning_id)

print(Similarity.wordlm_sim.__doc__)

sim1 = Similarity.wordlm_sim(wlm3, wlm5, meaning_id, lsimtype=CalcType.ENG)
sim2 = Similarity.wordlm_sim(wlm2, wlm6, meaning_id, lsimtype=CalcType.ENG)
sim3 = Similarity.wordlm_sim(wlm1, wlm7, meaning_id, lsimtype=CalcType.ENG)
sim4 = Similarity.wordlm_sim(wlm4, wlm8, meaning_id, lsimtype=CalcType.ENG)
print((sim1, sim2, sim3, sim4))

start = Time_.time_now()
result = Similarity.wordlm_col_sim([wlm3, wlm2, wlm1, wlm4],
                                   [wlm5, wlm6, wlm7, wlm8, wlm9],
                                   meaning_id,
                                   lsimtype=CalcType.ENG,
                                   pairs = True)
time = Time_.time_now(start)
print('sim=', result[0])
print('order1=', tuple(wlm.get_elem(Lang.ENG).text for wlm in result[1]))
print('order2=', tuple(wlm.get_elem(Lang.ENG).text for wlm in result[2]))
print('time=', time)

print('* End *')
    
# End of file