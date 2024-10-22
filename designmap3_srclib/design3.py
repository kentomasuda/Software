# -*- coding: utf-8 -*-
"""
Design 3

@author: MURAKAMI Tamotsu
@date: 2024-06-09
"""

# Must be first
from __future__ import annotations

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import json

# Library

class Design3(dict):
    """
    Design 3

    @author: MURAKAMI Tamotsu
    @date: 2024-06-08
    """
    
    FILE_DATA_ENG = 'data_eng.json'
    FILE_DATA_JPN = 'data_jpn.json'
    FILE_INFO = 'info.json'

    KEY_AUTHOR = 'author'
    KEY_BHS = 'behaviors'
    KEY_DATE = 'date'
    KEY_FNS = 'functions'
    KEY_LANG = 'lang'
    KEY_NAME = 'type'
    KEY_STS = 'structures'
    KEY_TYPE = 'type'
    KEY_UXS = 'userExperiences'
   
    VAL_NOUN = "Noun"  # noun、名詞、普通名詞
    VAL_PROPN = "PropN"  # proper noun、固有名詞
    
    VAL_ENG = "Eng"  # English
    VAL_JPN = "Jpn"  # Japanese

    def __init__(self,
                 author: str = None,
                 bhs: list = [],
                 date: str = None,
                 fns: list = [],
                 lang: str = None,
                 name: str = None,
                 sts: list = [],
                 type_: str = None,
                 uxs: list = []):
        """
        @author MURAKAMI Tamotsu
        @date 2024-06-08
        """
        
        super().__init__()
        
        self[Design3.KEY_AUTHOR] = author
        self[Design3.KEY_BHS] = bhs
        self[Design3.KEY_DATE] = date
        self[Design3.KEY_FNS] = fns
        self[Design3.KEY_LANG] = lang
        self[Design3.KEY_NAME] = name
        self[Design3.KEY_STS] = sts
        self[Design3.KEY_TYPE] = type_
        self[Design3.KEY_UXS] = uxs
    
    @staticmethod
    def load(dirpath: str,
             lang: str = VAL_JPN) -> Design3:
        """
        @author MURAKAMI Tamotsu
        @date 2024-06-09
        """
        
        if os.path.exists(dirpath):
            author = None
            bhs = []
            date = None
            fns = []
            name = None
            sts = []
            type_ = None
            uxs = []
            
            filepath = os.path.join(dirpath, Design3.FILE_INFO)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    info = json.load(f)

                if Design3.KEY_AUTHOR in info:
                    author =  info[Design3.KEY_AUTHOR]

                if Design3.KEY_DATE in info:
                    date =  info[Design3.KEY_DATE]

                if Design3.KEY_TYPE in info:
                    type_ =  info[Design3.KEY_TYPE]
            
            if lang == Design3.VAL_JPN:
                filepath = os.path.join(dirpath, Design3.FILE_DATA_JPN)
            elif lang == Design3.VAL_ENG:
                filepath = os.path.join(dirpath, Design3.FILE_DATA_ENG)
            else:
                filepath = None

            if filepath and os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if Design3.KEY_BHS in data:
                    bhs = data[Design3.KEY_BHS]

                if Design3.KEY_FNS in data:
                    fns = data[Design3.KEY_FNS]

                if Design3.KEY_NAME in data:
                    name = data[Design3.KEY_NAME]
            
                if Design3.KEY_STS in data:
                    sts = data[Design3.KEY_STS]

                if Design3.KEY_UXS in data:
                    uxs = data[Design3.KEY_UXS]
            
            if author or bhs or date or fns or lang or name or sts or type_ or uxs:
                return Design3(author = author,
                               bhs = bhs,
                               date = date,
                               fns = fns,
                               lang = lang,
                               name = name,
                               sts = sts,
                               type_ = type_,
                               uxs = uxs)
            else:
                return None

        else:
            print('Design3: path "{}" not found.'.format(dirpath))
            return None
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-03-09
"""

if __name__ == '__main__':

    print('* Test starts *')
    
   
    print('* Main ends *')

# End of file