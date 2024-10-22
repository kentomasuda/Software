# -*- coding: utf-8 -*-
"""
Computer-aided X sample
(X = design, engineering)

@author: MURAKAMI Tamotsu
@date: 2018-03-13
"""

import sys
import os

sys.path.append(os.pardir)

import glob
import json

from libs_py.lib_cax import SolidWorksJournalFile as SWJ

print('start')

data_dir = '../eduinfo_data/solidworks/'

with open(data_dir + 'swj_operations.json', 'r') as f:
    json_operations = json.load(f)

# Operation name list
oprnamelist = json_operations['names']

for dirf in ['LOG_Dec26_2017/*.swj', 'LOG_Jan05_2018/*.swj']:
    for file in glob.glob(data_dir + dirf):
        print(file)
        oprl, unkl = SWJ.read_oprs(file, oprnamelist)
        print(oprl)
        print(unkl)
        
print(SWJ.read_oprs.__doc__)

print('end')

# End of File