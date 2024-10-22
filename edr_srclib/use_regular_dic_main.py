# -*- coding: utf-8 -*-
"""
Use regular dictionaries main

@author: MURAKAMI Tamotsu
@date: 2019-02-06
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Library
from edr_lib.concept import Concept, CpcCol, CphCol, CptCol, RelLabel
from edr_lib.e_word import EwCol, EWord
from edr_lib.j_word import JwCol, JWord

"""
Main

Using regular dictionary is more general and versatile 
than using the simple dictionary.

@author: MURAKAMI Tamotsu
@date: 2019-02-06
"""

print('* Start *')

# 概念識別子から日本語概念説明を取得する。

print(JWord.search_jw_dic.__doc__)

result = JWord.search_jw_dic(concept_id='3ce65d', return_=JwCol.JPN_CONCEPT_EXPL)
print(result)

# 概念識別子から英語概念説明を取得する。

print(EWord.search_ew_dic.__doc__)

result = EWord.search_ew_dic(concept_id='3ce65d', return_=EwCol.ENG_CONCEPT_EXPL)
print(result)

# 概念識別子の一つ上位の概念識別子を取得する。

print(Concept.__doc__)

print(Concept.search_cpc_dic.__doc__)

result = Concept.search_cpc_dic(sub_concept_id='0f431a', return_=CpcCol.SUPER_CONCEPT_ID)
print(result)

# 概念識別子の英語概念説明を取得する。

print(Concept.search_cph_dic.__doc__)

result = Concept.search_cph_dic(concept_id='0f431a', return_=CphCol.ENG_CONCEPT_EXPL)
print(result)

# 概念識別子1と関係子'agent'の関係にある概念識別子2の対を取得する。

print(RelLabel.__doc__)

print(Concept.search_cpt_dic.__doc__)

result = Concept.search_cpt_dic(concept_id1='3f92e8', rel_label=RelLabel.AGENT.value,
                                return_=CptCol.CONCEPT_ID2)
print(result)

print('* End *')
        
# End of file