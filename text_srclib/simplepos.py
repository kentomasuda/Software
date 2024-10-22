# -*- coding: utf-8 -*-
"""
Simple Pos (part of speech)

@author: MURAKAMI Tamotsu
@date: 2024-01-02
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from misc_srclib.enumex import FlagEx

class SimplePos(FlagEx):
    """

    ADJ  = 0b0001  # Adjective, a
    ADV  = 0b0010  # Adverb, r
    N    = 0b0100  # Noun, n
    V    = 0b1000  # Verb, v

    @author: MURAKAMI Tamotsu
    @date: 2021-06-12
    """
    
    ADJ  = 0b0001  # Adjective, a
    ADV  = 0b0010  # Adverb, r
    N    = 0b0100  # Noun, n
    V    = 0b1000  # Verb, v
    
    def __repr__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-12-15
        """
        
        return self.__str__()
    
    def __str__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-12
        """
        
        allpos = SimplePos.all_(decode=True)
        
        if self in allpos:
            return self.name
        else:
            names = (pos.name for pos in allpos if bool(self & pos))
            if names:
                return '|'.join(names)
            else:
                return None

    @staticmethod
    def all_(decode: bool = False
             ): # -> SimplePos or tuple
        """
        Obtain all poses.
        
        def all_(cls,
                 decode: bool = False
                 ): # -> SimplePos or tuple
        
        @author: MURAKAMI Tamotsu
        @date: 2021-11-23
        """
        
        if decode:
            return (
                SimplePos.ADJ,
                SimplePos.ADV,
                SimplePos.N,
                SimplePos.V
                )
        else:
            return SimplePos.ADJ | SimplePos.ADV | SimplePos.N | SimplePos.V

    
    def decode(self) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-06
        """
        
        return tuple(pos for pos in SimplePos.all_(decode=True) if bool(self & pos))

    @staticmethod
    def encode(poses: tuple): # -> SimplePos:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-12
        """
        
        if len(poses) == 0:
            return None
        else:
            pos = poses[0]
        for p in poses[1:]:
            pos |= p
        
        return pos

    @staticmethod
    def is_simplepos(pos) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-01-02
        """
        
        if isinstance(pos, SimplePos):
            return True
        else:
            judge = False
            for p in SimplePos:
                if bool(pos & p):
                    judge = True
                    break
            if judge:
                return judge
            elif pos and (isinstance(pos, list) or isinstance(pos, set) or isinstance(pos, tuple)):
                judge = True
                for p in pos:
                    judge &= isinstance(p, SimplePos)
                    if not judge:
                        break
                return judge
            else:
                return False

    @classmethod
    def names(cls) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-14
        """
        
        return tuple(e.name for e in cls)

    def str_eng(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-12
        """
        
        return {SimplePos.ADJ: 'Adjective',
                SimplePos.ADV: 'Adverb',
                SimplePos.N: 'Noun',
                SimplePos.V: 'Verb'}[self]

    def str_jpn(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-12
        """
        
        return {SimplePos.ADJ: '形容詞',
                SimplePos.ADV: '副詞',
                SimplePos.N: '名詞',
                SimplePos.V: '動詞'}[self]

    def str_name(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-12-15
        """
        
        return self.name

class SimplePosTag:
    """

    @author: MURAKAMI Tamotsu
    @date: 2023-11-07
    """
    
    # Tag names
    AJ   = 'aj'   # Adjective
    AV   = 'av'   # Adverb
    N    = 'n'    # Noun
    V    = 'v'    # Verb
    T    = 't'    # Text
    # AJP  = 'ajp'  # Adjective phrase
    # AVP  = 'avp'  # Adverb phrase
    NP   = 'np'   # Noun phrase
    VP   = 'vp'   # Verb phrase
    # XP   = 'xp'   # Phrase
    
    @staticmethod
    def from_pos(pos: SimplePos): # -> SimplePosTag:
        """
    
        @author: MURAKAMI Tamotsu
        @date: 2023-10-20
        """
        
        if pos == SimplePos.ADJ:
            return SimplePosTag.AJ
        elif pos == SimplePos.ADV:
            return SimplePosTag.AV
        elif pos == SimplePos.N:
            return SimplePosTag.N
        elif pos == SimplePos.V:
            return SimplePosTag.V
        else:
            return None
    
    @staticmethod
    def pos(name: str) -> SimplePos:
        """
    
        @author: MURAKAMI Tamotsu
        @date: 2019-05-01
        """
        
        tag = name.lower()
        if tag == SimplePosTag.AJ:
            return SimplePos.ADJ
        elif tag == SimplePosTag.AV:
            return SimplePos.ADV
        elif tag == SimplePosTag.N:
            return SimplePos.N
        elif tag == SimplePosTag.V:
            return SimplePos.V
        else:
            return None
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-11-21
"""

if __name__ == '__main__':
    print('* Test start *')
    
    pos = SimplePos.N | SimplePos.V
    
    print(SimplePos.is_simplepos(pos))
    
    print('* Test End *')  

# End of file