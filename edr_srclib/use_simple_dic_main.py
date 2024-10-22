# -*- coding: utf-8 -*-
"""
Use simple dictionary main

@author: MURAKAMI Tamotsu
@date: 2019-02-06
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Library
from edr_lib.concept import Concept
from edr_lib.e_word import EWord, EwPos
from edr_lib.j_word import JWord, JwPos

"""
Main

For the following purposes, using the simple dictionary by methods below 
should be more efficient than using regular dictionaries.

@author: MURAKAMI Tamotsu
@date: 2019-02-06
"""

print('* Start *')

# 見出し語にあるかをチェックする。

print(JWord.check_headword.__doc__)

result = JWord.check_headword('テスト')
print(result)

result = JWord.check_headword('機能')
print(result)

print(EWord.check_headword.__doc__)

result = EWord.check_headword('nighter')
print(result)

# 見出し語から品詞を取得する。

print(JwPos.__doc__)

print(JWord.get_poses_by_headword.__doc__)

result = JWord.get_poses_by_headword('青い')
print(result)

print(EwPos.__doc__)

print(EWord.get_poses_by_headword.__doc__)

result = EWord.get_poses_by_headword('blue')
print(result)

# 見出し語から概念識別子を取得する。

print(JWord.get_concept_ids_by_headword.__doc__)

result = JWord.get_concept_ids_by_headword('色')
print(result)

# 概念識別子から見出し語を取得する。

print(JWord.get_headwords_by_concept_id.__doc__)

result = JWord.get_headwords_by_concept_id('3ce622')
print(result)

print(EWord.get_headwords_by_concept_id.__doc__)

result = EWord.get_headwords_by_concept_id('3ce622')
print(result)

# 概念識別子の一つ上位の概念識別子を取得する。

print(Concept.get_super_concept_ids.__doc__)

result = Concept.get_super_concept_ids('3ce622')
print(result)

# 概念識別子の一つ下位の概念識別子を取得する。

print(Concept.get_sub_concept_ids.__doc__)

result = Concept.get_sub_concept_ids('3ce622')
print(result)

print('* End *')
        
# End of file