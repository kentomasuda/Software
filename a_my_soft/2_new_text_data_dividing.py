# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:14:58 2024

@author: masuda1379

何分割にするかを入力して年代分割
"""

import time
import sys
import os
import numpy as np
import re
sys.path.append(os.pardir)

from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

# 手動入力部分
product_name = input("製品名を入力してください（例: カメラ）: ")
start_year = int(input("開始年を入力してください（例: 1990）: "))
end_year = int(input("終了年を入力してください（例: 2024）: "))
target_splits = int(input("最終的に何分割したいかを入力してください（例: 7）: "))
threshold_texts = 0.80  # 閾値（必要に応じて変更）
# 入力データをリストに格納
file_name = f"{product_name}_features.txt"
with open(file_name, 'r', encoding='utf-8') as file:
    data = file.read()

# 空行で分割してセクションを作成
sections = data.strip().split("\n\n")

# 年ごとに名前を設定
list_names = [str(start_year + i) for i in range(len(sections))]

# 各セクションをダブルクオーテーションとカンマで囲んで表示
formatted_sections = []
for idx, section in enumerate(sections):
    formatted_text = ",\n".join(
       '"' + re.sub(r'^\d+\.\s*|^-?\s*', '', line.strip()) + '"'  # 数字、ピリオド、ハイフン、空白を削除
       for line in section.strip().split("\n") if line.strip()
   )
    formatted_sections.append((list_names[idx], formatted_text))

# テキストを抽出
texts = [formatted for _, formatted in formatted_sections]

# 類似度を計算し、最も類似度が高いペアを結合する関数
def calculate_similarity_and_merge(texts, list_names, target_splits, threshold_texts):
    while len(texts) > target_splits:
        # 隣接する年代のペアの類似度を計算
        similarities = []
        for i in range(len(texts) - 1):
            texts1 = texts[i].split(",\n")
            texts2 = texts[i + 1].split(",\n")
            sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
            avg_similarity = np.mean(sims[0] + sims[1])
            similarities.append((avg_similarity, sims, i))
        
        # 類似度が最も高いペアを選び、そのペアを結合
        max_similarity, sims, idx_to_merge = max(similarities, key=lambda x: x[0])
        list1_sim, list2_sim = sims
        
        # list2の文で、類似度が「文結合用閾値」以下の文だけを選別
        texts2 = texts[idx_to_merge + 1].split(",\n")
        new_texts2_filtered = [texts2[i] for i, sim_value in enumerate(list2_sim) if sim_value < threshold_texts]
        
        # list1に、list2の閾値以下の文を追加して結合
        merged_text = texts[idx_to_merge] + (",\n" + ",\n".join(new_texts2_filtered) if new_texts2_filtered else "")
        
        # 年代を結合 (1990-1992の形式に変更)
        start_year = list_names[idx_to_merge].split('-')[0]  # 最初の年
        end_year = list_names[idx_to_merge + 1].split('-')[-1]  # 最後の年
        new_name = f"{start_year}-{end_year}"  # 結合後の名前
        
        # 結合した新しいテキストと名前でリストを更新
        texts = texts[:idx_to_merge] + [merged_text] + texts[idx_to_merge + 2:]
        list_names = list_names[:idx_to_merge] + [new_name] + list_names[idx_to_merge + 2:]
        
    return texts, list_names

# 実行開始時刻を取得
start_time = time.time()

# 類似度計算を行い、最終的に指定された分割数に達するまで結合を繰り返す
merged_texts, merged_names = calculate_similarity_and_merge(texts, list_names, target_splits, threshold_texts)

# セクション名を「年発売のカメラ」に変更
final_names = [f"{name}年発売の{product_name}" for name in merged_names]

# 実行終了時刻を取得
end_time = time.time()

# 結果を表示し、指定した形式でファイルに保存
output_filename = f"{product_name}_features_year.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    for i, (name, text) in enumerate(zip(final_names, merged_texts)):
        output_file.write(f"{name}\n{text}")
        
        # 最後の要素でない場合のみ改行を追加
        if i < len(final_names) - 1:
            output_file.write("\n\n")

# 経過時間を表示
elapsed_time = end_time - start_time
print(f"プログラムの実行時間: {elapsed_time:.2f}秒")
print(f"結果が {output_filename} に保存されました。")
