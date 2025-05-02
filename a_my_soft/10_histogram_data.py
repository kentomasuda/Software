# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:22:29 2025

@author: masuda1379
"""

import numpy as np
import sys
import os
sys.path.append(os.pardir)

# カスタムモジュールをインポート
sys.path.append('C:/path/to/your/sentence_transformers_srclib')
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

# ファイルからテキストデータを読み込む
file_path = '腕時計_カメラ_テレビ_音楽プレーヤー_掃除機_電話_features_year.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# 年ごとに空行で区切られているデータを分割
sections = data.strip().split("\n\n")

# 対象となる製品カテゴリのリスト
product_categories = ['電話', '掃除機', 'カメラ', '腕時計', '音楽プレーヤ', 'テレビ']

def extract_product_name(line: str) -> str:
    """
    年代＋製品名が含まれる行から製品カテゴリを抽出する関数。
    例: "1991-2006年発売の腕時計" -> "腕時計"
    """
    for product in product_categories:
        if product in line:
            return product
    return "その他"  # 万一該当しなかった場合

# 年とその機能記述を保持する辞書
# ここではキーとして「ファイルの１行目全文」を保持し、
# 追加で "product" と "features" を持つ形にする
entries = {}
for section in sections:
    lines = section.strip().split("\n")
    header_line = lines[0].strip()  # 例: "1991-2006年発売の腕時計"
    product_name = extract_product_name(header_line)
    features = lines[1:]  # 二行目以降が機能記述
    entries[header_line] = {
        "product": product_name,
        "features": features
    }

# 全エントリーをリスト化（比較のため）
all_keys = list(entries.keys())

# 同製品間の類似度を格納するリスト
same_product_similarities = []

# 異製品間の類似度を格納するリスト
diff_product_similarities = []

for i in range(len(all_keys)):
    for j in range(i + 1, len(all_keys)):
        key1 = all_keys[i]
        key2 = all_keys[j]
        product1 = entries[key1]["product"]
        product2 = entries[key2]["product"]
        texts1 = entries[key1]["features"]
        texts2 = entries[key2]["features"]

        # calc_texts_sims で各要素同士の最大類似度を算出
        simmaxs1, simmaxs2 = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)

        # 両方のリストを結合して平均類似度を計算
        combined_sims = simmaxs1 + simmaxs2
        average_similarity = np.mean(combined_sims)

        # 同製品か異製品かで振り分け
        if product1 == product2:
            same_product_similarities.append(average_similarity)
        else:
            diff_product_similarities.append(average_similarity)

# 結果表示
print("=== 同製品間の類似度リスト (件数: {}) ===".format(len(same_product_similarities)))
print(same_product_similarities)

print("\n=== 異製品間の類似度リスト (件数: {}) ===".format(len(diff_product_similarities)))
print(diff_product_similarities)
