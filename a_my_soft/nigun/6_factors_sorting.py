# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:04:03 2024

@author: masuda1379
"""

# ファイル名を指定
similarity_file = "共通性生成リスト.txt"
feature_file = "別製品間共通性.txt"

# similarとdifferentの情報を抽出
similarity_info = []
difference_info = []

with open(similarity_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

    # similarとdifferentの抽出
    section = None
    for line in lines:
        line = line.strip()
        if line.startswith("similar:"):
            section = "similar"
        elif line.startswith("different:"):
            section = "different"
        elif line == "":
            section = None
        elif section == "similar":
            similarity_info.append(line)
        elif section == "different":
            difference_info.append(line)

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
"""
# Similarのデータ
for sim in similarity_info:
    # 1990-1998年発売の腕時計と2000-2001年発売の腕時計のような行を抽出
    similar_data = sim.split("と")
    final_data.append(similar_data[0].strip())  # 例えば "1990-1998年発売の腕時計"
    final_data.append(similar_data[1].strip())  # 例えば "2000-2001年発売の腕時計"
    final_data.append("差異性")  # "差異性"を追加
    # 5個ずつ特徴を割り当てる
    if feature_groups:
        final_data.extend(feature_groups.pop(0))  # 次の5個の特徴を追加
    final_data.append("")  # 空行を追加
"""
# Differentのデータ
for diff in difference_info:
    # 1999年発売の腕時計と1994年発売のカメラのような行を抽出
    different_data = diff.split("と")
    final_data.append(different_data[0].strip())  # 例えば "1999年発売の腕時計"
    final_data.append(different_data[1].strip())  # 例えば "1994年発売のカメラ"
    #final_data.append("共通性")  # "共通性"を追加
    # 5個ずつ特徴を割り当てる
    if feature_groups:
        final_data.extend(feature_groups.pop(0))  # 次の5個の特徴を追加
    final_data.append("")  # 空行を追加

# 結果をファイルに保存
with open("マップ反映要素.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(final_data))

print("処理が完了しました。")
