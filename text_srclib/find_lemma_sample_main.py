# -*- coding: utf-8 -*-
"""
Find lemma sample main

@author: MURAKAMI Tamotsu
@date: 2022-12-16
"""

# For directory access
import os
import pprint
import sys
sys.path.append(os.pardir)

# Python

# Library
from text_srclib.tagging import Tagging
    
if __name__ == '__main__':

    print('* Main starts *')
    
    print(Tagging.find_edr_headword.__doc__)
    
    text = 'text中の見出し語を探す。'
    
    result = Tagging.find_edr_headword(text, simmin=0.8, progress=True)
    
    pprint.pprint(result)

    print('* Main ends *')
    
# End of file