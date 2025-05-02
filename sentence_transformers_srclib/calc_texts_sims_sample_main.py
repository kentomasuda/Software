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
        "8K動画撮影を可能にする。",
        "リアルタイム瞳AFを搭載する。",
        "ボディ内手ブレ補正を強化する。",
        "デュアルピクセルCMOS AF IIを採用する。",
        "高感度性能を向上させる。",
        "高速連写を実現する。",
        "4K 120fps動画撮影を可能にする。",
        "バリアングル液晶を搭載する。",
        "デュアルメモリーカードスロットを備える。",
        "AIによる被写体認識を行う。",
        "高解像度センサーを搭載する。",
        "ライブストリーミング機能を強化する。",
        "防塵防滴性能を向上させる。",
        "高速オートフォーカスを実現する。",
        "内蔵NDフィルターを搭載する。",
        "高精度な色再現を行う。",
        "高解像度EVFを搭載する。",
        "USB-C充電をサポートする。",
        "高性能な顔認識AFを搭載する。",
        "低照度性能を向上させる。",
        "高精度なホワイトバランスを提供する。",
        "多彩なフィルムシミュレーションを提供する。",
        "高精度な露出制御を行う。",
        "コンパクトなボディに高性能を詰め込む。",
        "デュアルピクセルAFを採用する。",
        "Bluetooth接続をサポートする。",
        "電子シャッターを高速化する。",
        "Wi-Fi接続を強化する。",
        "多重露光機能を強化する。",
        "スマートフォンとの連携を強化する。",
        "高速なデュアルカードスロットを搭載する。",
        "高精度な顔認識機能を搭載する。"
        ],

    texts2 = [
"AIが自動でシーンを認識して最適な設定を選ぶ。",
"8K動画を60fpsで撮影する。",
"リアルタイムで背景をぼかす。",
"手ぶれ補正を強化して5軸で補正する。",
"顔認識でフォーカスを自動調整する。",
"暗所での撮影性能を向上させる。",
"バッテリー寿命を延ばして長時間撮影を可能にする。",
"Wi-Fiで即座に写真を共有する。",
"4K動画を120fpsでスローモーション撮影する。",
"タッチスクリーンで直感的に操作する。",
"防水性能を強化して水中撮影を可能にする。",
"高解像度のセンサーで細部まで鮮明に撮影する。",
"音声コマンドで操作する。",
"360度カメラで全方位を撮影する。",
"自動でパノラマ写真を生成する。",
"被写体追尾機能で動く被写体を捉える。",
"高感度ISOでノイズを抑える。",
"デュアルピクセルAFで高速フォーカスを実現する。",
"Bluetoothでスマートフォンと連携する。",
"自動でHDR写真を生成する。"
        ]
    
    start = time.time()
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    end = time.time()
    print(end - start, ' sec.')
    print(sims)

    print('* Main ends *')
    
# End of file