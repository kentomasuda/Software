# -*- coding: utf-8 -*-
"""
EDR check_headword

@author: MURAKAMI Tamotsu
@date: 2022-01-18
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.edr import Edr
from text_lib.lang import Lang

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-01-18
"""

print('* Start *')

# 見出し語にあるかをチェックする。

print(Edr.check_headword.__doc__)

print(Edr.check_headword('きれいな', lang=Lang.JPN, suggest=True, simmin=0.3))

print(Edr.check_headword_polysemy('きれいだ', lang=Lang.JPN, simmin=0.3))

print(Edr.check_headword('good', lang=Lang.ENG, suggest=True, simmin=0.3))

print(Edr.check_headword_polysemy('good', lang=Lang.ENG, simmin=0.3))

print('* End *')
        
# End of file