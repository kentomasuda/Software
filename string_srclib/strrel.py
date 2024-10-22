# -*- coding: utf-8 -*-
"""
String relation

@author: MURAKAMI Tamotsu
@date: 2021-11-26
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from enum import Flag

# Library

class StrRel(Flag):
    """
    Relationships between two strings.

    DIFFERS =         0b00000000000001
    PRECEDES =        0b00000000000010
    SUCCEEDS =        0b00000000000100
    STARTS_WITH =     0b00000000001000
    STARTS =          0b00000000010000
    ENDS_WITH =       0b00000000100000
    ENDS =            0b00000001000000
    EQUALS =          0b00000010000000
    CONTAINS =        0b00000100000000
    CONTAINED_BY =    0b00001000000000
    SHARE_START =     0b00010000000000
    SHARE_MIDDLE =    0b00100000000000
    SHARE_END =       0b01000000000000
    SHARE_START_END = 0b10000000000000

    A: aaaa____
    B: ____bbbb
    A differs B

    A: aacc__
    B: __ccbb
    A precedes B
    
    A: __ccaa<br>
    B: bbcc__<br>
    A succeeds B

    A: ccaa
    B: cc__
    A starts with B
    
    A: cc__
    B: ccbb
    A starts B
    
    A: aacc
    B: __cc
    A ends with B

    A: __cc
    B: bbcc
    A ends B
    
    A: cc
    B: cc
    A equals B
    
    A: acca
    B: _cc_
    A contains B

    A: _cc_
    B: bccb
    A (is) contained by B

    A: ccaa
    B: ccbb
    A and B share start
    
    A: acca
    B: bccb
    A and B share middle
    
    A: aacc
    B: bbcc
    A and B share end
    
    A: cac
    B: cbbc
    A and B share start and end
   
    @author: MURAKAMI Tamotsu
    @date: 2021-11-26
    """
    
    DIFFERS =         0b00000000000001
    PRECEDES =        0b00000000000010
    SUCCEEDS =        0b00000000000100
    STARTS_WITH =     0b00000000001000
    STARTS =          0b00000000010000
    ENDS_WITH =       0b00000000100000
    ENDS =            0b00000001000000
    EQUALS =          0b00000010000000
    CONTAINS =        0b00000100000000
    CONTAINED_BY =    0b00001000000000
    SHARE_START =     0b00010000000000
    SHARE_MIDDLE =    0b00100000000000
    SHARE_END =       0b01000000000000
    SHARE_START_END = 0b10000000000000

    @staticmethod
    def all_(): # -> StrRel
        """
        def all_(): # -> StrRel

        Returns: DIFFERS | PRECEDES | SUCCEEDS | STARTS_WITH | STARTS | ENDS_WITH | ENDS | EQUALS | CONTAINS | CONTAINED_BY | SHARE_START | SHARE_MIDDLE | SHARE_END | SHARE_START_END

        @author: MURAKAMI Tamotsu
        @date: 2021-11-26
        """
        
        return DIFFERS | PRECEDES | SUCCEEDS | STARTS_WITH | STARTS | ENDS_WITH | ENDS | EQUALS | CONTAINS | CONTAINED_BY | SHARE_START | SHARE_MIDDLE | SHARE_END | SHARE_START_END
    
# End of file