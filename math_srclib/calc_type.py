# -*- coding: utf-8 -*-
"""
Calculation type.

@author: MURAKAMI Tamotsu
@date: 2022-11-22
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from enum import Enum

# Library

class CalcType(Enum):
    """
    Calculation type.
    
    NONE                   =  0
    ENG                    =  1
    FALSE                  =  2
    JPN                    =  3
    MAX                    =  4
    MAX_COMBI              =  5
    MEAN                   =  6
    MEAN_COMBI             =  7
    MAX_MAX_1_TO_M         =  8 # Max max one-to-many
    MEAN_MAX_1_TO_M        =  9 # Mean max one-to-many
    MEDIAN_COMBI           = 10
    MEDIAN_MAX_1_TO_M      = 11 # Median max one-to-many
    MEDIAN_HIGH_MAX_1_TO_M = 12 # High median max one-to-many
    MIN                    = 13
    NONE_MAX_1_TO_M        = 14 # List of max one-to-many
    ONE_TO_MANY            = 15
    ONE_TO_ONE             = 16
    TRUE                   = 17

    @author: MURAKAMI Tamotsu
    @date: 2022-11-22
    """
    
    NONE                   =  0
    ENG                    =  1
    FALSE                  =  2
    JPN                    =  3
    MAX                    =  4
    MAX_COMBI              =  5
    MEAN                   =  6
    MEAN_COMBI             =  7
    MAX_MAX_1_TO_M         =  8 # Max max one-to-many
    MEAN_MAX_1_TO_M        =  9 # Mean max one-to-many
    MEDIAN_COMBI           = 10
    MEDIAN_MAX_1_TO_M      = 11 # Median max one-to-many
    MEDIAN_HIGH_MAX_1_TO_M = 12 # High median max one-to-many
    MIN                    = 13
    NONE_MAX_1_TO_M        = 14 # List of max one-to-many
    ONE_TO_MANY            = 15
    ONE_TO_ONE             = 16
    TRUE                   = 17
    
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