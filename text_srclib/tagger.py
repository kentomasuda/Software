# -*- coding: utf-8 -*-
"""
Tagger

@author: MURAKAMI Tamotsu
@date: 2021-10-19
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from cabocha_srclib.cabocha import Cabocha
from cabocha_srclib.pos import Pos
from text_srclib.textxml import TextXml

class Tagger:
    """
    タグ付け
    
    @author MURAKAMI Tamotsu
    @date 2021-10-19
    """
    
    POS_TAG = {
        Pos.ADJECTIVE: TextXml.TAG_ADJ,
        Pos.ADVERB: TextXml.TAG_ADV,
        Pos.NOUN: TextXml.TAG_N,
        Pos.VERB: TextXml.TAG_V_POS
        }
    
    @staticmethod
    def parse(sentence: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-10-19
        
        """
        
        tagged = ''
        nopos_text = ''
        
        output = Cabocha.parse(sentence)
        
        for chunk in Cabocha.parse_output(output):
            for morph in chunk.morphemes:
                pos = morph.get_pos_info()[0]
                if pos == Pos.ADJECTIVE or pos == Pos.ADVERB or pos == Pos.NOUN or pos == Pos.VERB:
                    if nopos_text != '':
                        tagged += '<{1}>{0}</{1}>'.format(nopos_text, TextXml.TAG_T)
                        nopos_text = ''
                    org_form = morph.get_original_form()
                    lemma = morph.get_lemma()
                    if lemma is None or org_form == lemma:
                        tagged += '<{1}>{0}</{1}>'.format(org_form, Tagger.POS_TAG[pos])
                    else:
                        tagged += '<{1} jpn="{2}">{0}</{1}>'.format(org_form, Tagger.POS_TAG[pos], lemma)
                else:
                    nopos_text += morph.get_original_form()

        if nopos_text != '':
            tagged += '<{1}>{0}</{1}>'.format(nopos_text, TextXml.TAG_T)

        return tagged
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2021-10-19
"""

if __name__ == '__main__':

    print('* Test start *')
    
    tagged = Tagger.parse('これは文章です。CaboChaはうまく解析できたでしょうか。')
    print(tagged)    
    
    print('* Test end *')
    
# End of file