# -*- coding: utf-8 -*-
"""
EDR basic sample

@author: MURAKAMI Tamotsu
@date: 2020-07-11
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.edr import Edr
22
"""
Main

@author: MURAKAMI Tamotsu
@date: 2020-06-25
"""

print('* Start *')

print(Edr.load_simple_dict.__doc__)

Edr.load_simple_dict()

print(Edr.get_conceptid_by_input_word.__doc__)

conceptid = Edr.get_conceptid_by_input_word(word = 'きれいだ')
print(conceptid)

conceptid = Edr.get_conceptid_by_input_word(word = 'きれいな')
print(conceptid)

conceptid = Edr.get_conceptid_by_input_word(word = 'beautiful')
print(conceptid)

conceptid = Edr.get_conceptid_by_input_word()
print(conceptid)

print('* End *')       

# End of file