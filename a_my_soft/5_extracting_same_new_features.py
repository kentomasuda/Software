# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:19:38 2025

@author: masuda1379

緑線の抽出
"""

import sys
import os
sys.path.append(os.pardir)
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_



# 製品ファイルのパス一覧（例）
product_files = {
    '電話': '電話_features_output.txt',
    'カメラ': 'カメラ_features_output.txt',
    '腕時計': '腕時計_features_output.txt',
    '音楽プレーヤー': '音楽プレーヤー_features_output.txt',
    '掃除機': '掃除機_features_output.txt',
    'テレビ': 'テレビ_features_output.txt'
}


def parse_sections(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    # 空行でセクションを分割
    raw_sections = content.strip().split('\n\n')
    sections = []
    for sec in raw_sections:
        lines = sec.strip().splitlines()
        if len(lines) >= 2:
            # 1行目、2行目、3行目以降を分ける
            header1 = lines[0]
            header2 = lines[1]
            features = lines[2:]
            sections.append({
                'header1': header1,
                'header2': header2,
                'features': features
            })
    return sections

# 製品ごとにセクションをパース
all_sections = {}
for product, file_path in product_files.items():
    all_sections[product] = parse_sections(file_path)

results = []

# 異なる製品間で比較
products = list(all_sections.keys())
for i in range(len(products)):
    for j in range(i+1, len(products)):
        product_a = products[i]
        product_b = products[j]
        sections_a = all_sections[product_a]
        sections_b = all_sections[product_b]
        
        # 各セクションペアについて比較
        for sec_a in sections_a:
            for sec_b in sections_b:
                print(f"セクション比較中: [{sec_a['header1']} | {sec_b['header1']}]")
                for f1 in sec_a['features']:
                    for f2 in sec_b['features']:
                        similarity = SentenceTransformers_.calc_sim(f1, f2, cached=False)
                        if similarity >= 0.99:
                            # 類似度が高い組み合わせを記録
                            print(f"高類似度検出: {similarity} - 「{f1}」 <-> 「{f2}」")
                            results.append({
                                'sec_a_header1': sec_a['header1'],
                                'sec_a_header2': sec_a['header2'],
                                'sec_b_header1': sec_b['header1'],
                                'sec_b_header2': sec_b['header2'],
                                'similarity_sentence': f"{f1}"
                            })

with open('middle_node_edge_contents.txt', 'w', encoding='utf-8') as out_file:
    for item in results:
        out_file.write(item['sec_a_header1'] + '\n')
        out_file.write(item['sec_a_header2'] + '\n')
        out_file.write(item['sec_b_header1'] + '\n')
        out_file.write(item['sec_b_header2'] + '\n')
        out_file.write(item['similarity_sentence'] + '\n')
        out_file.write('\n')  # セクション間の区切り
