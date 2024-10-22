# -*- coding: utf-8 -*-
"""
Sentence basic sample

@author: MURAKAMI Tamotsu
@date: 2022-10-13
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from xml.etree import ElementTree

# Library
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.sentence import Sentence
from text_lib.text import Text_
from edr_lib.edr import Edr
from math_srclib.calc_type import CalcType
from text_srclib.text_similarity import TextSimilarity
from wordnet_lib.wordnet import WordNet

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-12-12
"""

if __name__ == "__main__":
    print('* Start *')
    
    """
    Select concept dictionary to handle meaning
    """

    meaning_id = Edr.ID # EDR
    # meaning_id = WordNet.ID # WordNet
    # meaning_id = (Edr.ID, WordNet.ID) # EDR and WordNet
    
    """
    Sentence
    """
    
    xmlstr = '<jpn><sen><s><n>自動車</n></s>が<v><v>走る</v></v>。</sen></jpn>'
    sj1 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(sj1, meaning_id)
    print('sj1 =', sj1)
    print('sj1.text =', sj1.get_text())
    
    # '<jpn><sen><s><n>自動車</n></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn>'
    lang = Lang.JPN
    s = Text_.xml_parse_tree(ElementTree.fromstring('<n>自動車</n>'), lang=lang)
    Meaning.fill_meaning(s, meaning_id)
    a = Text_.xml_parse_tree(ElementTree.fromstring('<av eng="fast">速く</av>'), lang=lang)
    Meaning.fill_meaning(a, meaning_id)
    v = Text_.xml_parse_tree(ElementTree.fromstring('<v>走る</v>'), lang=lang)
    Meaning.fill_meaning(v, meaning_id)
    sj2 = Sentence(s=s, a=a, v=v, lang=lang)
    print('sj2 =', sj2)
    print('sj2.text =', sj2.get_text())
    
    xmlstr = '<jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s>が<v><v>走る</v></v>。</sen></jpn>'
    sj3 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(sj3, meaning_id)
    print('sj3 =', sj3)
    
    xmlstr = '<jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn>'
    sj4 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(sj4, meaning_id)
    print(sj4)
    
    xmlstr = '<jpn><sen><s><n>列車</n></s>が<v><v>走る</v></v>。</sen></jpn>'
    sj5 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(sj5, meaning_id)
    print(sj5)
    
    print(TextSimilarity.sentence_sim.__doc__)

    print('sim(sj1,sj2)=', TextSimilarity.sentence_sim(sj1, sj2, meaning_id, scalar=False))
    print('sim(sj1,sj2)=', TextSimilarity.sentence_sim(sj1, sj2, meaning_id, scalar=True))
    
    print('sim(sj1,sj3)=', TextSimilarity.sentence_sim(sj1, sj3, meaning_id, scalar=False))
    print('sim(sj1,sj4)=', TextSimilarity.sentence_sim(sj1, sj4, meaning_id, scalar=False))
    print('sim(sj1,sj5)=', TextSimilarity.sentence_sim(sj1, sj5, meaning_id, scalar=False))
    print('sim(sj2,sj3)=', TextSimilarity.sentence_sim(sj2, sj3, meaning_id, scalar=False))
    print('sim(sj2,sj4)=', TextSimilarity.sentence_sim(sj2, sj4, meaning_id, scalar=False))
    print('sim(sj2,sj5)=', TextSimilarity.sentence_sim(sj2, sj5, meaning_id, scalar=False))
    print('sim(sj3,sj4)=', TextSimilarity.sentence_sim(sj3, sj4, meaning_id, scalar=False))
    print('sim(sj3,sj5)=', TextSimilarity.sentence_sim(sj3, sj5, meaning_id, scalar=False))
    print('sim(sj4,sj5)=', TextSimilarity.sentence_sim(sj4, sj5, meaning_id, scalar=False))
    
    """
    SentenceLm (language map)
    """
    
    xmlstr = '<lm><eng><sen>An<s><n>automobile</n></s><v><v eng="run">runs</v></v>.</sen></eng>\
        <jpn><sen><s><n>自動車</n></s>が<v><v>走る</v></v>。</sen></jpn></lm>'
    slm1 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm1, meaning_id)
    print(slm1)
    
    xmlstr = '<lm><eng><sen>An<s><n>automobile</n></s><v><v eng="run">runs</v></v><a><av>fast</av></a>.</sen></eng>\
        <jpn><sen><s><n>自動車</n></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn></lm>'
    slm2 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm2, meaning_id)
    print(slm2)
    
    xmlstr = '<lm><eng><sen>A<s><np><m><aj>red</aj></m><n>automobile</n></np></s><v><v eng="run">runs</v></v>.</sen></eng>\
        <jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s>が<v><v>走る</v></v>。</sen></jpn></lm>'
    slm3 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm3, meaning_id)
    print(slm3)
    
    xmlstr = '<lm><eng><sen>A<s><np><m><aj>white</aj></m><n>automobile</n></np></s><v><v eng="run">runs</v></v><a><av>fast</av></a>.</sen></eng>\
        <jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn></lm>'
    slm4 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm4, meaning_id)
    print(slm4)
    
    xmlstr = '<lm><eng><sen>A<s><n>train</n></s><v><v eng="run">runs</v></v>.</sen></eng>\
        <jpn><sen><s><n>列車</n></s>が<v><v>走る</v></v>。</sen></jpn></lm>'
    slm5 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm5, meaning_id)
    print(slm5)
    
    xmlstr = '<lm><eng><sen><s>A<n>camera</n></s><v><v eng="record">records</v></v><o>a<n>photograph</n></o>.</sen></eng>\
        <jpn><sen><s><n>カメラ</n></s>が<o><n>写真</n></o>を<v><v>記録する</v></v>。</sen></jpn></lm>'
    slm6 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm6, meaning_id)
    print(slm6)
    
    xmlstr = '<lm><eng><sen><s>A<n>user</n></s><v><v eng="keep">keeps</v></v><o>a<n>scene</n></o>.</sen></eng>\
        <jpn><sen><s><n>ユーザ</n></s>が<o><n>光景</n></o>を<v><v>保存する</v></v>。</sen></jpn></lm>'
    slm7 = Text_.xml_parse_tree(ElementTree.fromstring(xmlstr))
    Meaning.fill_meaning(slm7, meaning_id)
    print(slm7)
    
    print(TextSimilarity.sentencelm_sim.__doc__)
    
    # lsimtype = CalcType.JPN
    lsimtype = CalcType.MAX

    print('sim(slm1,slm2)=', TextSimilarity.sentencelm_sim(slm1, slm2, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm1,slm3)=', TextSimilarity.sentencelm_sim(slm1, slm3, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm1,slm4)=', TextSimilarity.sentencelm_sim(slm1, slm4, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm1,slm5)=', TextSimilarity.sentencelm_sim(slm1, slm5, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm1,slm6)=', TextSimilarity.sentencelm_sim(slm1, slm6, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm1,slm7)=', TextSimilarity.sentencelm_sim(slm1, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm2,slm3)=', TextSimilarity.sentencelm_sim(slm2, slm3, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm2,slm4)=', TextSimilarity.sentencelm_sim(slm2, slm4, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm2,slm5)=', TextSimilarity.sentencelm_sim(slm2, slm5, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm2,slm6)=', TextSimilarity.sentencelm_sim(slm2, slm6, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm2,slm7)=', TextSimilarity.sentencelm_sim(slm2, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm3,slm4)=', TextSimilarity.sentencelm_sim(slm3, slm4, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm3,slm5)=', TextSimilarity.sentencelm_sim(slm3, slm5, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm3,slm6)=', TextSimilarity.sentencelm_sim(slm3, slm6, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm3,slm7)=', TextSimilarity.sentencelm_sim(slm3, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm4,slm5)=', TextSimilarity.sentencelm_sim(slm4, slm5, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm4,slm6)=', TextSimilarity.sentencelm_sim(slm4, slm6, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm4,slm7)=', TextSimilarity.sentencelm_sim(slm4, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm5,slm6)=', TextSimilarity.sentencelm_sim(slm5, slm6, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm5,slm7)=', TextSimilarity.sentencelm_sim(slm5, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    print('sim(slm6,slm7)=', TextSimilarity.sentencelm_sim(slm6, slm7, meaning_id, lsimtype=lsimtype, scalar=False))
    
    print('* End *')
    
# End of file