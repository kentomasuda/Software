# -*- coding: utf-8 -*-
"""
Text relation

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
from edr_lib.edr import Edr
from edr_lib.relation import Relation
from math_srclib.calc_type import CalcType
from text_lib.meaning import Meaning
from text_lib.sentence import Sentence, SentenceLm
from text_lib.text import Text_
from text_lib.word_phrase import Word
from text_srclib.similarity import Similarity
from wordnet_lib.wordnet import WordNet

class TextRelation:
    """
    TextRelation (関係度)
    
    @author: MURAKAMI Tamotsu
    @date: 2020-09-12
    """
    
    @staticmethod
    def bag_rel(bag1: Bag,
                bag2: Bag,
                relf: Callable,
                scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                pairs: bool = False
                ) -> tuple:
        """
        Calculate relation between Bags.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-10-18
        """
        
        items1 = bag1.get_elems()
        items2 = bag2.get_elems()
        
        n1 = len(items1)
        n2 = len(items2)

        rels1 = [0] * n1
        rels2 = [0] * n2
        
        others1 = [None] * n1
        others2 = [None] * n2
        
        i1 = 0
        for item1 in items1:
            i2 = 0
            for item2 in items2:
                rel = relf(item1, item2)
                if rel > rels1[i1]:
                    rels1[i1] = rel
                    others1[i1] = item2
                if rel > rels2[i2]:
                    rels2[i2] = rel
                    others2[i2] = item1
                i2 += 1
            i1 += 1
        
        if scltype == CalcType.NONE_MAX_1_TO_M:
            if pairs:
                return (tuple(rels1), tuple(rels2), tuple(others1), tuple(others2))
            else:
                return (tuple(rels1), tuple(rels2))
        elif scltype == CalcType.MEAN_MAX_1_TO_M:
            freqs1 = bag1.get_freqs()
            freqs2 = bag2.get_freqs()
            relsum = sum(tuple(map(lambda rel, freq: rel * freq, rels1, freqs1)))\
                   + sum(tuple(map(lambda rel, freq: rel * freq, rels2, freqs2)))
            relmean = relsum / (sum(freqs1) + sum(freqs2))

            if pairs:
                return (relmean, tuple(others1), tuple(others2))
            else:
                return relmean
        else:
            msg = TextRelation.msg_unknown_val_for_attr_method('Error', scltype.name, 'scltype', 'TextRelation.bag_rel')
            print(msg)
            return None
    
    @staticmethod
    def collection_rel(col1: Collection,
                       col2: Collection,
                       relf: Callable,
                       scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                       pairs: bool = False
                       ): # -> number or tuple
        """
        Calculate relation between Collections.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-09-13
        """
        
        items1 = tuple(col1)
        items2 = tuple(col2)
        
        n1 = len(items1)
        n2 = len(items2)
        n = n1 + n2

        rels1 = [0] * n1
        rels2 = [0] * n2
        
        others1 = [None] * n1
        others2 = [None] * n2
        
        i1 = 0
        for item1 in items1:
            i2 = 0
            for item2 in items2:
                fullinfo = relf(item1, item2)
                if scltype == CalcType.NONE_MAX_1_TO_M:
                    rel = (sum(fullinfo[0]) + sum(fullinfo[1])) / n
                else:
                    if pairs:
                        rel = fullinfo[0]
                    else:
                        rel = fullinfo
                    
                if rel > rels1[i1]:
                    rels1[i1] = rel
                    others1[i1] = item2
                if rel > rels2[i2]:
                    rels2[i2] = rel
                    others2[i2] = item1
                i2 += 1
            i1 += 1
        
        if scltype != CalcType.NONE_MAX_1_TO_M:
            if scltype == CalcType.MAX_MAX_1_TO_M:
                colrel = (max(rels1) + max(rels2)) / 2
            elif scltype == CalcType.MEAN_MAX_1_TO_M:
                colrel = (sum(rels1) + sum(rels2)) / n
            else:
                msg = TextRelation.msg_unknown_val_for_attr_method('Error', scltype.name, 'scltype', 'TextRelation.collection_rel')
                print(msg)
                colrel = None
                
            if pairs:
                return (colrel, items1, tuple(others1), items2, tuple(others2))
            else:
                return colrel
        elif pairs: # scalar == False, pairs == True
            return (tuple(rels1), tuple(rels2), items1, tuple(others1), items2, tuple(others2))
        else: # scalar == False, pairs == False
            return (tuple(rels1), tuple(rels2))
    
    @staticmethod
    def msg_unknown_val_for_attr_method(msgtyp: str,
                                        val: str,
                                        attr: str,
                                        method: str
                                        ) -> str:
        """
        Message string.
        
        @author: MURAKAMI Tamotsu
        @date: 2020-09-13
        """
        
        return "\n{}: unknown '{}' for '{}' in '{}'.".format(msgtyp, val, attr, method)

    @staticmethod
    def sentence_rel_by_bow(sen1: Sentence,
                            sen2: Sentence,
                            meaning_id: str,
                            wrelf: Callable,
                            scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                            pairs: bool = False
                            ) -> float:
        """
        Calculate relation between two Sentences by bag-of-words.

        def sentence_rel_by_bow(sen1: Sentence,
                                sen2: Sentence,
                                meaning_id: str,
                                wrelf: Callable,
                                scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                                pairs: bool = False
                                ) -> float:

            sen1: Sentence instance.

            sen2: Sentence instance.

            meaning_id: Concept library to calculate relation.
                Edr.ID: Edr is used.
                (Edr.ID, WordNet.ID): Only Edr is used.

            wrelf: A function to calculate relation between two Words such as follows.
                lambda w1, w2:
                    TextRelation.word_rel(w1,
                                          w2,
                                          meaning_id = Edr.ID,
                                          wreltype = CalcType.MAX_MAX_1_TO_M)

            scltype: Obtain relation in what type of value.
                CalcType.MEAN_MAX_1_TO_M: Scalar mean of max values.
                CalcType.NONE_MAX_1_TO_M: List of max values.
            
            pairs:
                True: Tuple of relation value (scalar or list), items1, others1, items2 and others2 is returned.
                False: Just relation value (scalar or list) is returned.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-13
        """
        
        bag1 = sen1.bag_of_words()
        bag2 = sen2.bag_of_words()
    
        if scltype == CalcType.NONE_MAX_1_TO_M or scltype == CalcType.MEAN_MAX_1_TO_M:
            return TextRelation.bag_rel(bag1, bag2, relf = wrelf, scltype = scltype, pairs = pairs)
        else:
            msg = TextRelation.msg_unknown_val_for_attr_method('Error', scltype.name, 'scltype', 'TextRelation.sentence_rel_by_bow')
            print(msg)
            return None

    @staticmethod
    def sentencelm_col_rel_by_bow(senlms1: Collection,
                                  senlms2: Collection,
                                  meaning_id: str,
                                  wrelf: Callable,
                                  scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                                  pairs: bool = False
                                  ) -> float:
        """
        Calculate relation between two SentenceLm Collections by bag-of-words.

        def sentencelm_col_rel_by_bow(senlms1: Collection,
                                      senlms2: Collection,
                                      meaning_id: str,
                                      wrelf: Callable,
                                      wreltype: CalcType = CalcType.MAX_MAX_1_TO_M,
                                      scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                                      pairs: bool = False
                                      ) -> float:

            senlms1: Collection (tuple, list or set) of SentenceLms.

            senlms2: Collection (tuple, list or set) of SentenceLms.

            meaning_id: Concept library to calculate relation.
                Edr.ID: Edr is used.
                (Edr.ID, WordNet.ID): Only Edr is used.

            wrelf: A function to calculate relation between two Words such as follows.
                lambda w1, w2:
                    TextRelation.word_rel(w1,
                                          w2,
                                          meaning_id = Edr.ID,
                                          wreltype = CalcType.MAX_MAX_1_TO_M)

            scltype: Obtain relation in what type of value.
                CalcType.MAX_MAX_1_TO_M: Scalar max of max values.
                CalcType.MEAN_MAX_1_TO_M: Scalar mean of max values.
                CalcType.NONE_MAX_1_TO_M: List of max values.
            
            pairs:
                True: Tuple of relation value (scalar or list), items1, others1, items2 and others2 is returned.
                False: Just relation value (scalar or list) is returned.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-13
        """
        senlmrelf = lambda senlm1, senlm2:\
            TextRelation.sentencelm_rel_by_bow(
                    senlm1,
                    senlm2,
                    meaning_id = meaning_id,
                    wrelf = wrelf,
                    scltype = CalcType.MEAN_MAX_1_TO_M,
                    pairs = pairs)
        
        return TextRelation.collection_rel(senlms1,
                                           senlms2,
                                           relf = senlmrelf,
                                           scltype = scltype,
                                           pairs = pairs)

    @staticmethod
    def sentencelm_rel_by_bow(senlm1: SentenceLm,
                              senlm2: SentenceLm,
                              meaning_id: str,
                              wrelf: Callable,
                              scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                              pairs: bool = False
                              ) -> float:
        """
        Calculate relation between two SentenceLms by bag-of-words.

        def sentencelm_rel_by_bow(senlm1: SentenceLm,
                                  senlm2: SentenceLm,
                                  meaning_id: str,
                                  wrelf: Callable,
                                  scltype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                                  pairs: bool = False
                                  ) -> float:

            senlm1: SentenceLm.

            senlm2: SentenceLm.

            meaning_id: Concept library to calculate relation.
                Edr.ID: Edr is used.
                (Edr.ID, WordNet.ID): Only Edr is used.

            wrelf: A function to calculate relation between two Words such as follows.
                lambda w1, w2:
                    TextRelation.word_rel(w1,
                                          w2,
                                          meaning_id = Edr.ID,
                                          wreltype = CalcType.MAX_MAX_1_TO_M)

            scltype: Obtain relation in what type of value.
                CalcType.MAX_MAX_1_TO_M: Scalar max of max values.
                CalcType.MEAN_MAX_1_TO_M: Scalar mean of max values.
                CalcType.NONE_MAX_1_TO_M: List of max values.
            
            pairs:
                True: Tuple of relation value (scalar or list), items1, others1, items2 and others2 is returned.
                False: Just relation value (scalar or list) is returned.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-13
        """
        
        relmax = 0
        relinfo = None
        for lang in tuple(set(senlm1.get_langs()) & set(senlm2.get_langs())):
            sen1 = senlm1.get_sen(lang)
            sen2 = senlm2.get_sen(lang)
            fullinfo = TextRelation.sentence_rel_by_bow(sen1,
                                                        sen2,
                                                        meaning_id = meaning_id,
                                                        wrelf = wrelf,
                                                        scltype = scltype,
                                                        pairs = pairs)
            if scltype == CalcType.NONE_MAX_1_TO_M:
                freqs1 = sen1.bag_of_words().get_freqs()
                freqs2 = sen2.bag_of_words().get_freqs()
                relsum = sum(map(lambda rels, freqs: sum(map(lambda rel, freq: rel * freq,
                                                          rels,
                                                          freqs)),
                                 fullinfo[0:1],
                                 (freqs1, freqs2)))
                rel = relsum / (sum(freqs1) + sum(freqs2))
            elif scltype == CalcType.MEAN_MAX_1_TO_M:
                if pairs:
                    rel = fullinfo[0]
                else: # scalar = True, pairs = False 
                    rel = fullinfo
            else:
                msg = TextRelation.msg_unknown_val_for_attr_method('Error', scltype.name, 'scltype', 'TextRelation.sentencelm_rel_by_bow')
                print(msg)
                rel = 0
            
            if rel > relmax:
                relinfo = fullinfo
        
        return relinfo

    @staticmethod
    def step_to_rel(step: int
                   ): # -> number
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-09-12
        """
        
        if step is None:
            return 0
        else:
            return 1 / step

    @staticmethod
    def word_rel(w1: Word,
                 w2: Word,
                 meaning_id: str = Edr.ID,
                 wreltype: CalcType = CalcType.MAX_MAX_1_TO_M
                 ) -> float:
        """
        Calculate relation between two Words.

        def word_rel(w1: Word,
                     w2: Word,
                     meaning_id: str = Edr.ID,
                     wreltype: CalcType = CalcType.MAX_MAX_1_TO_M
                     ) -> float:
            
            w1: Word instance.

            w2: Word instance.

            meaning_id: Concept library to calculate relation.
                Edr.ID: Edr is used.
                (Edr.ID, WordNet.ID): Only Edr is used.

            wreltype: How to calculate ralation between two set of Edr concept ids.
                CalcType.MAX_MAX_1_TO_M: Scalar max of max values.
                CalcType.MEAN_MAX_1_TO_M: Scalar mean of max values.

        @author: MURAKAMI Tamotsu
        @date: 2020-11-14
        """
        
        if meaning_id == Edr.ID or Edr.ID in meaning_id:
            mid = Edr.ID
            cids1 = Meaning.get_meaning(w1, mid)
            cids2 = Meaning.get_meaning(w2, mid)

            rels = []
            for cid1 in cids1:
                for cid2 in cids2:
                    step = Relation.shortest_relation_chain_step(cid1, cid2)
                    rels.append(TextRelation.step_to_rel(step))
            
            if wreltype == CalcType.MAX_MAX_1_TO_M:
                return max(rels)
            elif wreltype == CalcType.MEAN_MAX_1_TO_M:
                return statistics.mean(rels)
            else:
                msg = TextRelation.msg_unknown_val_for_attr_method('Error', wreltype.name, 'wreltype', 'TextRelation.word_rel')
                print(msg)
                return None
        else:
            return None
   
"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-12-01
"""

if __name__ == '__main__':

    print('* Test start *')
    
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

    w1 = Text_.xml_parse_string('<jpn><n>リンゴ</n></jpn>')
    Meaning.fill_meaning(w1, meaning_id, suggest = sys.stdout)

    w2 = Text_.xml_parse_string('<jpn><v>食べる</v></jpn>')
    Meaning.fill_meaning(w2, meaning_id, suggest = sys.stdout)
    
    print(TextRelation.word_rel(w1, w2, meaning_id, wreltype = CalcType.MAX_MAX_1_TO_M))
    
    cids1 = Edr.headword_conceptids(w1.text, simplepos=True)
    cids2 = Edr.headword_conceptids(w2.text, simplepos=True)
    print('cids1 =', cids1)
    print('cids2 =', cids2)
    for cid1 in cids1:
        for cid2 in cids2:
            step = Relation.shortest_relation_chain_step(cid1, cid2)
            print('step({}, {}) = {}'.format(cid1, cid2, step))
            chains = Relation.shortest_relation_chains(cid1, cid2)
            for chain in chains:
                print('chain =', chain)
            rev_chains = Relation.shortest_relation_chains(cid2, cid1)
            for rev_chain in rev_chains:
                print('rev_chain =', rev_chain)

    sen1 = Text_.xml_parse_string('<jpn><sen><o><n>車</n></o><t>に</t><v><v>乗る</v></v><t>。</t></sen></jpn>')
    Meaning.fill_meaning(sen1, meaning_id, suggest = sys.stdout)

    sen2 = Text_.xml_parse_string('<jpn><sen><a><av eng="fast">速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>')
    Meaning.fill_meaning(sen2, meaning_id, suggest = sys.stdout)
    
    bag1 = sen1.bag_of_words()
    bag2 = sen2.bag_of_words()
    
#    bag1 = Bag()
#    bag1.add(w1)
#    
#    bag2 = Bag()
#    bag2.add(w2)
    
    wsimf = lambda w1, w2: Similarity.word_sim(w1, w2, meaning_id = Edr.ID, wsimtype = CalcType.MAX_COMBI)
    
    print(Similarity.bag_sim(bag1, bag2, simf = wsimf, scalar = True, pairs = False))

    wrelf = lambda w1, w2: TextRelation.word_rel(w1, w2, meaning_id = Edr.ID, wreltype = CalcType.MAX_MAX_1_TO_M)
    
    print(TextRelation.sentence_rel_by_bow(sen1, sen2, meaning_id = Edr.ID, wrelf = wrelf, scltype = CalcType.NONE_MAX_1_TO_M, pairs = True))

    senlm1 = Text_.xml_parse_string('<lm><eng><sen><v><v>ride</v></v><o><n>car</n></o><t>.</t></sen></eng><jpn><sen><o><n>車</n></o><t>に</t><v><v>乗る</v></v><t>。</t></sen></jpn></lm>')
    Meaning.fill_meaning(senlm1, meaning_id, suggest = sys.stdout)

    senlm2 = Text_.xml_parse_string('<lm><eng><sen><v><v>run</v></v><a><av>fast</av></a></sen></eng><jpn><sen><a><av eng="fast">速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn></lm>')
    Meaning.fill_meaning(senlm2, meaning_id, suggest = sys.stdout)

    print(TextRelation.sentencelm_rel_by_bow(senlm1, senlm2, meaning_id = Edr.ID, wrelf = wrelf, scltype = CalcType.MEAN_MAX_1_TO_M, pairs = True))

    print(TextRelation.sentencelm_col_rel_by_bow((senlm1, senlm2),
                                                 (senlm2, senlm1),
                                                 meaning_id = Edr.ID,
                                                 wrelf = wrelf,
                                                 scltype = CalcType.MEAN_MAX_1_TO_M,
                                                 pairs = False))

    print('* Test end *')
    
# End of file