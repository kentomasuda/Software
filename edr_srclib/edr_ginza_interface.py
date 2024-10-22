# -*- coding: utf-8 -*-
"""
EDR Ginza Interface

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

JwPos
JwPos.JN1  # 名詞：普通名詞
JwPos.JN2  # 名詞：固有名詞
JwPos.JN3  # 名詞：数詞
JwPos.JN4  # 名詞：時詞
JwPos.JN7  # 名詞：形式名詞
JwPos.JVE  # 動詞：動詞
JwPos.JAJ  # 形容詞：形容詞
JwPos.JAM  # 形容動詞：形容動詞
JwPos.JD1  # 副詞：普通副詞
JwPos.JD2  # 副詞：陳述副詞
JwPos.JNM  # 連体詞：連体詞
JwPos.JC1  # 接続詞：文接続詞
JwPos.JC3  # 接続詞：単語接続詞
JwPos.JT1  # 接頭語：形容詞的接頭語
JwPos.JT2  # 接頭語：副詞的接頭語
JwPos.JT3  # 接頭語：連体詞的接頭語
JwPos.JT4  # 接頭語：接頭小辞
JwPos.JN5  # 接頭語：前置助数詞
JwPos.JB1  # 接尾語：接尾語
JwPos.JUN  # 接尾語：単位
JwPos.JN6  # 接尾語：後置助数詞
JwPos.JEV  # 語尾：動詞語尾
JwPos.JEA  # 語尾：形容詞語尾
JwPos.JEM  # 語尾：形容動詞語尾
JwPos.JNP  # 構文要素：体言句
JwPos.JPR  # 構文要素：述語句
JwPos.JAP  # 構文要素：連体修飾句
JwPos.JMP  # 構文要素：連用修飾句
JwPos.JIP  # 構文要素：独立句
JwPos.JSE  # 構文要素：文
JwPos.JJO  # その他：助詞
JwPos.JJ1  # その他：助詞相当語
JwPos.JJD  # その他：助動詞
JwPos.JJP  # その他：助動詞相当語
JwPos.JAX  # その他：補助用言
JwPos.JIT  # その他：感動詞
JwPos.JSY  # その他：記号
JwPos.JN1_JVE  # 複合：普通名詞+動詞

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
from ginza_srclib.udpos import UdPos

class EdrGinzaInterface:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-12-02
    """

    KEY_AUTHOR = 'AUTHOR'
    KEY_DATE = 'DATE'
    KEY_EDR = 'EDR'
    KEY_EDR_GINZA = 'EDR_GINZA'
    KEY_GINZA = 'GINZA'
    KEY_LEMMA_EQ = 'LEMMA_EQ'
    KEY_LEMMA_SEQ = 'LEMMA_SEQ'  # Sequence
    KEY_SPLIT = 'SPLIT'

    
    # staticmethod
    # def udpos_to_jwpos(udpos: UdPos) -> Union[JwPos, None]:
    #     """
    #     @author: MURAKAMI Tamotsu
    #     @date: 2023-11-19
    #     """
        
    #     jwpos = None

    #     if bool(udpos & UdPos.NOUN): # 名詞
    #         jwpos = BoolEx.disjunction(jwpos, )
        
    #     if bool(udpos & UdPos.PROPN): # 固有名詞
    #     if bool(udpos & UdPos.VERB): # 動詞
    #     if bool(udpos & UdPos.ADJ): # 形容詞
    #     if bool(udpos & UdPos.ADV): # 副詞
    #     if bool(udpos & UdPos.INTJ): # 間投詞
    #     if bool(udpos & UdPos.PRON): # 代名詞
    #     if bool(udpos & UdPos.NUM): # 数詞
    #     if bool(udpos & UdPos.AUX): # 助動詞
    #     if bool(udpos & UdPos.CCONJ): # 接続詞
    #     if bool(udpos & UdPos.SCONJ): # 従属接続詞
    #     if bool(udpos & UdPos.DET): # 限定詞
    #     if bool(udpos & UdPos.ADP): # 接置詞
    #     if bool(udpos & UdPos.PART): # 接辞
    #     if bool(udpos & UdPos.PUNCT): # 句読点
    #     if bool(udpos & UdPos.SYM): # 記号
    #     if bool(udpos & UdPos.X): # その他
    #     if bool(udpos & _): # Default


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