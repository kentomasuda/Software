# -*- coding: utf-8 -*-
"""
Sentence Transformers

https://www.sbert.net/
https://nikkie-ftnext.hatenablog.com/entry/sentence-transformers-embeddings-introduction-en-ja

@author: MURAKAMI Tamotsu
@date: 2024-06-20
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from sentence_transformers import SentenceTransformer
from typing import Union

# Library
from math_srclib.numpy_ import NumPy_

class SentenceTransformers_:
    """
    @author: MURAKAMI Tamotsu
    @date: 2024-05-22
    """
    
    _model = None
    
    _cache = {}

    @staticmethod
    def calc_sim(s1: str,
                 s2: str,
                 cached: bool = False) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-06-02
        """
        
        if cached:
            if s1 in SentenceTransformers_._cache:
                # print('SentenceTransformers: "{}" hits cache.'.format(s1))
                embedding1 = SentenceTransformers_._cache[s1]
            else:
                embedding1 = None
                
            if s2 in SentenceTransformers_._cache:
                # print('SentenceTransformers: "{}" hits cache.'.format(s2))
                embedding2 = SentenceTransformers_._cache[s2]
            else:
                embedding2 = None
            
            if embedding1 is None:
                if embedding2 is None:
                    SentenceTransformers_.ensure_loaded()
                    embedding1, embedding2 = SentenceTransformers_._model.encode([s1, s2], convert_to_numpy=True)
                    SentenceTransformers_._cache[s1] = embedding1
                    SentenceTransformers_._cache[s2] = embedding2
                else:
                    SentenceTransformers_.ensure_loaded()
                    embedding1 = SentenceTransformers_._model.encode(s1, convert_to_numpy=True)
                    SentenceTransformers_._cache[s1] = embedding1

            elif embedding2 is None:
                SentenceTransformers_.ensure_loaded()
                embedding2 = SentenceTransformers_._model.encode(s2, convert_to_numpy=True)
                SentenceTransformers_._cache[s2] = embedding2

        else:
            SentenceTransformers_.ensure_loaded()
            embedding1, embedding2 = SentenceTransformers_._model.encode([s1, s2], convert_to_numpy=True)
        
        # print(s1, embedding1)
        # print(s2, embedding2)

        return NumPy_.cos_sim(embedding1, embedding2)

    @staticmethod
    def calc_texts_sims(texts1: Union[list, tuple],
                        texts2: Union[list, tuple],
                        cache: bool = False) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-06-20
        """

        simmaxs1 = [0] * len(texts1)
        simmaxs2 = [0] * len(texts2)
        
        i1 = 0
        for text1 in texts1:
            i2 = 0
            for text2 in texts2:
                sim = SentenceTransformers_.calc_sim(text1, text2, cached=cache)

                if sim > simmaxs1[i1]:
                    simmaxs1[i1] = sim
                    
                if sim > simmaxs2[i2]:
                    simmaxs2[i2] = sim
                
                i2 += 1
            i1 += 1

        
        return (simmaxs1, simmaxs2)

    @staticmethod
    def ensure_loaded():
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-04-10
        """
        
        if SentenceTransformers_._model is None:
            SentenceTransformers_._model = SentenceTransformer("stsb-xlm-r-multilingual")


"""
Test

@author: MURAKAMI Tamotsu
@date: 2024-04-10
"""

if __name__ == '__main__':

    print('* Test starts *')
    
    texts1 = ["Hello world", "Goodbye world"]
    texts2 = ["Hello there", "Goodbye there"]
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    print(sims)

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
    
    n = len(sentences)
    
    for i in range(n):
        for j in range(i + 1, n):
            sim = SentenceTransformers_.calc_sim(sentences[i], sentences[j])
            print((sim, sentences[i], sentences[j]))

    print('* Test ends *')
    
# End of file