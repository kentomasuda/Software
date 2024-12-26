# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 16:12:08 2024

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

# 年とその機能記述を辞書に格納
features_by_year = {}
for section in sections:
    lines = section.strip().split("\n")
    year = lines[0].strip()  # 一行目を年代として取得
    features = lines[1:]     # 二行目以降を機能記述としてリスト化
    features_by_year[year] = features

# 境界値設定
middle_threshold = 0.62
high_similarity_threshold = 0.8

# 年代ごとの類似度計算
years = list(features_by_year.keys())
different_list = []
high_similarity_pairs = []

for i in range(len(years)):
    for j in range(i + 1, len(years)):
        year1, year2 = years[i], years[j]
        texts1, texts2 = features_by_year[year1], features_by_year[year2]

        # SentenceTransformers_ の calc_texts_sims 関数を使用して、各要素の最大類似度を取得
        simmaxs1, simmaxs2 = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)

        # 両方のリストを結合して平均類似度を計算
        combined_sims = simmaxs1 + simmaxs2
        average_similarity = np.mean(combined_sims)

        # 平均類似度がmiddle_threshold未満の場合
        if average_similarity < middle_threshold:
            different_list.append(f"{year1}と{year2} (平均類似度: {average_similarity:.4f})")

            # 高い類似度を持つペアを抽出（双方の類似度が閾値以上の場合）
            for idx1, sim1 in enumerate(simmaxs1):
                if sim1 >= high_similarity_threshold:
                    # 浮動小数点の許容誤差を使って類似度を比較
                    tolerance = 1e-6
                    matching_indices = [
                        idx for idx, sim in enumerate(simmaxs2)
                        if abs(sim - sim1) < tolerance
                    ]
                    for idx2 in matching_indices:
                        sim2 = simmaxs2[idx2]
                        if sim2 >= high_similarity_threshold:
                            high_similarity_pairs.append(
                                (year1, year2, texts1[idx1], texts2[idx2], sim1)
                            )

# 結果を整理して出力
print("\ndifferent:")
for item in different_list:
    print(item)

# 高い類似度を持つ機能記述ペアを表示
if high_similarity_pairs:
    print("\n=== 類似度が0.8以上の機能記述ペア ===")
    for year1, year2, text1, text2, sim in high_similarity_pairs:
        print(f"{year1}と{year2} の機能記述間の類似度: {sim:.2f}")
        print(f"  {text1} <--> {text2}")
else:
    print("類似度が0.8以上の機能記述ペアはありません。")

# 結果をファイルに保存
output_filename = "high_similarity_pairs_with_descriptions.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    for item in different_list:
        output_file.write(f"{item}\n")

    output_file.write("\n=== 類似度が0.8以上の機能記述ペア ===\n")
    for year1, year2, text1, text2, sim in high_similarity_pairs:
        output_file.write(f"{year1}と{year2} の機能記述間の類似度: {sim:.2f}\n")
        output_file.write(f"  {text1} <--> {text2}\n")

print(f"結果が {output_filename} に保存されました。")
