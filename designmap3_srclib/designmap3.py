# -*- coding: utf-8 -*-
"""
Designmap3

@author: MURAKAMI Tamotsu
@date: 2024-06-08
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from designmap3_srclib.design3 import Design3


class DesignMap3:
    """
    @author: MURAKAMI Tamotsu
    @date: 2024-06-08
    """
    
    @staticmethod
    def load_designs(dirpath: str,
                     lang: str = Design3.VAL_JPN) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-06-08
        """
        
        files = os.listdir(dirpath)
        designs = []
        for file in files:
            if not (file.startswith('.') or file.startswith('_')):
                path = os.path.join(dirpath, file)
                if os.path.isdir(path):
                    design = Design3.load(path)
                    if design:
                        designs.append(design)
        
        return designs
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-06-08
"""
if __name__ == '__main__':
    print('* Test starts *')
    
    designs = DesignMap3.load_designs('../designmap3_data/')
    print(designs)
    
    print('* Test ends *')

# End of file