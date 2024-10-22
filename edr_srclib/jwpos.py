# -*- coding: utf-8 -*-
"""
EDR Japanese Pos

@author: MURAKAMI Tamotsu
@date: 2023-12-02
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from typing import Union

# Library
from edr_lib.edrpos import EdrPos
from text_srclib.simplepos import SimplePos

class JwPos(EdrPos):
    """
    POS (Part of Speech) of EDR JWord
    
    JN1 =     0b00000000000000000000000000000000000001  # 名詞：普通名詞
    JN2 =     0b00000000000000000000000000000000000010  # 名詞：固有名詞
    JN3 =     0b00000000000000000000000000000000000100  # 名詞：数詞
    JN4 =     0b00000000000000000000000000000000001000  # 名詞：時詞
    JN7 =     0b00000000000000000000000000000000010000  # 名詞：形式名詞
    JVE =     0b00000000000000000000000000000000100000  # 動詞：動詞
    JAJ =     0b00000000000000000000000000000001000000  # 形容詞：形容詞
    JAM =     0b00000000000000000000000000000010000000  # 形容動詞：形容動詞
    JD1 =     0b00000000000000000000000000000100000000  # 副詞：普通副詞
    JD2 =     0b00000000000000000000000000001000000000  # 副詞：陳述副詞
    JNM =     0b00000000000000000000000000010000000000  # 連体詞：連体詞
    JC1 =     0b00000000000000000000000000100000000000  # 接続詞：文接続詞
    JC3 =     0b00000000000000000000000001000000000000  # 接続詞：単語接続詞
    JT1 =     0b00000000000000000000000010000000000000  # 接頭語：形容詞的接頭語
    JT2 =     0b00000000000000000000000100000000000000  # 接頭語：副詞的接頭語
    JT3 =     0b00000000000000000000001000000000000000  # 接頭語：連体詞的接頭語
    JT4 =     0b00000000000000000000010000000000000000  # 接頭語：接頭小辞
    JN5 =     0b00000000000000000000100000000000000000  # 接頭語：前置助数詞
    JB1 =     0b00000000000000000001000000000000000000  # 接尾語：接尾語
    JUN =     0b00000000000000000010000000000000000000  # 接尾語：単位
    JN6 =     0b00000000000000000100000000000000000000  # 接尾語：後置助数詞
    JEV =     0b00000000000000001000000000000000000000  # 語尾：動詞語尾
    JEA =     0b00000000000000010000000000000000000000  # 語尾：形容詞語尾
    JEM =     0b00000000000000100000000000000000000000  # 語尾：形容動詞語尾
    JNP =     0b00000000000001000000000000000000000000  # 構文要素：体言句
    JPR =     0b00000000000010000000000000000000000000  # 構文要素：述語句
    JAP =     0b00000000000100000000000000000000000000  # 構文要素：連体修飾句
    JMP =     0b00000000001000000000000000000000000000  # 構文要素：連用修飾句
    JIP =     0b00000000010000000000000000000000000000  # 構文要素：独立句
    JSE =     0b00000000100000000000000000000000000000  # 構文要素：文
    JJO =     0b00000001000000000000000000000000000000  # その他：助詞
    JJ1 =     0b00000010000000000000000000000000000000  # その他：助詞相当語
    JJD =     0b00000100000000000000000000000000000000  # その他：助動詞
    JJP =     0b00001000000000000000000000000000000000  # その他：助動詞相当語
    JAX =     0b00010000000000000000000000000000000000  # その他：補助用言
    JIT =     0b00100000000000000000000000000000000000  # その他：感動詞
    JSY =     0b01000000000000000000000000000000000000  # その他：記号
    JN1_JVE = 0b10000000000000000000000000000000000000  # 複合：普通名詞+動詞

    @author: MURAKAMI Tamotsu
    @date: 2023-11-21
    """

    JN1 =     0b00000000000000000000000000000000000001  # 名詞：普通名詞
    JN2 =     0b00000000000000000000000000000000000010  # 名詞：固有名詞
    JN3 =     0b00000000000000000000000000000000000100  # 名詞：数詞
    JN4 =     0b00000000000000000000000000000000001000  # 名詞：時詞
    JN7 =     0b00000000000000000000000000000000010000  # 名詞：形式名詞
    JVE =     0b00000000000000000000000000000000100000  # 動詞：動詞
    JAJ =     0b00000000000000000000000000000001000000  # 形容詞：形容詞
    JAM =     0b00000000000000000000000000000010000000  # 形容動詞：形容動詞
    JD1 =     0b00000000000000000000000000000100000000  # 副詞：普通副詞
    JD2 =     0b00000000000000000000000000001000000000  # 副詞：陳述副詞
    JNM =     0b00000000000000000000000000010000000000  # 連体詞：連体詞
    JC1 =     0b00000000000000000000000000100000000000  # 接続詞：文接続詞
    JC3 =     0b00000000000000000000000001000000000000  # 接続詞：単語接続詞
    JT1 =     0b00000000000000000000000010000000000000  # 接頭語：形容詞的接頭語
    JT2 =     0b00000000000000000000000100000000000000  # 接頭語：副詞的接頭語
    JT3 =     0b00000000000000000000001000000000000000  # 接頭語：連体詞的接頭語
    JT4 =     0b00000000000000000000010000000000000000  # 接頭語：接頭小辞
    JN5 =     0b00000000000000000000100000000000000000  # 接頭語：前置助数詞
    JB1 =     0b00000000000000000001000000000000000000  # 接尾語：接尾語
    JUN =     0b00000000000000000010000000000000000000  # 接尾語：単位
    JN6 =     0b00000000000000000100000000000000000000  # 接尾語：後置助数詞
    JEV =     0b00000000000000001000000000000000000000  # 語尾：動詞語尾
    JEA =     0b00000000000000010000000000000000000000  # 語尾：形容詞語尾
    JEM =     0b00000000000000100000000000000000000000  # 語尾：形容動詞語尾
    JNP =     0b00000000000001000000000000000000000000  # 構文要素：体言句
    JPR =     0b00000000000010000000000000000000000000  # 構文要素：述語句
    JAP =     0b00000000000100000000000000000000000000  # 構文要素：連体修飾句
    JMP =     0b00000000001000000000000000000000000000  # 構文要素：連用修飾句
    JIP =     0b00000000010000000000000000000000000000  # 構文要素：独立句
    JSE =     0b00000000100000000000000000000000000000  # 構文要素：文
    JJO =     0b00000001000000000000000000000000000000  # その他：助詞
    JJ1 =     0b00000010000000000000000000000000000000  # その他：助詞相当語
    JJD =     0b00000100000000000000000000000000000000  # その他：助動詞
    JJP =     0b00001000000000000000000000000000000000  # その他：助動詞相当語
    JAX =     0b00010000000000000000000000000000000000  # その他：補助用言
    JIT =     0b00100000000000000000000000000000000000  # その他：感動詞
    JSY =     0b01000000000000000000000000000000000000  # その他：記号
    JN1_JVE = 0b10000000000000000000000000000000000000  # 複合：普通名詞+動詞

    NONE =    0b00000000000000000000000000000000000000  # 廃止予定
    ALL =     0b11111111111111111111111111111111111111  # 廃止予定
    
    def __repr__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-12-15
        """
        
        return self.__str__()

    def __str__(self):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-06
        """
        
        allpos = JwPos.all_(decode=True)
        
        if (self in allpos) or (self == JwPos.NONE):
            return self.name
        else:
            names = (pos.name for pos in allpos if bool(self & pos))
            if names:
                return '|'.join(names)
            else:
                return None

    @classmethod
    def all_(cls,
             decode: bool = False
             ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-06-06
        """
        
        if decode:
            return (
                JwPos.JN1,
                JwPos.JN2,
                JwPos.JN3,
                JwPos.JN4,
                JwPos.JN7,
                JwPos.JVE,
                JwPos.JAJ,
                JwPos.JAM,
                JwPos.JD1,
                JwPos.JD2,
                JwPos.JNM,
                JwPos.JC1,
                JwPos.JC3,
                JwPos.JT1,
                JwPos.JT2,
                JwPos.JT3,
                JwPos.JT4,
                JwPos.JN5,
                JwPos.JB1,
                JwPos.JUN,
                JwPos.JN6,
                JwPos.JEV,
                JwPos.JEA,
                JwPos.JEM,
                JwPos.JNP,
                JwPos.JPR,
                JwPos.JAP,
                JwPos.JMP,
                JwPos.JIP,
                JwPos.JSE,
                JwPos.JJO,
                JwPos.JJ1,
                JwPos.JJD,
                JwPos.JJP,
                JwPos.JAX,
                JwPos.JIT,
                JwPos.JSY,
                JwPos.JN1_JVE
                )
        else:
            return JwPos.JN1 |\
                JwPos.JN2 |\
                JwPos.JN3 |\
                JwPos.JN4 |\
                JwPos.JN7 |\
                JwPos.JVE |\
                JwPos.JAJ |\
                JwPos.JAM |\
                JwPos.JD1 |\
                JwPos.JD2 |\
                JwPos.JNM |\
                JwPos.JC1 |\
                JwPos.JC3 |\
                JwPos.JT1 |\
                JwPos.JT2 |\
                JwPos.JT3 |\
                JwPos.JT4 |\
                JwPos.JN5 |\
                JwPos.JB1 |\
                JwPos.JUN |\
                JwPos.JN6 |\
                JwPos.JEV |\
                JwPos.JEA |\
                JwPos.JEM |\
                JwPos.JNP |\
                JwPos.JPR |\
                JwPos.JAP |\
                JwPos.JMP |\
                JwPos.JIP |\
                JwPos.JSE |\
                JwPos.JJO |\
                JwPos.JJ1 |\
                JwPos.JJD |\
                JwPos.JJP |\
                JwPos.JAX |\
                JwPos.JIT |\
                JwPos.JSY |\
                JwPos.JN1_JVE
    
    def decode(self,
               simplepos: bool = False
               ) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-25
        """
        
        if simplepos:
            return tuple(JwPos.to_simplepos(jwpos) for jwpos in JwPos.all_() if bool(self & jwpos))
        else:
            return tuple(jwpos for jwpos in JwPos.all_(decode=True) if bool(self & jwpos))

    @staticmethod
    def encode(poses: Union[list, set, tuple]): # -> JwPos:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-01-18
        """
        
        if isinstance(poses, set):
            poslist = tuple(poses)
        else:
            poslist = poses
        
        encoded = poslist[0]
        
        for pos in poslist[1:]:
            encoded |= pos
        
        return encoded

    @staticmethod
    def is_jwpos(pos) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-10-05
        """
        
        if set(pos.decode()) & set(JwPos.all_(decode=True)):
            return True
        else:
            return False

    @staticmethod
    def jn1_jve_str() -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-11-22
        """
        
        return 'JN1;JVE'
    
    @staticmethod
    def parse(expr: str): # -> Union[JwPos, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-21
        """
        
        names = expr.split('|')
        
        pos = JwPos[names[0]]
        
        for name in names[1:]:
            pos |= JwPos[name]
        
        return pos

    @classmethod
    def pos_to_pos(cls,
                   jwpos, # : JwPos
                   simplepos: bool = False
                   ): # -> JwPos or SimplePos:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-25
        """
        
        if simplepos:
            return JwPos.to_simplepos(jwpos)
        else:
            return jwpos
        
    @staticmethod
    def to_simplepos(jwpos, # : JwPos
                     asis: bool = False # 該当がないとき、True: JwPosそのままを返す、False: Noneを返す。
                     ) -> SimplePos:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-25
        """
        
        simplepos = None
        
        for jwpos_elem in jwpos.decode():
            if jwpos_elem == JwPos.JAJ or jwpos_elem == JwPos.JAM:  # 形容動詞も含めている。
                if simplepos:
                    simplepos |= SimplePos.ADJ
                else:
                    simplepos = SimplePos.ADJ
            elif jwpos_elem == JwPos.JD1 or jwpos_elem == JwPos.JD2:
                if simplepos:
                    simplepos |= SimplePos.ADV
                else:
                    simplepos = SimplePos.ADV
            elif jwpos_elem == JwPos.JN1 or jwpos_elem == JwPos.JN2 or\
                 jwpos_elem == JwPos.JN3 or jwpos_elem == JwPos.JN4 or\
                 jwpos_elem == JwPos.JN7:
                if simplepos:
                    simplepos |= SimplePos.N
                else:
                    simplepos = SimplePos.N
            elif jwpos_elem == JwPos.JVE or jwpos_elem == JwPos.JN1_JVE:
                if simplepos:
                    simplepos |= SimplePos.V
                else:
                    simplepos = SimplePos.V
        
        if simplepos:
            return simplepos
        elif asis:
            return jwpos
        else:
            return None
    
    @classmethod
    def posname_to_simpleposname(cls,
                                 jwposname: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-04-16
        """
        
        if jwposname == 'JAJ' or jwposname == 'JAM':  # 形容動詞も含めている。
            return 'ADJ'
        elif jwposname == 'JD1' or jwposname == 'JD2':
            return 'ADV'
        elif jwposname == 'JN1' or jwposname == 'JN2' or jwposname == 'JN3' or jwposname == 'JN4' or jwposname == 'JN7':
            return 'N'
        elif jwposname == 'JVE' or jwposname.endswith('JVE'):
            return 'V'
        else:
            return None
    
    @staticmethod
    def from_simplepos(pos: SimplePos): # -> Union[JwPos, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-25
        """
        
        jwpos = None
        
        if bool(pos & SimplePos.ADJ):
            jwpos = JwPos.JAJ | JwPos.JAM  # 形容動詞も含めている。

        if bool(pos & SimplePos.ADV):
            if jwpos:
                jwpos |= (JwPos.JD1 | JwPos.JD2)
            else:
                jwpos = JwPos.JD1 | JwPos.JD2

        if bool(pos & SimplePos.N):
            if jwpos:
                jwpos |= (JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7)
            else:
                jwpos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7

        if bool(pos & SimplePos.V):
            if jwpos:
                jwpos |= (JwPos.JVE | JwPos.JN1_JVE)
            else:
                jwpos = JwPos.JVE | JwPos.JN1_JVE

        return jwpos
    
    def str_jpn(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-12-15
        """
        
        return {JwPos.JN1: '普通名詞',
                JwPos.JN2: '固有名詞',
                JwPos.JN3: '数詞',
                JwPos.JN4: '時詞',
                JwPos.JN7: '形式名詞',
                JwPos.JVE: '動詞',
                JwPos.JAJ: '形容詞',
                JwPos.JAM: '形容動詞',
                JwPos.JD1: '普通副詞',
                JwPos.JD2: '陳述副詞',
                JwPos.JNM: '連体詞',
                JwPos.JC1: '文接続詞',
                JwPos.JC3: '単語接続詞',
                JwPos.JT1: '形容詞的接頭語',
                JwPos.JT2: '副詞的接頭語',
                JwPos.JT3: '連体詞的接頭語',
                JwPos.JT4: '接頭小辞',
                JwPos.JN5: '前置助数詞',
                JwPos.JB1: '接尾語',
                JwPos.JUN: '単位',
                JwPos.JN6: '後置助数詞',
                JwPos.JEV: '動詞語尾',
                JwPos.JEA: '形容詞語尾',
                JwPos.JEM: '形容動詞語尾',
                JwPos.JNP: '体言句',
                JwPos.JPR: '述語句',
                JwPos.JAP: '連体修飾句',
                JwPos.JMP: '連用修飾句',
                JwPos.JIP: '独立句',
                JwPos.JSE: '文',
                JwPos.JJO: '助詞',
                JwPos.JJ1: '助詞相当語',
                JwPos.JJD: '助動詞',
                JwPos.JJP: '助動詞相当語',
                JwPos.JAX: '補助用言',
                JwPos.JIT: '感動詞',
                JwPos.JSY: '記号',
                JwPos.JN1_JVE: '普通名詞+動詞',
                JwPos.NONE: 'None',
                JwPos.ALL: 'All'}[self]

    def str_name(self) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-12-15
        """
        
        return self.name

"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-05-20
"""
if __name__ == '__main__':
    print('* Test start *')
    
    JWord.make_wordinfo_file(os.pardir + '/edr_data_share/jwordInfo.json', '2022-03-01')

    # JWord.ensure_simple_dic_loaded()

    # judge, info = JWord.check_headword('速', pos=SimplePos.N, suggest=True, simmin=0.0)
    # print((judge, info))
    
    # print(JWord.word_conceptids('青', pos=None))

    # for w in JWord.get_headwords(pos=SimplePos.V):
    #     print(w)
    
    # print(JWord.word_pos('青い', simplepos=True))
    
#    print(JWord.get_conceptid_by_input_word())
    
    # word_list = [
    #         'おもてなし',
    #         '和える',
    #         'まん中',
    #         '安心',
    #         ]
    
#    JWord.ensure_simple_dic_loaded()
#    JWord.ensure_jw_simple_dic_loaded_old()
#    print(JWord.headword_pos('青い', simplepos=False))
#    print(JWord.headword_conceptid('青い', simplepos=False))

    # result_list = []
    # start = Time_.time_now()
    # for word in word_list:
    #     result_list.append(JWord.check_headword(word,
    #                                             simplepos=True,
    #                                             suggest=True,
    #                                             simmin=0.0))
#        result_list.append(JWord.headword_conceptid_old(word, simplepos=True, suggest=False))
#        result_list.append(JWord.headword_conceptid(word, simplepos=True))
    # time = Time_.time_now(start)
    # for result in result_list:
    #     print(result)
    # print('time=', time)
    
#    print(JWord.conceptid_headword('3cf648', simplepos=True))

    #print(JWord.check_headword('1', simplepos=False, suggest=True))

    #print(JWord.headword_conceptid('青り', pos=JwPos.instance_by_name('JAJ'), simplepos=False, suggest=sys.stdout, simmin=0.2))

    #print(JWord.conceptid_headword('3ceaf1'))

    print('* Test end *')

# End of file