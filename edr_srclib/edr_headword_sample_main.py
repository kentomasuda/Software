# -*- coding: utf-8 -*-
"""
EDR headword sample

@author: MURAKAMI Tamotsu
@date: 2023-12-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.edr import Edr
from edr_srclib.jwpos import JwPos
from text_lib.lang import Lang
from text_srclib.simplepos import SimplePos

"""
Main

@author: MURAKAMI Tamotsu
@date: 2021-06-04
"""

if __name__ == '__main__':
    print('* Start *')
    
    print(JwPos.__doc__)
    
    print(SimplePos.__doc__)
    
    lang = Lang.JPN
    
    pos = SimplePos.N
    # pos = JwPos.JN2
    
    for word in Edr.get_headwords(lang=lang, pos=pos):
        print('{}: {}'.format(pos, word))

    print('* End *')       

# End of file