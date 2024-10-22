# -*- coding: utf-8 -*-
"""
Sentence comparison

@author: MURAKAMI Tamotsu
@date: 2020-11-30
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from text_lib.sentence_elem import SenElem

class SentenceComparison:
    """
    Sentence comparison
    
    @author: MURAKAMI Tamotsu
    @date: 2020-11-30
    """
    
    @staticmethod
    def compose(x1, x2):
        """

        Parameters
        ----------
        x1 : TYPE
            DESCRIPTION.
        x2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2020-11-30
        """
        
        val = None

        if not x1 is None:
            # Sentence 1 has element.
            if not x2 is None:
                # Sentence 2 has element.
                val = (x1 + x2) / 2
            else:
                # Only sentence 1 has element.
                val = x1 / 2
        elif not x2 is None:
            # Only sentence 2 has element.
            val = x2 / 2
        
        return val

class SentenceRel(dict):
    """
    Sentence relation
    
    @author: MURAKAMI Tamotsu
    @date: 2020-11-30
    """
    
    def __init__(self,
                 # Sentence 1
                 s1 = None,
                 v1 = None,
                 o1 = None,
                 oi1 = None,
                 c1 = None,
                 a1 = None,
                 # Sentence 2
                 s2 = None,
                 v2 = None,
                 o2 = None,
                 oi2 = None,
                 c2 = None,
                 a2 = None,
                 ):
        """

        Parameters
        ----------
        # Sentence 1
        s1 : TYPE, optional
            DESCRIPTION. The default is None.
        v1 : TYPE, optional
            DESCRIPTION. The default is None.
        o1 : TYPE, optional
            DESCRIPTION. The default is None.
        oi1 : TYPE, optional
            DESCRIPTION. The default is None.
        c1 : TYPE, optional
            DESCRIPTION. The default is None.
        a1 : TYPE, optional
            DESCRIPTION. The default is None.
        # Sentence 2
        s2 : TYPE, optional
            DESCRIPTION. The default is None.
        v2 : TYPE, optional
            DESCRIPTION. The default is None.
        o2 : TYPE, optional
            DESCRIPTION. The default is None.
        oi2 : TYPE, optional
            DESCRIPTION. The default is None.
        c2 : TYPE, optional
            DESCRIPTION. The default is None.
        a2 : TYPE, optional
            DESCRIPTION. The default is None.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        @author MURAKAMI Tamotsu
        @date 2020-11-30
        """
        
        # Subject
        s = SentenceComparison.compose(s1, s2)
        if not s is None:
            self[SenElem.S] = s

        # Verb
        v = SentenceComparison.compose(v1, v2)
        if not v is None:
            self[SenElem.V] = v

        # Object
        o = SentenceComparison.compose(o1, o2)
        if not o is None:
            self[SenElem.O] = o

        # Indirect object
        oi = SentenceComparison.compose(oi1, oi2)
        if not oi is None:
            self[SenElem.OI] = oi
   
        # Complement
        c = SentenceComparison.compose(c1, c2)
        if not c is None:
            self[SenElem.C] = c

        # Adverbial
        a = SentenceComparison.compose(a1, a2)
        if not a is None:
            self[SenElem.A] = a

class SentenceSim(dict):
    """
    Sentence similarity
    
    @author: MURAKAMI Tamotsu
    @date: 2020-11-30
    """
    
    def __init__(self,
                 # Sentence 1
                 s1 = None,
                 v1 = None,
                 o1 = None,
                 oi1 = None,
                 c1 = None,
                 a1 = None,
                 # Sentence 2
                 s2 = None,
                 v2 = None,
                 o2 = None,
                 oi2 = None,
                 c2 = None,
                 a2 = None,
                 ):
        """

        Parameters
        ----------
        # Sentence 1
        s1 : TYPE, optional
            DESCRIPTION. The default is None.
        v1 : TYPE, optional
            DESCRIPTION. The default is None.
        o1 : TYPE, optional
            DESCRIPTION. The default is None.
        oi1 : TYPE, optional
            DESCRIPTION. The default is None.
        c1 : TYPE, optional
            DESCRIPTION. The default is None.
        a1 : TYPE, optional
            DESCRIPTION. The default is None.
        # Sentence 2
        s2 : TYPE, optional
            DESCRIPTION. The default is None.
        v2 : TYPE, optional
            DESCRIPTION. The default is None.
        o2 : TYPE, optional
            DESCRIPTION. The default is None.
        oi2 : TYPE, optional
            DESCRIPTION. The default is None.
        c2 : TYPE, optional
            DESCRIPTION. The default is None.
        a2 : TYPE, optional
            DESCRIPTION. The default is None.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        @author MURAKAMI Tamotsu
        @date 2020-11-30
        """
        
        # Subject
        s = SentenceComparison.compose(s1, s2)
        if not s is None:
            self[SenElem.S] = s

        # Verb
        v = SentenceComparison.compose(v1, v2)
        if not v is None:
            self[SenElem.V] = v

        # Object
        o = SentenceComparison.compose(o1, o2)
        if not o is None:
            self[SenElem.O] = o

        # Indirect object
        oi = SentenceComparison.compose(oi1, oi2)
        if not oi is None:
            self[SenElem.OI] = oi
   
        # Complement
        c = SentenceComparison.compose(c1, c2)
        if not c is None:
            self[SenElem.C] = c

        # Adverbial
        a = SentenceComparison.compose(a1, a2)
        if not a is None:
            self[SenElem.A] = a

"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-11-30
"""

if __name__ == '__main__':

    print('* Test start *')
    
    rel = SentenceSim(o1=1, a1=1, a2=1)
    print('rel =', rel)

    sim = SentenceSim(s1=1, v2=1)
    print('sim =', sim)

    print('* Test end *')
    
# End of file