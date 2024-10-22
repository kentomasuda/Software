# -*- coding: utf-8 -*-
"""
Statistics sample

@author: MURAKAMI Tamotsu
@date: 2018-03-28
"""

import sys
import os

sys.path.append(os.pardir)

from libs_py.lib_stats import NGram

print('start')

data1 = ['t','h','i','s',
         'i','s',
         'n','g','r','a','m',
         't','e','s','t',
         'd','a','t','a',
         's','e','q','u','e','n','c','e']

data2 = [('t',0),('h',1),('i',2),('s',0),
         ('i',1),('s',2),
         ('n',0),('g',1),('r',2),('a',0),('m',1),
         ('t',2),('e',0),('s',1),('t',2),
         ('d',0),('a',1),('t',2),('a',0),
         ('s',1),('e',2),('q',0),('u',1),('e',2),('n',0),('c',1),('e',2)]

print(NGram.classify.__doc__)

dct = NGram.classify(data1, 1)
print(dct)
print()

dct = NGram.classify(data1, 2)
print(dct)
print()

dct = NGram.classify(data2, 1)
print(dct)
print()

dct = NGram.classify(data2, 1, key = (lambda x: x[0]))
print(dct)
print()

dct = NGram.classify(data2, 2)
print(dct)
print()

dct = NGram.classify(data2, 2, key = (lambda x: x[0]))
print(dct)
print()

print('end')

# End of File