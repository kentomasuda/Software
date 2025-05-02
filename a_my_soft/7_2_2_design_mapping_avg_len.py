# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 16:15:41 2025

@author: masuda1379
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:27:38 2025

@author: masuda1379
"""

import sys
import os
sys.path.append(os.pardir)
from pyvis.network import Network
import math
import re
import itertools  # <-- permutations 用
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

sys.path.append(os.pardir)

# ネットワークオブジェクトを作成（比較用ではなく、最終的に使う net は後ほど作る）
net = Network(height="750px", width="100%", notebook=True)

# ファイルリスト (先頭6つが製品ファイル, 7番目は追加データ)
file_paths = [
    'カメラ_features_output.txt',
    '腕時計_features_output.txt',
    '音楽プレーヤー_features_output.txt',
    '掃除機_features_output.txt',
    'テレビ_features_output.txt',
    '電話_features_output.txt',
    'filtered_filtered_high_similarity_pairs_with_descriptions.txt'
]

node_title_file_paths = ['カメラ_features_year.txt', '腕時計_features_year.txt', 
              '音楽プレーヤー_features_year.txt', '掃除機_features_year.txt', 
              'テレビ_features_year.txt', '電話_features_year.txt']

# 年代を抽出する関数
def extract_year_range(text):
    match = re.match(r'-(\d{4})年発売', text) or \
            re.match(r'(\d{4})-(\d{4})', text) or \
            re.match(r'(\d{4})', text)
    return match.group(0) if match else text

# 製品の種類を判断する関数
def get_product_type(text):
    if "カメラ" in text:
        return "カメラ", "lightblue"
    elif "腕時計" in text:
        return "腕時計", "lightgreen"
    elif "音楽プレーヤー" in text:
        return "音楽プレーヤー", "orange"
    elif "掃除機" in text:
        return "掃除機", "plum"
    elif "テレビ" in text:
        return "テレビ", "pink"
    elif "電話" in text:
        return "電話", "yellow"
    return None, None

# データをロードする関数
def load_data(file_paths):
    all_sections = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            sections = f.read().strip().split('\n\n')
            all_sections.extend(sections)
    return all_sections

#セクションからノードの中身を抽出
def load_node_titles(file_paths):
    """
    複数のテキストファイルを読み込み、
    各ファイル内の空行区切りセクションから
    「product_type_year」のキーとタイトル情報を抽出して
    dict としてまとめて返す。
    """
    node_titles = {}  # 全ファイル共通の辞書に統合

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 空行で区切り、1 セクションを 1 ブロックとして扱う
        sections = content.split('\n\n')

        for section in sections:
            lines = section.strip().split('\n')
            if not lines:  # 空セクションはスキップ
                continue
            
            # 先頭行（例: "2003年発売のカメラ"）をキー抽出の元情報とする
            original_line = lines[0].strip()
            
            # 2 行目以降をタイトル文字列としてまとめる
            title_str = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
            title_str = title_str.replace('"', '').replace(',', '')


            # 年代と製品タイプを抽出
            year_extracted = extract_year_range(original_line)  # 例: "2003年"
            product_type = get_product_type(original_line)[0]     # 例: "カメラ"
            
            # product_type と年が両方とも取れた場合にのみキーを作成
            # 例: "カメラ_2003年"
            if product_type and year_extracted:
                combined_key = f"{product_type}_{year_extracted}"
                node_titles[combined_key] = title_str

    return node_titles

# セクションからノードとエッジを追加
def process_sections(sections, net, added_nodes):
    middle_edges = []

    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) < 2:
            continue

        source = extract_year_range(lines[0])
        target = extract_year_range(lines[1])
        source_type, source_color = get_product_type(lines[0])
        target_type, target_color = get_product_type(lines[1])

        if not source_type or not target_type:
            continue

        source_node = f"{source_type}_{source}"
        target_node = f"{target_type}_{target}"
        source_title = node_titles_dict.get(source_node, "")
        target_title = node_titles_dict.get(target_node, "")
        edge_content = '\n'.join(lines[2:]) if len(lines) > 2 else "説明なし"

        # 追加順 (ソースノード → 中間ノード → ターゲットノード)

        # 1. ソースノード
        if source_node not in added_nodes:
            print(source_node)
            net.add_node(
                source_node,
                label=f"{source_type}\n{source}",
                title=source_title,
                size=80,
                shape="box",
                font=dict(size=18, color="black"),
                color=source_color
            )
            added_nodes.add(source_node)

        # 2. 同タイプの場合のみ中間ノードを先に追加
        if source_type == target_type:
            middle_node = f"middle_{source_node}_{target_node}"
            if middle_node not in added_nodes:
                net.add_node(
                    middle_node,
                    label=" ",
                    size=1,
                    color="rgba(0, 0, 0, 0)",  # 透明にする場合
                    shape="dot",
                    opacity=0
                )
                added_nodes.add(middle_node)
        
        # 3. ターゲットノード
        if target_node not in added_nodes:
            print(target_node)
            net.add_node(
                target_node,
                label=f"{target_type}\n{target}",
                title=target_title, 
                size=80,
                shape="box",
                font=dict(size=18, color="black"),
                color=target_color
            )
            added_nodes.add(target_node)

        # エッジの追加
        if source_type == target_type:
            # 中間ノードがある
            middle_node = f"middle_{source_node}_{target_node}"
            net.add_edge(source_node, middle_node, title=edge_content, color="blue",width=3, length=5)
            net.add_edge(middle_node, target_node, title=edge_content, color="blue", width=3,arrows="to", length=5)
            
            middle_edges.append({
                "middle_node": middle_node,
                "target_node": target_node,
                "content": edge_content
            })
        else:
            # 異なる製品タイプ
            net.add_edge(source_node, target_node, title=edge_content, color="green",width=3, length=200)

    return middle_edges


# ノードを円形に配置
def arrange_nodes_in_circle(network, exclude_transparent=True):
    all_nodes = [node for node in network.get_nodes() if not (exclude_transparent and "transparent" in node)]
    center_x, center_y = 0, 0
    radius = 1000
    num_nodes = len(all_nodes)
    angle_gap = 2 * math.pi / num_nodes

    for i, node in enumerate(all_nodes):
        angle = i * angle_gap
        x_pos = center_x + radius * math.cos(angle)
        y_pos = center_y + radius * math.sin(angle)
        if network.get_node(node):  # ノードが存在するか確認
            network.get_node(node)["x"] = x_pos
            network.get_node(node)["y"] = y_pos

def calc_avg_red_green_edge_length(network):
    """
    PyVis の network オブジェクトを受け取り、
    color='red' または color='green' のエッジについてのみ長さを計算して
    その平均値を返す。
    """
    node_positions = {}
    for node_id in network.get_nodes():
        node_data = network.get_node(node_id)
        if node_data is None:
            continue
        x = node_data.get('x', None)
        y = node_data.get('y', None)
        if x is None or y is None:
            x, y = 0, 0
        node_positions[node_id] = (x, y)

    edges = network.get_edges()

    distances = []
    for edge in edges:
        edge_color = edge.get('color', '')
        # 赤 or 緑のエッジのみ
        if edge_color in ['red', 'green']:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node in node_positions and to_node in node_positions:
                x1, y1 = node_positions[from_node]
                x2, y2 = node_positions[to_node]
                dist = math.hypot(x2 - x1, y2 - y1)
                distances.append(dist)

    if len(distances) == 0:
        return 0.0
    return sum(distances) / len(distances)


# ここから「赤＆緑の平均長が最小となるパターンを探索」するメイン処理
####################################################

# 1) 最初の6つのファイルが製品ごとのデータ (7番目は追加ファイル)
product_file_paths = file_paths[:6]
extra_file = file_paths[6]  # 'filtered_high_similarity_pairs_with_descriptions.txt'

# 2) 円順列(5!) → 120通りを生成
fixed_path = product_file_paths[0]  # 例: 'カメラ_features_output.txt' を固定
other_5 = product_file_paths[1:]    # 残り5ファイル
all_permutations_5 = list(itertools.permutations(other_5, 5))  # 5! = 120通り

best_network = None
best_avg_len = float('inf')
best_order = None

for perm in all_permutations_5:
    # 今回の順序
    current_order = [fixed_path] + list(perm)
    # 追加ファイルは常に最後に読み込み
    combined_paths = current_order + [extra_file]
    
    # ネットワークを作って配置・平均長を計算
    tmp_net = Network(height="750px", width="100%", notebook=True)
    tmp_added_nodes = set()

    sections = load_data(combined_paths)
    node_titles_dict = load_node_titles(node_title_file_paths)
    process_sections(sections, tmp_net, tmp_added_nodes)

    arrange_nodes_in_circle(tmp_net, exclude_transparent=True)
    tmp_net.toggle_physics(False)

    # 赤＆緑のエッジ平均長
    avg_len = calc_avg_red_green_edge_length(tmp_net)
    print(avg_len)

    # より短い場合は更新
    if avg_len < best_avg_len:
        best_avg_len = avg_len
        best_order = current_order
        best_network = tmp_net

# 最良結果を表示
print("=== 赤＆緑エッジの平均長が最も短い読み込み順(円順列) ===")
for i, p in enumerate(best_order, start=1):
    print(f"{i}: {p}")
print("平均長:", best_avg_len)

# 最終的なネットワークをHTML出力
best_network.show("network22.html")
print("network22.html に出力しました。")
