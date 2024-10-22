# -*- coding: utf-8 -*-
"""
Dict by list

Set や dict など、unhashable なものは dict の key にできない。
れらも key にできる疑似的な dict を list により実装する

@author: MURAKAMI Tamotsu
@date: 2024-03-24
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import statistics
from typing import Any
from typing import Callable
from typing import Union

# Library
from math_srclib.calc_type import CalcType


class ListDict(list):
    """
    Dict by list
    
    Set や dict など、unhashable なものは dict の key にできない。
    れらも key にできる疑似的な dict を list により実装する
    
    @author: MURAKAMI Tamotsu
    @date: 2024-03-24
    """
    
    def __init__(self):
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        super().__init__()

    def in_(self,
            key):
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        judge = False
        
        for kv in self:
            if kv[0] == key:
                judge = True
                break
        
        return judge

    def extract(self,
                key):
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        for kv in self:
            if kv[0] == key:
                val = kv[1]
                break
        
        return val
        
    def get_pair(self,
                 key) -> Union[list, None]:
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        pair = None

        for kv in self:
            if kv[0] == key:
                pair = kv
                break
        
        return pair

    def keys(self) -> list:
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        return [kv[0] for kv in self]

    def store(self,
              key,
              val):
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        new = True

        for kv in self:
            if kv[0] == key:
                kv[1] = val
                new = False
                break
        
        if new:
            self.append([key, val])
    
    def values(self) -> list:
        """

        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        return [kv[1] for kv in self]

"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-03-24
"""

if __name__ == '__main__':
    print('* Test starts *')

    ldict = ListDict()
    print(ldict)
   
    print('* Test ends *')

# End of file