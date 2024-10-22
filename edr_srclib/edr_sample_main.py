# -*- coding: utf-8 -*-
"""
EDR sample

@author: MURAKAMI Tamotsu
@date: 2023-12-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Library
from edr_lib.concept import EdrClsf
from edr_lib.e_word import EwPos
from edr_lib.edr import Edr
from edr_srclib.jwpos import JwPos
from text_lib.lang import Lang

"""
Main

@author: MURAKAMI Tamotsu
@date: 2019-06-27
"""

print('* Start *')

# 見出し語にあるかをチェックする。

print(Edr.check_headword.__doc__)

print(Edr.check_headword('機能', lang=Lang.JPN, suggest=True, simmin=0.25))

print(Edr.check_headword('good', lang=Lang.ENG, suggest=True, simmin=0.25))

# 見出し語から品詞を取得する。

print(JwPos.__doc__)

print(EwPos.__doc__)

print(Edr.headword_pos.__doc__)

print(Edr.headword_pos('青い'))

print(Edr.headword_pos('青い', simplepos=False))

print(Edr.headword_pos('青'))

print(Edr.headword_pos('青', simplepos=False))

print(Edr.headword_pos('blue'))

print(Edr.headword_pos('blue', simplepos=False))

# 見出し語から概念識別子を取得する。

print(Edr.headword_conceptid.__doc__)

print(Edr.headword_conceptid('色', lang=Lang.JPN))

print(Edr.headword_conceptid('color', lang=Lang.ENG))

# 概念識別子から見出し語を取得する。

print(Edr.conceptid_headword.__doc__)

print(Edr.conceptid_headword('3ce622', lang=Lang.JPN))

print('* ', Edr.conceptid_headword('30f93f', lang=Lang.JPN|Lang.ENG))

print(Edr.conceptid_of_classification.__doc__)

cid_org = '3cfd1a'

print('{}: {}'.format(cid_org, Edr.conceptid_headword(cid_org, lang=Lang.JPN|Lang.ENG)))

# 概念識別子の一つ上位の概念識別子を取得する。
cids = Edr.conceptid_of_classification(cid_org, clsf=EdrClsf.SUPER)
print(cids)
for cid in cids:
    print('{}: {}'.format(cid, Edr.conceptid_headword(cid, lang=Lang.JPN|Lang.ENG)))

# 概念識別子の一つ下位の概念識別子を取得する。
cids = Edr.conceptid_of_classification(cid_org, clsf=EdrClsf.SUB)
print(cids)
for cid in cids:
    print('{}: {}'.format(cid, Edr.conceptid_headword(cid, lang=Lang.JPN|Lang.ENG)))

print('* End *')
        
# End of file