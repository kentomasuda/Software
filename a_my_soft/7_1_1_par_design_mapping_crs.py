# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 00:48:09 2025

@author: masuda1379
"""

import sys
import os
sys.path.append(os.pardir)
from pyvis.network import Network
import math
import itertools
import re

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
            net.add_node(
                source_node,
                label=f"{source_type}\n{source}",
                title=source_title,
                size=80,
                shape="box",
                font=dict(size=25, color="black"),
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
        print(middle_node)
        
        # 3. ターゲットノード
        if target_node not in added_nodes:
            net.add_node(
                target_node,
                label=f"{target_type}\n{target}",
                title=target_title, 
                size=80,
                shape="box",
                font=dict(size=25, color="black"),
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
       # else:
            # 異なる製品タイプ
            #net.add_edge(source_node, target_node, title=edge_content, color="green", length=200)

    return



def process_intermediate_edges(file_path, net):
    middle_edges = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]  # 空行を除外

    # 5行ごとに処理
    for i in range(0, len(lines), 5):
        block = lines[i:i+5]
        if len(block) < 5:
            continue  # 5行未満のブロックは無視

        # ブロックの行をそれぞれ取得
        src1_line = block[0]
        tgt1_line = block[1]
        src2_line = block[2]
        tgt2_line = block[3]
        edge_content = block[4]

        # 年範囲とタイプ、色を抽出
        src1_year = extract_year_range(src1_line)
        tgt1_year = extract_year_range(tgt1_line)
        src2_year = extract_year_range(src2_line)
        tgt2_year = extract_year_range(tgt2_line)

        src1_type, src1_color = get_product_type(src1_line)
        tgt1_type, tgt1_color = get_product_type(tgt1_line)
        src2_type, src2_color = get_product_type(src2_line)
        tgt2_type, tgt2_color = get_product_type(tgt2_line)

        # ノードIDの作成
        src1_node = f"{src1_type}_{src1_year}"
        tgt1_node = f"{tgt1_type}_{tgt1_year}"
        src2_node = f"{src2_type}_{src2_year}"
        tgt2_node = f"{tgt2_type}_{tgt2_year}"
        

        middle_node1 = f"middle_{src1_node}_{tgt1_node}"
        middle_node2 = f"middle_{src2_node}_{tgt2_node}"



        # 緑線を使ってエッジを追加
        # 例としてmiddle_node1からmiddle_node2にエッジを張る場合
        net.add_edge(
            middle_node1, middle_node2,
            title=edge_content,
            color="red",  # 緑線
            length=50,
            width=4,# 距離の例
        )

        # 必要に応じて middle_edges リストに情報を追加
        middle_edges.append({
            "source": middle_node1,
            "target": middle_node2,
            "content": edge_content
        })

    return middle_edges



def safe_extract_year(year_string):
    try:
        # year_string の最初の4文字を整数として返す
        return int(year_string[:4])
    except ValueError:
        # 変換できない場合は無限大を返してソートの最後に配置
        return float('inf')


# 製品と年代ごとにノードを配置する関数
def arrange_nodes_by_product_and_year(network):
    product_groups = {}

    # 年のリストを収集
    all_years = []

    # ノードをグループ化（中間ノードは除外）
    for node in network.nodes:
        node_id = node["id"]
        if node_id.startswith("middle_"):
            continue

        parts = node_id.split("_")
        if len(parts) < 2:
            continue
        product_type = parts[0]
        year_str = parts[1]
        year = safe_extract_year(year_str)
        if year is None:
            continue  # 年が取れなければスキップ

        all_years.append(year)

        if product_type not in product_groups:
            product_groups[product_type] = []
        product_groups[product_type].append((year, node_id))

    # 年の範囲を決定
    if not all_years:
        return  # 年情報がなければ何もしない
    min_year = min(all_years)
    max_year = max(all_years)

    # スケールの設定: 年差1ごとのピクセル間隔（調整可能）
    x_scale = 170
    

    # 製品ごとに並べ替えと配置
    y_spacing = 450
    base_y = 0

    for product_type, nodes in product_groups.items():
        # 年代順にソート
        nodes.sort(key=lambda x: x[0])
        for year, node_id in nodes:
            node_obj = network.get_node(node_id)
            if node_obj:
                # 年に基づく x 座標の計算
                node_obj["x"] = (year - min_year) * x_scale
                node_obj["y"] = base_y
        base_y += y_spacing

# 中間ノードをソース・ターゲットの中間に配置する関数
def position_middle_nodes(network):
    for node in network.nodes:
        node_id = node["id"]
        if not node_id.startswith("middle_"):
            continue
        
        parts = node_id.split("_")
        if len(parts) < 5:
            continue
        
        source_node_id = f"{parts[1]}_{parts[2]}"
        target_node_id = f"{parts[3]}_{parts[4]}"
        
        source_node = network.get_node(source_node_id)
        target_node = network.get_node(target_node_id)
        
        if source_node and target_node:
            node["x"] = (source_node["x"] + target_node["x"]) / 2
            node["y"] = (source_node["y"] + target_node["y"]) / 2

            
            
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

# -- 1) 6つの製品ファイルだけ抜き出す（先頭6つ） --
product_file_paths = file_paths[:6]  # カメラ, 腕時計, 音楽プレーヤ, 掃除機, テレビ, 電話
extra_file = file_paths[6]  # 'filtered_high_similarity_pairs_with_descriptions.txt'

# -- 2) 円順列のために先頭固定 + 残りを全Permutation (5!) --
fixed_path = product_file_paths[0]  # "カメラ_features_output.txt" を固定とする例
other_5 = product_file_paths[1:]    # 残り5つ
all_permutations_5 = list(itertools.permutations(other_5, 5))  # 5! =120通り

best_network = None
best_crossings = -float('inf')
best_order = None

for perm in all_permutations_5:
    # 3) 現在の並び (円順列)
    current_order = [fixed_path] + list(perm)  # 全6つの順番
    # さらに extra_file を最後に読み込ませたい場合は、ここで追加
    # e.g. combined_paths = current_order + [extra_file]
    # ただし円形配置対象は6製品のみとし、extra_file のデータはノードやエッジを追加するが配置順には影響させない

    combined_paths = current_order + [extra_file]

    # 4) ネットワークを作成して配置
    tmp_net = Network(height="750px", width="100%", notebook=True)
    tmp_added_nodes = set()

    sections = load_data(combined_paths)
    node_titles_dict = load_node_titles(node_title_file_paths)
    process_sections(sections, tmp_net, tmp_added_nodes)
    middle_edges = process_intermediate_edges('filtered_middle_node_edge_contents.txt', tmp_net)
    arrange_nodes_by_product_and_year(tmp_net)

    # 中間ノードをソースとターゲットの間に配置
    position_middle_nodes(tmp_net)
    
    # 物理シミュレーションオフ
    tmp_net.toggle_physics(False)

    # 5) 交点数を計算
    crossings = count_intersections_in_pyvis(tmp_net)
    print(crossings)

    # 6) 最小交点なら更新
    if crossings > best_crossings:
        best_crossings = crossings
        best_order = current_order
        best_network = tmp_net

# 結果表示
print("=== 最小交点数を実現する読み込み順 ===")
for i, p in enumerate(best_order, 1):
    print(f"{i}: {p}")
print(f"交点数: {best_crossings}")

# best_network をHTML出力
best_network.show("network111.html")
print("最終的なネットワークを network11.html に出力しました。")