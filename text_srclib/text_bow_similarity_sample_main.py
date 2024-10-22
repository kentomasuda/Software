# -*- coding: utf-8 -*-
"""
Text bow similarity sample main

@author: MURAKAMI Tamotsu
@date: 2024-05-01
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import time

# Library
from text_srclib.text_similarity import TextSimilarity

"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-05-01
"""

if __name__ == '__main__':
    
    print('* Main starts *')
    
    print(TextSimilarity.calc_text_bow_sim.__doc__)
    
    texts1 = ['ソリティアはトランプゲームです。', '一人で遊びます。']
    texts2 = ['ババ抜きはトランプゲームです。', '複数で遊びます。']
    texts3 = ['七並べはトランプゲームです。', '複数で遊びます。']

    # 初回のみデータ読み込みに時間がかかるため、正確な時間比較のためにダミー実行。
    _ = TextSimilarity.calc_texts_bow_sim(texts1, texts2, method='EDR+ST')

    start = time.time()

    sim12 = TextSimilarity.calc_texts_bow_sim(texts1, texts2, method='EDR+ST')
    sim13 = TextSimilarity.calc_texts_bow_sim(texts1, texts3, method='EDR+ST')
    sim23 = TextSimilarity.calc_texts_bow_sim(texts2, texts3, method='EDR+ST')

    print('Time (sec) =', time.time() - start)
    
    print([sim12, sim13, sim23])

    start = time.time()

    sim12 = TextSimilarity.calc_texts_bow_sim(texts1, texts2, method='ST')
    sim13 = TextSimilarity.calc_texts_bow_sim(texts1, texts3, method='ST')
    sim23 = TextSimilarity.calc_texts_bow_sim(texts2, texts3, method='ST')
    
    print('Time (sec) =', time.time() - start)
    
    print([sim12, sim13, sim23])

    print('* Main ends *')
        
# End of file