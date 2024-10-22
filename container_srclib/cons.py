# -*- coding: utf-8 -*-
"""
Cons

@author: MURAKAMI Tamotsu
@date: 2023-11-04
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from typing import Any

# Library

class Cons:
    """
    Cons
        
    @author: MURAKAMI Tamotsu
    @date: 2023-10-21
    """
    
    def __init__(self,
                 head: Any,
                 tail # : Coons
                 ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-21
        """
        
        self.head = head
        self.tail = tail
    
    def __str__(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-21
        """
        
        return '({} . {})'.format(self.head, self.tail.__str__())

    def __repr__(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-21
        """
        
        return 'Cons({},{})'.format(self.head, self.tail.__repr__())
    
    def length(self,
               count: int = 0) -> int:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-22
        """
        
        if self.tail is None:
            return count + 1
        else:
            count += 1
            return self.tail.length(count=count)

    def to_list(self,
                reverse: bool = False) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-04
        """
        
        if self.tail is None:
            return [self.head]
        else:
            tail_list = self.tail.to_list(reverse=reverse)
            if reverse:
                tail_list.append(self.head)
            else:
                tail_list.insert(0, self.head)
            return tail_list

    def to_list_old(self,
                    listed: list = []) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-22
        """
        
        listed.append(self.head)

        if self.tail is None:
            return listed
        else:
            return self.tail.to_list_old(listed=listed)

"""
Test

@author: MURAKAMI Tamotsu
@date: 2023-10-22
"""

if __name__ == '__main__':
    print('* Test starts *')
    
    cons = Cons(3, None)
    cons = Cons(2, cons)
    cons = Cons(1, cons)
    cons = Cons(0, cons)
    
    print(cons)
    print(cons.length())
    print(cons.to_list())
    
    print('* Test ends *')

# End of file