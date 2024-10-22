# -*- coding: utf-8 -*-
"""
Natural language processing sample

@author: MURAKAMI Tamotsu
@date: 2018-01-11
"""

import sys
import os

sys.path.append(os.pardir)

from libs_py.lib_text import Cabocha
from libs_py.lib_text import Chunk
from libs_py.lib_text import Mecab
from libs_py.lib_text import Morpheme
from libs_py.lib_text import Pos
from libs_py.lib_text import PosSec1
from libs_py.lib_text import PosSec2
from libs_py.lib_text import PosSec3

print('start')

print(Pos.__doc__)
print(PosSec1.__doc__)
print(PosSec2.__doc__)
print(PosSec3.__doc__)
print(Morpheme.__doc__)
print(Chunk.__doc__)

# MeCab

# result = Mecab.parse('これは文章です。MeCabはうまく解析できるでしょうか。')
result = Mecab.parse('仕事をしている。')

print(result)

for m in Mecab.parse_result(result):
    print(vars(m))

# CaboCha
    
print(Cabocha.parse.__doc__)

result = Cabocha.parse('これは文章です。CaboChaはうまく解析できるでしょうか。')

print(result)

for c in Cabocha.parse_result(result):
    print(vars(c))
    for m in c.morphemes:
        print('\t', vars(m))

print('end')

# End of file