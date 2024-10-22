# -*- coding: utf-8 -*-
"""
Sentence Transformers

https://www.sbert.net/
https://nikkie-ftnext.hatenablog.com/entry/sentence-transformers-embeddings-introduction-en-ja

@author: MURAKAMI Tamotsu
@date: 2024-06-20
"""

import sys
import os
from concurrent.futures import ProcessPoolExecutor
from sentence_transformers import SentenceTransformer
from typing import Union, List, Tuple
from concurrent.futures import ThreadPoolExecutor


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
    def calc_sim(s1: str, s2: str, cached: bool = False) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2024-06-02
        """
        
        if cached:
            if s1 in SentenceTransformers_._cache:
                embedding1 = SentenceTransformers_._cache[s1]
            else:
                embedding1 = None
                
            if s2 in SentenceTransformers_._cache:
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
        
        return NumPy_.cos_sim(embedding1, embedding2)

    @staticmethod
    def calc_texts_sims(texts1: List[str], texts2: List[str], cache: bool = False) -> Tuple[List[float], List[float]]:
        simmaxs1 = [0] * len(texts1)
        simmaxs2 = [0] * len(texts2)
    
        SentenceTransformers_.ensure_loaded()  # モデルを一度だけロード
    
        # 並列処理用のスレッドプールを使用
        with ThreadPoolExecutor() as executor:
            embeddings = list(executor.map(lambda x: SentenceTransformers_._model.encode(x, convert_to_numpy=True), [texts1, texts2]))
            
            embedding1, embedding2 = embeddings[0], embeddings[1]
    
            for i1, text1 in enumerate(texts1):
                for i2, text2 in enumerate(texts2):
                    sim = NumPy_.cos_sim(embedding1[i1], embedding2[i2])
                    if sim > simmaxs1[i1]:
                        simmaxs1[i1] = sim
                    if sim > simmaxs2[i2]:
                        simmaxs2[i2] = sim
        
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
テスト

@author: MURAKAMI Tamotsu
@date: 2024-04-10
"""

if __name__ == '__main__':
    print('* テスト開始 *')
    
    texts1 = ["Hello world", "Goodbye world"]
    texts2 = ["Hello there", "Goodbye there"]
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    print(sims)

    sentences = [
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

    print('* テスト終了 *')
