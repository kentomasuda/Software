# -*- coding: utf-8 -*-
"""
Ginza parse sample main

https://megagonlabs.github.io/ginza/

@author: MURAKAMI Tamotsu
@date: 2023-11-28
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from ginza_srclib.ginza_ import Ginza_


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-11-28
"""

if __name__ == '__main__':

    print('* Main starts *')
    
    text = 'LGBTのような新しい概念にも対応できます。'

    text_lemma_pos_seq = Ginza_.parse_text(text)
    print(text_lemma_pos_seq)

    print('* Main ends *')
    
# End of file