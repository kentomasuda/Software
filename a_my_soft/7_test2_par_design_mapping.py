# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 21:40:56 2025

@author: masuda1379
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 17:00:17 2025

@author: masuda1379
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 13:55:58 2025

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

node_title_file_paths = ['カメラ_features_year.txt', '腕時計_features_year.txt', 
              '音楽プレーヤー_features_year.txt', '掃除機_features_year.txt', 
              'テレビ_features_year.txt', '電話_features_year.txt']

#intermediate_edges_file_path = ['filtered_middle_node_edge_contents.txt']

# ノードの重複を避けるためのセット
added_nodes = set()

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
                font=dict(size=30, color="black"),
                #color=source_color
                borderWidth=2,  # 淵の太さを4に設定
                color={'border': source_color, 'background': 'white'}
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
            print(target_node)
            net.add_node(
                target_node,
                label=f"{target_type}\n{target}",
                title=target_title, 
                size=80,
                shape="box",
                font=dict(size=30, color="black"),
                #color=source_color
                borderWidth=2,  # 淵の太さを4に設定
                color={'border': target_color, 'background': 'white'}
            )
            added_nodes.add(target_node)

        # エッジの追加
        if source_type == target_type:
            # 中間ノードがある
            middle_node = f"middle_{source_node}_{target_node}"
            net.add_edge(source_node, middle_node, title=edge_content, color="blue", width=2, length=5)
            net.add_edge(middle_node, target_node, title=edge_content, color="blue", width=2, arrows="to", length=5)
            
            middle_edges.append({
                "middle_node": middle_node,
                "target_node": target_node,
                "content": edge_content
            })
        else:
            # 異なる製品タイプ
            net.add_edge(source_node, target_node, title=edge_content, color="green",width=2, length=200)

    return


def process_intermediate_edges(file_path):
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
        

        # ノード追加（存在しない場合のみ）



        # 中間ノードを生成し追加（ここでは例として各ペア毎に中間ノードを作成）
        middle_node1 = f"middle_{src1_node}_{tgt1_node}"
        middle_node2 = f"middle_{src2_node}_{tgt2_node}"

        for m_node in [middle_node1, middle_node2]:
            if m_node not in added_nodes:
                net.add_node(
                    m_node,
                    label=" ",
                    size=1,
                    color="rgba(0, 0, 0, 0)",
                    shape="dot",
                    opacity=0
                )
                added_nodes.add(m_node)

        # 緑線を使ってエッジを追加
        # 例としてmiddle_node1からmiddle_node2にエッジを張る場合
        net.add_edge(
            middle_node1, middle_node2,
            title=edge_content,
            color="red",  # 緑線
            length=50,
            width=2
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
    x_spacing = 400
    y_spacing = 300
    base_y = 0

    # 各製品タイプごとにノード配置
    for product_type, nodes in product_groups.items():
        base_x = 0
        for year, node_id in nodes:
            node_obj = network.get_node(node_id)
            if node_obj:
                node_obj["x"] = base_x
                node_obj["y"] = base_y
            base_x += x_spacing
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


# データ読み込みと処理
sections = load_data(file_paths)

node_titles_dict = load_node_titles(node_title_file_paths)

#print(node_titles_dict)

process_sections(sections)
process_intermediate_edges('filtered_middle_node_edge_contents.txt')

# ノードを製品と年代ごとに配置（中間ノードは除外される）
arrange_nodes_by_product_and_year(net)

# 中間ノードをソースとターゲットの間に配置
position_middle_nodes(net)

# 物理シミュレーションを無効化
net.toggle_physics(False)

# HTMLで保存して表示
net.show("network_par.html")