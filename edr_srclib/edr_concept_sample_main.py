# -*- coding: utf-8 -*-
"""
EDR basic sample

@author: MURAKAMI Tamotsu
@date: 2023-10-31
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.concept import Concept


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-10-31
"""

if __name__ == "__main__":

    print('* Start *')
    
    ROOT = '3aa966'
    
    cid1 = '0f6744' # シリンダー
    cid2 = '0ec26b' # 気筒
    
    print(Concept.get_super_cids_with_step.__doc__)
    
    print(Concept.concept_expl.__doc__)

    print(Concept.get_cid_wp_sim_param_set.__doc__)

    step_super_cids_dict = Concept.get_super_cids_with_step(cid1)
    print(step_super_cids_dict)
    for cids in step_super_cids_dict.values():
        for cid in cids:
            print('{}: {}'.format(cid, Concept.concept_expl(cid)))
    
    step_super_cids_dict = Concept.get_super_cids_with_step(cid2)
    print(step_super_cids_dict)
    for cids in step_super_cids_dict.values():
        for cid in cids:
            print('{}: {}'.format(cid, Concept.concept_expl(cid)))
    
    cid_wp_sim_param_set = Concept.get_cid_wp_sim_param_set(cid1, cid2)
    print(cid_wp_sim_param_set)
    
    for n1, n2, nr, lcs in cid_wp_sim_param_set:
        print('{}: {}'.format(lcs, Concept.concept_expl(lcs)))

    result = Concept.calc_conceptid_wp_sim(cid1, cid2, lcs=True)
    print(result)
    
    cid3 = '10849b' # 便利
    step_super_cids_dict = Concept.get_super_cids_with_step(cid3)
    print(step_super_cids_dict)
    for cids in step_super_cids_dict.values():
        for cid in cids:
            print('{}: {}'.format(cid, Concept.concept_expl(cid)))

    print('* End *')       

# End of file