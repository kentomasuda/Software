# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 17:49:32 2024

@author: masuda1379

２，一年ごとの機能記述を変化の大きさによって分割
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
threshold_years = 0.80
threshold_texts = 0.85
start_year = int(input("開始年を入力してください（例: 2009）: "))
end_year = int(input("終了年を入力してください（例: 2011）: "))

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

# 関数定義：類似度計算と結合・独立の再帰的処理
def compare_and_merge(texts, list_names, idx=0):
    if idx >= len(texts) - 1:
        return texts, list_names

    # 2つのリストの類似度を計算
    texts1 = texts[idx].split(",\n")
    texts2 = texts[idx + 1].split(",\n")
    #print(f"比較中のデータ内容:\nリスト1: {texts1}\nリスト2: {texts2}")
    
    sims = SentenceTransformers_.calc_texts_sims(texts1, texts2, cache=False)
    list1, list2 = sims
    
    average_similarity_years = np.mean(list1 + list2)
    print(f"Comparing {list_names[idx]} and {list_names[idx + 1]}: 平均類似度: {average_similarity_years}")
    
    if average_similarity_years >= threshold_years:
        # list2の文で、類似度が「文結合用の閾値」以下の文だけを選別
        new_texts2_filtered = [texts2[i] for i, sim_value in enumerate(list2) if sim_value < threshold_texts]

        # list1に、list2の閾値以下の文を追加して結合
        new_text = texts[idx] + (",\n" + ",\n".join(new_texts2_filtered) if new_texts2_filtered else "")
        
        # 年代を結合（例: 2009-2011）
        start_year = list_names[idx].split('-')[0]  # 最初の年
        end_year = list_names[idx + 1].split('-')[-1]  # 最後の年
        new_name = f"{start_year}-{end_year}"
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

# セクション名を「年発売のカメラ」に変更
final_names = [f"{name}年発売の{product_name}" for name in merged_names]

# 実行終了時刻を取得
end_time = time.time()
"""
# 結果を表示
for name, text in zip(final_names, merged_texts):
    print(f"{name}:\n{text}\n")
"""
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
