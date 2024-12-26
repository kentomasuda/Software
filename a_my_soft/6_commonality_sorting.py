# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:11:19 2024

@author: masuda1379
"""

# ファイル名を指定
header_file = "共通性生成リスト.txt"
feature_file = "別製品間共通性.txt"

header_info = []

with open(header_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 各行の改行文字を削除
header_info = [line.strip() for line in lines]

# 結果を表示
print(header_info)

# "特徴的な機能"の部分を抽出
feature_info = []
with open(feature_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

    for line in lines:
        if "\"特徴的な機能\":" in line:
            feature = line.split(":")[1].strip().strip(",").strip("\"")
            feature_info.append(feature)

# 機能を5個ずつ割り当てる
feature_groups = [feature_info[i:i + 5] for i in range(0, len(feature_info), 5)]

# データを並び替えてまとめる
final_data = []

for header in header_info:
    # 1999年発売の腕時計と1994年発売のカメラのような行を抽出
    header_data = header.split("と")
    final_data.append(header_data[0].strip())  # 例えば "1999年発売の腕時計"
    final_data.append(header_data[1].strip())  # 例えば "1994年発売のカメラ"
    # 5個ずつ特徴を割り当てる
    if feature_groups:
        final_data.extend(feature_groups.pop(0))  # 次の5個の特徴を追加
    final_data.append("")  # 空行を追加

# 結果をファイルに保存
with open("マップ反映要素.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(final_data))

print("処理が完了しました。")