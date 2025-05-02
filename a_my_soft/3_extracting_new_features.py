# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:06:42 2025

@author: masuda1379
"""

import sys
import os
sys.path.append(os.pardir)

# Library
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_


# プロダクト名を指定（必要に応じて変更可能）
product_name = "テレビ"

# ファイルの読み込み
input_file_path = f'{product_name}_features_year.txt'   # 入力ファイル名に製品名を反映
output_file_path = f'{product_name}_features_output.txt'  # 出力ファイル名に製品名を反映

with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# セクションごとに分割（各セクションが1年代のデータを含む）
sections = content.strip().split('\n\n')

# 各年代ごとの年と機能記述のリストを作成
years = []
features_by_year = []

for section in sections:
    lines = section.strip().split('\n')
    year = lines[0]             # 最初の行が年代
    features = lines[1:]        # それ以降がその年代の機能記述
    years.append(year)
    features_by_year.append(features)

# 出力結果を保存するためのリスト
output_lines = []

# 前の年代との類似度計算と並べ替えを各年代ペアに対して実施
# 初めの年代には前の年代が存在しないため、2番目の年代から開始
for i in range(1, len(years)):
    prev_year = years[i-1]
    curr_year = years[i]
    prev_features = features_by_year[i-1]
    curr_features = features_by_year[i]
    
    # 現在の年代の各機能記述に対して、前の年代の機能記述との最大類似度を計算
    feature_similarities = []
    for feature in curr_features:
        
        # feature_text と prev_features の間で最大類似度を計算
        sim = SentenceTransformers_.calc_texts_sims([feature], prev_features, cache=False)[0]
        feature_similarities.append((feature, sim))
    
    # 類似度が低い順に並べ替え
    feature_similarities.sort(key=lambda x: x[1])
    
    # 出力用に結果を整形：年代ペアと類似度の低い上位10個の機能記述
    output_lines.append(f"{prev_year}\n{curr_year}")
    print(f"\n{prev_year}\n{curr_year}")
    top_features = feature_similarities[:10]  # 類似度が低い順に10個を選択
    for feature, sim in top_features:
        # 出力前に前後の引用符（"）およびカンマ（,）を削除
        cleaned_feature = feature.strip('",')
        output_lines.append(f"{cleaned_feature}")
        print(f"類似度: {sim} | 機能記述: {cleaned_feature}")
    output_lines.append("")  # セクション間の空行

# 結果を出力ファイルに保存
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write('\n'.join(output_lines))