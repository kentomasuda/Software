# -*- coding: utf-8 -*-
"""
EDR Ginza Parser

@author: MURAKAMI Tamotsu
@date: 2024-05-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import difflib
import json
import statistics
from typing import Callable
from typing import Union

# Library
from edr_lib.concept import Concept
from edr_lib.j_word import JWord
from edr_srclib.jwpos import JwPos
from edr_srclib.edr_ginza_interface import EdrGinzaInterface
from ginza_srclib.ginza_ import Ginza_
from ginza_srclib.udpos import UdPos
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_

class EdrGinzaParser:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-12-02
    """
    
    KEY_CIDS = 'CIDS'

    _n_ginza_edr_dict = None  # {nlemmas: {ginza_lemma_seq: [edr_lemma_jwpos]}}
    
    @staticmethod
    def add_conceptids(lemma_pos_seq: list,
                       jwpos: JwPos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
                                      JwPos.JVE |\
                                      JwPos.JAJ | JwPos.JAM |\
                                      JwPos.JD1 | JwPos.JD2 |\
                                      JwPos.JNM |\
                                      JwPos.JT1 | JwPos.JT2 | JwPos.JT3 | JwPos.JT4 | JwPos.JN5 |\
                                      JwPos.JB1 | JwPos.JUN | JwPos.JN6 |\
                                      JwPos.JNP | JwPos.JPR | JwPos.JAP | JwPos.JMP | JwPos.JIP | JwPos.JSE |\
                                      JwPos.JJD | JwPos.JJP | JwPos.JAX |\
                                      JwPos.JN1_JVE,
                       udpos: UdPos = UdPos.NOUN | UdPos.PROPN | UdPos.VERB | UdPos.ADJ |\
                                      UdPos.ADV | UdPos.PRON | UdPos.NUM) -> list:
        """
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

        UdPos
        UdPos.NOUN  # 名詞
        UdPos.PROPN  # 固有名詞
        UdPos.VERB  # 動詞
        UdPos.ADJ   # 形容詞
        UdPos.ADV   # 副詞
        UdPos.INTJ  # 間投詞
        UdPos.PRON  # 代名詞
        UdPos.NUM   # 数詞
        UdPos.AUX   # 助動詞
        UdPos.CCONJ   # 接続詞
        UdPos.SCONJ   # 従属接続詞
        UdPos.DET   # 限定詞
        UdPos.ADP   # 接置詞
        UdPos.PART  # 接辞
        UdPos.PUNCT  # 句読点
        UdPos.SYM   # 記号
        UdPos.X     # その他

        @author: MURAKAMI Tamotsu
        @date: 2023-12-02
        """
        
        lemma_pos_cids_seq = []
        
        for lemma_pos in lemma_pos_seq:
            if JWord.KEY_JWPOS in lemma_pos:
                pos = lemma_pos[JWord.KEY_JWPOS]
                if not pos is None:
                    valid_pos = pos & jwpos
                    
                    # 対症療法
                    if valid_pos == JwPos.NONE:
                        valid_pos = None
                    
                    if valid_pos:
                        cids = JWord.headword_conceptids(lemma_pos[Ginza_.KEY_LEMMA], valid_pos)
                        if cids:
                            lemma_pos[JWord.KEY_JWPOS] = valid_pos
                            lemma_pos[EdrGinzaParser.KEY_CIDS] = list(cids)  # tuple -> list
                            lemma_pos_cids_seq.append(lemma_pos)
            elif Ginza_.KEY_UDPOS in lemma_pos:
                # Ginza の lemma だが EDR の lemma ではない。
                pos = lemma_pos[Ginza_.KEY_UDPOS]
                if not pos is None:
                    valid_pos = pos & udpos
                    if valid_pos:
                        lemma_pos[Ginza_.KEY_UDPOS] = valid_pos
                        lemma_pos_cids_seq.append(lemma_pos)
        
        return lemma_pos_cids_seq

    @staticmethod
    def calc_sim(words1: Union[list, set, tuple],
                 words2: Union[list, set, tuple],
                 symmetricfn: Union[Callable, None] = None,
                 jwpos: JwPos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
                                JwPos.JVE |\
                                JwPos.JAJ | JwPos.JAM |\
                                JwPos.JD1 | JwPos.JD2 |\
                                JwPos.JNM |\
                                JwPos.JT1 | JwPos.JT2 | JwPos.JT3 | JwPos.JT4 | JwPos.JN5 |\
                                JwPos.JB1 | JwPos.JUN | JwPos.JN6 |\
                                JwPos.JNP | JwPos.JPR | JwPos.JAP | JwPos.JMP | JwPos.JIP | JwPos.JSE |\
                                JwPos.JJD | JwPos.JJP | JwPos.JAX |\
                                JwPos.JN1_JVE,
                 udpos: UdPos = UdPos.NOUN | UdPos.PROPN | UdPos.VERB | UdPos.ADJ |\
                                UdPos.ADV | UdPos.PRON | UdPos.NUM) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-02
        """
        
        target_words1 = [w for w in words1 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        target_words2 = [w for w in words2 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        
        simmaxs1 = {i:0 for i in range(len(target_words1))}

        if symmetricfn:
            simmaxs2 = {i:0 for i in range(len(target_words2))}

        i1 = 0
        for word1 in target_words1:
            lemma1 = word1[Ginza_.KEY_LEMMA]
            if EdrGinzaParser.KEY_CIDS in word1:
                cids1 = word1[EdrGinzaParser.KEY_CIDS]
            else:
                cids1 = None

            if symmetricfn:
                i2 = 0

            for word2 in target_words2:
                lemma2 = word2[Ginza_.KEY_LEMMA]

                if EdrGinzaParser.KEY_CIDS in word2:
                    cids2 = word2[EdrGinzaParser.KEY_CIDS]
                else:
                    cids2 = None

                if lemma1 == lemma2:
                    sim = 1
                elif cids1 is None or cids2 is None:
                    # Levenshtein
                    sim = (difflib.SequenceMatcher(None, lemma1, lemma2).ratio() + difflib.SequenceMatcher(None, lemma2, lemma1).ratio()) / 2
                else:
                    sim = Concept.calc_conceptids_wp_sim(cids1, cids2)

                if sim > simmaxs1[i1]:
                    simmaxs1[i1] = sim
                    
                if symmetricfn and sim > simmaxs2[i2]:
                    simmaxs2[i2] = sim
                
                if symmetricfn:
                    i2 += 1
            
            i1 += 1
        
        if simmaxs1:
            sim1 = statistics.mean(simmaxs1.values())
        else:
            sim1 = 0

        if symmetricfn:
            if simmaxs2:
                sim2 = statistics.mean(simmaxs2.values())
            else:
                sim2 = 0
            return symmetricfn([sim1, sim2])
        else:
            return sim1
        
    @staticmethod
    def calc_word_sim(word1: dict,
                      word2: dict) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-05-03
        """
        
        lemma1 = word1[Ginza_.KEY_LEMMA]

        if EdrGinzaParser.KEY_CIDS in word1:
            cids1 = word1[EdrGinzaParser.KEY_CIDS]
        else:
            cids1 = None

        lemma2 = word2[Ginza_.KEY_LEMMA]

        if EdrGinzaParser.KEY_CIDS in word2:
            cids2 = word2[EdrGinzaParser.KEY_CIDS]
        else:
            cids2 = None

        if lemma1 == lemma2:
            sim = 1
        elif cids1 is None or cids2 is None:
            # SentenceTransformer
            sim = SentenceTransformers_.calc_sim(lemma1, lemma2)
        else:
            sim = Concept.calc_conceptids_wp_sim(cids1, cids2)
        
        return sim

    @staticmethod
    def calc_word_sim_old(word1: dict,
                          word2: dict,
                          symmetricfn: Union[Callable, None] = None) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-01-30
        """
        
        lemma1 = word1[Ginza_.KEY_LEMMA]

        if EdrGinzaParser.KEY_CIDS in word1:
            cids1 = word1[EdrGinzaParser.KEY_CIDS]
        else:
            cids1 = None

        lemma2 = word2[Ginza_.KEY_LEMMA]

        if EdrGinzaParser.KEY_CIDS in word2:
            cids2 = word2[EdrGinzaParser.KEY_CIDS]
        else:
            cids2 = None

        if lemma1 == lemma2:
            sim = 1
        elif cids1 is None or cids2 is None:
            # Levenshtein
            sim = (difflib.SequenceMatcher(None, lemma1, lemma2).ratio() + difflib.SequenceMatcher(None, lemma2, lemma1).ratio()) / 2
        else:
            sim = Concept.calc_conceptids_wp_sim(cids1, cids2)
        
        return sim

    @staticmethod
    def calc_word_words_sims(word1: dict,
                             words2: Union[list, set, tuple],
                             totalfn: Union[Callable, None] = None,
                             jwpos: JwPos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
                                            JwPos.JVE |\
                                            JwPos.JAJ | JwPos.JAM |\
                                            JwPos.JD1 | JwPos.JD2 |\
                                            JwPos.JNM |\
                                            JwPos.JT1 | JwPos.JT2 | JwPos.JT3 | JwPos.JT4 | JwPos.JN5 |\
                                            JwPos.JB1 | JwPos.JUN | JwPos.JN6 |\
                                            JwPos.JNP | JwPos.JPR | JwPos.JAP | JwPos.JMP | JwPos.JIP | JwPos.JSE |\
                                            JwPos.JJD | JwPos.JJP | JwPos.JAX |\
                                            JwPos.JN1_JVE,
                             udpos: UdPos = UdPos.NOUN | UdPos.PROPN | UdPos.VERB | UdPos.ADJ |\
                                            UdPos.ADV | UdPos.PRON | UdPos.NUM) -> Union[float, int, list, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-15
        """
        
        if EdrGinzaParser._is_target_pos_word(word1, jwpos, udpos):
            target_word1 = word1
        else:
            target_word1 = None

        target_words2 = [w for w in words2 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        
        if target_word1 and target_words2:
            sim_lemmas = []
            lemma1 = target_word1[Ginza_.KEY_LEMMA]
            if EdrGinzaParser.KEY_CIDS in target_word1:
                cids1 = target_word1[EdrGinzaParser.KEY_CIDS]
            else:
                cids1 = None

            for target_word2 in target_words2:
                lemma2 = target_word2[Ginza_.KEY_LEMMA]

                if EdrGinzaParser.KEY_CIDS in target_word2:
                    cids2 = target_word2[EdrGinzaParser.KEY_CIDS]
                else:
                    cids2 = None

                if lemma1 == lemma2:
                    sim = 1
                elif cids1 is None or cids2 is None:
                    sim = (difflib.SequenceMatcher(None, lemma1, lemma2).ratio() + difflib.SequenceMatcher(None, lemma2, lemma1).ratio()) / 2
                else:
                    sim = Concept.calc_conceptids_wp_sim(cids1, cids2)

                sim_lemmas.append((sim, lemma2))
            
            if totalfn is None:
                return sim_lemmas
            else:
                return totalfn([sim_lemma[0] for sim_lemma in sim_lemmas])

        else:
            return None

    @staticmethod
    def calc_words_words_sims(words1: Union[list, set, tuple],
                              words2: Union[list, set, tuple],
                              totalfn: Union[Callable, None] = None,
                              symmetric: bool = False,
                              jwpos: JwPos = JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
                                             JwPos.JVE |\
                                             JwPos.JAJ | JwPos.JAM |\
                                             JwPos.JD1 | JwPos.JD2 |\
                                             JwPos.JNM |\
                                             JwPos.JT1 | JwPos.JT2 | JwPos.JT3 | JwPos.JT4 | JwPos.JN5 |\
                                             JwPos.JB1 | JwPos.JUN | JwPos.JN6 |\
                                             JwPos.JNP | JwPos.JPR | JwPos.JAP | JwPos.JMP | JwPos.JIP | JwPos.JSE |\
                                             JwPos.JJD | JwPos.JJP | JwPos.JAX |\
                                             JwPos.JN1_JVE,
                              udpos: UdPos = UdPos.NOUN | UdPos.PROPN | UdPos.VERB | UdPos.ADJ |\
                                             UdPos.ADV | UdPos.PRON | UdPos.NUM) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-16
        """
        
        target_words1 = [w for w in words1 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        target_words2 = [w for w in words2 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        
        sim_lemmas1 = [(None,-1,None) for i in range(len(target_words1))]

        if symmetric:
            sim_lemmas2 = [(None,-1,None) for i in range(len(target_words2))]

        i1 = 0
        for word1 in target_words1:
            lemma1 = word1[Ginza_.KEY_LEMMA]
            if EdrGinzaParser.KEY_CIDS in word1:
                cids1 = word1[EdrGinzaParser.KEY_CIDS]
            else:
                cids1 = None

            if symmetric:
                i2 = 0

            for word2 in target_words2:
                lemma2 = word2[Ginza_.KEY_LEMMA]

                if EdrGinzaParser.KEY_CIDS in word2:
                    cids2 = word2[EdrGinzaParser.KEY_CIDS]
                else:
                    cids2 = None

                if lemma1 == lemma2:
                    sim = 1
                elif cids1 is None or cids2 is None:
                    sim = (difflib.SequenceMatcher(None, lemma1, lemma2).ratio() + difflib.SequenceMatcher(None, lemma2, lemma1).ratio()) / 2
                else:
                    sim = Concept.calc_conceptids_wp_sim(cids1, cids2)

                if sim > sim_lemmas1[i1][1]:
                    sim_lemmas1[i1] = (lemma1, sim, lemma2)
                    
                if symmetric and sim > sim_lemmas2[i2][1]:
                    sim_lemmas2[i2] = (lemma2, sim, lemma1)
                
                if symmetric:
                    i2 += 1
            
            i1 += 1
        
        if totalfn:
            total1 = totalfn([sim_lemma[1] for sim_lemma in sim_lemmas1])
            if symmetric:
                return (total1, totalfn([sim_lemma[1] for sim_lemma in sim_lemmas2]))
            else:
                return total1
        elif symmetric:
            return (sim_lemmas1, sim_lemmas2)
        else:
            return sim_lemmas1
        
    @staticmethod
    def _ensure_edr_ginza_comparison_loaded():
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-20
        """
        
        if EdrGinzaParser._n_ginza_edr_dict is None:
            EdrGinzaParser._load_edr_ginza_comparison()

    @staticmethod
    def _is_target_pos_word(word: dict,
                            jwpos: JwPos,
                            udpos: UdPos) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-02
        """
        
        if JWord.KEY_JWPOS in word:
            return bool(word[JWord.KEY_JWPOS] & jwpos)
        elif Ginza_.KEY_UDPOS in word:
            return bool(word[Ginza_.KEY_UDPOS] & udpos)
        else:
            return False

    @staticmethod
    def _load_edr_ginza_comparison():
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-02
        """
        
        path = '../edr_data/Over100MB/edrGinzaComparison.json'
        
        print('Loading "{}"...'.format(path))
        
        with open(path, 'r', encoding='utf-8') as f:
            edr_ginza_dict = json.load(f)[EdrGinzaInterface.KEY_EDR_GINZA]
        
        n_ginza_edr_dict = {}
        
        for edr_lemma, jwpos_ginza in edr_ginza_dict.items():
            edr_lemma_jwpos = (edr_lemma, JwPos.parse(jwpos_ginza[JWord.KEY_JWPOS]))
            ginza_data = jwpos_ginza[EdrGinzaInterface.KEY_GINZA]

            # できるだけ細かく分割したものを使用する。
            if Ginza_.VAL_A in ginza_data:
                ginza_lemma_pos_seq = ginza_data[Ginza_.VAL_A][EdrGinzaInterface.KEY_LEMMA_SEQ]
            elif Ginza_.VAL_B in ginza_data:
                ginza_lemma_pos_seq = ginza_data[Ginza_.VAL_B][EdrGinzaInterface.KEY_LEMMA_SEQ]
            elif Ginza_.VAL_C in ginza_data:
                ginza_lemma_pos_seq = ginza_data[Ginza_.VAL_C][EdrGinzaInterface.KEY_LEMMA_SEQ]
            else:
                ginza_lemma_pos_seq = None

            ginza_lemma_seq = tuple([lemma_pos[0] for lemma_pos in ginza_lemma_pos_seq])
            nlemmas = len(ginza_lemma_seq)
            
            if nlemmas in n_ginza_edr_dict:
                ginza_edr_dict = n_ginza_edr_dict[nlemmas]
                if ginza_lemma_seq in ginza_edr_dict:
                    ginza_edr_dict[ginza_lemma_seq].append(edr_lemma_jwpos)
                else:
                    ginza_edr_dict[ginza_lemma_seq] = [edr_lemma_jwpos]
            else:
                n_ginza_edr_dict[nlemmas] = {ginza_lemma_seq: [edr_lemma_jwpos]}
        
        EdrGinzaParser._n_ginza_edr_dict = n_ginza_edr_dict
        
        # print(EdrGinzaParser._n_ginza_edr_dict)

    @staticmethod
    def parse_text(text: str,
                   keys: Union[list, set, tuple] = (Ginza_.KEY_LEMMA, Ginza_.KEY_UDPOS),
                   split_mode: str = "A",
                   model: str = 'ja_ginza') -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-05-03
        """
        
        EdrGinzaParser._ensure_edr_ginza_comparison_loaded()
        
        ginza_lemma_udpos_seq = Ginza_.parse_text(text, keys=keys, split_mode=split_mode, model=model)
        # ginza_lemma_udpos_seq = [(token[Ginza_.KEY_LEMMA], token[Ginza_.KEY_UDPOS]) for token in token_seq]
        
        lemma_pos_seq = []

        while ginza_lemma_udpos_seq:
            n_parsed = None
            for n in range(len(ginza_lemma_udpos_seq), 0, -1):
                if n in EdrGinzaParser._n_ginza_edr_dict:
                    ginza_edr_dict = EdrGinzaParser._n_ginza_edr_dict[n]
                    ginza_lemma_seq = tuple([lemma_pos[Ginza_.KEY_LEMMA] for lemma_pos in ginza_lemma_udpos_seq[:n]])
                    if ginza_lemma_seq in ginza_edr_dict:
                        edr_lemma_jwpos = ginza_edr_dict[ginza_lemma_seq][0]
                        n_parsed = n
                        break
            if n_parsed:
                lemma_pos_seq.append({Ginza_.KEY_LEMMA:edr_lemma_jwpos[0],
                                      JWord.KEY_JWPOS:edr_lemma_jwpos[1]})
                ginza_lemma_udpos_seq = ginza_lemma_udpos_seq[n_parsed:]
            else:
                lemma_pos_seq.append({Ginza_.KEY_LEMMA:ginza_lemma_udpos_seq[0][Ginza_.KEY_LEMMA],
                                      Ginza_.KEY_UDPOS:UdPos.parse(ginza_lemma_udpos_seq[0][Ginza_.KEY_UDPOS])})
                ginza_lemma_udpos_seq = ginza_lemma_udpos_seq[1:]
        
        return lemma_pos_seq

    @staticmethod
    def select_target_pos_words(words: Union[list, set, tuple],
                                jwpos: JwPos,
                                udpos: UdPos) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-12-06
        """
        
        return [word for word in words if EdrGinzaParser._is_target_pos_word(word, jwpos=jwpos, udpos=udpos)]

"""
Test

@author: MURAKAMI Tamotsu
@date: 2023-11-30
"""
if __name__ == '__main__':
    print('* Test start *')
    
    text = '立ち上がれフランスの政治家'
    # text = '立ち上がる'
    lemma_pos_seq = EdrGinzaParser.parse_text(text, split_mode="A")
    print(lemma_pos_seq)

    # text1 = '白い自動車が速く走る。LGBT。'
    # lemma_pos_seq1 = EdrGinzaParser.parse_text(text1)
    # print(lemma_pos_seq1)
    # lemma_pos_cids_seq1 = EdrGinzaParser.add_conceptids(lemma_pos_seq1)
    # print(lemma_pos_cids_seq1)

    # text2 = '白い車が疾走する。'
    # lemma_pos_seq2 = EdrGinzaParser.parse_text(text2)
    # print(lemma_pos_seq2)
    # lemma_pos_cids_seq2 = EdrGinzaParser.add_conceptids(lemma_pos_seq2)
    # print(lemma_pos_cids_seq2)
    
    # sim12 = EdrGinzaParser.calc_sim(lemma_pos_cids_seq1, lemma_pos_cids_seq2)
    # sim21 = EdrGinzaParser.calc_sim(lemma_pos_cids_seq2, lemma_pos_cids_seq1)
    
    # print((sim12, sim21))

    print('* Test end *')

# End of file