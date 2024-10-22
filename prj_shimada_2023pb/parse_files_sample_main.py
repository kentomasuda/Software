# -*- coding: utf-8 -*-
"""
Parse files sample main

@author: MURAKAMI Tamotsu
@date: 2023-11-02
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from datetime import datetime
import json
from typing import Union

# Library
from edr_srclib.edr_parser import EdrParser

def delimit(text: str,
            punc: Union[str, None] = None) -> list:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-11-02
    """
    
    COMMA = '、'
    POINT = '。'

    if not punc is None:
        return [*text.split(punc)]
    elif COMMA in text:
        texts = []
        for x in text.split(COMMA):
            texts.extend(delimit(x, POINT))
        return texts
    elif POINT in text:
        texts = []
        for x in text.split(POINT):
            texts.extend(delimit(x, COMMA))
        return texts
    elif text:
        return [text]

"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-11-01
"""
if __name__ == '__main__':
    print('* Main start *')
    
    DIR_IN = './Data'
    DIR_OUT = './Output'
    
    KEY_AUTHOR = 'author'
    KEY_DATE = 'date'
    KEY_WORDS = 'words'
    
    author = 'MURAKAMI Tamotsu'

    for file_in in [filename for filename in os.listdir(DIR_IN) if filename.endswith('.txt')]:
        with open(os.path.join(DIR_IN, file_in), 'r', encoding='utf-8') as fin:
            text = fin.read()
            texts = []
            for x in text.split():
                if x:
                    texts.extend(delimit(x))
            words = []
            for x in texts:
                if x:
                    tagged = EdrParser.parse(x)[-1]
                    words.extend(tagged)
            now = datetime.now()
            data = {KEY_DATE: now.strftime('%Y-%m-%d %H:%M:%S'),
                    KEY_AUTHOR: author,
                    KEY_WORDS: words}
            file_out = file_in.replace('.txt', '.text.json')
            with open(os.path.join(DIR_OUT, file_out), 'w', encoding='utf-8') as fout:
                json.dump(data, fout, ensure_ascii=False, indent=0)

    print('* Main end *')

# End of file