# -*- coding: utf-8 -*-
"""
Handling.

@author: MURAKAMI Tamotsu
@date: 2021-06-30
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from enum import Enum

# Library

class Handling(Enum):
    """
    @author: MURAKAMI Tamotsu
    @date: 2021-06-30
    """
    
    ERROR      = 1
    ERROR_EXIT = 2
    IGNORE     = 3
    WARNING    = 4
    
    def __repr__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-03-19
        """
        
        return self.name        

    def __str__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-03-19
        """
        
        return self.name        

# End of file