# -*- coding: utf-8 -*-
"""
EDR relation basic sample

@author: MURAKAMI Tamotsu
@date: 2020-12-10
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.concept import Concept
from edr_lib.edr import Edr
from edr_lib.relation import Relation, RelationChain, RelLabel
from text_lib.lang import Lang

"""
Main

@author: MURAKAMI Tamotsu
@date: 2020-12-10
"""

print('* Start *')

print(RelLabel.__doc__)

print(Relation.concept_from_tos_set_by_relation.__doc__)

concept_from_tos_set = Relation.concept_from_tos_set_by_relation(RelLabel.AGENT)
for concept_from_tos in concept_from_tos_set:
    print(concept_from_tos)

cids1 = Edr.headword_conceptid('食べる', lang=Lang.JPN, as_tuple=True)

print(Relation.concept_tos_by_concept_from_and_relation.__doc__)

concept_from = cids1[1]
words_from = Edr.conceptid_headwords(concept_from, lang=Lang.JPN)
if words_from:
    print(words_from, '- object ->')
else:
    print(Concept.concept_expl(concept_from), '- object ->')

concept_tos = Relation.concept_tos_by_concept_from_and_relation(cids1[0], RelLabel.OBJECT)
for concept_to in concept_tos:
    words_to = Edr.conceptid_headwords(concept_to, lang=Lang.JPN)
    if words_to:
        print(words_to)
    else:
        print(Concept.concept_expl(concept_to))

cids2 = Edr.headword_conceptid('りんご', lang=Lang.JPN, as_tuple=True)

print(Relation.relation_between_concepts.__doc__)

print(Relation.relation_between_concepts(cids1[0], cids2[0]))

print(Relation.shortest_relation_chain_step.__doc__)

print(Relation.shortest_relation_chains.__doc__)

for cid1 in cids1:
    for cid2 in cids2:
        print(Relation.shortest_relation_chain_step(cid1, cid2))

print(RelationChain.print_expl.__doc__)

chains = Relation.shortest_relation_chains(cids1[0], cids2[0], num=1, progress=True)

print(chains)

for chain in chains:
    chain.print_expl(lang= Lang.ENG | Lang.JPN)

print('* End *')       

# End of file