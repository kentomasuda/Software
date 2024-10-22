# -*- coding: utf-8 -*-
"""
Calculate similarity sample main

@author: MURAKAMI Tamotsu
@date: 2024-06-09
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from designmap3_srclib.design3 import Design3
from designmap3_srclib.designmap3 import DesignMap3
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_


"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-06-09
"""
if __name__ == '__main__':
    print('* Main start *')
    
    
    DIR_IN = '../designmap3_1_data'
    DIR_OUT = './Output'
    
    if not os.path.isdir(DIR_OUT):
        os.mkdir(DIR_OUT)

    designs = DesignMap3.load_designs(DIR_IN)
    print(designs)
    n = len(designs)
    
    sim_fni_fnj_list = []
    
    for i in range(0, 1):
        design_i = designs[i]
        fns_i = design_i[Design3.KEY_FNS]
        for fni in fns_i:
            for j in range(i + 1, 2):
                design_j = designs[j]
                fns_j = design_j[Design3.KEY_FNS]
                for fnj in fns_j:
                    sim = SentenceTransformers_.calc_sim(fni, fnj, cached=True)
                    print((sim, fni, fnj))
                    sim_fni_fnj_list.append((sim, fni, fnj))

    sim_fni_fnj_list.sort()
    with open(os.path.join(DIR_OUT, 'sim_fni_fnj_list.txt'), 'w', encoding='utf-8') as f:
        for sim_fni_fnj in sim_fni_fnj_list:
            print(sim_fni_fnj, file=f)
    
    print('* Main end *')

# End of file