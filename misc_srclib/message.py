# -*- coding: utf-8 -*-
"""
Message

@author: MURAKAMI Tamotsu
@date: 2019-06-23
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from misc_srclib.time_ import Time_

class Message:
    """
    Message
    
    @author: MURAKAMI Tamotsu
    @date: 2019-06-23
    """
    
    @staticmethod
    def print_progress(count: int,
                       outof: int,
                       progress: int = None,
                       prglabel: str = ''
                       ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-06-23
        """
        
        if not progress is None and count % progress == 0:
            print('{}{}/{} at {}'.format(prglabel, count, outof, Time_.filetime()))

"""
Test

@author: MURAKAMI Tamotsu
@date: 2019-06-23
"""
if __name__ == '__main__':
    print('* Test start *')
    
        
    print('* Test end *')
        
# End of file