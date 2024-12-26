# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:24:21 2024

@author: masuda1379

４，結合されたファイルから、各製品。各年代間の類似度を計算して三段階に分ける
"""

import numpy as np
import sys
import os
sys.path.append(os.pardir)

# カスタムモジュールをインポート
sys.path.append('C:/path/to/your/sentence_transformers_srclib')
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

# モデルのロード
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

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

# すべての年代間で類似度を計算して出力
years = list(features_by_year.keys())
similarities = {}

# ユーザーによる手動入力で境界値を設定
#similar_threshold = float(input("similar と middle の境界となる類似度を入力してください（例: 0.85）: "))
similar_threshold = 0.87
middle_threshold = 0.62
#middle_threshold = float(input("middle と different の境界となる類似度を入力してください（例: 0.70）: "))


# 各カテゴリーごとのリストを作成
similar_list = []
middle_list = []
different_list = []
# 数値を格納するリストを用意
similarity_values = []

for i in range(len(years)):
    for j in range(i + 1, len(years)):
        year1, year2 = years[i], years[j]
        texts1, texts2 = features_by_year[year1], features_by_year[year2]

        # SentenceTransformers_ の calc_texts_sims 関数を使用して、各要素の最大類似度を取得
        simmaxs1, simmaxs2 = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)

        # 両方のリストを結合して平均類似度を計算
        combined_sims = simmaxs1 + simmaxs2
        average_similarity = np.mean(combined_sims)
        
        # 結果を詳細に出力
        print(f"{year1}と{year2}の機能記述の平均類似度: {average_similarity:.4f}")
        
        # 数値をリストに追加
        similarity_values.append(average_similarity)

        # 類似度に応じた分類
        if average_similarity >= similar_threshold:
            similarity_category = "similar"
            similar_list.append(f"{year1}と{year2}")
        elif average_similarity >= middle_threshold:
            similarity_category = "middle"
            middle_list.append(f"{year1}と{year2}")
        else:
            similarity_category = "different"
            different_list.append(f"{year1}と{year2}")

# 数値リストを出力
print("\n==== 類似度数値リスト ====")
print(similarity_values)

# 結果を整理して出力
print("\nsimilar:")
for item in similar_list:
    print(item)

print("\nmiddle:")
for item in middle_list:
    print(item)

print("\ndifferent:")
for item in different_list:
    print(item)

# ファイルに保存
output_filename = "年代製品間類似度.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.write("similar:\n")
    for item in similar_list:
        output_file.write(f"{item}\n")

    output_file.write("\nmiddle:\n")
    for item in middle_list:
        output_file.write(f"{item}\n")

    output_file.write("\ndifferent:\n")
    for item in different_list:
        output_file.write(f"{item}\n")

print(f"結果が {output_filename} に保存されました。")
