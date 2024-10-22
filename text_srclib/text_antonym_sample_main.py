# -*- coding: utf-8 -*-
"""
Text antonym sample

@author: MURAKAMI Tamotsu
@date: 2020-09-22
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from typing import Collection

# Library
from edr_lib.concept import Concept
from edr_lib.edr import Edr
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from wordnet_lib.wordnet import WordNet
from wordnet_lib.wnlink import WnLink

class Method:
    """
    @author: MURAKAMI Tamotsu
    @date: 2020-09-22
    """
    
    @staticmethod
    def print_antonymous_conceptid_words(conceptids1: Collection,
                                         conceptids2: Collection
                                         ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-09-22
        """
        
        antonymous_pairs = set()
        
        for conceptid1 in conceptids1:
            for conceptid2 in conceptids2:
                sim, lcsset = Concept.similarity_wp_value(conceptid1, conceptid2, lcs = True)
                antonymous_pairs.add((sim,
                                      conceptid1,
                                      Edr.conceptid_headwords(conceptid1, lang = Lang.JPN | Lang.ENG, langinfo = False),
                                      conceptid2,
                                      Edr.conceptid_headwords(conceptid2, lang = Lang.JPN | Lang.ENG, langinfo = False),
                                      lcsset,
                                      tuple(Concept.concept_expl(lcs, lang = Lang.JPN | Lang.ENG) for lcs in lcsset)))
        """
        対立する概念識別子の組合せのバリエーションを、類似度が高い順にプリントする。
        高い類似度は、概念階層の低い（頂点のrootからのステップ数が大きい）ところでつながる組合せであるので、
        比較に妥当性があり（文脈が近い）、発想が出やすい可能性がある。
        """
        for sim, cid1, words1, cid2, words2, lcsset, lcsexpl in sorted(antonymous_pairs, reverse = True):
            print('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(sim, cid1, words1, cid2, words2, lcsset, lcsexpl))

#    @staticmethod
#    def print_linked_synset_lemmas(synsets: Collection,
#                                   link: WnLink = WnLink.ALL
#                                   ):
#        """
#        まだ使用していない。
#        
#        @author: MURAKAMI Tamotsu
#        @date: 2020-09-22
#        """
#
#        prev_synsets = synsets
#        old_lemmas = set()
#        for synset in prev_synsets:
#            old_lemmas |= WordNet.synset_lemmas(synset, lang = Lang.JPN | Lang.ENG)
#        print('0:', sorted(old_lemmas))
#        
#        if isinstance(prev_synsets, set):
#            old_synsets = prev_synsets
#        else:
#            old_synsets = set(prev_synsets)
#
#        for step in range(3):
#            new_synsets = set()
#            for synset in prev_synsets:
#                new_synsets |= (WordNet.linked_synsets(synset, link = link, linkinfo = False) - old_synsets)
#            if new_synsets:
#                lemmas = set()
#                for synset in new_synsets:
#                    lemmas |= WordNet.synset_lemmas(synset, lang = Lang.JPN | Lang.ENG)
#                new_lemmas = lemmas - old_lemmas
#                print('{}: {}'.format(step + 1, sorted(new_lemmas)))
#                prev_synsets = new_synsets
#                old_synsets |= new_synsets
#                old_lemmas |= new_lemmas
#            else:
#                break

"""
Main

@author: MURAKAMI Tamotsu
@date: 2020-09-22
"""

if __name__ == '__main__':

    print('* start *')
    
    meaning_id = Edr.ID
    
    wlm1 = Text_.xml_parse_string('<lm><jpn><aj cid="3cfe13,3cf941">重い</aj></jpn><eng><aj>heavy</aj></eng></lm>')
    Meaning.fill_meaning(wlm1, meaning_id, suggest = sys.stdout)
    print(Meaning.meaning_json_string(wlm1.get_word(Lang.JPN), meaning_id))
    
    wlm2 = Text_.xml_parse_string('<lm><jpn><aj cid="0f2091,1fadb3,3c4bb5,3ce892,0fec83,3ceb74,3cee97">強い</aj></jpn><eng><aj>strong</aj></eng></lm>')
    Meaning.fill_meaning(wlm2, meaning_id, suggest = sys.stdout)
    print(Meaning.meaning_json_string(wlm2.get_word(Lang.JPN), meaning_id))
    
    wlm3 = Text_.xml_parse_string('<lm><jpn><aj cid="3bf881,3cec92">軽い</aj></jpn><eng><aj>light</aj></eng></lm>')
    Meaning.fill_meaning(wlm3, meaning_id, suggest = sys.stdout)
    print(Meaning.meaning_json_string(wlm3.get_word(Lang.JPN), meaning_id))
    
    wlm4 = Text_.xml_parse_string('<lm><jpn><aj cid="3ce670,1ee06a">弱い</aj></jpn><eng><aj>strong</aj></eng></lm>')
    Meaning.fill_meaning(wlm4, meaning_id, suggest = sys.stdout)
    print(Meaning.meaning_json_string(wlm4.get_word(Lang.JPN), meaning_id))
    
    wlm5 = Text_.xml_parse_string('<lm><jpn><aj>美しい</aj></jpn><eng><aj>beautiful</aj></eng></lm>')
    Meaning.fill_meaning(wlm5, meaning_id, suggest = sys.stdout)
    print(Meaning.meaning_json_string(wlm5.get_word(Lang.JPN), meaning_id))

    # "強い" と "軽い"
    conceptids1 = Meaning.meaning(wlm2.get_word(Lang.JPN), meaning_id)
    conceptids2 = Meaning.meaning(wlm3.get_word(Lang.JPN), meaning_id)
    
    Method.print_antonymous_conceptid_words(conceptids1, conceptids2)

print('* end *')

# End of file