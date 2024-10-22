# -*- coding: utf-8 -*-
"""
Ginza

https://megagonlabs.github.io/ginza/

@author: MURAKAMI Tamotsu
@date: 2024-05-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import ginza
import spacy
from typing import Union

# Library

class Ginza_:
    """
    @author MURAKAMI Tamotsu
    @date 2024-05-03
    """
    
    KEY_LEMMA = 'LEMMA'
    KEY_TEXT = 'TEXT'
    KEY_UDPOS = 'UDPOS'
    
    VAL_A = 'A'
    VAL_B = 'B'
    VAL_C = 'C'
    
    nlp = None
    
    staticmethod
    def ensure_loaded(model: str = 'ja_ginza'):
        """
        Parameters
        ----------
        model : str, optional
            'ja_ginza_electra' for Trnasformers モデル
            'ja_ginza' for 従来モデル
            The default is 'ja_ginza'.

        Returns
        -------
        None.

        @author MURAKAMI Tamotsu
        @date 2024-05-03
        """
        
        if Ginza_.nlp is None:
            print('Spacy.Loading "{}"...'.format(model))
            Ginza_.nlp = spacy.load(model)

    staticmethod
    def get(token, key: str):
        """
        構文従属関係

        @author MURAKAMI Tamotsu
        @date 2023-11-30
        """
        
        match key:
            case Ginza_.KEY_LEMMA:
                return token.lemma_
            case Ginza_.KEY_TEXT:
                return token.text
            case Ginza_.KEY_UDPOS:
                return token.pos_
            case _:
                return None

    staticmethod
    def get_dep(token):
        """
        構文従属関係

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """
        
        return token.dep_

    staticmethod
    def get_head(token):
        """
        構文上の親のトークン
        
        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.head
    
    staticmethod
    def get_i(token):
        """
        トークン番号
        
        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.i
    
    staticmethod
    def get_lemma(token):
        """
        レンマ(基本形)

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """
        
        return token.lemma_

    staticmethod
    def get_pos(token):
        """
        Universal Dependenciesの品詞タグ

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """
        
        return token.pos_

    staticmethod
    def get_shape(token):
        """
        正書法の特徴（x:文字,d:数値）

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """
        
        return token.shape_

    staticmethod
    def get_tag(token):
        """
        日本語の品詞タグ

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """
        
        return token.tag_

    staticmethod
    def get_text(token):
        """
        テキスト

        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.text
    
    # 以下は仮名
    
    staticmethod
    def get_morph(token,
                  type_: str):
        """
        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.morph.get(type_)
    
    staticmethod
    def get_norm(token):
        """
        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.norm_
    
    staticmethod
    def get_orth(token):
        """
        @author MURAKAMI Tamotsu
        @date 2023-11-13
        """

        return token.orth_
    
    # 以上は仮名

    staticmethod
    def parse_text(text: str,
                   keys: Union[list, set, tuple] = (KEY_TEXT, KEY_LEMMA, KEY_UDPOS),
                   split_mode: str = "C",
                   model: str = 'ja_ginza') -> list:
        """
        形態素の分割モード
        「GiNZA」では、3種類の形態素を切り替えて利用することができます。
        A：選挙 / 管理 / 委員 / 会
        B：選挙 / 管理 / 委員会
        C：選挙管理委員会 (デフォルト)

        @author MURAKAMI Tamotsu
        @date 2024-05-03
        """
        
        split_mode_try = split_mode
        parsed = None
        success = False
        
        while success == False:
            try:
                tokens = Ginza_.text_to_tokens(text,
                                               split_mode=split_mode_try,
                                               model=model)
                parsed = [{key:Ginza_.get(token, key) for key in keys}
                          for token in tokens]
                # parsed = [{Ginza_.KEY_TEXT: Ginza_.get_text(token),
                #            Ginza_.KEY_LEMMA: Ginza_.get_lemma(token),
                #            Ginza_.KEY_UDPOS: Ginza_.get_pos(token)}
                #           for token in tokens]
                success = True
            except Exception as e:
                split_mode_failed = split_mode_try
                match split_mode_try:
                    case Ginza_.VAL_A:
                        split_mode_try = Ginza_.VAL_B
                    case Ginza_.VAL_B:
                        split_mode_try = Ginza_.VAL_C
                    case Ginza_.VAL_C:
                        split_mode_try = None
                        success = True  # 解決できないのでループを終了する。
                    case _:
                        split_mode_try = None
                        success = True  # 解決できないのでループを終了する。
                    
                print('Error and try split_mode "{}"->"{}" ({}).'.format(split_mode_failed, split_mode_try, e))
        
        return parsed

    staticmethod
    def text_to_tokens(text: str,
                       split_mode: str = "C",
                       model: str = 'ja_ginza') -> list:
        """
        形態素の分割モード
        「GiNZA」では、3種類の形態素を切り替えて利用することができます。
        A：選挙 / 管理 / 委員 / 会
        B：選挙 / 管理 / 委員会
        C：選挙管理委員会 (デフォルト)

        @author MURAKAMI Tamotsu
        @date 2024-05-03
        """
        
        Ginza_.ensure_loaded(model=model)
        ginza.set_split_mode(Ginza_.nlp, split_mode)
        
        tokens = []
        doc = Ginza_.nlp(text)
        
        for sent in doc.sents:
            tokens.extend([token for token in sent])
        
        return tokens
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-03-17
"""

if __name__ == '__main__':

    print('* Test starts *')
    
    #text = '生成AI'
    text = 'LGBTは、新しい概念です。'
    # text = '立ち上がれフランスの政治家'
    # text = '東京都杉並区'
    parsed = Ginza_.parse_text(text,
                               keys=(Ginza_.KEY_TEXT, Ginza_.KEY_LEMMA, Ginza_.KEY_UDPOS),
                               split_mode="A",
                               model='ja_ginza')
    print(parsed)
    
    # tokens = Ginza_.text_to_tokens('とてもきれいな選挙管理委員会でした。そして、明日も設計します。')
    # tokens = Ginza_.text_to_tokens(text, split_mode="A")
    # try:
    #     for token in tokens:
    #         print(Ginza_.get_text(token))
    #         print(Ginza_.get_lemma(token))
    #         print(Ginza_.get_pos(token))
    # except Exception as e:
    #     print(e)

    # for token in tokens:
    #     print(Ginza_.get_i(token), end=', ')
    #     print(Ginza_.get_orth(token), end=', ')
    #     print(Ginza_.get_lemma(token), end=', ')
    #     print(Ginza_.get_norm(token), end=', ')
    #     print(Ginza_.get_morph(token, 'Reading'), end=', ')
    #     print(Ginza_.get_pos(token), end=', ')
    #     print(Ginza_.get_morph(token, 'Inflection'), end=', ')
    #     print(Ginza_.get_tag(token), end=', ')
    #     print(Ginza_.get_dep(token), end=', ')
    #     print(Ginza_.get_head(token), end=', ')
    #     print(Ginza_.get_shape(token), end=', ')
    #     print(Ginza_.get_text(token))
    
    # nlp = spacy.load('ja_ginza')
    # # doc = nlp('銀座でランチをご一緒しましょう。')
    # # doc = nlp('とてもgreatな一日だ。')
    # doc = nlp('とてもグレートな一日だ。')
    # for sent in doc.sents:
    #     for token in sent:
    #         # print(dir(token))
    #         # print()

    #         # print(
    #         #     token.i,
    #         #     token.lang,
    #         # )

    #         print(
    #             token.i,
    #             token.orth_,
    #             token.lemma_,
    #             token.norm_,
    #             token.morph.get("Reading"),
    #             token.pos_,
    #             token.morph.get("Inflection"),
    #             token.tag_,
    #             token.dep_,
    #             token.head.i,
    #         )

    #     print('EOS')
    
    # doc = nlp('明日もそうありたい。')
    # for sent in doc.sents:
    #     for token in sent:

    #         print(
    #             token.i,
    #             token.orth_,
    #             token.lemma_,
    #             token.norm_,
    #             token.morph.get("Reading"),
    #             token.pos_,
    #             token.morph.get("Inflection"),
    #             token.tag_,
    #             token.dep_,
    #             token.head.i,
    #         )

    #     print('EOS')

    print('* Test ends *')
    
# End of file