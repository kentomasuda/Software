# -*- coding: utf-8 -*-
"""
EDR parse sample mainr

@author: MURAKAMI Tamotsu
@date: 2023-10-24
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_srclib.edr_parser import EdrParser


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-10-24
"""
if __name__ == '__main__':
    print('* Main start *')
    
    text = 'これは、見出し語を検出したテストです。'
    
    print('Similar is false (厳密一致のみ).')
    
    seqs = EdrParser.parse(text, similar=False)
    
    for seq in seqs[-10:]:
        print(seq)

    print('Similar is true (類似一致を含む).')

    seqs = EdrParser.parse(text, similar=True)
    
    for seq in seqs[-10:]:
        print(seq)

    print('* Main end *')

# End of file