# -*- coding: utf-8 -*-
"""
EDR explanation sample main

@author: MURAKAMI Tamotsu
@date: 2022-10-13
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import pprint

# Library
from edr_lib.edr import Edr

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-10-13
"""
if __name__ == '__main__':
    print('* Main starts *')
    
    text = '赤'
    expls = Edr.get_headword_expl(text)
    print(text)
    pprint.pprint(expls)

    text = '緑化'
    expls = Edr.get_headword_expl(text)
    print(text)
    pprint.pprint(expls)

    print('* Test end *')

# End of file