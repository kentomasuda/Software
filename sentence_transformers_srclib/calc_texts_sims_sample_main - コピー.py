# -*- coding: utf-8 -*-
"""
Calculate texts similarities sample main

@author: MURAKAMI Tamotsu
@date: 2024-06-20
"""
#For directory access
import sys
import os
sys.path.append(os.pardir)


import numpy as np

# Library
from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_
#from sentence_transformers import SentenceTransformer


"""
Main

@author: MURAKAMI Tamotsu
@date: 2024-06-20
"""

import sys
import os

# 'sentence_transformers_srclib' ディレクトリのフルパスを追加
sys.path.append('C:/path/to/your/sentence_transformers_srclib')

from sentence_transformers_srclib.sentence_transformers_ import SentenceTransformers_


if __name__ == '__main__':

    print('* Main starts *')

    texts1 = [
"腕時計は時間を表示する。",
"腕時計は日付を表示する。",
"腕時計はアラーム機能を持つ。",
"腕時計はストップウォッチ機能を持つ。",
"腕時計はタイマー機能を持つ。",
"腕時計はバックライトを搭載する。",
"腕時計は防水機能を持つ。",
"腕時計は耐衝撃性を持つ。",
"腕時計はワールドタイム機能を持つ。",
"腕時計はソーラー充電機能を持つ。",
"腕時計は電波受信機能を持つ。",
"腕時計はデジタル表示とアナログ表示を併用するモデルがある。",
"腕時計はカレンダー機能を持つ。",
"腕時計は高度計や気圧計を搭載するモデルがある。",
"腕時計はGPS機能を持つモデルがある。",
]

    texts2 = [
"腕時計は時間を表示する。",
"腕時計は日付を表示する。",
"腕時計はアラーム機能を持つ。",
"腕時計はストップウォッチ機能を持つ。",
"腕時計はタイマー機能を持つ。",
"腕時計はバックライトを搭載する。",
"腕時計は防水機能を持つ。",
"腕時計は耐衝撃性を持つ。",
"腕時計はワールドタイム機能を持つ。",
"腕時計はソーラー充電機能を持つ。",
"腕時計はBluetooth接続機能を持つ。",
"腕時計はGPS機能を持つ。",
"腕時計は心拍数モニターを搭載する。",
"腕時計はフィットネストラッキング機能を持つ。",
"腕時計はスマートフォン通知機能を持つ。",
"腕時計は音楽再生コントロール機能を持つ。",
"腕時計はカスタマイズ可能なウォッチフェイスを提供する。",
"腕時計は高度計を搭載する。",
"腕時計は気圧計を搭載する。",
"腕時計はコンパス機能を持つ。",
]
    
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    print(sims)
    list1, list2 = sims

# 2つのリストを結合
    combined_list = list1 + list2

# 平均を計算
    average_similarity = np.mean(combined_list)

    print(average_similarity)

    print('* Main ends *')
    
# End of file