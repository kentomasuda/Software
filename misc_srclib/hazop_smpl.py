# -*- coding: utf-8 -*-
"""
HAZOP sample

@author: MURAKAMI Tamotsu
@date: 2018-08-20
"""

import sys
import os
sys.path.append(os.pardir)

# Library
from misc_lib.hazop import GuideWord

print('start')

print(list(GuideWord))

for gw in list(GuideWord):
    print('{} <-> {}'.format(gw, gw.opposite()))

print('end')

# End of file