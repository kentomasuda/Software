"""
Created on Sun Oct  6 01:00:02 2024

@author: 7491939865
"""
import time
import sys
import os
sys.path.append(os.pardir)

from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

import numpy as np
import re

# 手動入力部分
"""
threshold_years = float(input("年代を結合する際の類似度の閾値を入力してください（例: 0.7）: "))
threshold_texts = float(input("文を結合する際の類似度の閾値を入力してください（例: 0.5）: "))
start_year = int(input("開始年を入力してください（例: 1980）: "))
end_year = int(input("終了年を入力してください（例: 2020）: "))
"""

threshold_years = 0.86
threshold_texts = 0.80
start_year = 1990
end_year = 2025

# 入力データをリストに格納
with open('filtered_generated_text.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# 空行で分割してセクションを作成
sections = data.strip().split("\n\n")

# 自動的にリストの数を検出
num_lists = len(sections)

# 周期を計算（自動検出されたリスト数に基づく）
period = (end_year - start_year) // num_lists

# 名前を付ける
list_names = [f"{start_year + i * period}-{start_year + (i + 1) * period}" for i in range(num_lists)]

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


# 関数定義：類似度計算と結合・独立の再帰的処理
def compare_and_merge(texts, list_names, idx=0):
    if idx >= len(texts) - 1:
        return texts, list_names

    # 2つのリストの類似度を計算
    texts1 = texts[idx].split(",\n")
    texts2 = texts[idx + 1].split(",\n")
    
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    list1, list2 = sims
    
    average_similarity_years = np.mean(list1 + list2)
    print(f"Comparing {list_names[idx]} and {list_names[idx + 1]}: 平均類似度: {average_similarity_years}")
    
    if average_similarity_years >= threshold_years:
        # list2（1995-2000）の文で、類似度が「文結合用の閾値」以下の文だけを選別
        new_texts2_filtered = [texts2[i] for i, sim_value in enumerate(list2) if sim_value < threshold_texts]

        # 1990-1995に、1995-2000の閾値以下の文を追加して結合
        new_text = texts[idx] + (",\n" + ",\n".join(new_texts2_filtered) if new_texts2_filtered else "")
        
        # 年代を結合（例: 1990-2000）
        new_name = f"{list_names[idx].split('-')[0]}-{list_names[idx + 1].split('-')[1]}"
        print(f"結合: {list_names[idx]} と {list_names[idx + 1]} を {new_name} に結合しました。\n")
        
        # 新しいリストに置き換えて、再帰的に次を比較
        return compare_and_merge(
            texts[:idx] + [new_text] + texts[idx + 2:],  # 結合したリストを追加
            list_names[:idx] + [new_name] + list_names[idx + 2:],  # 結合した名前を追加
            idx  # 同じ位置で再度比較
        )
    else:
        # 年代を独立させる場合、次のペアを比較
        print(f"独立: {list_names[idx]} を独立させます。\n")
        return compare_and_merge(texts, list_names, idx + 1)

# 実行開始時刻を取得
start_time = time.time()

# 最初のペアから開始して結合または独立を繰り返す
merged_texts, merged_names = compare_and_merge(texts, list_names)

# 実行終了時刻を取得
end_time = time.time()

# 結果を表示
for name, text in zip(merged_names, merged_texts):
    print(f"{name}:\n{text}\n")
    
# 経過時間を表示
elapsed_time = end_time - start_time
print(f"プログラムの実行時間: {elapsed_time:.2f}秒")
