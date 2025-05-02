# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:41:31 2025

@author: masuda1379
"""

import re

file_path = 'middle_node_edge_contents.txt'  # 実際のデータファイルのパスを指定
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

sections = [section.strip() for section in data.strip().split("\n\n") if section.strip()]


# 各セクションについて情報を抽出し、リストに保存
section_info_list = []

for section in sections:
    lines = section.split("\n")
    if len(lines) < 4:
        continue

    year1_prefix = lines[0][:4]
    year2_prefix = lines[2][:4]

    device_pattern = r"の(.+)"
    device1_match = re.search(device_pattern, lines[0])
    device2_match = re.search(device_pattern, lines[2])
    device1 = device1_match.group(1).strip() if device1_match else ""
    device2 = device2_match.group(1).strip() if device2_match else ""

    feature = lines[4].strip()

    # セクション単位の情報をタプルで保持
    section_info_list.append({
        "section": section,
        "year1": year1_prefix,
        "year2": year2_prefix,
        "device1": device1,
        "device2": device2,
        "feature": feature
    })

def year_sum(y1_str, y2_str):
    try:
        return int(y1_str) + int(y2_str)
    except:
        return float('inf')

# フィルタリングの結果を保持するリスト（初期状態では全てのセクションを含む）
filtered_sections = section_info_list.copy()

for i in range(len(section_info_list)):
    for j in range(i + 1, len(section_info_list)):
        sec_i = section_info_list[i]
        sec_j = section_info_list[j]

        # デバイス1とデバイス2が一致しているか確認
        if sec_i["device1"] == sec_j["device1"] and sec_i["device2"] == sec_j["device2"]:
            # 特徴のいずれかが一致しているか確認
            print(sec_i["feature"], sec_j["feature"])
            if sec_i["feature"] == sec_j["feature"]:  
                # 古い方を残す（年の合計が小さい方）
                sum_i = year_sum(sec_i["year1"], sec_i["year2"])
                sum_j = year_sum(sec_j["year1"], sec_j["year2"])

                if sum_i <= sum_j:
                    # sec_j のほうが新しい場合、リストから削除
                    if sec_j in filtered_sections:
                        filtered_sections.remove(sec_j)
                else:
                    # sec_i のほうが新しい場合、リストから削除
                    if sec_i in filtered_sections:
                        filtered_sections.remove(sec_i)

for sec in filtered_sections:
    print("-----")
    print(sec["section"])
    
print(len(filtered_sections))


output_file_path = 'filtered_middle_node_edge_contents.txt'  # 出力ファイル名

with open(output_file_path, 'w', encoding='utf-8') as outfile:
    content = "\n\n".join(
        "\n".join(sec["section"].splitlines())
        for sec in filtered_sections
    )
    outfile.write(content)
    
print(f"フィルタリングされたセクションが {output_file_path} に保存されました。")