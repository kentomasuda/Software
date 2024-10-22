# -*- coding: utf-8 -*-
"""
Quantity unit sample

@author: MURAKAMI Tamotsu
@date: 2018-04-12
"""

import sys
import os
sys.path.append(os.pardir)

from fractions import Fraction as Frac

from libs_py.lib_unit import Dimension as Dim
from libs_py.lib_unit import Unit

print('start')

x = Dim(Frac(1, 2), 0, 0, 0, 0, 0, 0)
y = Dim(3, 0, 0, 0, 0, 0, 0)
z = Dim.mul(x, y)

print(vars(x))
print(vars(y))
print(vars(z))

s = 'kg*m/s^-2'

print(Unit.tokenize(s))

Unit.load_si_base_units()

print(Unit.si_base_units)

Unit.load_si_derived_units()

print(Unit.si_derived_units)

Unit.load_si_prefixes()

print(Unit.si_prefixes)

print('end')

# End of file