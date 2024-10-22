# -*- coding: utf-8 -*-
"""
Text library bag-of-words sample

@author: MURAKAMI Tamotsu
@date: 2022-10-18
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from container_srclib.bag import Bag
from edr_lib.edr import Edr
from math_srclib.calc_type import CalcType
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.sentence import SentenceLm
from text_lib.sentence_elem import SentenceElem
from text_lib.text import Text_
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet

print('* Start *')

# Select concept dictionary to handle meaning
# meaning_id = Edr.ID # EDR
# meaning_id = WordNet.ID # WordNet
meaning_id = (Edr.ID, WordNet.ID) # EDR and WordNet

# Sentence

sen1 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen1, meaning_id, suggest=sys.stdout)

sen2 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s><t>が</t><a><av eng="fast">速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen2, meaning_id, suggest=sys.stdout)

sen3 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen3, meaning_id, suggest=sys.stdout)

sen4 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s><t>が</t><a><av eng="fast">速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>')
Meaning.fill_meaning(sen4, meaning_id, suggest=sys.stdout)

"""
文要素ごとの bag-of-words を取得する方法
"""

print(Bag.__doc__)

print(SentenceElem.bag_of_words.__doc__)

if sen4.get_subject():
    print('S: ', SentenceElem.bag_of_words(sen4.get_subject()))

if sen4.get_verb():
    print('V: ', SentenceElem.bag_of_words(sen4.get_verb()))

if sen4.get_object():
    print('O: ', SentenceElem.bag_of_words(sen4.get_object()))

if sen4.get_indirect_object():
    print('Oi: ', SentenceElem.bag_of_words(sen4.get_indirect_object()))

if sen4.get_complement():
    print('C: ', SentenceElem.bag_of_words(sen4.get_complement()))

if sen4.get_adverbial():
    print('A: ', SentenceElem.bag_of_words(sen4.get_adverbial()))

"""
Sentence について、文要素 (sentence element) ごとに bag-of-words で類似度を計算し、それを総合して Sentence の類似度とする。
処理の内容は、text_srclib/Similarity.sentence_sim_by_elem_bow に書かれている。
"""

print(Similarity.sentence_sim_by_elem_bow.__doc__)

sentences = (sen1, sen2, sen3, sen4)
n = len(sentences)
for i in range(n):
    sen1 = sentences[i]
    for j in range(i + 1, n):
        sen2 = sentences[j]
        elemsim = Similarity.sentence_sim_by_elem_bow(sen1, sen2, meaning_id)
        sim = Similarity.sentence_sim_by_elem_bow(sen1, sen2, meaning_id, scalar = True)
        print('{}, {}: "{}", "{}"'.format(sim, elemsim, sen1.get_text(), sen2.get_text()))

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

"""
SentenceLm について、文要素 (sentence element) ごとに bag-of-words で類似度を計算し、それを総合して SentenceLm の類似度とする。
処理の内容は、text_srclib/Similarity.sentencelm_sim_by_elem_bow に書かれている。
"""

print(Similarity.sentencelm_sim_by_elem_bow.__doc__)

slms = (slm1, slm2, slm3, slm4, slm5, slm6, slm7, slm8, slm9)
n = len(slms)
for i in range(n):
    slmi = slms[i]
    for j in range(i + 1, n):
        slmj = slms[j]
        elemsim = Similarity.sentencelm_sim_by_elem_bow(slmi, slmj, meaning_id)
        sim = Similarity.sentencelm_sim_by_elem_bow(slmi, slmj, meaning_id, scalar = True)
        print('{}, {}: "{}", "{}"'.format(sim, elemsim, slmi.get_sen(Lang.JPN).get_text(), slmj.get_sen(Lang.JPN).get_text()))

"""
Sentence の bag-of-words を取得し、Similarity.bag_sim により Sentence の類似度を計算する。
処理の内容は、text_srclib/Similarity.bag_sim に書かれている。
"""

print(Bag.get_elems.__doc__)

print(SentenceLm.bag_of_words.__doc__)

print(Similarity.bag_sim.__doc__)

# Word の類似度計算に使用する関数。
wsimf = lambda w1, w2: Similarity.word_sim(w1,
                                           w2,
                                           meaning_id = meaning_id,
                                           wsimexp = 1,
                                           wsimtype = CalcType.MAX_COMBI,
                                           msimtype = CalcType.MAX)

bowj1 = slm1.bag_of_words(Lang.JPN)
bowj2 = slm2.bag_of_words(Lang.JPN)
bowj3 = slm3.bag_of_words(Lang.JPN)
bowj4 = slm4.bag_of_words(Lang.JPN)
bowj5 = slm5.bag_of_words(Lang.JPN)
bowj6 = slm6.bag_of_words(Lang.JPN)
bowj7 = slm7.bag_of_words(Lang.JPN)
bowj8 = slm8.bag_of_words(Lang.JPN)
bowj9 = slm9.bag_of_words(Lang.JPN)

bows = (bowj1, bowj2, bowj3, bowj4, bowj5, bowj6, bowj7, bowj8, bowj9)
n = len(bows)
for i in range(n):
    seni = slms[i].get_sen(Lang.JPN).get_text()
    bowi = bows[i]
    wordlisti = tuple(w.get_text() for w in bowi.get_elems())
    for j in range(i + 1, n):
        senj = slms[j].get_sen(Lang.JPN).get_text()
        bowj = bows[j]
        wordlistj = tuple(w.get_text() for w in bowj.get_elems())
        fullinfo = Similarity.bag_sim(bowi, bowj, simf = wsimf, scalar = False, pairs = True)
        sim = Similarity.bag_sim(bowi, bowj, simf = wsimf, scalar = True, pairs = False)
        simlisti = fullinfo[0]
        simlistj = fullinfo[1]
        otherlisti = tuple(w.get_text() if w else None for w in fullinfo[2])
        otherlistj = tuple(w.get_text() if w else None for w in fullinfo[3])
        """
        sim: 頻度で重みづけ平均しスカラー化した総合類似度。
        simlisti: bow i の 各 Word について、bow j の 各 Word との間に得られた類似度の最大値。順番は wordlisti に対応。 
        simlistj: bow j の 各 Word について、bow i の 各 Word との間に得られた類似度の最大値。順番は wordlistj に対応。
        wordlisti: bow i の Word リスト。
        otherlisti: simlisti の計算において bow i の 各 Word に対応付けられた bow j の Word。類似度が 0 だった場合は None。
        wordlistj: bow j の Word リスト。
        otherlistj: simlistj の計算において bow j の 各 Word に対応付けられた bow i の Word。類似度が 0 だった場合は None。
        """
        print('"{}", "{}": {}, {}, {}, {}-{}, {}-{}'.format(seni, senj, sim, simlisti, simlistj, wordlisti, otherlisti, wordlistj, otherlistj))

print('* End *')
    
# End of file