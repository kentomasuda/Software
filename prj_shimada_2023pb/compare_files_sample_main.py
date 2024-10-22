# -*- coding: utf-8 -*-
"""
Compare files sample main

@author: MURAKAMI Tamotsu
@date: 2023-11-09
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import json
from xml.etree import ElementTree

# Library
from designmap3_srclib.designmap3 import DesignMap3
from edr_lib.edr import Edr
from misc_srclib.handling import Handling
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.simplepos import SimplePosTag
from text_srclib.text_similarity import TextSimilarity


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-11-09
"""
if __name__ == '__main__':
    print('* Main start *')
    
    # Extension
    EXT_TEXT_JSON = '.text.json'
    
    KEY_DIFF1 = 'diff1'
    KEY_DIFF2 = 'diff2'
    KEY_COMMON = 'common'
    KEY_WORDS = 'words'
    
    
    DIR_IN = './Data'
    DIR_OUT = './Output'
    
    if not os.path.isdir(DIR_OUT):
        os.mkdir(DIR_OUT)

    author = 'MURAKAMI Tamotsu'
    
    meaning_id = Edr.ID
    
    design_dict = {}

    for file_in in [filename for filename in os.listdir(DIR_IN) if filename.endswith('.text.json')]:
        with open(os.path.join(DIR_IN, file_in), 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            texts = data[DesignMap3.KEY_WORDS]
            words = []
            for text in texts:
                elem = ElementTree.fromstring(text)
                tag = elem.tag
                if tag == SimplePosTag.AJ or tag == SimplePosTag.AV or tag == SimplePosTag.N or tag == SimplePosTag.V:
                    word = Text_.xml_parse_tree(elem, lang=Lang.JPN, unexpected=Handling.IGNORE)
                    Meaning.fill_meaning(word, meaning_id=meaning_id)
                    words.append(word)
        design_dict[file_in.replace(EXT_TEXT_JSON, '')] = {KEY_WORDS: words}
    
    names = tuple(design_dict.keys())
    n = len(names)
    
    sim_threshold = 0.9
    
    analysis = []

    for i in range(n):
        name_i = names[i]
        words_i = design_dict[name_i][KEY_WORDS]
        texts_i = {w.get_text() for w in words_i}
        for j in range(i + 1, n):
            name_j = names[j]
            print('Comparing "{}" and "{}"...'.format(name_i, name_j))
            words_j = design_dict[name_j][KEY_WORDS]
            texts_j = {w.get_text() for w in words_j}
            texts_common = set()
            for wi in words_i:
                for wj in words_j:
                    sim = TextSimilarity.word_sim(wi, wj, meaning_id=meaning_id)
                    if sim >= sim_threshold:
                        texts_common.add(wi.get_text())
                        texts_common.add(wj.get_text())
            texts_diff1 = texts_i - texts_common
            texts_diff2 = texts_j - texts_common
            sim = len(texts_common) / len(texts_i | texts_j)
            analysis.append([(sim, name_i, name_j), {KEY_COMMON: texts_common, KEY_DIFF1: texts_diff1, KEY_DIFF2: texts_diff2}])

    for key, val in sorted(analysis):
        print(key, val)
    
    print('* Main end *')

# End of file