# -*- coding: utf-8 -*-
"""
Miscellaneous

@author: MURAKAMI Tamotsu
@date: 2024-01-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library

class Misc:
    """
    Miscellaneous

    @author: MURAKAMI Tamotsu
    @date: 2024-01-03
    """
    
    @staticmethod
    def range_alternate(*args) -> list:
        """
        Range (両振り)
        
        range_alternate(stop)
        range_alternate(start, stop, step)

        @author: MURAKAMI Tamotsu
        @date: 2024-01-03
        """
        
        match len(args):
            case 1:
                stop = args[0]
                start = 0
                step = 1
            case 2:
                start, stop = args
                step = 1
            case 3:
                start, stop, step = args
        
        ra = []

        for x in range(start, stop, step):
            if x != 0:
                ra.extend([x, -x])
            else:
                ra.append(x)

        return ra

"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-01-03
"""
if __name__ == '__main__':
    print('* Test start *')

    print(Misc.range_alternate(0, 10, 1))

    print('* Test end *')

# End of file