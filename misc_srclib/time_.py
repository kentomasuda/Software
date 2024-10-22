# -*- coding: utf-8 -*-
"""
Time
@author: MURAKAMI Tamotsu
@date: 2019-02-28
"""

# Directory management
import sys
import os
sys.path.append(os.pardir)

# Python
from datetime import datetime
from io import StringIO
import time

class Time_:
    """
    Time
    @author: MURAKAMI Tamotsu
    @date: 2019-01-25
    """
    
    @staticmethod
    def filetime() -> str:
        """
        Return str describing present time which is usable in a file name:
        year-month-date_hour-minute-second.

        def filetime() -> str:

        @author: MURAKAMI Tamotsu
        @date: 2019-01-25
        """
        
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    @staticmethod
    def time_now(from_: float = None,
                 message: StringIO = None
                 ) -> float:
        """
        def time_now(from_: float = None,
                     silent: bool = False
                     ) -> float:

        @author: MURAKAMI Tamotsu
        @date: 2019-02-28
        """
        
        now = time.time()
        
        if from_ is None:
            sec = now
        else:
            sec = now - from_
        
        if not message is None:
            message.write('{} sec\n'.format(sec))
            
        return sec

"""
Test

@author: MURAKAMI Tamotsu
@date: 2019-01-25
"""
if __name__ == '__main__':
    print('* Test start *')
    
    start = Time_.time_now()

    print(Time_.filetime())
    
    Time_.time_now(from_=start)
        
    print('* Test end *')
        
# End of file