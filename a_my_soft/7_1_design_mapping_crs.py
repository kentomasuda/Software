# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 18:29:27 2025

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
file_paths = ['カメラ_features_output.txt', '腕時計_features_output.txt', 
              '音楽プレーヤー_features_output.txt', '掃除機_features_output.txt', 
              'テレビ_features_output.txt', '電話_features_output.txt', 
              'filtered_filtered_high_similarity_pairs_with_descriptions.txt']

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
            net.add_edge(source_node, middle_node, title=edge_content, color="blue", length=5)
            net.add_edge(middle_node, target_node, title=edge_content, color="blue", arrows="to", length=5)
            
            middle_edges.append({
                "middle_node": middle_node,
                "target_node": target_node,
                "content": edge_content
            })
        else:
            # 異なる製品タイプ
            net.add_edge(source_node, target_node, title=edge_content, color="red", length=200)

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
            
            
# --- 1) 2D線分交差判定関数 ---
def do_intersect(p1, p2, p3, p4):
    """
    2次元平面上の線分 p1-p2 と p3-p4 が交差しているかを返す (True/False)。
    p1, p2, p3, p4 は (x, y) タプル。
    端点の共有のみの場合は交差とみなさない実装例（必要に応じて変える）。
    """

    def orientation(a, b, c):
        # 3点 a, b, c の並び (反時計回り、時計回り、一直線上など)
        return ((b[1] - a[1]) * (c[0] - b[0])) - ((b[0] - a[0]) * (c[1] - b[1]))

    def on_segment(a, b, c):
        # b が線分 a-c 上にあるかチェック
        if min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and \
           min(a[1], c[1]) <= b[1] <= max(a[1], c[1]):
            return True
        return False

    # p1,p2 と p3,p4 の向き
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    # 一般ケース
    if o1*o2 < 0 and o3*o4 < 0:
        return True

    # 特殊ケース（一直線上で重なる）
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True

    return False

# --- 2) PyVis ネットワーク内の交点を数える ---
def count_intersections_in_pyvis(network):
    # 1. ノードの (x, y) 座標を取得
    node_positions = {}
    for node_id in network.get_nodes():
        node_data = network.get_node(node_id)
        if node_data is None:
            continue
        x = node_data.get('x', None)
        y = node_data.get('y', None)
        # 座標が None の場合、arrange_nodes_in_circle が効いていない可能性がある
        if x is None or y is None:
            # 物理エンジンが動いていない or 手動配置がない場合は (0, 0) として扱う等
            x, y = 0, 0
        node_positions[node_id] = (x, y)

    # 2. エッジ情報を取得
    edges = network.get_edges()  
    # 例: [{'from': '腕時計_1990', 'to': '腕時計_1991', 'color': 'blue', ...}, ...]

    # 3. 線分ペアを全探索して交差を数える
    intersection_count = 0
    edge_list = []  # ( (x1,y1), (x2,y2), from_node, to_node ) を格納

    for edge in edges:
        from_node = edge.get('from')
        to_node   = edge.get('to')
        if from_node in node_positions and to_node in node_positions:
            p1 = node_positions[from_node]
            p2 = node_positions[to_node]
            edge_list.append((p1, p2, from_node, to_node))

    # 全ペア比較
    for i in range(len(edge_list)):
        for j in range(i+1, len(edge_list)):
            p1, p2, f1, t1 = edge_list[i]
            p3, p4, f2, t2 = edge_list[j]

            # 同じノード共有 → 線分の端点が同じ場合は交差とみなさない(場合による)
            if len({f1, t1, f2, t2}) < 4:
                continue

            if do_intersect(p1, p2, p3, p4):
                intersection_count += 1

    return intersection_count

# ここまでが交点数を数える関数群

# --- データ読み込みと処理 ---
sections = load_data(file_paths)
middle_edges = process_sections(sections)

# ノードを円形に配置
arrange_nodes_in_circle(net)

# 物理シミュレーションを無効化
net.toggle_physics(False)

# 交点数を計算
num_crossings = count_intersections_in_pyvis(net)
print("エッジ交点数:", num_crossings)

# HTMLで保存して表示
net.show("network1.html")