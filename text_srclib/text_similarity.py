# -*- coding: utf-8 -*-
"""
Text similarity

@author: MURAKAMI Tamotsu
@date: 2024-05-03
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
import statistics
import numpy
from typing import Callable
from typing import Union

# Library
from container_srclib.bag import Bag
from container_srclib.listdict import ListDict
from edr_lib.concept import Concept
from edr_lib.edr import Edr
from edr_srclib.edr_ginza_parser import EdrGinzaParser
from edr_srclib.jwpos import JwPos
from ginza_srclib.ginza_ import Ginza_
from ginza_srclib.udpos import UdPos
from math_srclib.calc_type import CalcType
from math_lib.number import Number
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.phraselm import PhraseLm
from text_lib.sentence import Sentence
from text_lib.sentence import SentenceLm
from text_lib.sentence_elem import SentenceElem
from text_lib.verb_phrase import VerbPhrase, VerbPhraseLm
from text_lib.word_phrase import Phrase
from text_lib.word_phrase import Word
from text_lib.wordlm import WordLm
from wordnet_lib.wordnet import WordNet

class TextSimilarity:
    """
    Text similarity (類似度)
    
    @author: MURAKAMI Tamotsu
    @date: 2024-03-25
    """
    
    LSIMTYPE_DEFAULT = CalcType.MAX
    WSIMEXP_DEFAULT = 1
    WSIMTYPE_DEFAULT = CalcType.MEDIAN_MAX_1_TO_M
    MSIMTYPE_DEFAULT = CalcType.MAX

    # Parameters
    
    ignore_s = None
    langtype = None
    meaning_id = None
    msimtype = None
    simeq_fn_ux = None
    simeq_st = None
    wsimexp = None
    wsimtype = None
    
    @staticmethod
    def analyze_sentence(sen: Sentence,
                         meaning_num: tuple = None, # 以上以下
                         meaning_simmin: tuple = None # 以上以下
                         )-> dict:
        """
        Parameters
        ----------
        sen : Sentence
            DESCRIPTION.
        meaning_num : tuple, optional
            DESCRIPTION. The default is None.
        # 以上以下                         meaning_simmin : tuple, optional
            DESCRIPTION. The default is None # 以上以下.

        Returns
        -------
        dict
            DESCRIPTION.

        @author: MURAKAMI Tamotsu
        @date: 2022-10-18
        """
        
        sen_data = []
        for w in sen.bag_of_words().get_elems():
            data = TextSimilarity.analyze_word(w, meaning_num=meaning_num, meaning_simmin=meaning_simmin)
            if bool(data):
                sen_data.append((w, data))
        
        return tuple(sen_data)
        
    @staticmethod
    def analyze_sentencelm(senlm: SentenceLm,
                           meaning_num: tuple = None, # 以上以下
                           meaning_simmin: tuple = None # 以上以下
                           )-> dict:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-12-23
        """
        
        senlm_data = []
        for sen in senlm.get_sens():
            data = TextSimilarity.analyze_sentence(sen, meaning_num=meaning_num, meaning_simmin=meaning_simmin)
            if data:
                senlm_data.extend(data)
        
        return tuple(senlm_data)
        
    @staticmethod
    def analyze_word(w: Word,
                     meaning_num: tuple = None, # 以上以下
                     meaning_simmin: tuple = None # 以上以下
                     )-> dict:
        """
        Parameters
        ----------
        w : Word
            DESCRIPTION.

        Returns
        -------
        dict
            DESCRIPTION.

        @author: MURAKAMI Tamotsu
        @date: 2020-12-23
        """
        
        KEY_MEANING_NUM_EDR = 'meaning_num_edr'
        KEY_MEANING_NUM_WORDNET = 'meaning_num_wn'
        KEY_MEANING_SIMMIN_EDR = 'meaning_simmin_edr'
        KEY_MEANING_SIMMIN_WORDNET = 'meaning_simmin_edr'

        data = {}
        
        meaning_set_edr = tuple(Meaning.get_meaning(w, Edr.ID, suggest=False, simmin=0, polysemy=False))
        meaning_set_wn = tuple(Meaning.get_meaning(w, WordNet.ID, suggest=False, simmin=0, polysemy=False))
        
        if not meaning_num is None:
            meaning_num_min, meaning_num_max = meaning_num
            # EDR
            meaning_num_edr = len(meaning_set_edr)
            if Number.in_range(meaning_num_edr, meaning_num_min, meaning_num_max):
                data[KEY_MEANING_NUM_EDR] = meaning_num_edr
            # WordNet
            meaning_num_wn = len(meaning_set_wn)
            if Number.in_range(meaning_num_wn, meaning_num_min, meaning_num_max):
                data[KEY_MEANING_NUM_WORDNET] = meaning_num_wn

        if not meaning_simmin is None:
            meaning_simmin_min, meaning_simmin_max = meaning_simmin
            # EDR
            n = len(meaning_set_edr)
            sims = []
            for i in range(n):
                cid1 = meaning_set_edr[i]
                for j in range(i + 1, n):
                    cid2 = meaning_set_edr[j]
                    sims.append(Concept.similarity_wp_value(cid1, cid2))
            if sims:
                simmin_edr = min(sims)
                if Number.in_range(simmin_edr, meaning_simmin_min, meaning_simmin_max):
                    data[KEY_MEANING_SIMMIN_EDR] = simmin_edr
            # WordNet
            n = len(meaning_set_wn)
            sims = []
            for i in range(n):
                synset1 = meaning_set_wn[i]
                for j in range(i + 1, n):
                    synset2 = meaning_set_wn[j]
                    sims.append(WordNet.similarity_wp_value(synset1, synset2))
            if sims:
                simmin_wn = min(sims)
                if Number.in_range(simmin_wn, meaning_simmin_min, meaning_simmin_max):
                    data[KEY_MEANING_SIMMIN_WORDNET] = simmin_wn

        return data
    
    @staticmethod
    def bag_sim(bag1: Bag,
                bag2: Bag,
                simf: Callable,
                freq: bool = False,
                bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                scalar: bool = False,
                pairs: bool = False) -> Union[float, int, tuple]:
        """
        Calculate similarity between Bags.
        廃止予定。今後は Bag.calc_sim を使用する。
        
        def bag_sim(bag1: Bag,
                    bag2: Bag,
                    simf: Callable,
                    freq: bool = False,
                    bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                    scalar: bool = False,
                    pairs: bool = False) -> Union[float, int, tuple]:

        @author: MURAKAMI Tamotsu
        @date: 2023-11-15
        """
        
        return Bag.calc_sim(bag1,
                            bag2,
                            simf=simf,
                            freq=freq,
                            bsimtype=bsimtype,
                            scalar=scalar,
                            pairs=pairs)

    @staticmethod
    def calc_text_bow_sim(text1: str,
                          text2: str,
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
                                         UdPos.ADV | UdPos.PRON | UdPos.NUM,
                          method: str = 'EDR+ST') -> Union[float, int]:
        """
        テキストを Ginza で形態素解析し、EDR の見出し語は概念識別子を取得する。
        出現語で bow を構成し、 bow の類似度を返す。

        Parameters
        ----------
        text1 : str
        text2 : str
            類似度を計算するテキスト。
        jwpos : JwPos, optional
            EDR見出し語の品詞（edr_srclib/jwpos.py）。
            ここで指定した品詞に該当する語のみ、類似度計算の対象となる。
            The default is JwPos.JN1 | JwPos.JN2 | JwPos.JN3 | JwPos.JN4 | JwPos.JN7 |\
                           JwPos.JVE |\
                           JwPos.JAJ | JwPos.JAM |\
                           JwPos.JD1 | JwPos.JD2 |\
                           JwPos.JNM |\
                           JwPos.JT1 | JwPos.JT2 | JwPos.JT3 | JwPos.JT4 | JwPos.JN5 |\
                           JwPos.JB1 | JwPos.JUN | JwPos.JN6 |\
                           JwPos.JNP | JwPos.JPR | JwPos.JAP | JwPos.JMP | JwPos.JIP | JwPos.JSE |\
                           JwPos.JJD | JwPos.JJP | JwPos.JAX |\
                           JwPos.JN1_JVE.
        udpos : UdPos, optional
            EDR 見出し語得ない語の、Ginza による品詞（ginza_srclib/udpos.py）。
            ここで指定した品詞に該当する語のみ、類似度計算の対象となる。
            The default is UdPos.NOUN | UdPos.PROPN | UdPos.VERB | UdPos.ADJ |\
                           UdPos.ADV | UdPos.PRON | UdPos.NUM.
        method : str, optional
            "EDR+ST": EDR 見出し語同士は EDR の概念階層で類似度計算し、それ以外の場合は SentenceTransformers で類似度計算する。
            "ST": ("EDR+ST"以外) すべて SentenceTransformers で類似度計算する。
            The default is 'EDR+ST'.

        Returns
        -------
        Union[float, int]
            計算された類似度。

        @author: MURAKAMI Tamotsu
        @date: 2024-03-25
        """
        
        lemma_pos_seq1 = EdrGinzaParser.parse_text(text1, model='ja_ginza')
        bow1 = TextSimilarity._words_to_bow([w for w in lemma_pos_seq1
                                             if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)])

        lemma_pos_seq2 = EdrGinzaParser.parse_text(text2, model='ja_ginza')
        bow2 = TextSimilarity._words_to_bow([w for w in lemma_pos_seq2
                                             if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)])
        
        words1 = bow1.keys()
        words2 = bow2.keys()
        
        if method == 'EDR+ST':
            words1 = EdrGinzaParser.add_conceptids(words1)
            words2 = EdrGinzaParser.add_conceptids(words2)

        simmaxs1 = {i:0 for i in range(len(words1))}
        simmaxs2 = {i:0 for i in range(len(words2))}

        i1 = 0
        for word1 in words1:
            lemma1 = word1[Ginza_.KEY_LEMMA]
            if EdrGinzaParser.KEY_CIDS in word1:
                cids1 = word1[EdrGinzaParser.KEY_CIDS]
            else:
                cids1 = None

            i2 = 0
            for word2 in words2:
                lemma2 = word2[Ginza_.KEY_LEMMA]
                if EdrGinzaParser.KEY_CIDS in word2:
                    cids2 = word2[EdrGinzaParser.KEY_CIDS]
                else:
                    cids2 = None

                if lemma1 == lemma2:
                    sim = 1
                elif method == 'EDR+ST' and cids1 and cids2:
                    # EDR
                    sim = Concept.calc_conceptids_wp_sim(cids1, cids2)
                else:
                    # SentenceTransformers
                    sim = SentenceTransformers_.calc_sim(lemma1, lemma2)

                if sim > simmaxs1[i1]:
                    simmaxs1[i1] = sim
                    
                if sim > simmaxs2[i2]:
                    simmaxs2[i2] = sim
                
                i2 += 1
            
            i1 += 1
        
        if simmaxs1:
            # 加重平均
            sim1 = numpy.average(list(simmaxs1.values()), weights=bow1.values())
        else:
            sim1 = 0

        if simmaxs2:
            # 加重平均
            sim2 = numpy.average(list(simmaxs2.values()), weights=bow2.values())
        else:
            sim2 = 0
        
        return (sim1 + sim2) / 2

    @staticmethod
    def calc_texts_bow_sim(texts1: Union[list, tuple],
                           texts2: Union[list, tuple],
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
                                          UdPos.ADV | UdPos.PRON | UdPos.NUM,
                           method: str = 'EDR+ST') -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        simmaxs1 = {i:0 for i in range(len(texts1))}
        simmaxs2 = {i:0 for i in range(len(texts2))}

        i1 = 0
        for text1 in texts1:
            i2 = 0
            for text2 in texts2:
                sim = TextSimilarity.calc_text_bow_sim(text1,
                                                       text2,
                                                       jwpos=jwpos,
                                                       udpos=udpos,
                                                       method=method)

                if sim > simmaxs1[i1]:
                    simmaxs1[i1] = sim
                    
                if sim > simmaxs2[i2]:
                    simmaxs2[i2] = sim
                
                i2 += 1
            i1 += 1
        
        if simmaxs1:
            sim1 = numpy.mean(list(simmaxs1.values()))
        else:
            sim1 = 0

        if simmaxs2:
            sim2 = numpy.mean(list(simmaxs2.values()))
        else:
            sim2 = 0
        
        return (sim1 + sim2) / 2

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
        @date: 2024-05-03
        """
        
        if EdrGinzaParser._is_target_pos_word(word1, jwpos, udpos):
            target_word1 = word1
        else:
            target_word1 = None

        target_words2 = [w for w in words2 if EdrGinzaParser._is_target_pos_word(w, jwpos, udpos)]
        
        if target_word1 and target_words2:
            sim_lemmas = []
            lemma1 = target_word1[Ginza_.KEY_LEMMA]

            for target_word2 in target_words2:
                lemma2 = target_word2[Ginza_.KEY_LEMMA]

                if lemma1 == lemma2:
                    sim = 1
                else:
                    sim = SentenceTransformers_.calc_sim(lemma1, lemma2)

                sim_lemmas.append((sim, lemma2))
            
            if totalfn is None:
                return sim_lemmas
            else:
                return totalfn([sim_lemma[0] for sim_lemma in sim_lemmas])

        else:
            return None

    @staticmethod
    def calc_word_words_sims_edr(word1: dict,
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
        @date: 2024-05-03
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
                    sim = SentenceTransformers_.calc_sim(lemma1, lemma2)
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
    def langmap_sim(lm1,
                    lm2,
                    simf: Callable,
                    lsimtype: CalcType = CalcType.MAX
                    ) -> dict:
        """
        Language map similarity.
        0 <= return value <= 1

        def langmap_sim(lm1,
                        lm2,
                        simf: Callable,
                        lsimtype: CalcType = CalcType.MIN
                        ): # -> number

            lsimtype:
                CalcType.ENG:
                CalcType.JPN:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

        @author: MURAKAMI Tamotsu
        @date: 2022-12-12
        """
        
        dict1 = lm1.langmap
        dict2 = lm2.langmap
        
        if lsimtype == CalcType.JPN:
            if Lang.JPN in dict1 and Lang.JPN in dict2:
                return simf(dict1[Lang.JPN], dict2[Lang.JPN])
            else:
                return None
        elif lsimtype == CalcType.ENG:
            if Lang.ENG in dict1 and Lang.ENG in dict2:
                return simf(dict1[Lang.ENG], dict2[Lang.ENG])
            else:
                return None
        elif lsimtype == CalcType.MAX or lsimtype == CalcType.MEAN or lsimtype == CalcType.MIN:
            langsimdict = {lang:simf(dict1[lang], dict2[lang]) for lang in (dict1.keys() & dict2.keys())}
            if len(langsimdict) >= 2:
                simlist = tuple(langsimdict.values())
                if isinstance(simlist[0], dict):
                    meanlist = tuple(statistics.mean(tuple(simdict.values())) for simdict in simlist)
                    if lsimtype == CalcType.MAX:
                        return simlist[meanlist.index(max(meanlist))]
                    elif lsimtype == CalcType.MIN:
                        return simlist[meanlist.index(min(meanlist))]
                    elif lsimtype == CalcType.MEAN:
                        print('lsimtype=CalcType.MEAN is invalid for scalar=False.')
                        return None
                    else:
                        print('Unexpected value {} for lsimtype.'.format(lsimtype))
                        return None
                else:
                    # simlist[0] should be a number.
                    if lsimtype == CalcType.MAX:
                        return max(simlist)
                    elif lsimtype == CalcType.MIN:
                        return min(simlist)
                    elif lsimtype == CalcType.MEAN:
                        return statistics.mean(simlist)
                    else:
                        print('Unexpected value {} for lsimtype.'.format(lsimtype))
                        return None
            elif len(langsimdict) == 1:
                return tuple(langsimdict.values())[0]
            else:
                # len(langsimdict) == 0
                return None
        else:
            print('Unexpected value {} for lsimtype.'.format(lsimtype))
            return None

    @staticmethod
    def phrase_sim(ph1: Union[Phrase, Word],
                   ph2: Union[Phrase, Word],
                   meaning_id = Meaning.MEANING_ID_DEFAULT,
                   scalar: bool = True,
                   cross: Union[float, int] = None,
                   wsimexp: Union[float, int] = 1,
                   wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                   msimtype: CalcType = CalcType.MAX,
                   bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M) -> Union[float, int]:
        """
        Phrase similarity
        
        def phrase_sim(ph1: Union[Phrase, Word],
                       ph2: Union[Phrase, Word],
                       meaning_id = Meaning.MEANING_ID_DEFAULT,
                       scalar: bool = True,
                       cross: Union[float, int] = None,
                       wsimexp: Union[float, int] = 1,
                       wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                       msimtype: CalcType = CalcType.MAX
                       ) -> Union[float, int]:

        Parameters
        ----------
        ph1 : Union[Phrase, Word]
            Phrase or Word.
        ph2 : Union[Phrase, Word]
            Phrase or Word.
        meaning_id : TYPE, optional
            The default is Meaning.MEANING_ID_DEFAULT.
        scalar : bool, optional
            The default is True.
        cross : Union[float, int], optional
            通常は主辞同士、修飾語同士の類似度の平均を計算する。
            例えば、
            1:'<np><m><n>警察</n></m><n>犬</n></np>'
            2:'<np><m><n>犬</n></m><n>小屋</n></np>'
            では、1:"犬"と2:"小屋"、1:"警察"と2:"犬"の類似度が総合されるので、値は低い。
            cross は句の主辞と修飾語の交差比較（主辞1と修飾語2、主辞2と修飾語1）を加える際の重み。
            それによって、1:"警察"と2:"小屋"、1:"犬"と2:"犬"の類似度も重みcrossで考慮されるので、値が上がる。
            The default is None (cross=0).
        wsimexp : TYPE, optional
            The default is WSIMEXP_DEFAULT.
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI
            CalcType.MEAN_COMBI
            CalcType.MEAN_MAX_1_TO_M
            CalcType.MEDIAN_MAX_1_TO_M
            The default is CalcType.MEDIAN_MAX_1_TO_M.
        msimtype : CalcType, optional
            Meaning similarity type.
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.

        Returns
        -------
        Union[float, int]
            0 <= Similarity <= 1.

        @author: MURAKAMI Tamotsu
        @date: 2022-12-18
        """
        
        if isinstance(ph1, Phrase):
            pw1 = ph1.contract()
        else:
            pw1 = ph1  # Word
            
        if isinstance(ph2, Phrase):
            pw2 = ph2.contract()
        else:
            pw2 = ph2  # Word

        if isinstance(pw1, Phrase):
            head = pw1.get_head()
            if isinstance(head, tuple):
                headbag1 = Bag(elems=head)
            else:
                headbag1 = Bag(elem=head)
            
            mods = pw1.modifiers
            if isinstance(mods, tuple):
                modbag1 = Bag(elems=mods)
            else:
                modbag1 = Bag(elem=mods)
 
            if isinstance(pw2, Phrase):
                # Head similarity
                head = pw2.get_head()
                if isinstance(head, tuple):
                    headbag2 = Bag(elems=head)
                else:
                    headbag2 = Bag(elem=head)
                sim_h = TextSimilarity.bag_sim(
                    headbag1,
                    headbag2,
                    simf = lambda x, y:
                        TextSimilarity.word_sim(
                            x,
                            y,
                            meaning_id=meaning_id,
                            wsimexp=wsimexp,
                            wsimtype=wsimtype,
                            msimtype=msimtype),
                    bsimtype = bsimtype,
                    scalar = True,
                    pairs = False)
                # Modifiers similarity
                mods = pw2.modifiers
                if isinstance(mods, tuple):
                    modbag2 = Bag(elems=mods)
                else:
                    modbag2 = Bag(elem=mods)
                sim_m = TextSimilarity.bag_sim(
                    modbag1,
                    modbag2,
                    simf = lambda x, y:
                        TextSimilarity.phrase_sim(
                            x,
                            y,
                            meaning_id=meaning_id,
                            wsimexp=wsimexp,
                            wsimtype=wsimtype,
                            msimtype=msimtype),
                    bsimtype = bsimtype,
                    scalar = True,
                    pairs = False)
                sim_straight = Number.simple((sim_h + sim_m) / 2)
                if sim_straight < 1 and cross:
                    sim_hm = TextSimilarity.bag_sim(
                        headbag1,
                        modbag2,
                        simf = lambda x, y:
                            TextSimilarity.phrase_sim(
                                x,
                                y,
                                meaning_id=meaning_id,
                                scalar=scalar,
                                cross=cross,
                                wsimexp=wsimexp,
                                wsimtype=wsimtype,
                                msimtype=msimtype),
                        bsimtype = bsimtype,
                        scalar = True,
                        pairs = False)
                    sim_mh = TextSimilarity.bag_sim(
                        modbag1,
                        headbag2,
                        simf = lambda x, y:
                            TextSimilarity.phrase_sim(
                                x,
                                y,
                                meaning_id=meaning_id,
                                scalar=scalar,
                                cross=cross,
                                wsimexp=wsimexp,
                                wsimtype=wsimtype,
                                msimtype=msimtype),
                        bsimtype = bsimtype,
                        scalar = True,
                        pairs = False)
                    sim_cross = Number.simple((sim_h + sim_m + (sim_hm + sim_mh) * cross) / (2 + cross * 2))
                    if sim_cross > sim_straight:
                        if scalar:
                            return sim_cross
                        else:
                            return {Phrase.TAG_H:sim_h, Phrase.TAG_M:sim_m, Phrase.TAG_HM:(sim_hm, sim_mh)}
                    else:
                        if scalar:
                            return sim_straight
                        else:
                            return {Phrase.TAG_H:sim_h, Phrase.TAG_M:sim_m}
                else:
                    if scalar:
                        return sim_straight
                    else:
                        return {Phrase.TAG_H:sim_h, Phrase.TAG_M:sim_m}
            else:
                # pw2 is Word
                headbag2 = Bag(elem=pw2)
                sim_h = TextSimilarity.bag_sim(
                    headbag1,
                    headbag2,
                    simf = lambda x, y:
                        TextSimilarity.word_sim(
                            x,
                            y,
                            meaning_id=meaning_id,
                            wsimexp=wsimexp,
                            wsimtype=wsimtype,
                            msimtype=msimtype),
                    bsimtype = bsimtype,
                    scalar = True,
                    pairs = False)
                sim_straight = sim_h / 2
                if cross:
                    sim_mh = TextSimilarity.bag_sim(
                        modbag1,
                        headbag2,
                        simf = lambda x, y:
                            TextSimilarity.phrase_sim(
                                x,
                                y,
                                meaning_id=meaning_id,
                                scalar=scalar,
                                cross=cross,
                                wsimexp=wsimexp,
                                wsimtype=wsimtype,
                                msimtype=msimtype),
                        bsimtype = bsimtype,
                        scalar = True,
                        pairs = False)
                    sim_cross = (sim_h + sim_mh * cross) / (1 + cross)
                    if sim_cross > sim_straight:
                        if scalar:
                            return sim_cross
                        else:
                            return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0, Phrase.TAG_HM:sim_mh}
                    else:
                        if scalar:
                            return sim_straight
                        else:
                            return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0}
                else:
                    if scalar:
                        return sim_straight
                    else:
                        return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0}
        elif isinstance(pw2, Phrase):
            # pw1 is Word
            headbag1 = Bag(elem=pw1)
            head = pw2.get_head()
            if isinstance(head, tuple):
                headbag2 = Bag(elems=head)
            else:
                headbag2 = Bag(elem=head)
            mods = pw2.modifiers
            if isinstance(mods, tuple):
                modbag2 = Bag(elems=mods)
            else:
                modbag2 = Bag(elem=mods)
            sim_h = TextSimilarity.bag_sim(
                headbag1,
                headbag2,
                simf = lambda x, y:
                    TextSimilarity.word_sim(
                        x,
                        y,
                        meaning_id=meaning_id,
                        wsimexp=wsimexp,
                        wsimtype=wsimtype,
                        msimtype=msimtype),
                bsimtype = bsimtype,
                scalar = True,
                pairs = False)
            sim_straight = sim_h / 2
            if cross:
                sim_hm = TextSimilarity.bag_sim(
                    headbag1,
                    modbag2,
                    simf = lambda x, y:
                        TextSimilarity.phrase_sim(
                            x,
                            y,
                            meaning_id=meaning_id,
                            scalar=scalar,
                            cross=cross,
                            wsimexp=wsimexp,
                            wsimtype=wsimtype,
                            msimtype=msimtype),
                    bsimtype = bsimtype,
                    scalar = True,
                    pairs = False)
                sim_cross = (sim_h + sim_hm * cross) / (1 + cross)
                if sim_cross > sim_straight:
                    if scalar:
                        return sim_cross
                    else:
                        return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0, Phrase.TAG_HM:sim_hm}
                else:
                    if scalar:
                        return sim_straight
                    else:
                        return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0}
            else:
                if scalar:
                    return sim_straight
                else:
                    return {Phrase.TAG_H:sim_h, Phrase.TAG_M:0}
        else:
            # pw1, pw2 are Words
            sim_h = TextSimilarity.word_sim(
                pw1,
                pw2,
                meaning_id=meaning_id,
                wsimexp=wsimexp,
                wsimtype=wsimtype,
                msimtype=msimtype)
            if scalar:
                return sim_h
            else:
                return {Phrase.TAG_H:sim_h}

    @staticmethod
    def phraselm_sim(phlm1: Union[PhraseLm, WordLm],
                     phlm2: Union[PhraseLm, WordLm],
                     meaning_id = Meaning.MEANING_ID_DEFAULT,
                     scalar: bool = True,
                     wsimexp: Union[float, int] = 1,
                     wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                     msimtype: CalcType = CalcType.MAX,
                     lsimtype: CalcType = CalcType.MAX,
                     bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M) -> Union[float, int]:
        """
        PhraseLm similarity.
        

        Parameters
        ----------
        phlm1 : PhraseLm or WordLm
        phlm2 : PhraseLm or WordLm
        meaning_id : str
        wsimexp : int or float, optional
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEAN_MAX_1_TO_M:
            The default is WSIMTYPE_DEFAULT.
        msimtype : CalcType, optional
            Meaning similarity type.
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is MSIMTYPE_DEFAULT.
        lsimtype : CalcType, optional
            Language similarity type.
            CalcType.ENG: 英語の意味の類似度を返す。
            CalcType.JPN: 日本語の意味の類似度を返す。
            CalcType.MAX: 各言語の意味の類似度の最大値を返す。
            CalcType.MEAN: 各言語の意味の類似度の平均を返す。(Valid when scalar=True.)
            CalcType.MIN: 各言語の意味の類似度の最小値を返す。
            The default is CalcType.MAX.

        Returns
        -------
        float
            0 <= Similarity <= 1.

        @author: MURAKAMI Tamotsu
        @date: 2022-12-18
        """
        
        return TextSimilarity.langmap_sim(
            phlm1,
            phlm2,
            simf = lambda x, y: TextSimilarity.phrase_sim(
                x,
                y,
                meaning_id=meaning_id,
                scalar=scalar,
                wsimexp=wsimexp,
                wsimtype=wsimtype,
                msimtype=msimtype,
                bsimtype=bsimtype),
            lsimtype=lsimtype)

    @staticmethod
    def print_parameters():
        """
        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2020-12-23
        """
        
        for key, val in TextSimilarity.__dict__.items():
            if isinstance(val, staticmethod):
                pass
            elif not key.startswith('__'):
                print('TextSimilarity.{}={}'.format(key, val))

    @staticmethod
    def reset_parameters():
        """
        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2022-10-27
        """

        TextSimilarity.ignore_s = False
        TextSimilarity.langtype = CalcType.MAX
        TextSimilarity.meaning_id = Meaning.MEANING_ID_DEFAULT
        TextSimilarity.msimtype = TextSimilarity.MSIMTYPE_DEFAULT
        # TextSimilarity.simeq_fn_ux = 0.95
        # TextSimilarity.simeq_st = 0.75
        TextSimilarity.wsimexp = TextSimilarity.WSIMEXP_DEFAULT
        # TextSimilarity.wsimtype = TextSimilarity.WSIMTYPE_DEFAULT

    @staticmethod
    def sentence_sim(sen1: Sentence,
                     sen2: Sentence,
                     meaning_id = Meaning.MEANING_ID_DEFAULT,
                     ignore_s: Union[bool, int, float] = False,
                     scalar: bool = True,
                     wsimexp: Union[float, int] = 1,
                     wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                     msimtype: CalcType = CalcType.MAX,
                     bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M) -> Union[float, int, dict]:
        """
        Sentence similarity by flexible sentence element comparison.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-12-17
        """
        
        v1_bow = SentenceElem.bag_of_words(sen1.get_verb())
        o1_bow = SentenceElem.bag_of_words(sen1.get_object())
        oi1_bow = SentenceElem.bag_of_words(sen1.get_indirect_object())
        c1_bow = SentenceElem.bag_of_words(sen1.get_complement())
        a1_bow = SentenceElem.bag_of_words(sen1.get_adverbial())
        
        v2_bow = SentenceElem.bag_of_words(sen2.get_verb())
        o2_bow = SentenceElem.bag_of_words(sen2.get_object())
        oi2_bow = SentenceElem.bag_of_words(sen2.get_indirect_object())
        c2_bow = SentenceElem.bag_of_words(sen2.get_complement())
        a2_bow = SentenceElem.bag_of_words(sen2.get_adverbial())
        
        ignore_s_type = type(ignore_s)

        bows1 = {}
        if ignore_s_type == bool and ignore_s == False:
            s1_bow = SentenceElem.bag_of_words(sen1.get_subject())
            if s1_bow and len(s1_bow) > 0:
                bows1[SentenceElem.KEY_S] = s1_bow
        if v1_bow and len(v1_bow) > 0:
            bows1[SentenceElem.KEY_V] = v1_bow
        if o1_bow and len(o1_bow) > 0:
            bows1[SentenceElem.KEY_O] = o1_bow
        if oi1_bow and len(oi1_bow) > 0:
            bows1[SentenceElem.KEY_OI] = oi1_bow
        if c1_bow and len(c1_bow) > 0:
            bows1[SentenceElem.KEY_C] = c1_bow
        if a1_bow and len(a1_bow) > 0:
            bows1[SentenceElem.KEY_A] = a1_bow
        sims1 = {elem:0 for elem in bows1.keys()}
        
        bows2 = {}
        if ignore_s_type == bool and ignore_s == False:
            s2_bow = SentenceElem.bag_of_words(sen2.get_subject())
            if s2_bow and len(s2_bow) > 0:
                bows2[SentenceElem.KEY_S] = s2_bow
        if v2_bow and len(v2_bow) > 0:
            bows2[SentenceElem.KEY_V] = v2_bow
        if o2_bow and len(o2_bow) > 0:
            bows2[SentenceElem.KEY_O] = o2_bow
        if oi2_bow and len(oi2_bow) > 0:
            bows2[SentenceElem.KEY_OI] = oi2_bow
        if c2_bow and len(c2_bow) > 0:
            bows2[SentenceElem.KEY_C] = c2_bow
        if a2_bow and len(a2_bow) > 0:
            bows2[SentenceElem.KEY_A] = a2_bow
        sims2 = {elem:0 for elem in bows2.keys()}
        
        simf = lambda x, y: TextSimilarity.word_sim(
            x,
            y,
            meaning_id=meaning_id,
            wsimexp=wsimexp,
            wsimtype=wsimtype,
            msimtype=msimtype)
        
        # simf = lambda x, y: TextSimilarity.phrase_sim(
        #     x,
        #     y,
        #     meaning_id=meaning_id,
        #     scalar=True,
        #     cross=0.5,
        #     wsimexp=wsimexp,
        #     wsimtype=wsimtype,
        #     msimtype=msimtype)

        for elem1, bow1 in bows1.items():
            for elem2, bow2 in bows2.items():
                elem_set = {elem1, elem2}
                if elem_set != {SentenceElem.KEY_S, SentenceElem.KEY_O} and elem_set != {SentenceElem.KEY_S, SentenceElem.KEY_OI} and elem_set != {SentenceElem.KEY_O, SentenceElem.KEY_OI}:
                    sim = TextSimilarity.bag_sim(bow1, bow2, simf=simf, scalar=True, bsimtype=bsimtype, pairs=False)
                    if sim > sims1[elem1]:
                        sims1[elem1] = sim
                    if sim > sims2[elem2]:
                        sims2[elem2] = sim

        # if ignore_s == True:
        #     if SentenceElem.KEY_S in sims1:
        #         del sims1[SentenceElem.KEY_S]
        #     if SentenceElem.KEY_S in sims2:
        #         del sims2[SentenceElem.KEY_S]

        if ignore_s_type == float or ignore_s_type == int:
            sims1[SentenceElem.KEY_S] = ignore_s
            sims2[SentenceElem.KEY_S] = ignore_s

        # n1 = len(sims1)
        # n2 = len(sims2)
        
        sentence_sim = {}
        
        for elem in (SentenceElem.KEY_S, SentenceElem.KEY_V, SentenceElem.KEY_O, SentenceElem.KEY_OI, SentenceElem.KEY_C, SentenceElem.KEY_A):
            sim = TextSimilarity.tally_similarity(sims1, sims2, elem) #, n1, n2)
            if not sim is None:
                sentence_sim[elem] = sim
        
        if scalar:
            return statistics.mean(sentence_sim.values())
        else:
            return sentence_sim

    @staticmethod
    def sentence_sim_by_comp_elem_bow(sen1: Sentence,
                                      sen2: Sentence,
                                      wsimf: Callable = lambda x, y:
                                          TextSimilarity.word_sim(x,
                                                                  y,
                                                                  TextSimilarity.meaning_id),
                                      ignore_s: bool = False,
                                      scalar: bool = True):
        """
        廃止予定
        Sentence similarity by comparable sentence element bows.
        
        @author: MURAKAMI Tamotsu
        @date: 2021-09-07
        """
        
        s1_bow = SentenceElem.bag_of_words(sen1.get_subject())
        v1_bow = SentenceElem.bag_of_words(sen1.get_verb())
        o1_bow = SentenceElem.bag_of_words(sen1.get_object())
        oi1_bow = SentenceElem.bag_of_words(sen1.get_indirect_object())
        c1_bow = SentenceElem.bag_of_words(sen1.get_complement())
        a1_bow = SentenceElem.bag_of_words(sen1.get_adverbial())
        
        s2_bow = SentenceElem.bag_of_words(sen2.get_subject())
        v2_bow = SentenceElem.bag_of_words(sen2.get_verb())
        o2_bow = SentenceElem.bag_of_words(sen2.get_object())
        oi2_bow = SentenceElem.bag_of_words(sen2.get_indirect_object())
        c2_bow = SentenceElem.bag_of_words(sen2.get_complement())
        a2_bow = SentenceElem.bag_of_words(sen2.get_adverbial())
        
        bows1 = {}
        if len(s1_bow) > 0:
            bows1[SentenceElem.KEY_S] = s1_bow
        if len(v1_bow) > 0:
            bows1[SentenceElem.KEY_V] = v1_bow
        if len(o1_bow) > 0:
            bows1[SentenceElem.KEY_O] = o1_bow
        if len(oi1_bow) > 0:
            bows1[SentenceElem.KEY_OI] = oi1_bow
        if len(c1_bow) > 0:
            bows1[SentenceElem.KEY_C] = c1_bow
        if len(a1_bow) > 0:
            bows1[SentenceElem.KEY_A] = a1_bow
        sims1 = {elem:0 for elem in bows1.keys()}
        
        bows2 = {}
        if len(s2_bow) > 0:
            bows2[SentenceElem.KEY_S] = s2_bow
        if len(v2_bow) > 0:
            bows2[SentenceElem.KEY_V] = v2_bow
        if len(o2_bow) > 0:
            bows2[SentenceElem.KEY_O] = o2_bow
        if len(oi2_bow) > 0:
            bows2[SentenceElem.KEY_OI] = oi2_bow
        if len(c2_bow) > 0:
            bows2[SentenceElem.KEY_C] = c2_bow
        if len(a2_bow) > 0:
            bows2[SentenceElem.KEY_A] = a2_bow
        sims2 = {elem:0 for elem in bows2.keys()}
    
        for elem1, bow1 in bows1.items():
            for elem2, bow2 in bows2.items():
                elem_set = {elem1, elem2}
                if elem_set != {SentenceElem.KEY_S, SentenceElem.KEY_O} and elem_set != {SentenceElem.KEY_S, SentenceElem.KEY_OI} and elem_set != {SentenceElem.KEY_O, SentenceElem.KEY_OI}:
                    sim = TextSimilarity.bag_sim(bow1, bow2, simf=wsimf, scalar=True, pairs=False)
                    if sim > sims1[elem1]:
                        sims1[elem1] = sim
                    if sim > sims2[elem2]:
                        sims2[elem2] = sim

        if ignore_s == True:
            if SentenceElem.KEY_S in sims1:
                del sims1[SentenceElem.KEY_S]
            if SentenceElem.KEY_S in sims2:
                del sims2[SentenceElem.KEY_S]
        elif ignore_s == '1':
            sims1[SentenceElem.KEY_S] = 1
            sims2[SentenceElem.KEY_S] = 1
        

        n1 = len(sims1)
        n2 = len(sims2)
        
        sentence_sim = {}
        
        for elem in (SentenceElem.KEY_S, SentenceElem.KEY_V, SentenceElem.KEY_O, SentenceElem.KEY_OI, SentenceElem.KEY_C, SentenceElem.KEY_A):
            sim = TextSimilarity.tally_similarity(sims1, sims2, elem, n1, n2)
            if not sim is None:
                sentence_sim[elem] = sim
        
        if scalar:
            return statistics.mean(sentence_sim.values())
        else:
            return sentence_sim

    @staticmethod
    def sentencelm_sim(senlm1: SentenceLm,
                       senlm2: SentenceLm,
                       meaning_id = Meaning.MEANING_ID_DEFAULT,
                       ignore_s: bool = False,
                       scalar: bool = True,
                       wsimexp: Union[float, int] = 1,
                       wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                       msimtype: CalcType = CalcType.MAX,
                       lsimtype: CalcType = CalcType.MAX,
                       bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M
                       ) -> Union[float, int]:
        """
        SentenceLm similarity.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-12-17
        """
        
        return TextSimilarity.langmap_sim(
            senlm1,
            senlm2,
            simf = lambda x, y: TextSimilarity.sentence_sim(
                x,
                y,
                meaning_id=meaning_id,
                ignore_s=ignore_s,
                scalar=scalar,
                wsimexp=wsimexp,
                wsimtype=wsimtype,
                msimtype=msimtype,
                bsimtype=bsimtype),
            lsimtype=lsimtype)

    @staticmethod
    def sentencelm_sim_by_comp_elem_bow(senlm1: SentenceLm,
                                        senlm2: SentenceLm,
                                        wsimf: Callable = lambda x, y:
                                            TextSimilarity.word_sim(x,
                                                                    y,
                                                                    TextSimilarity.meaning_id),
                                        ignore_s: bool = False,
                                        scalar: bool = True):
        """
        廃止予定
        SentenceLm similarity by comparing sentence element bows flexibly.
        
        def sentencelm_sim_by_comp_elem_bow(senlm1: SentenceLm,
                                            senlm2: SentenceLm,
                                            wsimf: Callable = lambda x, y:
                                                TextSimilarity.word_sim(x,
                                                                        y,
                                                                        TextSimilarity.meaning_id),
                                            ignore_s: bool = False,
                                            scalar: bool = True):
        
        ignore_s:
            True: 主語の比較を含まない類似度を返す。
            False: 主語の比較を含む類似度を返す。
            '1': 主語の類似度を 1 とした文の類似度を返す。
        
        scalar:
            True: 類似度 sim を一つの数値 （0 <= sim <= 1） で返す。
            False: 文要素ごとの類似度の dict を返す。dict の key は、
                SentenceElem.KEY_S
                SentenceElem.KEY_V
                SentenceElem.KEY_O
                SentenceElem.KEY_OI
                SentenceElem.KEY_C
                SentenceElem.KEY_A
                となっている。

        @author: MURAKAMI Tamotsu
        @date: 2021-09-07
        """
        
        sime = TextSimilarity.sentence_sim_by_comp_elem_bow(
            senlm1.get_sen(Lang.ENG),
            senlm2.get_sen(Lang.ENG),
            wsimf=wsimf,
            ignore_s=ignore_s,
            scalar=scalar)
        simj = TextSimilarity.sentence_sim_by_comp_elem_bow(
            senlm1.get_sen(Lang.JPN),
            senlm2.get_sen(Lang.JPN),
            wsimf=wsimf,
            ignore_s=ignore_s,
            scalar=scalar)

        if scalar:
            return max(sime, simj)
        else:
            meane = statistics.mean(sime.values())
            meanj = statistics.mean(sime.values())
            if meane > meanj:
                return sime
            else:
                return simj


    @staticmethod
    def simdict_format(simdict: dict,
                       num: int) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-07-21
        """
        
        keyvals = ''
        kvformat = '{{}}:{{:.{}f}},'.format(num)
        for key, val in simdict.items():
            keyvals += kvformat.format(key, val)
        
        return '{' + keyvals[:-1] + '}'
    
    @staticmethod
    def simdict_max(sims1: dict,
                    sims2: dict):
        """
        @author: MURAKAMI Tamotsu
        @date: 2021-07-17
        """
        
        simdict = {}
        for elem in (SentenceElem.KEY_S, SentenceElem.KEY_V, SentenceElem.KEY_O, SentenceElem.KEY_OI, SentenceElem.KEY_C, SentenceElem.KEY_A):
            if elem in sims1:
                if elem in sims2:
                    simdict[elem] = max(sims1[elem], sims2[elem])
                else:
                    simdict[elem] = sims1[elem]
            elif elem in sims2:
                simdict[elem] = sims2[elem]
        
        return simdict
        
    @staticmethod
    def tally_similarity(sims1: dict,
                         sims2: dict,
                         elem: str,
                         w1: Union[float, int] = 1,
                         w2: Union[float, int] = 1
                         ) -> Union[float, int, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-26
        """
        
        if elem in sims1:
            sim1 = sims1[elem]
            if elem in sims2:
                sim2 = sims2[elem]
            else:
                sim2 = 0
            sim = (sim1 * w1 + sim2 * w2) / (w1 + w2)
        elif elem in sims2:
            sim = sims2[elem] * w2 / (w1 + w2)
        else:
            sim = None
        
        return sim

    @staticmethod
    def verbphrase_sim(vp1: VerbPhrase,
                       vp2: VerbPhrase,
                       meaning_id = Meaning.MEANING_ID_DEFAULT,
                       scalar: bool = True,
                       wsimexp: Union[float, int] = 1,
                       wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                       msimtype: CalcType = CalcType.MAX):
        """
        VerbPhrase similarity by flexible sentence element comparison.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-12-12
        """
        
        v1_bow = SentenceElem.bag_of_words(vp1.get_verb())
        o1_bow = SentenceElem.bag_of_words(vp1.get_object())
        oi1_bow = SentenceElem.bag_of_words(vp1.get_indirect_object())
        c1_bow = SentenceElem.bag_of_words(vp1.get_complement())
        a1_bow = SentenceElem.bag_of_words(vp1.get_adverbial())
        
        v2_bow = SentenceElem.bag_of_words(vp2.get_verb())
        o2_bow = SentenceElem.bag_of_words(vp2.get_object())
        oi2_bow = SentenceElem.bag_of_words(vp2.get_indirect_object())
        c2_bow = SentenceElem.bag_of_words(vp2.get_complement())
        a2_bow = SentenceElem.bag_of_words(vp2.get_adverbial())
        
        bows1 = {}
        if len(v1_bow) > 0:
            bows1[SentenceElem.KEY_V] = v1_bow
        if len(o1_bow) > 0:
            bows1[SentenceElem.KEY_O] = o1_bow
        if len(oi1_bow) > 0:
            bows1[SentenceElem.KEY_OI] = oi1_bow
        if len(c1_bow) > 0:
            bows1[SentenceElem.KEY_C] = c1_bow
        if len(a1_bow) > 0:
            bows1[SentenceElem.KEY_A] = a1_bow
        sims1 = {elem:0 for elem in bows1.keys()}
        
        bows2 = {}
        if len(v2_bow) > 0:
            bows2[SentenceElem.KEY_V] = v2_bow
        if len(o2_bow) > 0:
            bows2[SentenceElem.KEY_O] = o2_bow
        if len(oi2_bow) > 0:
            bows2[SentenceElem.KEY_OI] = oi2_bow
        if len(c2_bow) > 0:
            bows2[SentenceElem.KEY_C] = c2_bow
        if len(a2_bow) > 0:
            bows2[SentenceElem.KEY_A] = a2_bow
        sims2 = {elem:0 for elem in bows2.keys()}
        
        wsimf = lambda x, y: TextSimilarity.word_sim(
            x,
            y,
            meaning_id=meaning_id,
            wsimexp=wsimexp,
            wsimtype=wsimtype,
            msimtype=msimtype)
        
        for elem1, bow1 in bows1.items():
            for elem2, bow2 in bows2.items():
                elem_set = {elem1, elem2}
                if elem_set != {SentenceElem.KEY_O, SentenceElem.KEY_OI}:
                    sim = TextSimilarity.bag_sim(bow1, bow2, simf=wsimf, scalar=True, pairs=False)
                    if sim > sims1[elem1]:
                        sims1[elem1] = sim
                    if sim > sims2[elem2]:
                        sims2[elem2] = sim

        n1 = len(sims1)
        n2 = len(sims2)
        vp_sim = {}
        
        for elem in (SentenceElem.KEY_V, SentenceElem.KEY_O, SentenceElem.KEY_OI, SentenceElem.KEY_C, SentenceElem.KEY_A):
            sim = TextSimilarity.tally_similarity(sims1, sims2, elem, n1, n2)
            if not sim is None:
                vp_sim[elem] = sim
        
        if scalar:
            return statistics.mean(vp_sim.values())
        else:
            return vp_sim

    @staticmethod
    def verbphraselm_sim(vplm1: VerbPhraseLm,
                         vplm2: VerbPhraseLm,
                         meaning_id = Meaning.MEANING_ID_DEFAULT,
                         scalar: bool = True,
                         wsimexp: Union[float, int] = 1,
                         wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                         msimtype: CalcType = CalcType.MAX,
                         lsimtype: CalcType = CalcType.MAX
                         ) -> float:
        """
        VerbPhraseLm similarity.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-12-12
        """
        
        return TextSimilarity.langmap_sim(
            vplm1,
            vplm2,
            simf = lambda x, y: TextSimilarity.verbphrase_sim(
                x,
                y,
                meaning_id=meaning_id,
                scalar=scalar,
                wsimexp=wsimexp,
                wsimtype=wsimtype,
                msimtype=msimtype),
            lsimtype=lsimtype)

    @staticmethod
    def word_sim(w1: Word,
                 w2: Word,
                 meaning_id: Union[str, list, set, tuple] = Edr.ID,
                 wsimexp: Union[float, int] = 1,
                 wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                 msimtype: CalcType = CalcType.MAX) -> Union[float, int]:
        """
        Calculate similarity between two Words.

        def word_sim(w1: Word,
                     w2: Word,
                     meaning_id: Union[str, list, set, tuple] = Meaning.MEANING_ID_DEFAULT,
                     wsimexp: Union[float, int] = 1,
                     wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                     msimtype: CalcType = CalcType.MAX) -> Union[float, int]:

        Parameters
        ----------
        w1 : Word
        w2 : Word
        meaning_id : str
            Specify concept dictionary to calculate similarity.
            Edr.ID: Calculate similarity by EDR concept id's.
            WordNet.ID: Calculate similarity by WordNet synsets.
            (Edr.ID, WordNet.ID): Both.
        wsimexp : int or float, optional
            The default is 1.
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEDIAN_COMBI:
            CalcType.MAX_MAX_1_TO_M:
            CalcType.MEAN_MAX_1_TO_M:
            CalcType.MEDIAN_MAX_1_TO_M:
            The default is CalcType.MEDIAN_MAX_1_TO_M.
        msimtype : CalcType, optional
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.

        Returns
        -------
        float or int
            0 <= Similarity <= 1

        @author: MURAKAMI Tamotsu
        @date: 2023-05-23
        """
        
        if isinstance(w1, Word) and isinstance(w2, Word):
            if w1.lang == w2.lang and w1.text == w2.text and w1.pos == w2.pos:
                return 1
            elif isinstance(meaning_id, str):
                if meaning_id in w1.meaning:
                    meaning_set1 = w1.meaning[meaning_id]
                else:
                    meaning_set1 = set()
                    
                if meaning_id in w2.meaning:
                    meaning_set2 = w2.meaning[meaning_id]
                else:
                    meaning_set2 = set()
                
                if meaning_set1 and meaning_set2:
                    ncommon = len(meaning_set1 & meaning_set2)
                    nwhole = len(meaning_set1 | meaning_set2)
                    jaccard = ncommon / nwhole
                    if jaccard == 1:
                        return jaccard
                    elif wsimtype == CalcType.MAX_COMBI:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_max_combi(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MEAN_COMBI:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_mean_combi(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MEDIAN_COMBI:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_median_combi(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MAX_MAX_1_TO_M:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_max_one_to_many(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       scalarfn=max,
                                       wsimtype=wsimtype,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MEAN_MAX_1_TO_M:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_max_one_to_many(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       scalarfn=statistics.mean,
                                       wsimtype=wsimtype,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MEDIAN_MAX_1_TO_M:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_max_one_to_many(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       scalarfn=statistics.median,
                                       wsimtype=wsimtype,
                                       wsimexp=wsimexp))
                    elif wsimtype == CalcType.MEDIAN_HIGH_MAX_1_TO_M:
                        return max(jaccard,
                                   TextSimilarity.word_sim_by_max_one_to_many(
                                       meaning_set1,
                                       meaning_set2,
                                       meaning_id,
                                       scalarfn=statistics.median_high,
                                       wsimtype=wsimtype,
                                       wsimexp=wsimexp))
                    else:
                        print("Word_sim: unknown similarity type {} for 'wsimtype'.".format(wsimtype))
                else:
                    return 0
    
            elif isinstance(meaning_id, list) or isinstance(meaning_id, set) or isinstance(meaning_id, tuple):
                sims = [TextSimilarity.word_sim(w1, w2, mid, wsimexp=wsimexp, wsimtype=wsimtype) for mid in meaning_id]
                if msimtype == CalcType.MAX:
                    return max(sims)
                elif msimtype == CalcType.MEAN:
                    return statistics.mean(sims)
                elif msimtype == CalcType.MIN:
                    return min(sims)
                else:
                    print("Word_sim: unknown similarity type {} for 'msimtype'.".format(msimtype))
                    return None
        else:
            if not isinstance(w1, Word):
                print("Word_sim: {} is not Word.".format(w1))
            if not isinstance(w2, Word):
                print("Word_sim: {} is not Word.".format(w2))
            return None

    @staticmethod
    def word_sim_by_max_combi(meanings1: Union[float, int],
                              meanings2: Union[float, int],
                              meaning_id: str,
                              wsimexp: Union[float, int]) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-27
        """
        
        simmax = 0

        if meaning_id == Edr.ID:
            for m1 in meanings1:
                for m2 in meanings2:
                    sim = Concept.calc_conceptid_wp_sim(m1, m2) ** wsimexp
                    if sim > simmax:
                        simmax = sim
                    if simmax == 1:
                        break
                if simmax == 1:
                    break
        elif meaning_id == WordNet.ID and simmax < 1:
            for m1 in meanings1:
                for m2 in meanings2:
                    sim = WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    if sim > simmax:
                        simmax = sim
                    if simmax == 1:
                        break
                if simmax == 1:
                    break
        
        return simmax

    @staticmethod
    def word_sim_by_mean_combi(meanings1: Union[list, set, tuple],
                               meanings2: Union[list, set, tuple],
                               meaning_id: str,
                               wsimexp: Union[float, int]) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-27
        """
        
        simsum = 0
        count = 0
        
        if meaning_id == Edr.ID:
            for m1 in meanings1:
                for m2 in meanings2:
                    simsum += Concept.calc_conceptid_wp_sim(m1, m2) ** wsimexp
                    count += 1
        elif meaning_id == WordNet.ID:
            for m1 in meanings1:
                for m2 in meanings2:
                    simsum += WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    count += 1
        
        return simsum / count

    @staticmethod
    def word_sim_by_median_combi(meanings1: Union[list, set, tuple],
                                 meanings2: Union[list, set, tuple],
                                 meaning_id: str,
                                 wsimexp: Union[float, int]) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-27
        """
        
        sims = []
        
        if meaning_id == Edr.ID:
            for m1 in meanings1:
                for m2 in meanings2:
                    sims.append(Concept.calc_conceptid_wp_sim(m1, m2) ** wsimexp)
        elif meaning_id == WordNet.ID:
            for m1 in meanings1:
                for m2 in meanings2:
                    sims.append(WordNet.similarity_wp_value(m1, m2) ** wsimexp)
        
        return statistics.median(sims)

    @staticmethod
    def word_sim_by_max_one_to_many(meanings1: Union[list, set, tuple],
                                    meanings2: Union[list, set, tuple],
                                    meaning_id: str,
                                    scalarfn: Callable,
                                    wsimtype: CalcType,
                                    wsimexp: Union[float, int]) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-27
        """
        
        if meaning_id == Edr.ID:
            sim = Concept.calc_conceptids_wp_sim(meanings1, meanings2, simtype=wsimtype) ** wsimexp
            return sim
        elif meaning_id == WordNet.ID:
            maxdict1 = {m:0 for m in meanings1}
            maxdict2 = {m:0 for m in meanings2}
            for m1 in meanings1:
                for m2 in meanings2:
                    sim = WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    maxdict1[m1] = max(maxdict1[m1], sim)
                    maxdict2[m2] = max(maxdict2[m2], sim)
        
            return (scalarfn(maxdict1.values()) + scalarfn(maxdict2.values())) / 2

    @staticmethod
    def wordlm_sim(wlm1: WordLm,
                   wlm2: WordLm,
                   meaning_id = Meaning.MEANING_ID_DEFAULT,
                   wsimexp: Union[float, int] = 1,
                   wsimtype: CalcType = CalcType.MEDIAN_MAX_1_TO_M,
                   msimtype: CalcType = CalcType.MAX,
                   lsimtype: CalcType = CalcType.MAX
                   ) -> float:
        """
        Calculate similarity between WordLm's.

        Parameters
        ----------
        wlm1 : WordLm
        wlm2 : WordLm
        meaning_id : str
            Specify concept dictionary to calculate similarity.
            WordNet.ID: Calculate similarity by WordNet synsets.
            Edr.ID: Calculate similarity by EDR concept id's.
            (WordNet.ID, Edr.ID): Calculates similarity for each meaning_id and summarize by 'msimtype'.
        wsimexp : TYPE, optional
            The default is WSIMEXP_DEFAULT.
        wsimtype : CalcType, optional
             Word similarity type.
             CalcType.MAX_COMBI:
             CalcType.MEAN_COMBI:
             CalcType.MEAN_MAX_1_TO_M:
             The default is WSIMTYPE_DEFAULT.
        msimtype : CalcType, optional
             Meaning similarity type.
             CalcType.MAX:
             CalcType.MEAN:
             CalcType.MIN:
             The default is CalcType.MAX.
        lsimtype : CalcType, optional
            Language similarity type.
            CalcType.ENG: 英語の意味の類似度を返す。
            CalcType.JPN: 日本語の意味の類似度を返す。
            CalcType.MAX: 各言語の意味の類似度の最大値を返す。
            CalcType.MEAN: 各言語の意味の類似度の平均を返す。
            CalcType.MIN: 各言語の意味の類似度の最小値を返す。
            The default is CalcType.MAX.

        Returns
        -------
        float
            類似度 s （0 <= s <=1).

        @author: MURAKAMI Tamotsu
        @date: 2022-12-12
        """
        
        return TextSimilarity.langmap_sim(
            wlm1,
            wlm2,
            simf = lambda x, y: TextSimilarity.word_sim(
                x,
                y,
                meaning_id=meaning_id,
                wsimexp=wsimexp,
                wsimtype=wsimtype,
                msimtype=msimtype),
            lsimtype=lsimtype)

    @staticmethod
    def _words_to_bow(words: Union[list, set, tuple]) -> ListDict:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-03-24
        """
        
        bow = ListDict()
        
        for w in words:
            if bow.in_(w):
                bow.get_pair(w)[1] += 1
            else:
                bow.store(w, 1)
        
        return bow

# Initialize

TextSimilarity.reset_parameters()

"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-03-24
"""

if __name__ == '__main__':

    print('* Test start *')
    
#    TextSimilarity.reset_parameters()

    texts1 = ['ソリティアはトランプゲームです。', '一人で遊びます。']
    texts2 = ['ババ抜きはトランプゲームです。', '複数で遊びます。']
    texts3 = ['七並べはトランプゲームです。', '複数で遊びます。']

    sim12 = TextSimilarity.calc_texts_bow_sim(texts1, texts2, method='EDR+ST')
    sim13 = TextSimilarity.calc_texts_bow_sim(texts1, texts3, method='EDR+ST')
    sim23 = TextSimilarity.calc_texts_bow_sim(texts2, texts3, method='EDR+ST')
    
    print([sim12, sim13, sim23])

    sim12 = TextSimilarity.calc_texts_bow_sim(texts1, texts2, method='ST')
    sim13 = TextSimilarity.calc_texts_bow_sim(texts1, texts3, method='ST')
    sim23 = TextSimilarity.calc_texts_bow_sim(texts2, texts3, method='ST')
    
    print([sim12, sim13, sim23])

    print('* Test end *')
    
# End of file