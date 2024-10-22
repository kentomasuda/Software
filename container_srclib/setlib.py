# -*- coding: utf-8 -*-
"""
Set library

@author: MURAKAMI Tamotsu
@date: 2020-02-27
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library

class SetLib:
    """
    Set library
    
    @author: MURAKAMI Tamotsu
    @date: 2020-02-27
    """
    
    @staticmethod
    def dice_index(s1: set,
                   s2: set
                   ): # -> number
        """
        Dice index
        
        @author: MURAKAMI Tamotsu
        @date: 2020-02-27
        """
        
        return 2 * len(s1 & s2) / (len(s1) + len(s2))

    @staticmethod
    def jaccard_index(s1: set,
                      s2: set
                      ): # -> number
        """
        Jaccard index
        
        @author: MURAKAMI Tamotsu
        @date: 2020-02-27
        """
        
        return len(s1 & s2) / len(s1 | s2)

    @staticmethod
    def simpson_index(s1: set,
                      s2: set
                      ): # -> number
        """
        Simpson index
        
        @author: MURAKAMI Tamotsu
        @date: 2020-02-27
        """
        
        return len(s1 & s2) / min(len(s1), len(s2))

"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-02-27
"""
if __name__ == '__main__':

    print('* Test start *')
    
    print('* Test end *')

# End of file