# -*- coding: utf-8 -*-
"""
Universal Dependencies Pos (part of speech)

https://tt-tsukumochi.com/archives/5368

・NOUN : 名詞
　・名詞-普通名詞 (但しVERB,ADJとして使われるものを除く) (例: パン)
・PROPN : 固有名詞
　・名詞-固有名詞 (例: 大阪)
・VERB : 動詞
　・動詞(但し非自立となるものを除く) (例: 食べる)
　・名詞+サ変可能で動詞の語尾が付いたもの (例: '食事'する)
・ADJ : 形容詞
　・形容詞(但し非自立となるものを除く) (例: 小さい)
　・形状詞 (例: 豊か)
　・連体詞(但しDETを除く) (例: 大きな)
　・名詞-形状詞可能で形状詞の語尾が付く場合 (例: '自由'な)
・ADV : 副詞
　・副詞 (例: ゆっくり)
・INTJ : 間投詞
　・間投詞 (例: あっ)
・PRON : 代名詞
　・代名詞 (例: 彼)
・NUM : 数詞
　・名詞-数詞 (例: 5)
・AUX : 助動詞
　・助動詞 (例: た)
　・動詞/形容詞のうち非自立のもの (例: して'いる', 食べ'にくい’)
・CCONJ : 接続詞
　・接続詞または助詞-接続助詞のうち、等位接 続詞として用いるもの (例: と)
・SCONJ : 従属接続詞
　・接続詞・助詞-接続助詞(CONJとなるものを除く) (例: て)
　・準体助詞 (例: 行く'の'が)
・DET : 限定詞
　・連体詞の一部 (例: この, その, あんな, どんな)
・ADP : 接置詞
　・助詞-格助詞 (例: が)
　・副助詞 (例: しか)
　・係助詞 (例: こそ)
・PART : 接辞
　・助詞-終助詞 (例: 何時です'か')
　・接尾辞 (例: 深'さ')
・PUNCT : 句読点
　・補助記号-句点/読点/括弧開/括弧閉
・SYM : 記号
　・記号・補助記号のうちPUNCT以外のもの
・X : その他
　・空白

@author: MURAKAMI Tamotsu
@date: 2023-11-16
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from misc_srclib.enumex import FlagEx
from text_srclib.simplepos import SimplePos
from typing import Union

class UdPos(FlagEx):
    """
    Universal Dependencies Pos (part of speech)

    @author: MURAKAMI Tamotsu
    @date: 2023-11-12
    """
    
    NOUN  = 0b00000000000000001  # 名詞
    PROPN = 0b00000000000000010  # 固有名詞
    VERB  = 0b00000000000000100  # 動詞
    ADJ   = 0b00000000000001000  # 形容詞
    ADV   = 0b00000000000010000  # 副詞
    INTJ  = 0b00000000000100000  # 間投詞
    PRON  = 0b00000000001000000  # 代名詞
    NUM   = 0b00000000010000000  # 数詞
    AUX   = 0b00000000100000000  # 助動詞
    CCONJ = 0b00000001000000000  # 接続詞
    SCONJ = 0b00000010000000000  # 従属接続詞
    DET   = 0b00000100000000000  # 限定詞
    ADP   = 0b00001000000000000  # 接置詞
    PART  = 0b00010000000000000  # 接辞
    PUNCT = 0b00100000000000000  # 句読点
    SYM   = 0b01000000000000000  # 記号
    X     = 0b10000000000000000  # その他

    def __repr__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        return self.__str__()

    def __str__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        if self in UdPos:
            return self.name
        else:
            names = (pos.name for pos in UdPos if bool(self & pos))
            if names:
                return '|'.join(names)
            else:
                return None

    @staticmethod
    def parse(expr: str): # -> Union[UdPos, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        names = expr.split('|')
        
        pos = UdPos[names[0]]
        
        for name in names[1:]:
            pos |= UdPos[name]
        
        return pos

    def to_simplepos(self) -> Union[SimplePos, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-12
        """
        
        if bool(self & (UdPos.NOUN | UdPos.PROPN)):
            return SimplePos.N
        elif bool(self & UdPos.VERB):
            return SimplePos.V
        elif bool(self & UdPos.ADJ):
            return SimplePos.ADJ
        elif bool(self & UdPos.ADV):
            return SimplePos.ADV
        else:
            return None


"""
Test

@author: MURAKAMI Tamotsu
@date: 2023-11-16
"""

if __name__ == '__main__':
    print('* Test start *')
    
    pos = UdPos.NOUN | UdPos.ADJ
    
    print(pos)
    
    print(UdPos.parse('NOUN|ADJ'))
    
    print('* Test End *')  

# End of file