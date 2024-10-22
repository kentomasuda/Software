# -*- coding: utf-8 -*-
"""
Enum extended

@author: MURAKAMI Tamotsu
@date: 2021-11-10
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from enum import Enum
from enum import Flag

# Library

class EnumEx(Enum):
    """
    @author: MURAKAMI Tamotsu
    @date: 2019-05-03
    """
    
    @classmethod
    def all_(cls) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-05-03
        """
        
        return [e for e in cls]

    @classmethod
    def all_value(cls) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-02-01
        """
        
        return tuple([e.value for e in cls])
    
    @classmethod
    def index(cls, eorc):
        """
        
        e: Enum or a collection (list, set or tuple) of Enum's.  
        
        @author: MURAKAMI Tamotsu
        @date: 2019-05-03
        """
        
        l = cls.all_()
        if isinstance(eorc, cls):
            return l.index(eorc)
        elif isinstance(eorc, list) or isinstance(eorc, set) or isinstance(eorc, tuple):
            return [l.index(e) for e in eorc]
    
    @classmethod
    def instance_by_name(cls, name): # -> Enum
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-05-02
        """
        
        try:
            return cls[name]
        except KeyError:
            return None

class FlagEx(Flag):
    """
    @author: MURAKAMI Tamotsu
    @date: 2019-04-30
    """

    def __repr__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-05-17
        """
       
        return self.name
        
    def __str__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-05-17
        """
       
        return self.name
        
    @classmethod
    def decode(cls, self) -> set:
        """
        Decode the bit flag to a set of the flags.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-11-24
        """
        
        return {f for f in cls.all_() if bool(self & f)}
    
    @classmethod
    def encode(cls, flags: list): # -> cls        
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-04-30
        """
        
        flag = cls.NONE
        
        for f in flags:
            flag |= f
            
        return flag
    
    @classmethod
    def instance_by_name(cls, name): # -> Flag
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-05-02
        """
        
        try:
            return cls[name]
        except KeyError:
            return None
        
"""
Test

@author: MURAKAMI Tamotsu
@date: 2019-02-01
"""
if __name__ == '__main__':
    print('* Test start *')

    print('* Test end *')

# End of file