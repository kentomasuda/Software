# -*- coding: utf-8 -*-
"""
Calculate texts similarities sample main

@author: MURAKAMI Tamotsu
@date: 2024-06-20
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import time

# Library
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_
    
"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-06-20pip install --upgrade sentence-transformers
pip install --upgrade sentence-transformers

"""

if __name__ == '__main__':

    print('* Main starts *')

    texts1 = [
  "Go-Proは、高品質なビデオと写真を撮影する基本的な役割を持つ。",
  "Go-Proは、4K解像度でのビデオ撮影が可能である。",
  "Go-Proは、防水性能を備えており、アクションシーンでの使用に適している。",
  "Go-Proは、広角レンズを使用して広範囲の視野を提供する。",
  "Go-Proは、手ぶれ補正機能を搭載しており、滑らかな映像を撮影できる。",
  "Go-Proは、Wi-FiとBluetooth接続をサポートしており、スマートフォンとの連携が簡単である。",
  "Go-Proは、スローモーション撮影機能を備えている。",
  "Go-Proは、タイムラプス撮影機能を持ち、長時間の変化を短時間で再生できる。",
  "Go-Proは、耐衝撃性に優れており、過酷な環境でも使用できる。"
],

    texts2 = [
        "人間が犬に嚙みついた。",
        "製品がユーザを治す。",
        "花が咲く。"
        ]
    
    start = time.time()
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    end = time.time()
    print(end - start, ' sec.')
    print(sims)

    print('* Main ends *')
    
# End of file