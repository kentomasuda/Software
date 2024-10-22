# -*- coding: utf-8 -*-
"""
Sentence Transformers test main

https://nikkie-ftnext.hatenablog.com/entry/sentence-transformers-embeddings-introduction-en-ja

Install:
pip install sentence-transformers

@author: MURAKAMI Tamotsu
@date: 2024-04-10
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

# Library

    
"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-01-24
"""

if __name__ == '__main__':

    print('* Main starts *')

    model = SentenceTransformer("stsb-xlm-r-multilingual")
    
    sentences = [
        # "犬が人間に嚙みついた",
        # "人間が犬に嚙みついた",
        # "人間に犬が嚙みついた",
        # "猫が人間に嚙みついた",
        # "人間が猫に嚙みついた",
        # "Refrigerator cools food",
        # "Refrigerator make food cool",
        # "ユーザが製品を直す",
        # "製品がユーザを癒す",
        # "製品がユーザを治す",
        "赤",
        "青",
        "黒",
        "共産主義",
        "経理",
    ]
    
    embeddings = model.encode(sentences, convert_to_tensor=True)
    
    n = len(embeddings)
    
    for i in range(n):
        sentence_i = sentences[i]
        embedding_i = embeddings[i]
        for j in range(i + 1, n):
            sentence_j = sentences[j]
            embedding_j = embeddings[j]
            sim = util.cos_sim(embedding_i.reshape(1, -1), embedding_j.reshape(1, -1))
            print((sim, sentence_i, sentence_j))

    print('* Main ends *')
    
# End of file