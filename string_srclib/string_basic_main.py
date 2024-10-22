# -*- coding: utf-8 -*-
"""
String library basic sample

@author: MURAKAMI Tamotsu
@date: 2021-11-27
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from string_srclib.string import String
from string_srclib.strrel import StrRel

print('* Test start *')

print(String.compare.__doc__)

print(StrRel.__doc__)

print(String.similarity.__doc__)

STRING_PAIRS = (
        ('東京', 'とうきょう'),
        ('トウキョウ', 'とうきょう'),
        ('東大', '大学'),
        ('計る', '設計'),
        ('設計研', '設計'),
        ('青', '青い'),
        ('不自由な', '自由な'),
        ('大学', '東京大学'),
        ('等しい', '等しい'),
        ('機械工学科', '工学'),
        ('工学', '機械工学専攻'),
        ('青い', '青く'),
        ('自然科学', '天然素材'),
        ('東京大学', '京都大学'),
        ('阪神タイガース', '阪急ブレーブス'),
        )

for pair in STRING_PAIRS:
    str1, str2 = pair 
    rel = String.compare(str1, str2, case = True, zenhan = True, match = True, unmatch = True)
    print('"{}", "{}": {}'.format(str1, str2, rel))

for pair in STRING_PAIRS:
    str1, str2 = pair 
    sim = String.similarity(str1, str2, case = True, zenhan = True)
    print('"{}", "{}": {}'.format(str1, str2, sim))

print('* Test end *')
    
# End of file