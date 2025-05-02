# -*- coding: utf-8 -*-
"""
NumPy library

@author: MURAKAMI Tamotsu
@date: 2024-05-01
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import math
from nptyping import NDArray
# from nptyping import Float, Shape
import numpy
from typing import Union

# Library
from math_srclib.math_ import Math_

class NumPy_():
    """
    NumPy array list

    @author: MURAKAMI Tamotsu
    @date: 2024-02-09
    """
    
    @staticmethod
    def array_eq(x: NDArray,
                 y: NDArray,
                 abs_tol: float = Math_.ABS_TOL) -> bool:
        """
        numpy.float64 は約 1e-15 刻みの小数が表現できる。

        @author: MURAKAMI Tamotsu
        @date: 2024-02-09
        """
        
        n = x.shape[0]
        judge = True
        for i in range(n):
            if not math.isclose(x[i], y[i], abs_tol=abs_tol):
                judge = False
                break
        
        return judge
    
    
    @staticmethod
    def cos_sim(x: NDArray,
                y: NDArray) -> Union[float, int]:
        """
        Cosine similarity.

        @author: MURAKAMI Tamotsu
        @date: 2024-01-30
        """

        return numpy.dot(x, y) / (numpy.linalg.norm(x) * numpy.linalg.norm(y))
    
    # @staticmethod
    # def float_eq(x: float,
    #              y: float,
    #              tol: float = 1e-14) -> bool:
    #     """
    #     廃止予定。math.iscloseを使用する。
    #     numpy.float64 は約 1e-15 刻みの小数が表現できる。

    #     @author: MURAKAMI Tamotsu
    #     @date: 2024-01-17
    #     """
        
    #     d = x - y
        
    #     return x == y or (d <= 0 and d >= -tol) or (d >= 0 and d <= tol)
    
    @staticmethod
    def vector_angle(vec1: NDArray,
                     vec2: NDArray) -> Union[float, int]:
        """
        ベクトルの長さは 1 とする。
        Angle is in radian.

        @author: MURAKAMI Tamotsu
        @date: 2024-01-15
        """
        
        cos = numpy.dot(vec1, vec2)
        if cos < -1:
            cos = -1
        elif cos > 1:
            cos = 1
        angle = numpy.arccos(cos)
        
        vp = numpy.cross(vec1, vec2)

        if vp >= 0:
            return angle
        else:
            return -angle

class NpArrayList(list):
    """
    Numpy array list

    @author: MURAKAMI Tamotsu
    @date: 2024-01-13
    """
    
    def append_ifnew(self,
                     x: NDArray):
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-01-13
        """
        
        exists = False
        
        for y in self:
            if numpy.all(x == y):
                exists = True
                break
        
        if not exists:
            self.append(x)

"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-01-15
"""
if __name__ == '__main__':
    print('* Test start *')
    
    vec0 = numpy.array([1, 0])
    vec1 = numpy.array([0, 1])
    vec2 = numpy.array([-1, 0])
    vec3 = numpy.array([0, -1])
    
    print(NumPy_.vector_angle(vec0, vec0))
    print(NumPy_.vector_angle(vec0, vec1))
    print(NumPy_.vector_angle(vec0, vec2))
    print(NumPy_.vector_angle(vec0, vec3))
    print(NumPy_.vector_angle(vec1, vec0))
    print(NumPy_.vector_angle(vec2, vec0))
    print(NumPy_.vector_angle(vec3, vec0))
    
    # l = NpArrayList()
    # print(l)
    # l.append('a')
    # print(l)

    print('* Test end *')

# End of file