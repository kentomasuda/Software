# -*- coding: utf-8 -*-
"""
Text similarity

@author: MURAKAMI Tamotsu
@date: 2022-10-18
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
import statistics
from typing import Callable, Collection

# Library
from container_srclib.bag import Bag
from container_lib.collection import Collection_
from container_lib.dict import Dict_
from edr_lib.concept import Concept
from edr_lib.edr import Edr
from math_lib.number import Number
from math_srclib.calc_type import CalcType
from text_lib.lang import Lang
from text_lib.sentence import Sentence, SentenceLm
from text_lib.sentence_elem import SenElem, SentenceElem
from text_lib.text import Text_
from text_lib.word_phrase import Phrase
from text_lib.word_phrase import Word
from text_lib.wordlm import WordLm
from text_srclib.text_similarity import TextSimilarity
from wordnet_lib.wordnet import WordNet

class Similarity:
    """
    String (類似度)
    
    @author: MURAKAMI Tamotsu
    @date: 2020-01-30
    """
    
#    WSIMTYPE = 'comb_max'
#    WSIMTYPE = 'comb_mean'
#    WSIMTYPE = 'COMB_MEANMAX'
    
    @staticmethod
    def _sim_empty_mod(sim,
                       empty_mod
                       ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-03-28
        """
        
        if empty_mod is None:
            return sim
        else: # odd_mode is a number
            return (sim + empty_mod) / 2

    @staticmethod
    def bag_sim(bag1: Bag,
                bag2: Bag,
                simf: Callable,
                scalar: bool = False,
                pairs: bool = False
                ) -> tuple:
        """
        Calculate similarity between Bags.
        
        def bag_sim(bag1: Bag,
                    bag2: Bag,
                    simf: Callable,
                    scalar: bool = False,
                    pairs: bool = False
                    ) -> tuple:

        @author: MURAKAMI Tamotsu
        @date: 2022-10-18
        """
        
        items1 = bag1.get_elems()
        items2 = bag2.get_elems()
        
        n1 = len(items1)
        n2 = len(items2)

        sims1 = [0] * n1
        sims2 = [0] * n2
        
        others1 = [None] * n1
        others2 = [None] * n2
        
        i1 = 0
        for item1 in items1:
            i2 = 0
            for item2 in items2:
                sim = simf(item1, item2)
                if sim > sims1[i1]:
                    sims1[i1] = sim
                    others1[i1] = item2
                if sim > sims2[i2]:
                    sims2[i2] = sim
                    others2[i2] = item1
                i2 += 1
            i1 += 1
        
        if scalar:
            freqs1 = bag1.get_freqs()
            freqs2 = bag2.get_freqs()
            # simsum = sum(tuple(map(lambda sim, freq: sim * freq, sims1, freqs1)))\
            #        + sum(tuple(map(lambda sim, freq: sim * freq, sims2, freqs2)))
            # simmean = simsum / (sum(freqs1) + sum(freqs2))
            simsum1 = sum(tuple(map(lambda sim, freq: sim * freq, sims1, freqs1)))
            simsum2 = sum(tuple(map(lambda sim, freq: sim * freq, sims2, freqs2)))
            simmean = (n1 * simsum1 / sum(freqs1) + n2 * simsum2 / sum(freqs2)) / (n1 + n2)
            if pairs:
                return (simmean, tuple(others1), tuple(others2))
            else:
                return simmean
        elif pairs: # scalar == False, pairs == True
            return (tuple(sims1), tuple(sims2), tuple(others1), tuple(others2))
        else: # scalar == False, pairs == False
            return (tuple(sims1), tuple(sims2))
    
    @staticmethod
    def calc_simdict(simdicts,
                     type_: str, #: 'MAX', 'MEAN' or 'MIN'. To be discontinued. Use calctype.
                     calctype: CalcType
                     ) -> dict:
        """
        def calc_simdict(simdicts,
                         type_: str, #: 'MAX', 'MEAN' or 'MIN'. To be discontinued. Use calctype.
                         calctype: CalcType
                         ) -> dict:
            
            calctype:
                CalcType.MAX
                CalcType.MEAN
                CalcType.MIN

        @author: MURAKAMI Tamotsu
        @date: 2020-07-13
        """
        
        simdict = None
        sim = None
        
        if calctype == CalcType.MAX or type_ == 'MAX':
            for sdict in simdicts:
                s = sum(sdict.values())
                if sim is None or s > sim:
                    sim = s
                    simdict = sdict
            return simdict
        elif calctype == CalcType.MIN or type_ == 'MIN':
            for sdict in simdicts:
                s = sum(sdict.values())
                if sim is None or s < sim:
                    sim = s
                    simdict = sdict
            return simdict
        elif calctype == CalcType.MEAN or type_ == 'MEAN':
            return Dict_.mean_(simdicts)
        else:
            return None
    
    @staticmethod
    def collection_sim(col1: Collection,
                       col2: Collection,
                       simf: Callable,
                       emptysim = 1,
                       scalar: bool = False, # To be discontinued. Use scltype.
                       scltype: CalcType = CalcType.NONE,
                       simtype: CalcType = CalcType.ONE_TO_ONE,
                       pairs: bool = False
                       ): # -> number or tuple
        """
        Calculate similarity between Collections.
        
        def collection_sim(col1: Collection,
                           col2: Collection,
                           simf: Callable,
                           emptysim = 1,
                           scalar: bool = False, # To be discontinued. Use scltype.
                           scltype: CalcType = CalcType.NONE,
                           simtype: CalcType = CalcType.ONE_TO_MANY,
                           pairs: bool = False
                           ): # -> number or tuple
            
            simf: A function to calculate similarity.
                  Its return value x must be 0 <= x <= 1.
 
            emptysim: Control the return value when both col1 and col2 are empty.
                      When we compare an empty collection and non-empty collection,
                      its similarity should be 0 because they are different.
                      When we compare two empty collections, there are two possible answers:
                          0 because there is no similar elements, and
                          1 because they are same empty collections.
                A number: It returns the number.
                None: If scalar is True, it returns 0.
                      Otherwise it returns ().
            
            scalar: To be discontinued. Use scltype.
                False: It returns a tuple of similarities for item pairs.
                True: It returns mean of similarities for item pairs.
            
            scltype:
                CalcType.NONE: It returns a tuple of similarities for item pairs.
                CalcType.MAX: It returns max of similarities for item pairs.
                CalcType.MEAN: It returns mean of similarities for item pairs.
            
            simtype: See Collection_.compare.__doc__.
                CalcType.ONE_TO_MANY:
                CalcType.ONE_TO_ONE:
            
            pairs: See Collection_.compare.__doc__.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-07-13
        """
        
        n1 = len(col1)
        n2 = len(col2)
        
        if not n1 == 0 and not n2 == 0:  # Both are non-empty.
            if pairs:
                siml, el1, el2 = Collection_.compare(col1,
                                                     col2,
                                                     simf=simf,
                                                     simtype = simtype,
                                                     pairs=pairs)
                if scltype != CalcType.NONE:
                    return (Similarity.sim_scalar(siml, n1, n2, scltype = scltype), el1, el2)
                else:
                    return (siml, el1, el2)
            else:
                siml = Collection_.compare(col1,
                                           col2,
                                           simf=simf,
                                           simtype = simtype,
                                           pairs=pairs)
                if scltype != CalcType.NONE:
                    return Similarity.sim_scalar(siml, n1, n2, scltype = scltype)
                else:
                    return siml
        elif n1 == 0 and n2 == 0: # Both are empty
            if not emptysim is None:
                sim = emptysim
            else:
                if scltype != CalcType.NONE:
                    sim = 0
                else:
                    sim = ()

            if pairs:
                return (sim, (), ())
            else:
                return sim
        else: # Empty and non-empty
            if scltype != CalcType.NONE:
                sim = 0
            else:
                sim = ()
                
            if pairs:
                return (sim, (), ())
            else:
                return sim
    
    @staticmethod
    def langmap_sim(lm1,
                    lm2,
                    simf: Callable,
                    invalid, # Return value when the result is invalid.
                    lsimtype: CalcType = CalcType.MIN,
                    type_ = None # Not used 
                    ): # -> number
        """
        Language map similarity.
        0 <= return value <= 1

        def langmap_sim(lm1,
                        lm2,
                        simf: Callable,
                        invalid, # Return value when the result is invalid.
                        type_, # Not used 
                        lsimtype: CalcType = CalcType.MIN
                        ): # -> number

            lsimtype:
                CalcType.ENG:
                CalcType.JPN:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

        @author: MURAKAMI Tamotsu
        @date: 2020-05-31
        """
        
        dict1 = lm1.langmap
        dict2 = lm2.langmap
        
        if lsimtype == CalcType.JPN:
            if Lang.JPN in dict1 and Lang.JPN in dict2:
                return simf(dict1[Lang.JPN], dict2[Lang.JPN])
            else:
                return invalid
        elif lsimtype == CalcType.ENG:
            if Lang.ENG in dict1 and Lang.ENG in dict2:
                return simf(dict1[Lang.ENG], dict2[Lang.ENG])
            else:
                return invalid
        elif lsimtype == CalcType.MAX or lsimtype == CalcType.MEAN or lsimtype == CalcType.MIN:
            siml = [simf(dict1[lang], dict2[lang]) for lang in (dict1.keys() & dict2.keys())]
            if lsimtype == CalcType.MAX:
                return max(siml)
            elif lsimtype == CalcType.MEAN:
                return statistics.mean(siml)
            elif lsimtype == CalcType.MIN:
                return min(siml)
            else:
                return invalid
        else:
            return invalid

    @staticmethod
    def phrase_col_sim(col1: Collection,
                       col2: Collection,
                       meaning_id: str,
                       wsimexp = 1,
                       wsimtype: CalcType = CalcType.MAX_COMBI,
                       msimtype: CalcType = CalcType.MAX,
                       emptysim = 1,
                       scalar: str = None,
                       scltype: CalcType = CalcType.NONE,
                       colsim: CalcType = CalcType.ONE_TO_ONE,
                       pairs: bool = False
                       ): # -> tuple or number
        """
        Phrase collection similarity.
        
        def phrase_col_sim(col1: Collection,
                           col2: Collection,
                           meaning_id: str,
                           wsimexp = 1,
                           wsimtype: CalcType = CalcType.MAX_COMBI,
                           msimtype: CalcType = CalcType.MAX,
                           emptysim = 1,
                           scalar: str = None,
                           scltype: CalcType = CalcType.NONE,
                           colsim: CalcType = CalcType.ONE_TO_ONE,
                           pairs: bool = False
                           ): # -> tuple or number
            
            scltype:
                CalcType.NONE
                CalcType.MEAN

            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            colsim:
                CalcType.ONE_TO_MANY:
                CalcType.ONE_TO_ONE:

            'scalar': When it is True, the similarity is returned as a number
                      instead of a tuple.
    
            'pairs': When it is False, just similarity is returned.
                     When it is True, a tuple
                     (similarity, element list1, element list2) is returned.
                     The two element lists shows how elements in 'col1' and 'col2'
                     are paired, i.e., i-th element of element list1 is paired with
                     i-th element of element list2.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda x, y: Similarity.phrase_sim(x,
                                                                                    y,
                                                                                    meaning_id,
                                                                                    wsimexp = wsimexp,
                                                                                    wsimtype = wsimtype,
                                                                                    msimtype = msimtype)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)

    @staticmethod
    def phrase_sim(pw1, # Phrase or Word
                   pw2, # Phrase or Word
                   meaning_id: str,
                   wsimexp = 1,
                   wsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                   msimtype: CalcType = CalcType.MAX
                   ) -> float:
        """
        Phrase similarity

        def phrase_sim(pw1, # Phrase or Word
                       pw2, # Phrase or Word
                       meaning_id: str,
                       wsimexp = 1,
                       wsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                       msimtype: CalcType = CalcType.MAX
                       ) -> float:

        Parameters
        ----------
        pw1 : Phrase or Word
        pw2 : Phrase or Word
        meaning_id : str
        wsimexp : int or float, optional
            The default is 1.
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEAN_MAX_1_TO_M:
            The default is CalcType.MEAN_MAX_1_TO_M.
        msimtype : CalcType, optional
            Meaning similarity type.
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.

        Returns
        -------
        float
            0 <= Similarity <= 1.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """

        if isinstance(pw1, Phrase):
            if isinstance(pw2, Phrase):
                # Head similarity
                simh = Similarity.word_sim(pw1.head,
                                           pw2.head,
                                           meaning_id,
                                           wsimexp=wsimexp,
                                           wsimtype=wsimtype,
                                           msimtype=msimtype)
                
                if pw1.modifiers and pw2.modifiers:
                    # Modifiers similarity
                    simm = Similarity.word_col_sim(pw1.modifiers,
                                                   pw2.modifiers,
                                                   meaning_id,
                                                   wsimexp = wsimexp,
                                                   wsimtype = wsimtype,
                                                   msimtype = msimtype,
                                                   scalar = 'mean',
                                                   scltype = CalcType.MEAN,
                                                   pairs = False)
                    sim = Number.simple((simh + simm) / 2)
                elif pw1.modifiers or pw2.modifiers: # One is not empty and the other is empty.
                    simm = 0
                    sim = (simh + simm) / 2
                else: # Both are empty
                    sim = simh
            elif isinstance(pw2, Word):
                simh = Similarity.word_sim(pw1.head, pw2, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                if pw1.modifiers:
                    simm = 0
                    sim = (simh + simm) / 2
                else:
                    sim = simh
            else:
                sim = None
        elif isinstance(pw1, Word):
            if isinstance(pw2, Phrase):
                simh = Similarity.word_sim(pw1, pw2.head, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                if pw2.modifiers:
                    simm = 0
                    sim = (simh + simm) / 2
                else:
                    sim = simh
            elif isinstance(pw2, Word):
                sim = Similarity.word_sim(pw1, pw2, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
            else:
                sim = None
        else:
            sim = None
        
        return sim

    @staticmethod
    def phraselm_col_sim(col1: Collection,
                         col2: Collection,
                         meaning_id: str,
                         langtype: str = 'MIN', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                         lang_invalid = 0, # Return value when the result for langtype is invalid.
                         wsimexp = 1,
                         wsimtype: CalcType = CalcType.MAX_COMBI,
                         msimtype: CalcType = CalcType.MAX,
                         emptysim = 1,
                         scalar: str = None,
                         scltype: CalcType = CalcType.NONE,
                         colsim: CalcType = CalcType.ONE_TO_ONE,
                         pairs: bool = False
                         ): # -> tuple or number
        """
        PhraseLm collection similarity.
        This calculate a similarity between phrase collections for each language
        in the language maps.

        def phraselm_col_sim(col1: Collection,
                             col2: Collection,
                             meaning_id: str,
                             langtype: str = 'MIN', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                             lang_invalid = 0, # Return value when the result for langtype is invalid.
                             wsimexp = 1,
                             wsimtype: CalcType = CalcType.MAX_COMBI,
                             msimtype: CalcType = CalcType.MAX,
                             emptysim = 1,
                             scalar: str = None,
                             scltype: CalcType = CalcType.NONE,
                             colsim: CalcType = CalcType.ONE_TO_ONE,
                             pairs: bool = False
                             ): # -> tuple or number
        
            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            colsim:
                CalcType.ONE_TO_MANY:
                CalcType.ONE_TO_ONE:

            scalar: When it is True, the similarity is returned as a number
                instead of a tuple.

            pairs: When it is False, just a similarity is returned.
                When it is True, a tuple
                (similarity, element list1, element list2) is returned.
                The two element lists shows how elements in 'col1' and 'col2'
                are paired, i.e., i-th element of element list1 is paired with
                i-th element of element list2.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda x, y:
                                                 Similarity.phraselm_sim(x,
                                                                         y,
                                                                         meaning_id,
                                                                         langtype = langtype,
                                                                         lang_invalid = lang_invalid,
                                                                         wsimexp = wsimexp,
                                                                         wsimtype = wsimtype,
                                                                         msimtype = msimtype)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)

    @staticmethod
    def phraselm_sim(pw1, # PhraseLm or WordLm
                     pw2, # PhraseLm or WordLm
                     meaning_id = (Edr.ID, WordNet.ID),
                     langtype: str = 'MAX', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                     lang_invalid = 0, # Return value when the result for langtype is invalid.
                     wsimexp = 1,
                     wsimtype: CalcType = CalcType.MAX_COMBI,
                     msimtype: CalcType = CalcType.MAX
                     ) -> float:
        """
        PhraseLm similarity.
        

        Parameters
        ----------
        pw1 : PhraseLm or WordLm
        pw2 : PhraseLm or WordLm
        meaning_id : str
        langtype : str, optional
            'MAX'
            'MEAN'
            'MIN'
            'JPN'
            'ENG'
            The default is 'MEAN'.
        lang_invalid : optional
            Return value when the result for langtype is invalid.
            The default is 0.
            DESCRIPTION. The default is 1.
        wsimexp : int or float, optional
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEAN_MAX_1_TO_M:
            The default is CalcType.MAX_COMBI.
        msimtype : CalcType, optional
            Meaning similarity type.
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.

        Returns
        -------
        float
            0 <= Similarity <= 1.

        @author: MURAKAMI Tamotsu
        @date: 2021-10-01
        """
        
        return Similarity.langmap_sim(pw1,
                                      pw2,
                                      simf = (lambda x, y: Similarity.phrase_sim(x,
                                                                                 y,
                                                                                 meaning_id,
                                                                                 wsimexp = wsimexp,
                                                                                 wsimtype = wsimtype,
                                                                                 msimtype = msimtype)),
                                      type_ = langtype,
                                      invalid = lang_invalid)

    @staticmethod
    def scalar_max(sim) -> float:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-03-29
        """
        
        if sim: # Not empty
            return max(sim)
        else:
            return 0

    @staticmethod
    def scalar_mean(sim: dict) -> float:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-03-29
        """
        
        if sim: # Not empty
            return statistics.mean(sim.values())
        else:
            return 0
    
    @staticmethod
    def scalarize(sim, # : Collection, number or None
                  type_: str, # 'MAX', 'MEAN' or 'MIN'
                  invalid # Return value when the result is invalid.
                  ): # -> number
        """
        def scalarize(sim, # : Collection, number or None
                      type_: str, # 'MAX', 'MEAN' or 'MIN'
                      invalid # Return value when the result is invalid.
                      ): # -> number

        @author: MURAKAMI Tamotsu
        @date: 2019-12-06
        """
        
        if isinstance(sim, Collection):
            if type_ == 'MAX':
                return max(sim)
            elif type_ == 'MIN':
                return min(sim)
            elif type_ == 'MEAN':
                return statistics.mean(sim)
            else:
                return invalid
        elif isinstance(sim, int) or isinstance(sim, float):
            return sim
        else:
            return invalid

    @staticmethod
    def sentence_col_sim(col1: Collection,
                         col2: Collection,
                         meaning_id: str,
                         wsimexp = 1,
                         wsimtype: CalcType = CalcType.MAX_COMBI,
                         msimtype: CalcType = CalcType.MAX,
                         pattern: bool = True,
                         emptysim = 1,
                         scalar: str = None,
                         scltype: CalcType = CalcType.NONE,
                         colsim: CalcType = CalcType.ONE_TO_MANY,
                         pairs: bool = False
                         ): # -> tuple or number
        """
        Sentence collection similarity.
        
        def sentence_col_sim(col1: Collection,
                             col2: Collection,
                             meaning_id: str,
                             wsimexp = 1,
                             wsimtype: CalcType = CalcType.MAX_COMBI,
                             msimtype: CalcType = CalcType.MAX,
                             pattern: bool = True,
                             emptysim = 1,
                             scalar: str = None,
                             scltype: CalcType = CalcType.NONE,
                             colsim: CalcType = CalcType.ONE_TO_MANY,
                             pairs: bool = False
                             ): # -> tuple or number

            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            colsim:
                CalcType.ONE_TO_MANY:
                CalcType.ONE_TO_ONE:

            pattern: When it is True, similarity between sentences of different
                   sentence patterns is estimated as zero.
                   When it is False, partial similarity between sentences of
                   different sentence patterns is estimated.

            scalar: When it is True, the similarity is returned as a number
                      instead of a tuple.
    
            pairs: When it is False, just a similarity is returned.
                     When it is True, a tuple
                     (similarity, element list1, element list2) is returned.
                     The two element lists shows how elements in 'col1' and 'col2'
                     are paired, i.e., i-th element of element list1 is paired with
                     i-th element of element list2.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda sen1, sen2:\
                                                 Similarity.sentence_sim(sen1,
                                                                         sen2,
                                                                         meaning_id,
                                                                         wsimexp=wsimexp,
                                                                         wsimtype=wsimtype,
                                                                         msimtype=msimtype,
                                                                         pattern=pattern,
                                                                         scalar='mean',
                                                                         scltype = CalcType.MEAN)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         simtype = colsim,
                                         scltype = scltype,
                                         pairs = pairs)
    
    @staticmethod
    def sentence_col_sim_by_elem_bow(col1: Collection,
                                     col2: Collection,
                                     meaning_id: str,
                                     wsimexp = 1,
                                     wsimtype: CalcType = CalcType.MAX_COMBI,
                                     msimtype: CalcType = CalcType.MAX,
                                     pattern: bool = True,
                                     emptysim = 1,
                                     scalar: bool = False,
                                     scltype: CalcType = CalcType.NONE,
                                     colsim: CalcType = CalcType.ONE_TO_MANY,
                                     pairs: bool = False
                                     ): # -> tuple or number
        """
        Sentence collection similarity by element bag-of-words.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-09-06
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda sen1, sen2:\
                                                 Similarity.sentence_sim_by_elem_bow(sen1,
                                                                                     sen2,
                                                                                     meaning_id,
                                                                                     wsimexp = wsimexp,
                                                                                     wsimtype = wsimtype,
                                                                                     msimtype = msimtype,
                                                                                     pattern = pattern,
                                                                                     scalar = scalar)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         simtype = colsim,
                                         scltype = scltype,
                                         pairs = pairs)
    
    @staticmethod
    def sentence_sim(sen1: Sentence,
                     sen2: Sentence,
                     meaning_id: str,
                     wsimexp = 1,
                     wsimtype: CalcType = CalcType.MAX_COMBI,
                     msimtype: CalcType = CalcType.MAX,
                     pattern: bool = False,
                     scalar: bool = False,
                     scltype: CalcType = CalcType.NONE
                     ):
        """
        Sentence similarity

        Parameters
        ----------
        sen1 : Sentence
        sen2 : Sentence
        meaning_id : str
        wsimexp : int or float, optional
            The default is 1.
        wsimtype : CalcType, optional
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEAN_MAX_1_TO_M:
            The default is CalcType.MAX_COMBI.
        msimtype : CalcType, optional
            DESCRIPTION. The default is CalcType.MAX.
        pattern : bool, optional
            True: Similarity between sentences of different
                  sentence patterns is estimated as an empty dict (zero).
            False: Partial similarity between sentences of
                   different sentence patterns is estimated.
            The default is False.
        scalar : bool, optional
            For backward compatibility. Use scltype.
            When it is True, the return value is a number instead of a dict.
            DESCRIPTION. The default is False.
        scltype : CalcType, optional
            Scalar type.
            CalcType.NONE: Dict is returned.
            CalcType.MEAN: Number is returned.
            The default is CalcType.NONE.

        Returns
        -------
        sim : TYPE
            Dict or number.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
       
        if pattern and (sen1.pattern != sen2.pattern):
            if scltype != CalcType.NONE:
                sim = 0
            else:
                sim = {} # Empty dict
        else:
            sim = {}
            
            if sen1.subjects and sen2.subjects:
                if len(sen1.subjects) == 1 and len(sen2.subjects) == 1:
                    sim[SenElem.S] = Similarity.phrase_sim(
                            sen1.subjects[0],
                            sen2.subjects[0],
                            meaning_id,
                            wsimexp=wsimexp,
                            wsimtype=wsimtype,
                            msimtype=msimtype)
                else:
                    sim[SenElem.S] = Similarity.phrase_col_sim(sen1.subjects, sen2.subjects, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.subjects or sen2.subjects:
                sim[SenElem.S] = 0
            else: # Both empty
                sim[SenElem.S] = 1

            if sen1.verbs and sen2.verbs:
                if len(sen1.verbs) == 1 and len(sen2.verbs) == 1:
                    sim[SenElem.V] = Similarity.phrase_sim(sen1.verbs[0], sen2.verbs[0], meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                else:
                    sim[SenElem.V] = Similarity.phrase_col_sim(sen1.verbs, sen2.verbs, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.verbs or sen2.verbs:
                sim[SenElem.V] = 0
            else: # Both empty
                pass
            
            if sen1.objects and sen2.objects:
                if len(sen1.objects) == 1 and len(sen2.objects) == 1:
                    sim[SenElem.O] = Similarity.phrase_sim(sen1.objects[0], sen2.objects[0], meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                else:
                    sim[SenElem.O] = Similarity.phrase_col_sim(sen1.objects, sen2.objects, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.objects or sen2.objects:
                sim[SenElem.O] = 0
            else: # Both empty
                pass
            
            if sen1.indirect_objects and sen2.indirect_objects:
                if len(sen1.indirect_objects) == 1 and len(sen2.indirect_objects) == 1:
                    sim[SenElem.OI] = Similarity.phrase_sim(sen1.indirect_objects[0], sen2.indirect_objects[0], meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                else:
                    sim[SenElem.OI] = Similarity.phrase_col_sim(sen1.indirect_objects, sen2.indirect_objects, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.indirect_objects or sen2.indirect_objects:
                sim[SenElem.OI] = 0
            else: # Both empty
                pass
            
            if sen1.complements and sen2.complements:
                if len(sen1.complements) == 1 and len(sen2.complements) == 1:
                    sim[SenElem.C] = Similarity.phrase_sim(sen1.complements[0], sen2.complements[0], meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                else:
                    sim[SenElem.C] = Similarity.phrase_col_sim(sen1.complements, sen2.complements, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.complements or sen2.complements:
                sim[SenElem.C] = 0
            else: # Both empty
                pass
            
            if sen1.adverbials and sen2.adverbials:
                if len(sen1.adverbials) == 1 and len(sen2.adverbials) == 1:
                    sim[SenElem.A] = Similarity.phrase_sim(sen1.adverbials[0], sen2.adverbials[0], meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype)
                else:
                    sim[SenElem.A] = Similarity.phrase_col_sim(sen1.adverbials, sen2.adverbials, meaning_id, wsimexp=wsimexp, wsimtype=wsimtype, msimtype=msimtype, scalar='mean', scltype = CalcType.MEAN)
            elif sen1.adverbials or sen2.adverbials:
                sim[SenElem.A] = 0
            else: # Both empty
                pass

            if scltype == CalcType.MEAN:
                sim = Similarity.scalar_mean(sim) # number

        return sim
    
    @staticmethod
    def sentence_sim_by_elem_bow(sen1: Sentence,
                                 sen2: Sentence,
                                 meaning_id: str,
                                 ignore_s: bool = False,
                                 wsimexp = 1,
                                 wsimtype: CalcType = CalcType.MAX_COMBI,
                                 msimtype: CalcType = CalcType.MAX,
                                 pattern: bool = False,
                                 scalar: bool = False
                                 ): # -> dict or number
        """
        Sentence similarity by sentence element bag-of-words.
        
        def sentence_sim_by_elem_bow(sen1: Sentence,
                                     sen2: Sentence,
                                     meaning_id: str,
                                     ignore_s: bool = False,
                                     wsimexp = 1,
                                     wsimtype: CalcType = CalcType.MAX_COMBI,
                                     msimtype: CalcType = CalcType.MAX,
                                     pattern: bool = False,
                                     scalar: bool = False
                                     ): # -> dict or number

        @author: MURAKAMI Tamotsu
        @date: 2021-02-09
        """
        
        wsimf = lambda w1, w2: Similarity.word_sim(w1,
                                                   w2,
                                                   meaning_id = meaning_id,
                                                   wsimexp = wsimexp,
                                                   wsimtype = wsimtype,
                                                   msimtype = msimtype)
        
        if pattern and (sen1.pattern != sen2.pattern):
            if scalar:
                sim = 0
            else:
                sim = {} # Empty dict
        else:
            sim = {}
            
            if ignore_s:
                sim[SenElem.S] = 1
            elif sen1.get_subject() and sen2.get_subject():
                sim[SenElem.S] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_subject()),
                                                    SentenceElem.bag_of_words(sen2.get_subject()),
                                                    simf = wsimf,
                                                    scalar = True,
                                                    pairs = False)
            elif sen1.get_subject() or sen2.get_subject(): # One is empty and the other is not.
                sim[SenElem.S] = 0
            else: # Both empty
                pass

            if sen1.get_verb() and sen2.get_verb():
                sim[SenElem.V] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_verb()),
                                                    SentenceElem.bag_of_words(sen2.get_verb()),
                                                    simf = wsimf,
                                                    scalar = True,
                                                    pairs = False)
            elif sen1.get_verb() or sen2.get_verb():
                sim[SenElem.V] = 0
            else:
                pass
            
            if sen1.get_object() and sen2.get_object():
                sim[SenElem.O] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_object()),
                                                    SentenceElem.bag_of_words(sen2.get_object()),
                                                    simf = wsimf,
                                                    scalar = True,
                                                    pairs = False)
            elif sen1.get_object() or sen2.get_object():
                sim[SenElem.O] = 0
            else: # Both empty
                pass
            
            if sen1.get_indirect_object() and sen2.get_indirect_object():
                sim[SenElem.OI] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_indirect_object()),
                                                     SentenceElem.bag_of_words(sen2.get_indirect_object()),
                                                     simf = wsimf,
                                                     scalar = True,
                                                     pairs = False)
            elif sen1.get_indirect_object() or sen2.get_indirect_object():
                sim[SenElem.OI] = 0
            else: # Both empty
                pass
            
            if sen1.get_complement() and sen2.get_complement():
                sim[SenElem.C] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_complement()),
                                                    SentenceElem.bag_of_words(sen2.get_complement()),
                                                    simf = wsimf,
                                                    scalar = True,
                                                    pairs = False)
            elif sen1.get_complement() or sen2.get_complement():
                sim[SenElem.C] = 0
            else: # Both empty
                pass
            
            if sen1.get_adverbial() and sen2.get_adverbial():
                sim[SenElem.A] = Similarity.bag_sim(SentenceElem.bag_of_words(sen1.get_adverbial()),
                                                    SentenceElem.bag_of_words(sen2.get_adverbial()),
                                                    simf = wsimf,
                                                    scalar = True,
                                                    pairs = False)
            elif sen1.get_adverbial() or sen2.get_adverbial():
                sim[SenElem.A] = 0
            else: # Both empty
                pass

            if scalar:
                sim = Similarity.scalar_mean(sim) # number

        return sim
    
    @staticmethod
    def sentencelm_col_sim(col1: Collection,
                           col2: Collection,
                           meaning_id: str,
                           langtype: str = 'MIN', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                           lang_invalid = 0, # Return value when the result for langtype is invalid.
                           wsimexp = 1,
                           wsimtype: CalcType = CalcType.MAX_COMBI,
                           msimtype: CalcType = CalcType.MAX,
                           pattern: bool = True,
                           emptysim = 1,
                           scalar: str = None,
                           scltype: CalcType = CalcType.NONE,
                           colsim: CalcType = CalcType.ONE_TO_MANY, # or CalcType.ONE_TO_ONE
                           pairs: bool = False
                           ): # -> tuple or number
        """
        SentenceLm collections similarity

        This calculate a similarity between sentence collections for each
        language in the language maps.

        def sentencelm_col_sim(col1: Collection,
                               col2: Collection,
                               meaning_id: str,
                               langtype: str = 'MEAN', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                               lang_invalid = 0, # Return value when the result for langtype is invalid.
                               wsimexp = 1,
                               wsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M, # or 'MAX_COMBI' or 'MEAN_COMBI'.
                               pattern: bool = True,
                               emptysim = 1,
                               scalar: str = None,
                               colsim: CalcType = CalcType.ONE_TO_MANY, # or CalcType.ONE_TO_ONE
                               pairs: bool = False
                               ): # -> tuple or number

            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            'pattern': When it is True, similarity between sentences of different
                       sentence patterns is calculated as 0.
                       When it is False, partial similarity between sentences of
                       different sentence patterns is calculated.
    
            'scalar': When it is True, the similarity is returned as a number
                      instead of a tuple.
    
            scltype:
                CalcType.NONE
                CalcType.MEAN
    
            'pairs': When it is False, just a similarity is returned.
                     When it is True, a tuple
                     (similarity, element list1, element list2) is returned.
                     The two element lists shows how elements in 'col1' and 'col2'
                     are paired, i.e., i-th element of element list1 is paired with
                     i-th element of element list2.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-13
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf= (lambda slm1, slm2:\
                                                Similarity.sentencelm_sim(slm1,
                                                                          slm2,
                                                                          meaning_id,
                                                                          langtype=langtype,
                                                                          lang_invalid=lang_invalid,
                                                                          wsimexp=wsimexp,
                                                                          wsimtype=wsimtype,
                                                                          msimtype=msimtype,
                                                                          pattern=pattern,
                                                                          scalar='mean',
                                                                          scltype = scltype)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)
    
    @staticmethod
    def sentencelm_col_sim_by_elem_bow(col1: Collection,
                                       col2: Collection,
                                       meaning_id: str,
                                       langtype: str = 'MIN', # : 'MAX', 'MEAN', 'MIN', 'JPN' or 'ENG'
                                       lang_invalid = 0, # Return value when the result for langtype is invalid.
                                       wsimexp = 1,
                                       wsimtype: CalcType = CalcType.MAX_COMBI,
                                       msimtype: CalcType = CalcType.MAX,
                                       pattern: bool = True,
                                       emptysim = 1,
                                       scalar: str = None,
                                       scltype: CalcType = CalcType.NONE,
                                       colsim: CalcType = CalcType.ONE_TO_MANY, # or CalcType.ONE_TO_ONE
                                       pairs: bool = False
                                       ): # -> tuple or number
        """
        SentenceLm collections similarity by element bag-of-words.

        This calculate a similarity between sentence collections for each
        language in the language maps.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-06
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf= (lambda slm1, slm2:\
                                                Similarity.sentencelm_sim_by_elem_bow(slm1,
                                                                                      slm2,
                                                                                      meaning_id,
                                                                                      langtype = langtype,
                                                                                      lang_invalid = lang_invalid,
                                                                                      wsimexp = wsimexp,
                                                                                      wsimtype = wsimtype,
                                                                                      msimtype = msimtype,
                                                                                      pattern = pattern,
                                                                                      scalar = True)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)
    
    @staticmethod
    def sentencelm_sim(sen1: SentenceLm,
                       sen2: SentenceLm,
                       meaning_id: str,
                       langtype: CalcType = CalcType.MIN,
                       lang_invalid = 0, # Return value when the result for langtype is invalid.
                       wsimexp = 1,
                       wsimtype: CalcType = CalcType.MAX_COMBI,
                       msimtype: CalcType = CalcType.MAX,
                       pattern: bool = False,
                       scalar: bool = False,
                       scltype: CalcType = CalcType.NONE
                       ):
        """
        SentenceLm similarity
        
        This calculate a similarity between sentences for each language in the
        language maps.

        Parameters
        ----------
        sen1 : SentenceLm
        sen2 : SentenceLm
        meaning_id : str
        langtype : CalcType, optional
            Language type.
            CaclType.MAX, 'MAX'
            CaclType.MEAN, 'MEAN
            CaclType.MIN, 'MIN'
            CaclType.JPN, 'JPN'
            CaclType.ENG, 'ENG'
            The default is CalcType.MIN.
        lang_invalid : TYPE, optional
            Return value when the result for langtype is invalid.
            DESCRIPTION. The default is 0.
        wsimexp : int or float, optional
            The default is 1.
        wsimtype : CalcType, optional
            Word similarity type.
            CalcType.MAX_COMBI:
            CalcType.MEAN_COMBI:
            CalcType.MEAN_MAX_1_TO_M:
            The default is CalcType.MAX_COMBI.
        msimtype : CalcType, optional
            Meaning similarity type.
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.
        pattern : bool, optional
            DESCRIPTION. The default is False.
        scalar : bool, optional
            For backward compatibility. Use scltype.
            The default is False.
        scltype : CalcType, optional
            CaclType.NONE
            CaclType.MEAN
            The default is CalcType.NONE.

        Returns
        -------
        Dict or number.
            Similarity.

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        lm1 = sen1.langmap
        lm2 = sen2.langmap
        
        simdict = None
        simdicts = []
        
        if langtype == CalcType.JPN or langtype == 'JPN':
            if Lang.JPN in lm1 and Lang.JPN in lm2:
                simdict = Similarity.sentence_sim(lm1[Lang.JPN],
                                                  lm2[Lang.JPN],
                                                  meaning_id,
                                                  wsimexp = wsimexp,
                                                  wsimtype = wsimtype,
                                                  msimtype = msimtype,
                                                  pattern = pattern,
                                                  scalar = None,
                                                  scltype = CalcType.NONE)
                if scltype == CalcType.MEAN:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return lang_invalid
        elif langtype == CalcType.ENG or langtype == 'ENG':
            if Lang.ENG in lm1 and Lang.ENG in lm2:
                simdict = Similarity.sentence_sim(lm1[Lang.ENG],
                                                  lm2[Lang.ENG],
                                                  meaning_id,
                                                  wsimexp = wsimexp,
                                                  wsimtype = wsimtype,
                                                  msimtype = msimtype,
                                                  pattern = pattern,
                                                  scalar = None,
                                                  scltype = CalcType.NONE)
                if scltype == CalcType.MEAN:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return lang_invalid
        elif langtype == CalcType.MAX or langtype == CalcType.MEAN or langtype == CalcType.MIN or\
             langtype == 'MAX' or langtype == 'MEAN' or langtype == 'MIN': 
            for lang in (lm1.keys() & lm2.keys()):
                simdicts.append(Similarity.sentence_sim(lm1[lang],
                                                        lm2[lang],
                                                        meaning_id,
                                                        wsimexp = wsimexp,
                                                        wsimtype = wsimtype,
                                                        msimtype = msimtype,
                                                        pattern = pattern,
                                                        scalar = None,
                                                        scltype = CalcType.NONE))
            simdict = Similarity.calc_simdict(simdicts, type_ = langtype, calctype = langtype)
            if simdict:
                if scltype != CalcType.NONE or scalar:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return None
        else:
            return None
    
    @staticmethod
    def sentencelm_sim_by_elem_bow(sen1: SentenceLm,
                                   sen2: SentenceLm,
                                   meaning_id = TextSimilarity.meaning_id,
                                   ignore_s: bool = False,
                                   langtype: CalcType = TextSimilarity.langtype,
                                   lang_invalid = 0, # Return value when the result for langtype is invalid.
                                   wsimexp = TextSimilarity.wsimexp,
                                   wsimtype: CalcType = TextSimilarity.wsimtype,
                                   msimtype: CalcType = TextSimilarity.msimtype,
                                   pattern: bool = False,
                                   scalar: bool = False,
                                   scltype: CalcType = CalcType.NONE
                                   ): # -> dict or number
        """
        SentenceLm similarity by element bag-of-words.

        @author: MURAKAMI Tamotsu
        @date: 2021-01-23
        """
        
        lm1 = sen1.langmap
        lm2 = sen2.langmap
        
        simdict = None
        simdicts = []
        
        if langtype == CalcType.JPN or langtype == 'JPN':
            if Lang.JPN in lm1 and Lang.JPN in lm2:
                simdict = Similarity.sentence_sim_by_elem_bow(lm1[Lang.JPN],
                                                              lm2[Lang.JPN],
                                                              meaning_id,
                                                              ignore_s = ignore_s,
                                                              wsimexp = wsimexp,
                                                              wsimtype = wsimtype,
                                                              msimtype = msimtype,
                                                              pattern = pattern,
                                                              scalar = scalar)
                if scltype == CalcType.MEAN:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return lang_invalid
        elif langtype == CalcType.ENG or langtype == 'ENG':
            if Lang.ENG in lm1 and Lang.ENG in lm2:
                simdict = Similarity.sentence_sim_by_elem_bow(lm1[Lang.ENG],
                                                              lm2[Lang.ENG],
                                                              meaning_id,
                                                              ignore_s = ignore_s,
                                                              wsimexp = wsimexp,
                                                              wsimtype = wsimtype,
                                                              msimtype = msimtype,
                                                              pattern = pattern,
                                                              scalar = False)
                if scltype == CalcType.MEAN:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return lang_invalid
        elif langtype == CalcType.MAX or langtype == CalcType.MEAN or langtype == CalcType.MIN or\
             langtype == 'MAX' or langtype == 'MEAN' or langtype == 'MIN': 
            for lang in (lm1.keys() & lm2.keys()):
                simdicts.append(Similarity.sentence_sim_by_elem_bow(lm1[lang],
                                                                    lm2[lang],
                                                                    meaning_id,
                                                                    ignore_s = ignore_s,
                                                                    wsimexp = wsimexp,
                                                                    wsimtype = wsimtype,
                                                                    msimtype = msimtype,
                                                                    pattern = pattern,
                                                                    scalar = False))
            simdict = Similarity.calc_simdict(simdicts, type_ = langtype, calctype = langtype)
            if simdict:
                if scltype != CalcType.NONE or scalar:
                    return statistics.mean(simdict.values())
                else:
                    return simdict
            else:
                return None
        else:
            return None
    
    @staticmethod
    def sim_scalar(sims: tuple,
                   n1: int,
                   n2: int,
                   scltype: CalcType = CalcType.MEAN
                   ): # -> number
        """
        Translate a tuple of similarities to a number.

        'sims': A tuple of similarities between elements1 and elements2.
        
        'scltype': CalcType.MEAN or CalcType.MAX.
            'max' and 'mean' are available for backward compatibility, but will be discontinued.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-07-13
        """
        
        if scltype == CalcType.MEAN or scltype == 'mean':
            return statistics.mean(sims)
#            return Number.simple(sum(sims) * 2 / (n1 + n2))
        elif scltype == CalcType.MAX or scltype == 'max':
            return max(sims)
        else:
            print("Unknown scltype = '{}'".format(scltype))
            return None

    @staticmethod
    def word_col_sim(col1: Collection, # of Words
                     col2: Collection, # of Words 
                     meaning_id: str,
                     wsimexp = 1,
                     wsimtype: CalcType = CalcType.MAX_COMBI,
                     msimtype: CalcType = CalcType.MAX,
                     emptysim = 1,
                     scalar: str = None, # To be discontinued.
                     scltype: CalcType = CalcType.NONE,
                     colsim: CalcType = CalcType.ONE_TO_ONE,
                     pairs: bool = False
                     ): # -> tuple or number
        """
        Calculate similarity between Word Collections.
        
        def word_col_sim(col1: Collection, # of Words
                         col2: Collection, # of Words 
                         meaning_id: str,
                         wsimexp = 1,
                         wsimtype: CalcType = CalcType.MAX_COMBI,
                         msimtype: CalcType = CalcType.MAX,
                         emptysim = 1,
                         scalar: str = None, # To be discontinued.
                         scltype: CalcType = CalcType.NONE,
                         colsim: CalcType = CalcType.ONE_TO_ONE,
                         pairs: bool = False
                         ): # -> tuple or number

            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            colsim:
                CalcType.ONE_TO_MANY:
                CalcType.ONE_TO_ONE:

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda x, y: Similarity.word_sim(x,
                                                                                  y,
                                                                                  meaning_id,
                                                                                  wsimexp = wsimexp,
                                                                                  wsimtype = wsimtype,
                                                                                  msimtype = msimtype)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)

    @staticmethod
    def word_sim(w1: Word,
                 w2: Word,
                 meaning_id: str,
                 wsimexp = 1,
                 wsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                 msimtype: CalcType = CalcType.MAX
                 ) -> float:
        """
        Calculate similarity between two Words.

        def word_sim(w1: Word,
                     w2: Word,
                     meaning_id: str,
                     wsimexp = 1,
                     wsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                     msimtype: CalcType = CalcType.MAX
                     ) -> float:

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
            CalcType.MEAN_MAX_1_TO_M:
            The default is CalcType.MEAN_MAX_1_TO_M.
        msimtype : CalcType, optional
            CalcType.MAX:
            CalcType.MEAN:
            CalcType.MIN:
            The default is CalcType.MAX.

        Returns
        -------
        float
            0 <= Similarity <= 1

        @author: MURAKAMI Tamotsu
        @date: 2021-07-17
        """
        
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
                if wsimtype == CalcType.MAX_COMBI or wsimtype == 'MAX_COMBI' or wsimtype == 'comb_max': # 後者2つは廃止予定。
                    return Similarity.word_sim_by_max_combi(meaning_set1, meaning_set2, meaning_id, wsimexp=wsimexp)
                elif wsimtype == CalcType.MEAN_COMBI or wsimtype == 'MEAN_COMBI' or wsimtype == 'comb_mean': # 後者は廃止予定。
                    return Similarity.word_sim_by_mean_combi(meaning_set1, meaning_set2, meaning_id, wsimexp=wsimexp)
                elif wsimtype == CalcType.MEAN_MAX_1_TO_M:
                    return Similarity.word_sim_by_mean_max_one_to_many(meaning_set1, meaning_set2, meaning_id, wsimexp=wsimexp)
                else:
                    print("Word_sim: unknown similarity type {} for 'wsimtype'.".format(wsimtype))
            else:
                return 0

        elif isinstance(meaning_id, list) or isinstance(meaning_id, set) or isinstance(meaning_id, tuple):
            sims = [Similarity.word_sim(w1, w2, mid, wsimexp=wsimexp, wsimtype=wsimtype) for mid in meaning_id]
            if msimtype == CalcType.MAX:
                return max(sims)
            elif msimtype == CalcType.MEAN:
                return statistics.mean(sims)
            elif msimtype == CalcType.MIN:
                return min(sims)
            else:
                print("Word_sim: unknown similarity type {} for 'msimtype'.".format(msimtype))
                return None

    @staticmethod
    def word_sim_by_max_combi(meaning_set1: Collection,
                              meaning_set2: Collection,
                              meaning_id: str,
                              wsimexp = 1
                              ): # -> number
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-11-14
        """
        
        simmax = 0

        if meaning_id == Edr.ID:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    sim = Concept.similarity_wp_value(m1, m2) ** wsimexp
                    if sim > simmax:
                        simmax = sim
                    if simmax == 1:
                        break
                if simmax == 1:
                    break
        elif meaning_id == WordNet.ID and simmax < 1:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    sim = WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    if sim > simmax:
                        simmax = sim
                    if simmax == 1:
                        break
                if simmax == 1:
                    break
        
        return simmax

    @staticmethod
    def word_sim_by_mean_combi(meaning_set1: Collection,
                               meaning_set2: Collection,
                               meaning_id: str,
                               wsimexp = 1
                               ): # -> number
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-10-14
        """
        
        simsum = 0
        count = 0
        
        if meaning_id == Edr.ID:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    simsum += Concept.similarity_wp_value(m1, m2) ** wsimexp
                    count += 1
        elif meaning_id == WordNet.ID:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    simsum += WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    count += 1
        
        return simsum / count

    @staticmethod
    def word_sim_by_mean_max_one_to_many(meaning_set1: Collection,
                                         meaning_set2: Collection,
                                         meaning_id: str,
                                         wsimexp = 1
                                         ): # -> number
        """
        Mean of maxes.
        
        @author: MURAKAMI Tamotsu
        @date: 2021-07-16
        """
        
        maxdict1 = {m:0 for m in meaning_set1}
        maxdict2 = {m:0 for m in meaning_set2}
        
        if meaning_id == Edr.ID:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    sim = Concept.similarity_wp_value(m1, m2) ** wsimexp
                    maxdict1[m1] = max(maxdict1[m1], sim)
                    maxdict2[m2] = max(maxdict2[m2], sim)
        elif meaning_id == WordNet.ID:
            for m1 in meaning_set1:
                for m2 in meaning_set2:
                    sim = WordNet.similarity_wp_value(m1, m2) ** wsimexp
                    maxdict1[m1] = max(maxdict1[m1], sim)
                    maxdict2[m2] = max(maxdict2[m2], sim)

        return (statistics.mean(maxdict1.values()) + statistics.mean(maxdict2.values())) / 2

    @staticmethod
    def wordlm_col_sim(col1: Collection,
                       col2: Collection,
                       meaning_id: str,
                       lsimtype: CalcType = CalcType.MIN,
                       lang_invalid = 0, # Return value when the result for langtype is invalid.
                       wsimexp = 1,
                       wsimtype: CalcType = CalcType.MAX_COMBI,
                       msimtype: CalcType = CalcType.MAX,
                       emptysim = 1,
                       scalar: bool = False,
                       scltype: CalcType = CalcType.NONE,
                       colsim: CalcType = CalcType.ONE_TO_ONE,
                       pairs: bool = False,
                       langtype = None # Not used
                       ): # -> tuple or number
        """
        Calculate similarity between collections of WordLm's.

        def wordlm_col_sim(col1: Collection,
                           col2: Collection,
                           meaning_id: str,
                           lsimtype: CalcType = CalcType.MIN,
                           lang_invalid = 0, # Return value when the result for langtype is invalid.
                           wsimexp = 1,
                           wsimtype: CalcType = CalcType.MAX_COMBI,
                           msimtype: CalcType = CalcType.MAX,
                           emptysim = 1,
                           scalar: bool = False,
                           scltype: CalcType = CalcType.NONE,
                           colsim: CalcType = CalcType.ONE_TO_ONE,
                           pairs: bool = False,
                           langtype = None # Not used
                           ): # -> tuple or number

            wsimtype:
                CalcType.MAX_COMBI:
                CalcType.MEAN_COMBI:
                CalcType.MEAN_MAX_1_TO_M:

            msimtype:
                CalcType.MAX:
                CalcType.MEAN:
                CalcType.MIN:

            scalar: When it is True, the similarity is returned as a number
                instead of a tuple.

            pairs: When it is False, just similarity is returned.
                When it is True, a tuple
                (similarity, element list1, element list2) is returned.
                The two element lists shows how elements in 'col1' and 'col2'
                are paired, i.e., i-th element of element list1 is paired with
                i-th element of element list2.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.collection_sim(col1,
                                         col2,
                                         simf = (lambda x, y:
                                                 Similarity.wordlm_sim(x,
                                                                       y,
                                                                       meaning_id,
                                                                       lsimtype = lsimtype,
                                                                       lang_invalid = lang_invalid,
                                                                       wsimexp = wsimexp,
                                                                       wsimtype = wsimtype,
                                                                       msimtype = msimtype)),
                                         emptysim = emptysim,
                                         scalar = scalar,
                                         scltype = scltype,
                                         simtype = colsim,
                                         pairs = pairs)

    @staticmethod
    def wordlm_sim(w1: WordLm,
                   w2: WordLm,
                   meaning_id: str,
                   lsimtype: CalcType = CalcType.MIN,
                   lang_invalid = 0, # Return value when the result for langtype is invalid.
                   wsimexp = 1,
                   wsimtype: CalcType = CalcType.MAX_COMBI,
                   msimtype: CalcType = CalcType.MAX,
                   langtype = None # Not used
                   ) -> float:
        """
        Calculate similarity between WordLm's.

        Parameters
        ----------
        w1 : WordLm
        w2 : WordLm
        meaning_id : str
            Specify concept dictionary to calculate similarity.
            WordNet.ID: Calculate similarity by WordNet synsets.
            Edr.ID: Calculate similarity by EDR concept id's.
            (WordNet.ID, Edr.ID): Calculates similarity for each meaning_id and summarize by 'msimtype'.
        lsimtype : CalcType, optional
            Language similarity type.
            CalcType.ENG: 英語の意味の類似度を返す。
            CalcType.JPN: 日本語の意味の類似度を返す。
            CalcType.MAX: 各言語の意味の類似度の最大値を返す。
            CalcType.MEAN: 各言語の意味の類似度の平均を返す。
            CalcType.MIN: 各言語の意味の類似度の最小値を返す。
            The default is CalcType.MIN.
        lang_invalid : TYPE, optional
            The default is 0.
            Return value when the result for langtype is invalid.
        wsimexp : TYPE, optional
            The default is 1.
        wsimtype : CalcType, optional
             Word similarity type.
             CalcType.MAX_COMBI:
             CalcType.MEAN_COMBI:
             CalcType.MEAN_MAX_1_TO_M:
             The default is CalcType.MAX_COMBI.
        msimtype : CalcType, optional
             Meaning similarity type.
             CalcType.MAX:
             CalcType.MEAN:
             CalcType.MIN:
             The default is CalcType.MAX.
        langtype : TYPE, optional
             For backward compatibility. Use lsimtype.

        Returns
        -------
        float
            類似度 s （0 <= s <=1).

        @author: MURAKAMI Tamotsu
        @date: 2020-07-15
        """
        
        return Similarity.langmap_sim(w1,
                                      w2,
                                      simf = (lambda x, y:
                                              Similarity.word_sim(x,
                                                                  y,
                                                                  meaning_id,
                                                                  wsimexp = wsimexp,
                                                                  wsimtype = wsimtype,
                                                                  msimtype = msimtype)),
                                      lsimtype = lsimtype,
                                      invalid = lang_invalid)
   
"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-07-15
"""

if __name__ == '__main__':

    print('* Test start *')
    
    # Library
    from text_lib.meaning import Meaning
    
#    meaning_id = Edr.ID
#    meaning_id = WordNet.ID
    meaning_id = (Edr.ID, WordNet.ID)
    
#    LANGTYPE = 'MAX'
    LANGTYPE = 'MEAN'
#    LANGTYPE = 'MIN'
#    LANGTYPE = 'JPN'
#    LANGTYPE = 'ENG'
    
    WSIMEXP = 2

    Edr.load_simple_dict()
    WordNet.load_synlink_dict()

    # Word
    
    print(Text_.xml_parse_string.__doc__)

    wlm1 = Text_.xml_parse_string('<lm><eng><n>product</n></eng></lm>')
    Meaning.fill_meaning(wlm1, meaning_id)

    wlm2 = Text_.xml_parse_string('<lm><eng><v>display</v></eng></lm>')
    Meaning.fill_meaning(wlm2, meaning_id)
    
    wlm3 = Text_.xml_parse_string('<lm><eng><n>photograph</n></eng></lm>')
    Meaning.fill_meaning(wlm3, meaning_id)

    wlm4 = Text_.xml_parse_string('<lm><eng><n>illustration</n></eng></lm>')
    Meaning.fill_meaning(wlm4, meaning_id)
    
    msimtype = CalcType.MEAN

    wordlms = (wlm1, wlm2, wlm3, wlm4)
    n = len(wordlms)
    for i in range(n):
        w1 = wordlms[i]
        for j in range(i + 1, n):
            w2 = wordlms[j]
            sims = []
            for wsimtype in (CalcType.MAX_COMBI, CalcType.MEAN_MAX_1_TO_M, CalcType.MEAN_COMBI):
                sims.append(Similarity.wordlm_sim(w1, w2, meaning_id, wsimtype = wsimtype, msimtype = msimtype))
            print('{}, {}: {}'.format(w1.get_text(), w2.get_text(), sims))

#    wordlm1_1 = Text_.xml_parse_string('<lm><eng><aj>red</aj></eng><jpn><aj>赤い</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm1_1, meaning_id)
#
#    wordlm1_2 = Text_.xml_parse_string('<lm><eng><aj>big</aj></eng><jpn><aj>大きい</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm1_2, meaning_id)
#
#    wordlm1_3 = Text_.xml_parse_string('<lm><eng><aj>heavy</aj></eng><jpn><aj>重い</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm1_3, meaning_id)
#
#    wordlm1_4 = Text_.xml_parse_string('<lm><eng><n>automobile</n></eng><jpn><n>自動車</n></jpn></lm>')
#    Meaning.fill_meaning(wordlm1_4, meaning_id)
#
#    wordlm2_1 = Text_.xml_parse_string('<lm><eng><aj>light</aj></eng><jpn><aj>軽い</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm2_1, meaning_id)
#
#    wordlm2_2 = Text_.xml_parse_string('<lm><eng><n>car</n></eng><jpn><n>車</n></jpn></lm>')
#    Meaning.fill_meaning(wordlm2_2, meaning_id)
#    
#    wordlm2_3 = Text_.xml_parse_string('<lm><eng><aj>white</aj></eng><jpn><aj>白い</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm2_3, meaning_id)
#
#    wordlm2_4 = Text_.xml_parse_string('<lm><eng><aj>fast</aj></eng><jpn><aj>速い</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm2_4, meaning_id)
#
#    wordlm2_5 = Text_.xml_parse_string('<lm><eng><aj>small</aj></eng><jpn><aj>小さい</aj></jpn></lm>')
#    Meaning.fill_meaning(wordlm2_5, meaning_id)
    
    """
    ['赤い', '大きい', '重い', '自動車']
    と
    ['軽い', '車', '白い', '速い', '小さい']
    の類似度を計算すると、後者を
    ['白い', '小さい', '軽い', '車']
    の順に前者に対応させた場合に、類似度の合計が最大になることが求まる。
    """

#    start = Time_.time_now()
#    sim = Similarity.wordlm_col_sim([wordlm1_1, wordlm1_2, wordlm1_3, wordlm1_4],
#                                    [wordlm2_1, wordlm2_2, wordlm2_3, wordlm2_4, wordlm2_5],
#                                    meaning_id,
#                                    colsim = CalcType.ONE_TO_MANY, # 2020-03-27
#                                    pairs = True)
#    time = Time_.time_now(start)
#    print('sim=', sim)
#    print('time=', time)
#    print()

    """
    print(Word.__doc__)
    print(Text_.xml_parse_string.__doc__)
    print(Meaning.fill_meaning.__doc__)
    
    words_out = []
    word1 = Text_.xml_parse_string('<jpn><n>自動車</n></jpn>', words_out)
    print('word1 = ', word1)
    print('words_out = ', words_out)
    Meaning.fill_meaning(word1, meaning_id)
    print('word1 = ', word1)
    print('words_out = ', words_out)
    print('synsets = ', word1.meaning[WordNet.ID])
    print("concept id's = ", word1.meaning[Edr.ID])
    
    words_out = []
    word2 = Text_.xml_parse_string('<jpn><n>車</n></jpn>', words_out)
    Meaning.fill_meaning(word2, meaning_id)
    print('word2 = ', word2)
    print('words_out = ', words_out)
    
    words_out = []
    word3 = Text_.xml_parse_string('<jpn><n>車輪</n></jpn>', words_out)
    Meaning.fill_meaning(word3, meaning_id)
    print('word3 = ', word3)
    print('words_out = ', words_out)
    
    sim1 = Similarity.word_sim(word2, word3, WordNet.ID)
    sim2 = Similarity.word_sim(word2, word3, Edr.ID)
    sim3 = Similarity.word_sim(word2, word3, (WordNet.ID, Edr.ID))
    print('sim = ', [sim1, sim2, sim3])

    # Phrase
    
    words_out = []
    phrase1 = Text_.xml_parse_string('<jpn><np><m><aj>白い</aj></m><n>自動車</n></np></jpn>', words_out)
    Meaning.fill_meaning(phrase1, meaning_id)
    print('phrase1 = ', phrase1)
    print('words_out = ', words_out)
    
    words_out = []
    phrase2 = Text_.xml_parse_string('<jpn><np><m><aj>白い</aj></m><n>馬</n></np></jpn>', words_out)
    Meaning.fill_meaning(phrase2, meaning_id)
    print('phrase2 = ', phrase2)
    print('words_out = ', words_out)
    
    words_out = []
    phrase3 = Text_.xml_parse_string('<jpn><np><m><aj>赤い</aj></m><n>自動車</n></np></jpn>', words_out)
    Meaning.fill_meaning(phrase3, meaning_id)
    print('phrase3 = ', phrase3)
    print('words_out = ', words_out)

    sim1 = Similarity.phrase_sim(word1, phrase1, meaning_id, empty_mod=0)
    sim2 = Similarity.phrase_sim(word1, phrase1, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phrase_sim(phrase1, phrase2, meaning_id, empty_mod=0)
    sim2 = Similarity.phrase_sim(phrase1, phrase2, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phrase_sim(phrase1, phrase3, meaning_id, empty_mod=0)
    sim2 = Similarity.phrase_sim(phrase1, phrase3, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phrase_sim(phrase2, phrase3, meaning_id, empty_mod=0)
    sim2 = Similarity.phrase_sim(phrase2, phrase3, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    col1 = (word1, word2)
    col2 = (word2, word3)
    
    sim1 = Similarity.word_col_sim(col1, col2, meaning_id, scalar=True, pairs=False)
    print('sim1 = ', sim1)
    sim2 = Similarity.word_col_sim(col1, col2, meaning_id, scalar=True, pairs=True)
    print('sim2 = ', sim2)
    sim3 = Similarity.word_col_sim(col1, col2, meaning_id, scalar=False, pairs=False)
    print('sim3 = ', sim3)
    sim4 = Similarity.word_col_sim(col1, col2, meaning_id, scalar=False, pairs=True)
    print('sim4 = ', sim4)

    col1 = (phrase1, phrase2)
    col2 = (phrase3, word1)
    
    sim1 = Similarity.phrase_col_sim(col1, col2, meaning_id, scalar=True, pairs=False)
    print('sim1 = ', sim1)
    sim2 = Similarity.phrase_col_sim(col1, col2, meaning_id, scalar=True, pairs=True)
    print('sim2 = ', sim2)
    sim3 = Similarity.phrase_col_sim(col1, col2, meaning_id, scalar=False, pairs=False)
    print('sim3 = ', sim3)
    sim4 = Similarity.phrase_col_sim(col1, col2, meaning_id, scalar=False, pairs=True)
    print('sim4 = ', sim4)
    
    
    words_out = []
    wordlm3 = Text_.xml_parse_string('<lm><eng><n>bike</n></eng><jpn><n>バイク</n></jpn></lm>', words_out)
    Meaning.fill_meaning(wordlm3, meaning_id)
    print('wordlm3 = ', wordlm3)
    print('words_out = ', words_out)
    
    sim1 = Similarity.wordlm_sim(wordlm1, wordlm2, meaning_id)
    sim2 = Similarity.wordlm_sim(wordlm1, wordlm3, meaning_id)
    print('sim = ', [sim1, sim2])

    words_out = []
    phraselm1 = Text_.xml_parse_string('<lm><eng><np><m><aj>white</aj></m><n>automobile</n></np></eng><jpn><np><m><aj>白い</aj></m><n>自動車</n></np></jpn></lm>', words_out)
    Meaning.fill_meaning(phraselm1, meaning_id)
    print('phraselm1 = ', phraselm1)
    print('words_out = ', words_out)
    
    words_out = []
    phraselm2 = Text_.xml_parse_string('<lm><eng><np><m><aj>white</aj></m><n>horse</n></np></eng><jpn><np><m><aj>白い</aj></m><n>馬</n></np></jpn></lm>', words_out)
    Meaning.fill_meaning(phraselm2, meaning_id)
    print('phraselm2 = ', phraselm2)
    print('words_out = ', words_out)
    
    words_out = []
    phraselm3 = Text_.xml_parse_string('<lm><eng><np><m><aj>red</aj></m><n>automobile</n></np></eng><jpn><np><m><aj>赤い</aj></m><n>自動車</n></np></jpn></lm>', words_out)
    Meaning.fill_meaning(phraselm3, meaning_id)
    print('phraselm3 = ', phraselm3)
    print('words_out = ', words_out)

    sim1 = Similarity.phraselm_sim(wordlm1, phraselm1, meaning_id, empty_mod=0)
    sim2 = Similarity.phraselm_sim(wordlm1, phraselm1, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phraselm_sim(phraselm1, phraselm2, meaning_id, empty_mod=0)
    sim2 = Similarity.phraselm_sim(phraselm1, phraselm2, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phraselm_sim(phraselm1, phraselm3, meaning_id, empty_mod=0)
    sim2 = Similarity.phraselm_sim(phraselm1, phraselm3, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.phraselm_sim(phraselm2, phraselm3, meaning_id, empty_mod=0)
    sim2 = Similarity.phraselm_sim(phraselm2, phraselm3, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])

    col1 = (wordlm1, wordlm2)
    col2 = (wordlm2, wordlm3)
    
    sim1 = Similarity.wordlm_col_sim(col1, col2, meaning_id, scalar=True, pairs=False)
    print('sim1 = ', sim1)
    sim2 = Similarity.wordlm_col_sim(col1, col2, meaning_id, scalar=True, pairs=True)
    print('sim2 = ', sim2)
    sim3 = Similarity.wordlm_col_sim(col1, col2, meaning_id, scalar=False, pairs=False)
    print('sim3 = ', sim3)
    sim4 = Similarity.wordlm_col_sim(col1, col2, meaning_id, scalar=False, pairs=True)
    print('sim4 = ', sim4)

    col1 = (phraselm1, phraselm2)
    col2 = (phraselm3, wordlm1)
    
    sim1 = Similarity.phraselm_col_sim(col1, col2, meaning_id, scalar=True, pairs=False)
    print('sim1 = ', sim1)
    sim2 = Similarity.phraselm_col_sim(col1, col2, meaning_id, scalar=True, pairs=True)
    print('sim2 = ', sim2)
    sim3 = Similarity.phraselm_col_sim(col1, col2, meaning_id, scalar=False, pairs=False)
    print('sim3 = ', sim3)
    sim4 = Similarity.phraselm_col_sim(col1, col2, meaning_id, scalar=False, pairs=True)
    print('sim4 = ', sim4)
    
    sen1 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s>が<v><v>走る</v></v>。</sen></jpn>', words_out)
    Meaning.fill_meaning(sen1, meaning_id)
    print('sen1 = ', sen1)
    print('words_out = ', words_out)
    
    words_out = []
    sen2 = Text_.xml_parse_string('<jpn><sen><s><n>自動車</n></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn>', words_out)
    Meaning.fill_meaning(sen2, meaning_id)
    print('sen2 = ', sen2)
    print('words_out = ', words_out)
    
    words_out = []
    sen3 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s>が<v><v>走る</v></v>。</sen></jpn>', words_out)
    Meaning.fill_meaning(sen3, meaning_id)
    print('sen3 = ', sen3)
    print('words_out = ', words_out)
    
    words_out = []
    sen4 = Text_.xml_parse_string('<jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn>', words_out)
    Meaning.fill_meaning(sen4, meaning_id)
    print('sen4 = ', sen4)
    print('words_out = ', words_out)
    
    sim1 = Similarity.sentence_sim(sen1, sen2, meaning_id, pattern=True, empty_adv=0)
    sim2 = Similarity.sentence_sim(sen1, sen2, meaning_id, pattern=True, empty_adv=None)
    sim3 = Similarity.sentence_sim(sen1, sen2, meaning_id, pattern=False, empty_adv=0)
    sim4 = Similarity.sentence_sim(sen1, sen2, meaning_id, pattern=False, empty_adv=None)
    print('sim = ', [sim1, sim2, sim3, sim4])
    
    sim1 = Similarity.sentence_sim(sen1, sen3, meaning_id, empty_mod=0)
    sim2 = Similarity.sentence_sim(sen1, sen3, meaning_id, empty_mod=None)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.sentence_sim(sen1, sen4, meaning_id, pattern=False, empty_mod=0)
    sim2 = Similarity.sentence_sim(sen1, sen4, meaning_id, pattern=False, empty_mod=None, empty_adv=None)
    sim3 = Similarity.sentence_sim(sen1, sen4, meaning_id, pattern=False, scalar=True, empty_mod=0)
    print('sim = ', [sim1, sim2, sim3])
    
    words_out = []
    senlm1 = Text_.xml_parse_string('<lm><eng><sen>An <s><n>automobile</n></s> <v><v>run</v></v>.</sen></eng><jpn><sen><s><n>自動車</n></s>が<v><v>走る</v></v>。</sen></jpn></lm>', words_out)
    Meaning.fill_meaning(senlm1, meaning_id)
    print('senlm1 = ', senlm1)
    print('words_out = ', words_out)
    
    words_out = []
    senlm2 = Text_.xml_parse_string('<lm><eng><sen>An <s><n>automobile</n></s> <v><v>run</v></v> <a><av>fast</av></a>.</sen></eng><jpn><sen><s><n>自動車</n></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn></lm>', words_out)
    Meaning.fill_meaning(senlm2, meaning_id)
    print('senlm2 = ', senlm2)
    print('words_out = ', words_out)
    
    words_out = []
    senlm3 = Text_.xml_parse_string('<lm><eng><sen>A <s><np><m><aj>red</aj></m> <n>automobile</n></np></s> <v><v>run</v></v>.</sen></eng><jpn><sen><s><np><m><aj>赤い</aj></m><n>自動車</n></np></s>が<v><v>走る</v></v>。</sen></jpn></lm>', words_out)
    Meaning.fill_meaning(senlm3, meaning_id)
    print('senlm3 = ', senlm3)
    print('words_out = ', words_out)
    
    words_out = []
    senlm4 = Text_.xml_parse_string('<lm><eng><sen>A <s><np><m><aj>white</aj></m> <n>automobile</n></np></s> <v><v>run</v></v> <a><av>fast</av></a>.</sen></eng><jpn><sen><s><np><m><aj>白い</aj></m><n>自動車</n></np></s>が<a><av>速く</av></a><v><v>走る</v></v>。</sen></jpn></lm>', words_out)
    Meaning.fill_meaning(senlm4, meaning_id)
    print('senlm4 = ', senlm4)
    print('words_out = ', words_out)
    
    sim1 = Similarity.sentencelm_sim(senlm1, senlm2, meaning_id, pattern=True)
    sim2 = Similarity.sentencelm_sim(senlm1, senlm2, meaning_id, pattern=False)
    print('sim = ', [sim1, sim2])
    
    sim1 = Similarity.sentencelm_sim(senlm1, senlm3, meaning_id)
    print('sim = ', [sim1])
    
    sim1 = Similarity.sentencelm_sim(senlm1, senlm4, meaning_id, pattern=False)
    sim2 = Similarity.sentencelm_sim(senlm1, senlm4, meaning_id, pattern=False, scalar=True, empty_mod=0)
    print('sim = ', [sim1, sim2])
    
    col1 = [sen1, sen2]
    col2 = [sen3, sen4]

    sim1 = Similarity.sentence_col_sim(col1, col2, meaning_id, pattern=False)
    sim2 = Similarity.sentence_col_sim(col1, col2, meaning_id, pattern=False, scalar=True)
    print('sim = ', [sim1, sim2])
    
    col1 = [senlm1, senlm2]
    col2 = [senlm3, senlm4]

    sim1 = Similarity.sentencelm_col_sim(col1, col2, meaning_id, pattern=False, empty_mod=0)
    sim2 = Similarity.sentencelm_col_sim(col1, col2, meaning_id, pattern=False, empty_mod=None, empty_adv=None)
    sim3 = Similarity.sentencelm_col_sim(col1, col2, meaning_id, pattern=False, scalar=True, empty_mod=0)
    print('sim = ', [sim1, sim2, sim3])

    """

#    words_out = []
#    word4 = Text_.xml_parse_string('<jpn><v>記録する</v></jpn>', words_out)
#    Meaning.fill_meaning(word4, meaning_id)
#    print('word4 = ', word4)
#    print('words_out = ', words_out)
#    
#    words_out = []
#    word5 = Text_.xml_parse_string('<jpn><v>冷やす</v></jpn>', words_out)
#    Meaning.fill_meaning(word5, meaning_id)
#    print('word5 = ', word5)
#    print('words_out = ', words_out)
#    
#    sim1 = Similarity.word_sim(word4, word5, WordNet.ID, wsimexp=WSIMEXP, wsimtype=CalcType.MEAN_MAX_1_TO_M) # 2020-03-27
#    sim2 = Similarity.word_sim(word4, word5, Edr.ID, wsimexp=WSIMEXP, wsimtype=CalcType.MEAN_MAX_1_TO_M) # 2020-03-27
#    sim3 = Similarity.word_sim(word4, word5, (WordNet.ID, Edr.ID), wsimexp=WSIMEXP, wsimtype=CalcType.MEAN_MAX_1_TO_M) # 2020-03-27
#    print('sim = ', [sim1, sim2, sim3])
#
#    words_out = []
#    senlm5 = Text_.xml_parse_string('<lm><eng><sen><v><v>record</v></v>a<o><n>photograph</n></o>.</sen></eng><jpn><sen><o><n>写真</n></o>を<v><v>記録する</v></v>。</sen></jpn></lm>', words_out)
#    Meaning.fill_meaning(senlm5, meaning_id)
#    print('senlm5 = ', senlm5)
#    print('words_out = ', words_out)
#    
#    words_out = []
#    senlm6 = Text_.xml_parse_string('<lm><eng><sen><v><v>cool</v></v><o><n>food</n>and<n>drink</n></o>.</sen></eng><jpn><sen><o><n>食材</n>や<n>飲料</n></o>を<v><v>冷やす</v></v>。</sen></jpn></lm>', words_out)
#    Meaning.fill_meaning(senlm6, meaning_id)
#    print('senlm6 = ', senlm6)
#    print('words_out = ', words_out)
#    
#    sim1 = Similarity.sentencelm_sim(senlm5, senlm6, meaning_id, langtype=LANGTYPE, wsimexp=WSIMEXP, pattern=False)
#    sim2 = Similarity.sentencelm_sim(senlm5, senlm6, meaning_id, langtype=LANGTYPE, wsimexp=WSIMEXP, pattern=False, scalar=True)
#    print('sim = ', [sim1, sim2])
#
#    words_out = []
#    senlm7 = Text_.xml_parse_string('<lm><eng><sen><v><v>keep</v></v>a<o><n>scene</n></o>.</sen></eng><jpn><sen><o><n>光景</n></o>を<v><v>保存する</v></v>。</sen></jpn></lm>', words_out)
#    Meaning.fill_meaning(senlm7, meaning_id)
#    print('senlm7 = ', senlm7)
#    print('words_out = ', words_out)
#    
#    words_out = []
#    senlm8 = Text_.xml_parse_string('<lm><eng><sen><v><v>worry</v></v>about<o><np><m><n>film</n></m><n>consumption</n></np></o>.</sen></eng><jpn><sen><o><np><m><n>フィルム</n></m><n eng="consumption">消費</n></np></o>を<v><v>心配する</v></v>。</sen></jpn></lm>', words_out)
#    Meaning.fill_meaning(senlm8, meaning_id)
#    print('senlm8 = ', senlm8)
#    print('words_out = ', words_out)
#    
#    words_out = []
#    senlm9 = Text_.xml_parse_string('<lm><eng><sen><v><v>keep</v></v><o><n>food</n></o><c><aj>fresh</aj></c>.</sen></eng><jpn><sen><o><n>食材</n></o>を<c><aj jpn="新鮮だ">新鮮</aj>に</c><v><v>保つ</v></v>。</sen></jpn></lm>', words_out)
#    Meaning.fill_meaning(senlm9, meaning_id)
#    print('senlm9 = ', senlm9)
#    print('words_out = ', words_out)
#    
#    sim1 = Similarity.sentencelm_sim(senlm7, senlm9, meaning_id, langtype=LANGTYPE, wsimexp=WSIMEXP, pattern=False)
#    sim2 = Similarity.sentencelm_sim(senlm7, senlm9, meaning_id, langtype=LANGTYPE, wsimexp=WSIMEXP, pattern=False, scalar=True)
#    print('sim = ', [sim1, sim2])

    print('* Test end *')
    
# End of file