# -*- coding: utf-8 -*-
"""
Math library

@author: MURAKAMI Tamotsu
@date: 2024-02-09
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import math

# Library

class Math_():
    """
    NumPy array list

    @author: MURAKAMI Tamotsu
    @date: 2024-02-09
    """
    
    ABS_TOL = 1e-12  # for math.isclose(x, y, *, abs_tol)
    
    @staticmethod
    def round_(x: float,
               k: int) -> float:
        """
        数値xを有効数字k桁に丸めた値を返す。

        Parameters
        ----------
        x : float
            丸める数値。
        k : int
            丸める有効数字桁数。

        Returns
        -------
        float
            有効数字k桁に丸められた値。

        https://scienceboy.jp/88io/2021/02/valid-digits/

        @author: MURAKAMI Tamotsu
        @date: 2024-02-01
        """
        
        if x == 0:
            return 0
        else:
            return round(x, k - math.floor(math.log10(abs(x)))- 1)

"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-02-01
"""
if __name__ == '__main__':
    print('* Test start *')
    
    x = 0.000000
    r = Math_.round_(x, 3)
    print(r)

    print('* Test end *')

# End of file