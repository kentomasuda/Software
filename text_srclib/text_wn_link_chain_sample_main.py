# -*- coding: utf-8 -*-
"""
Text WordNet link chain basic sample

@author: MURAKAMI Tamotsu
@date: 2020-09-20
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Library
from text_lib.lang import Lang
from text_lib.meaning import Meaning
from text_lib.text import Text_
from wordnet_lib.wordnet import LinkChain
from wordnet_lib.wordnet import WordNet
from wordnet_lib.wnlink import WnLink

print('* start *')

print(Lang.__doc__)

print(WordNet.__doc__)

print(WordNet.check_lemma.__doc__)

meaning_id = WordNet.ID

"""
wlm1 = Text_.xml_parse_string('<lm><jpn><aj syn="01184932-a,01187611-a,01185916-a">重い</aj></jpn><eng><aj>heavy</aj></eng></lm>')
Meaning.fill_meaning(wlm1, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm1.get_word(Lang.JPN), meaning_id))

wlm2 = Text_.xml_parse_string('<lm><jpn><aj syn="02321009-a,02447344-a,02275412-a,02323726-a,01825671-a,01826575-a,01513512-a">強い</aj></jpn><eng><aj>strong</aj></eng></lm>')
Meaning.fill_meaning(wlm2, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm2.get_word(Lang.JPN), meaning_id))

wlm3 = Text_.xml_parse_string('<lm><jpn><n>重いこと</n></jpn><eng><n>heaviness</n></eng></lm>')
Meaning.fill_meaning(wlm3, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm3.get_word(Lang.ENG), meaning_id))

wlm4 = Text_.xml_parse_string('<lm><jpn><n>強いこと</n></jpn><eng><n>strongness</n></eng></lm>')
Meaning.fill_meaning(wlm4, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm4.get_word(Lang.ENG), meaning_id))

wlm5 = Text_.xml_parse_string('<lm><jpn><aj syn="01191876-a,01186733-a,02414188-a,00991678-a,01186408-a">軽い</aj></jpn><eng><aj>light</aj></eng></lm>')
Meaning.fill_meaning(wlm5, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm5.get_word(Lang.JPN), meaning_id))

wlm6 = Text_.xml_parse_string('<lm><jpn><aj syn="00709215-a,02040233-a,02325304-a,02325097-a,02040049-a,02324397-a,01827766-a">弱い</aj></jpn><eng><aj>strong</aj></eng></lm>')
Meaning.fill_meaning(wlm6, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm6.get_word(Lang.JPN), meaning_id))
"""

wlm7 = Text_.xml_parse_string('<lm><jpn><n>軽さ</n></jpn><eng><n>lightness</n></eng></lm>')
Meaning.fill_meaning(wlm7, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm7.get_word(Lang.JPN), meaning_id))

wlm8 = Text_.xml_parse_string('<lm><jpn><n>弱いこと</n></jpn><eng><n>weakness</n></eng></lm>')
Meaning.fill_meaning(wlm8, meaning_id, suggest = sys.stdout)
print(Meaning.meaning_json_string(wlm8.get_word(Lang.ENG), meaning_id))

synsets1 = Meaning.meaning(wlm7.get_word(Lang.JPN), meaning_id)
synsets2 = Meaning.meaning(wlm8.get_word(Lang.ENG), meaning_id)

minstep = None
shortest_chains = set()
for synset1 in synsets1:
    for synset2 in synsets2:
        print('{}, {}'.format(synset1, synset2))
        all_link_step = WordNet.synset_shortest_chain_steps(synset1, synset2)
        if all_link_step > 0:
            #chains = WordNet.synset_shortest_chains(synset1, synset2, link = WnLink.SIM | WnLink.HYPE | WnLink.HYPO | WnLink.ATTR, maxstep = minstep)
            chains = WordNet.synset_shortest_chains_fast(synset1, synset2)
            if chains:
                step = LinkChain.step(chains[0])
                if minstep is None:
                    minstep = step
                    shortest_chains |= set(chains)
                    print('minstep = ', minstep)
                elif step < minstep:
                    minstep = step
                    shortest_chains.clear()
                    shortest_chains |= set(chains)
                    print('minstep = ', minstep)
                elif step == minstep:
                    shortest_chains |= set(chains)

print('final minstep = ', minstep)
print('{} chains'.format(len(shortest_chains)))
for chain in shortest_chains:
    chain.print_(lang = Lang.ENG | Lang.JPN)

print('* end *')

# End of file