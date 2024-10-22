#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Text xml

@author: MURAKAMI Tamotsu
@date: 2021-07-04
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from xml.etree.ElementTree import Element

# Library
from text_lib.text import Text_

class TextXml:
    """
    Text xml
    
    @author: MURAKAMI Tamotsu
    @date: 2021-07-03
    """
    
    ATTR_ENG = 'eng'
    ATTR_JPN = 'jpn'

    TAG_A = 'a'
    TAG_ADJ = 'aj'
    TAG_ADV = 'av'
    TAG_C = 'c'
    TAG_ENG = 'eng'
    TAG_JPN = 'jpn'
    TAG_LM = 'lm'
    TAG_M = 'm'
    TAG_N = 'n'
    TAG_NP = 'np'
    TAG_O = 'o'
    TAG_OI = 'oi'
    TAG_S = 's'
    TAG_SEN = 'sen'
    TAG_T = 't'
    TAG_V_POS = 'v'
    TAG_V_SEN_ELEM = 'v'

    @staticmethod
    def msg_unexpected_attr(attr: str,
                            tag: str):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-28
        """
        
        print('Unexpected attribute "{}" in tag "{}".'.format(attr, tag))

    @staticmethod
    def msg_unexpected_tag(child: str,
                           parent: str):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-27
        """
        
        print('Unexpected tag "{}" under tag "{}".'.format(child, parent))

    @staticmethod
    def no_space_after(x: str) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-07-04
        """
        
        judge = False
        
        for y in ('(', '[', '{'):
            if x.endswith(y):
                judge = True
                break;
        
        return judge

    @staticmethod
    def no_space_before(x: str) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-07-04
        """
        
        judge = False
        
        for y in (',', '.', '!', '?', ';', ':', '%', ')', ']', '}'):
            if x.startswith(y):
                judge = True
                break;
        
        return judge

    @staticmethod
    def parse_lm(lm: Element):
        """
        Language map (言語マップ)

        @author: MURAKAMI Tamotsu
        @date: 2021-06-28
        """

        words_out = None

        return Text_.xml_parse_tree(lm, words_out)

"""
Test

@author: MURAKAMI Tamotsu
@date: 2021-06-27
"""

if __name__ == '__main__':
    print('* Test starts *')
    
    print('* Test ends *')

# End of file