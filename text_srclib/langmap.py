# -*- coding: utf-8 -*-
"""
Language map　（言語マップ)

@author: MURAKAMI Tamotsu
@date: 2022-10-09
"""

# For directory management
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from text_lib.lang import Lang
from text_lib.lang import LangTag
from text_lib.phraselm import PhraseLm
from text_lib.sentence import Sentence
from text_lib.sentence import SentenceLm
from text_lib.syntactic_elem import SyntacticElem, SyntacticElemLm
from text_lib.word_phrase import Phrase
from text_lib.word_phrase import Word
from text_lib.wordlm import WordLm

class LangMap(dict):
    """
    @author: MURAKAMI Tamotsu
    @date: 2022-10-09
    """
    
    def __init__(self,
                 lang: Lang = None,
                 elem = None):
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-09
        """
        
        super().__init__()
        
        self.set_elem(lang, elem)
    
    @staticmethod        
    def dict_to_string(langtag_elemstr_dict: dict) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-09-30
        """
        
        LANGTAGS = LangTag.all_()
        langs_str = ''

        for langtag, elemstr in langtag_elemstr_dict.items():
            if langtag in LANGTAGS:
                langs_str += '<{}>{}</{}>'.format(langtag, elemstr, langtag)
        
        return '<{}>{}</{}>'.format(SyntacticElem.TAG_LM, langs_str, SyntacticElem.TAG_LM)
        
    @staticmethod        
    def fromdict(lang_elem_dict: dict) -> SyntacticElemLm:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-07-02
        """
        
        elems = tuple(lang_elem_dict.values())
        typeset = set(type(elem) for elem in elems)
        
        if typeset == {Sentence}:
            senlm = SentenceLm(elems[0])
            for sen in elems[1:]:
                senlm.set_sen(sen)
            return senlm
        elif typeset == {Phrase}:
            phlm = PhraseLm(elems[0])
            for ph in elems[1:]:
                phlm.set_phrase(ph)
            return phlm
        elif typeset == {Word}:
            wlm = WordLm(elems[0])
            for w in elems[1:]:
                wlm.set_word(w)
            return wlm
        
    def get_elem(self,
                 lang: Lang): # -> element:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-09
        """
        
        if lang in self:
            return self[lang]
        else:
            return None

    def set_elem(self,
                 lang: Lang,
                 elem):
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-09
        """

        if (not lang is None) and (not elem is None):
            self[lang] = elem

"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-10-09
"""

if __name__ == '__main__':
    print('* Test starts *')
    
    langmap = LangMap()
    print(langmap)
    langmap.set_elem('a', 'b')
    print(langmap)
    
    # print(LangMap.dict_to_string({}))
   
    print('* Test ends *')
    
    # End of file