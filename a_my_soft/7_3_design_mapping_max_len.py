# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:44:37 2025

@author: masuda1379
"""
import sys
import os
sys.path.append(os.pardir)
from pyvis.network import Network
import math
import re
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

sys.path.append(os.pardir)

# ネットワークオブジェクトを作成
net = Network(height="750px", width="100%", notebook=True)

# ファイルリスト
file_paths = [
    'カメラ_features_output.txt',
    '腕時計_features_output.txt',
    '音楽プレーヤー_features_output.txt',
    '掃除機_features_output.txt',
    'テレビ_features_output.txt',
    '電話_features_output.txt',
    'filtered_filtered_high_similarity_pairs_with_descriptions.txt'
]

# ノードの重複を避けるためのセット
added_nodes = set()

# 年代を抽出する関数
def extract_year_range(text):
    match = re.match(r'-(\d{4})年発売', text) or \
            re.match(r'(\d{4})-(\d{4})', text) or \
            re.match(r'(\d{4})年', text)
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
        return "掃除機", "purple"
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

# セクションからノードとエッジを追加
def process_sections(sections):
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
        edge_content = '\n'.join(lines[2:]) if len(lines) > 2 else "説明なし"

        # 追加順 (ソースノード → 中間ノード → ターゲットノード)

        # 1. ソースノード
        if source_node not in added_nodes:
            net.add_node(
                source_node,
                label=f"{source_type}\n{source}",
                size=80,
                shape="box",
                font=dict(size=14, color="black"),
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
            net.add_node(
                target_node,
                label=f"{target_type}\n{target}",
                size=80,
                shape="box",
                font=dict(size=14, color="black"),
                color=target_color
            )
            added_nodes.add(target_node)

        # エッジの追加
        if source_type == target_type:
            # 中間ノードがある
            middle_node = f"middle_{source_node}_{target_node}"
            net.add_edge(source_node, middle_node, title=edge_content, color="blue",width=4, length=5)
            net.add_edge(middle_node, target_node, title=edge_content, color="blue",width=4, arrows="to", length=5)
            
            middle_edges.append({
                "middle_node": middle_node,
                "target_node": target_node,
                "content": edge_content
            })
        else:
            # 異なる製品タイプ
            net.add_edge(source_node, target_node, title=edge_content, color="red",width=4, length=200)

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


def calc_max_red_green_edge_length(network):
    """
    PyVis の network オブジェクトを受け取り、
    color='red' または color='green' のエッジだけを対象に
    一番長い線分の長さを返す。
    """
    # 1. ノード座標の取得
    node_positions = {}
    for node_id in network.get_nodes():
        node_data = network.get_node(node_id)
        if node_data is None:
            continue
        x = node_data.get('x', None)
        y = node_data.get('y', None)
        if x is None or y is None:
            # 座標が確定していない場合(物理シミュレーション未実行など)
            x, y = 0, 0
        node_positions[node_id] = (x, y)

    # 2. エッジ情報を取得
    edges = network.get_edges()
    
    # 3. 赤 or 緑のエッジ長を調べる
    max_dist = 0.0
    for edge in edges:
        edge_color = edge.get('color', '')
        # 対象は赤か緑のみ
        if edge_color in ['red', 'green']:
            from_node = edge.get('from')
            to_node   = edge.get('to')
            if from_node in node_positions and to_node in node_positions:
                x1, y1 = node_positions[from_node]
                x2, y2 = node_positions[to_node]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist > max_dist:
                    max_dist = dist
    
    return max_dist
                    
                    
sections = load_data(file_paths)
middle_edges = process_sections(sections)
arrange_nodes_in_circle(net)
net.toggle_physics(False)

# 緑と赤エッジのうち、一番長い線の長さを取得
max_len = calc_max_red_green_edge_length(net)
print(f"緑＆赤のエッジの最大長: {max_len}")

# HTMLで保存して表示
net.show("network3.html")