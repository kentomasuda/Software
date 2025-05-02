# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:43:41 2025

@author: masuda1379
"""

import numpy as np
import sys
import os
sys.path.append(os.pardir)

# カスタムモジュールをインポート
sys.path.append('C:/path/to/your/sentence_transformers_srclib')
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

# 入力データが含まれるテキストファイルのパスを指定
input_file_path = 'high_similarity_pairs_with_descriptions1111.txt'  # 適宜変更してください
output_file_path = 'filtered_high_similarity_pairs_with_descriptions1111.txt'  # 出力ファイルのパスを指定

# ファイルの読み込み
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 空行で区切られた各セクションに分割
sections = content.strip().split('\n\n')

filtered_sections = []  # 類似度によってフィルタリングされたセクションを保持

# 各セクションを処理
for section in sections:
    lines = section.strip().split('\n')
    
    # セクションが最低4行（タイトル2行＋機能記述2行）あるか確認
    if len(lines) < 4:
        continue  # 必要な行がなければスキップ

    # 最初の2行はタイトル、3,4行目は機能記述
    title_lines = lines[:2]
    raw_feature1 = lines[2]
    raw_feature2 = lines[3]
    
    # 機能記述から前後の引用符（"）およびカンマ（,）を削除
    feature1 = raw_feature1.strip('",')
    feature2 = raw_feature2.strip('",')
    
    # 3行目と4行目の機能記述間の類似度を計算
    sim = SentenceTransformers_.calc_texts_sims([feature1], [feature2], cache=False)[0][0]
    print(sim)
    # 類似度が0.9を超える場合のみセクションを保持
    if sim > 0.87:
        # 出力時に機能記述をクリーンにする
        cleaned_feature1 = feature1
        cleaned_feature2 = feature2
        # タイトル行とクリーンな機能記述を含むセクションを構築
        filtered_section = title_lines + [cleaned_feature1, cleaned_feature2]
        filtered_sections.append('\n'.join(filtered_section))
    # 類似度が0.9以下の場合は、セクション全体を削除（何も追加しない）

print(len(filtered_sections))

# フィルタリングされた結果を出力ファイルに保存
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write('\n\n'.join(filtered_sections))

print("フィルタリングが完了しました。結果は", output_file_path, "に保存されました。")
