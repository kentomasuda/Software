# -*- coding: utf-8 -*-
"""
Word（語） basic sample

@author: MURAKAMI Tamotsu
@date: 2023-12-03
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.edr import Edr
from edr_srclib.jwpos import JwPos
from math_srclib.calc_type import CalcType
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.similarity import Similarity
from text_srclib.simplepos import SimplePos
from wordnet_lib.wordnet import WordNet

"""
Main

@author: MURAKAMI Tamotsu
@date: 2021-06-08
"""

if __name__ == "__main__":
    print('* Start *')
    
    """
    EDR電子化辞書における品詞
    """
    
    print(JwPos.__doc__)


    """
    複数の電子化辞書で共通に使用できる単純化した品詞
    """
    
    print(SimplePos.__doc__)

    """
    意味を扱う概念辞書を選択する。
    Select concept dictionary to handle meaning.
    """

    meaning_id = Edr.ID # EDR
    # meaning_id = WordNet.ID # WordNet
    # meaning_id = (Edr.ID, WordNet.ID) # Both EDR and WordNet
    
    """
    EDR電子化辞書の見出し語にあるかどうかの確認。
    """
    
    print(Edr.check_headword.__doc__)

    print(Edr.check_headword('きれい', lang=Lang.JPN, pos=JwPos.JAM, suggest=True))
    print(Edr.check_headword('きれい', lang=Lang.JPN, pos=SimplePos.ADJ, suggest=True))
    print(Edr.check_headword('きれいだ', lang=Lang.JPN, pos=JwPos.JAM, suggest=True))
    print(Edr.check_headword('きれいだ', lang=Lang.JPN, pos=SimplePos.ADJ, suggest=True))
    
    """
    Generate Word instance
    """
    
    print(Text_.xml_parse_string.__doc__)

    wj1 = Text_.xml_parse_string('<jpn><aj>美しい</aj></jpn>')
    print(wj1)
    Meaning.fill_meaning(wj1, meaning_id) # 電子化辞書で意味を付加する。
    print(wj1)
    print(Meaning.meaning_json_string(wj1, meaning_id)) # 語の内容の説明文字列を生成する。

    we1 = Text_.xml_parse_string('<eng><aj>beautiful</aj></eng>')
    print(we1)
    Meaning.fill_meaning(we1, meaning_id) # 電子化辞書で意味を付加する。
    print(we1)
    print(Meaning.meaning_json_string(we1, meaning_id)) # 語の内容の説明文字列を生成する。

    wj2 = Text_.xml_parse_string('<jpn><aj>清潔だ</aj></jpn>')
    Meaning.fill_meaning(wj2, meaning_id) # 電子化辞書で意味を付加する。
    print(wj2)
    print(Meaning.meaning_json_string(wj2, meaning_id)) # 語の内容の説明文字列を生成する。

    we2 = Text_.xml_parse_string('<eng><aj>clean</aj></eng>')
    Meaning.fill_meaning(we2, meaning_id) # 電子化辞書で意味を付加する。
    print(we2)
    print(Meaning.meaning_json_string(we2, meaning_id)) # 語の内容の説明文字列を生成する。

    wj3 = Text_.xml_parse_string('<jpn><aj>衛生的だ</aj></jpn>')
    Meaning.fill_meaning(wj3, meaning_id) # 電子化辞書で意味を付加する。
    print(wj3)
    print(Meaning.meaning_json_string(wj3, meaning_id)) # 語の内容の説明文字列を生成する。

    we3 = Text_.xml_parse_string('<eng><aj>sanitary</aj></eng>')
    Meaning.fill_meaning(we3, meaning_id) # 電子化辞書で意味を付加する。
    print(we3)
    print(Meaning.meaning_json_string(we3, meaning_id)) # 語の内容の説明文字列を生成する。

    wj4 = Text_.xml_parse_string('<jpn><av>とても</av></jpn>')
    Meaning.fill_meaning(wj4, meaning_id) # 電子化辞書で意味を付加する。
    print(wj4)
    print(Meaning.meaning_json_string(wj4, meaning_id)) # 語の内容の説明文字列を生成する。

    wj5 = Text_.xml_parse_string('<jpn><aj>きれいだ</aj></jpn>')
    Meaning.fill_meaning(wj5, meaning_id) # 電子化辞書で意味を付加する。
    print(wj5)
    print(Meaning.meaning_json_string(wj5, meaning_id)) # 語の内容の説明文字列を生成する。

    """
    Wordの類似度評価
    """
    
    print(Similarity.word_sim.__doc__)
    
    print(Similarity.word_sim(wj1, wj2, meaning_id))
    print(Similarity.word_sim(wj1, wj3, meaning_id))
    print(Similarity.word_sim(wj2, wj3, meaning_id))
    print(Similarity.word_sim(wj4, wj5, meaning_id))

    """
    Generate WordLm (language map) instance
    複数言語の対応データを一つにまとめて作成できる。
    日本語データを作成し、後日英語で発表や論文を執筆する際に英語データを作り直す、等の手間を省く。
    """
    
    wlm1 = Text_.xml_parse_string('<lm><jpn><aj>美しい</aj></jpn><eng><aj>beautiful</aj></eng></lm>')
    print(wlm1)
    Meaning.fill_meaning(wlm1, meaning_id) # 電子化辞書で意味を付加する。
    print(wlm1)

    wlm2 = Text_.xml_parse_string('<lm><jpn><aj>清潔だ</aj></jpn><eng><aj>clean</aj></eng></lm>')
    print(wlm2)
    Meaning.fill_meaning(wlm2, meaning_id) # 電子化辞書で意味を付加する。
    print(wlm2)
    
    wlm3 = Text_.xml_parse_string('<lm><jpn><aj>衛生的だ</aj></jpn><eng><aj>sanitary</aj></eng></lm>')
    print(wlm3)
    Meaning.fill_meaning(wlm3, meaning_id) # 電子化辞書で意味を付加する。
    print(wlm3)

    """
    WordLmの類似度評価
    """
    
    print(Similarity.wordlm_sim.__doc__)
    
    print(Similarity.wordlm_sim(wlm1, wlm2, meaning_id, lsimtype=CalcType.JPN))
    print(Similarity.wordlm_sim(wlm1, wlm2, meaning_id, lsimtype=CalcType.ENG))

    print(Similarity.wordlm_sim(wlm1, wlm3, meaning_id, lsimtype=CalcType.JPN))
    print(Similarity.wordlm_sim(wlm1, wlm3, meaning_id, lsimtype=CalcType.ENG))

    print(Similarity.wordlm_sim(wlm2, wlm3, meaning_id, lsimtype=CalcType.JPN))
    print(Similarity.wordlm_sim(wlm3, wlm3, meaning_id, lsimtype=CalcType.ENG))
    
    """
    EDRの見出し語かどうかの判定方法の一つ
    """
    
    words = Text_.xml_parse_string('<jpn><n>見出し</n><n>見出しでない</n></jpn>')
    meaning_id = Edr.ID
    Meaning.fill_meaning(words, meaning_id) # 電子化辞書で意味を付加する。
    
    for word in words:
        print(word.get_text())
        print(word.get_meaning(meaning_id))
    
    print('* End *')
    
# End of file