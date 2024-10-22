# -*- coding: utf-8 -*-
"""
Mathematics sample

@author: MURAKAMI Tamotsu
@date: 2018-08-13
"""

import sys
import os
sys.path.append(os.pardir)

# Python
from fractions import Fraction

# Library
from math_lib.math import Math

print('start')

print(Math.eval_prefix.__doc__)

frac = True

#expr = 100
#expr = 10.0
#expr = Fraction(2, 1)
#expr = Fraction(1, 2)
#expr = ('-', 20.0)
#expr = ('/', 1, 5)
#expr = ('*', 5.0, ('/', 1.0, 10.0))
expr = ('^', ('/', 1, 2), 3.0)

print('expr=', expr)
val = Math.eval_prefix(expr, frac=frac)
print('val=', val)

print('* end *')

# End of file