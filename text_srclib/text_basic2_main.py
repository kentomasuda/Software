# -*- coding: utf-8 -*-
"""
Text library basic sample 2

@author: MURAKAMI Tamotsu
@date: 2021-11-28
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from text_lib.meaning import Meaning
from text_lib.text import Text_
from edr_lib.edr import Edr
from text_lib.sentence import Sentence, SentenceLm
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet

print('* Start *')

# Select concept dictionary to handle meaning
# meaning_id = Edr.ID # EDR
# meaning_id = WordNet.ID # WordNet
meaning_id = (Edr.ID, WordNet.ID) # EDR and WordNet

# Phrase

phj1 = Text_.xml_parse_string('<jpn><np><m><aj>白い</aj></m><n>自動車</n></np></jpn>')
print(phj1)
Meaning.fill_meaning(phj1, meaning_id)
print(phj1)

phj2 = Text_.xml_parse_string('<jpn><np><m><aj>白い</aj></m><n>馬</n></np></jpn>')
Meaning.fill_meaning(phj2, meaning_id)

phj3 = Text_.xml_parse_string('<jpn><np><m><aj>赤い</aj></m><n>自動車</n></np></jpn>')
Meaning.fill_meaning(phj3, meaning_id)

phj4 = Text_.xml_parse_string('<jpn><np><m><aj>速い</aj></m><n>人</n></np></jpn>')
Meaning.fill_meaning(phj4, meaning_id)

phrases = (phj1, phj2, phj3, phj4)
n = len(phrases)
for i in range(n):
    ph1 = phrases[i]
    for j in range(i, n):
        ph2 = phrases[j]
        sim = Similarity.phrase_sim(ph1, ph2, meaning_id)
        print('{}: "{}", "{}"'.format(sim, ph1.get_text(), ph2.get_text()))

# PhraseLm (language map)
        
plm1 = Text_.xml_parse_string('<lm><eng><np><m><aj>white</aj></m><n>automobile</n></np></eng><jpn><np><m><aj>白い</aj></m><n>自動車</n></np></jpn></lm>')
Meaning.fill_meaning(plm1, meaning_id)

plm2 = Text_.xml_parse_string('<lm><eng><np><m><aj>white</aj></m><n>horse</n></np></eng><jpn><np><m><aj>白い</aj></m><n>馬</n></np></jpn></lm>')
Meaning.fill_meaning(plm2, meaning_id)

plm3 = Text_.xml_parse_string('<lm><eng><np><m><aj>red</aj></m><n>automobile</n></np></eng><jpn><np><m><aj>赤い</aj></m><n>自動車</n></np></jpn></lm>')
Meaning.fill_meaning(plm3, meaning_id)

plm4 = Text_.xml_parse_string('<lm><eng><np><m><aj>fast</aj></m><n>person</n></np></eng><jpn><np><m><aj>速い</aj></m><n>人</n></np></jpn></lm>')
Meaning.fill_meaning(plm4, meaning_id)

phraselms = (plm1, plm2, plm3, plm4)
n = len(phrases)
for i in range(n):
    plm1 = phraselms[i]
    for j in range(i, n):
        plm2 = phraselms[j]
        sim = Similarity.phraselm_sim(plm1, plm2, meaning_id)
        print('{}: {}, {}'.format(sim, plm1.get_text(), plm2.get_text()))

# Sentence

sen1 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen1, meaning_id)

sen2 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s><t>が</t><a><av>速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen2, meaning_id)

sen3 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen3, meaning_id)

sen4 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s><t>が</t><a><av>速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen4, meaning_id)

sentences = (sen1, sen2, sen3, sen4)
n = len(sentences)
for i in range(n):
    sen1 = sentences[i]
    for j in range(i, n):
        sen2 = sentences[j]
        simset = Similarity.sentence_sim(sen1, sen2, meaning_id)
        sim = Similarity.sentence_sim(sen1, sen2, meaning_id, scalar = True)
        print('{}, {}: "{}", "{}"'.format(sim, simset, sen1.get_text(), sen2.get_text()))

# SentenceLm (language map)

slm1 = Text_.xml_parse_string('<lm><eng><sen><t>An</t><s><n>automobile</n></s><v><v>run</v></v><t>.</t></sen></eng><jpn><sen><s><n>自動車</n></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm1, meaning_id)

slm2 = Text_.xml_parse_string('<lm><eng><sen><t>An</t><s><n>automobile</n></s><v><v>run</v></v><a><av>fast</av></a><t>.</t></sen></eng><jpn><sen><s><n>自動車</n></s><t>が</t><a><av>速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm2, meaning_id)

slm3 = Text_.xml_parse_string('<lm><eng><sen><t>A</t><s><np><m><aj>red</aj></m><n>automobile</n></np></s><v><v>run</v></v><t>.</t></sen></eng><jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm3, meaning_id)

slm4 = Text_.xml_parse_string('<lm><eng><sen><t>A</t><s><np><m><aj>white</aj></m><n>automobile</n></np></s><v><v>run</v></v><a><av>fast</av></a><t>.</t></sen></eng><jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s><t>が</t><a><av>速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm4, meaning_id)

slm5 = Text_.xml_parse_string('<lm><eng><sen><v><v>record</v></v>a<o><n>photograph</n></o><t>.</t></sen></eng><jpn><sen><o><n>写真</n></o><t>を</t><v><v>記録する</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm5, meaning_id)

slm6 = Text_.xml_parse_string('<lm><eng><sen><v><v>cool</v></v><o><n>food</n>and<n>drink</n></o><t>.</t></sen></eng><jpn><sen><o><n>食材</n><t>や</t><n>飲料</n></o><t>を</t><v><v>冷やす</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm6, meaning_id)

slm7 = Text_.xml_parse_string('<lm><eng><sen><v><v>keep</v></v>a<o><n>scene</n></o><t>.</t></sen></eng><jpn><sen><o><n>光景</n></o><t>を</t><v><v>保存する</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm7, meaning_id)

slm8 = Text_.xml_parse_string('<lm><eng><sen><v><v>worry</v></v>about<o><np><m><n>film</n></m><n>consumption</n></np></o><t>.</t></sen></eng><jpn><sen><o><np><m><n>フィルム</n></m><n eng="consumption">消費</n></np></o><t>を</t><v><v>心配する</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm8, meaning_id)

slm9 = Text_.xml_parse_string('<lm><eng><sen><v><v>keep</v></v><o><n>food</n></o><c><aj>fresh</aj></c><t>.</t></sen></eng><jpn><sen><o><n>食材</n></o><t>を</t><c><aj jpn="新鮮だ">新鮮</aj><t>に</t></c><v><v>保つ</v></v><t>。</t></sen></jpn></lm>')
Meaning.fill_meaning(slm9, meaning_id)

sentencelms = (slm1, slm2, slm3, slm4, slm5, slm6, slm7, slm8, slm9)
n = len(sentencelms)
for i in range(n):
    slmi = sentencelms[i]
    for j in range(i, n):
        slmj = sentencelms[j]
        simset = Similarity.sentencelm_sim(slmi, slmj, meaning_id)
        sim = Similarity.sentencelm_sim(slmi, slmj, meaning_id, scalar = True)
        print('{}, {}: "{}", "{}"'.format(sim, simset, slmi.get_text(), slmj.get_text()))

print(SentenceLm.get_sens.__doc__)

sens = slm1.get_sens()

print(Sentence.get_text.__doc__)

for sen in sens:
    print(sen.get_text())

print('* End *')
    
# End of file