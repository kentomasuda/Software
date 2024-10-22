# -*- coding: utf-8 -*-
"""
Bool extended

@author: MURAKAMI Tamotsu
@date: 2023-11-19
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from typing import Any

# Library

class BoolEx:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-11-19
    """
    
    @classmethod
    def disjunction(x: Any,
                    y: Any) -> Any:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-19
        """
        
        if x is None:
            return y
        else:
            return x | y
        
"""
Test

@author: MURAKAMI Tamotsu
@date: 2019-02-01
"""
if __name__ == '__main__':
    print('* Test start *')

    print('* Test end *')

# End of file