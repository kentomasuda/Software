# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:18:08 2024

@author: masuda1379
"""
import sys
import os
sys.path.append(os.pardir)
from pyvis.network import Network
import re
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_

# ネットワークオブジェクトを作成
net = Network(height="750px", width="100%", notebook=True)

# ファイルリスト
file_paths = ['カメラ_features_output.txt', '腕時計_features_output.txt', '音楽プレーヤー_features_output.txt', '掃除機_features_output.txt', 'テレビ_features_output.txt', '電話_features_output.txt', 'マップ反映要素.txt']

# ノードの重複を避けるためのセット
added_nodes = set()

# 年代を抽出する関数
def extract_year_range(text):
    # 「-XXXX年発売」に一致する場合
    match = re.match(r'-(\d{4})年発売', text)
    if match:
        return f"-{match.group(1)}"
    
    # 「XXXX-XXXX」に一致する場合
    match_range = re.match(r'(\d{4})-(\d{4})', text)
    if match_range:
        return f"{match_range.group(1)}-{match_range.group(2)}"

    # 「XXXX年」に一致する場合
    match_single = re.match(r'(\d{4})年', text)
    if match_single:
        return match_single.group(1)
    
    # どれにも一致しない場合
    return text

# 製品の種類を判断する関数
def get_product_type(text):
    if "\u30ab\u30e1\u30e9" in text:
        return "カメラ", "lightblue"
    elif "\u8155\u6642\u8a08" in text:
        return "腕時計", "lightgreen"
    elif "\u97f3\u697d\u30d7\u30ec\u30fc\u30e4\u30fc" in text:
        return "音楽プレーヤー", "orange"
    elif "\u6383\u9664\u6a5f" in text:
        return "掃除機", "purple"
    elif "\u30c6\u30ec\u30d3" in text:
        return "テレビ", "pink"
    elif "\u96fb\u8a71" in text:
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
    middle_edges = []  # 青い矢印の情報を保持

    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) < 2:
            continue
        
        # 一行目と二行目から情報を取得
        source = extract_year_range(lines[0])
        target = extract_year_range(lines[1])
        source_type, source_color = get_product_type(lines[0])
        target_type, target_color = get_product_type(lines[1])
        
        if not source_type or not target_type:
            continue
        
        # 製品タイプごとにノード名を一意化
        source_node = f"{source_type}_{source}"
        target_node = f"{target_type}_{target}"
        edge_content = '\n'.join(lines[2:]) if len(lines) > 2 else "\u8aac\u660e\u306a\u3057"
        
        # ノードを追加（重複チェック）
        if source_node not in added_nodes:
            net.add_node(
                source_node,
                label=f"{source_type}\n{source}",
                size=30,
                shape="box",
                font=dict(size=14, color="black"),
                color=source_color
            )
            added_nodes.add(source_node)
        
        if target_node not in added_nodes:
            net.add_node(
                target_node,
                label=f"{target_type}\n{target}",
                size=30,
                shape="box",
                font=dict(size=14, color="black"),
                color=target_color
            )
            added_nodes.add(target_node)
        
        # 同じ製品タイプの場合、青い矢印の前後に小さなノードを挿入
        if source_type == target_type:  # 同じ製品の場合
            middle_node = f"middle_{source_node}_{target_node}"
            net.add_node(middle_node, label=" ", size=1, color="rgba(0, 0, 0, 0)", shape="dot", opacity=0)
            
            # 青い矢印を作成
            net.add_edge(source_node, middle_node, title=edge_content, color="blue", length=5)
            net.add_edge(middle_node, target_node, title=edge_content, color="blue", arrows="to", length=5)
            
            # 中間ノードのエッジ情報を保存
            middle_edges.append({
                "middle_node": middle_node,
                "target_node": target_node,
                "content": edge_content
            })
        else:  # 異なる製品の場合
            net.add_edge(source_node, target_node, title=edge_content, color="red", length=200)



    # 異なる target_node を持つ青い矢印の比較
    threshold = 0.99  # 類似度閾値
    for i in range(len(middle_edges)):
        for j in range(i + 1, len(middle_edges)):
            edge1 = middle_edges[i]
            edge2 = middle_edges[j]
    
            # target_node の製品タイプが異なる場合のみ比較
            product_type1 = edge1["target_node"].split("_")[0]  # カメラまたは腕時計を取得
            product_type2 = edge2["target_node"].split("_")[0]
    
            if product_type1 != product_type2:  # 異なる製品タイプの場合
                # エッジ説明を改行で分割して各機能を取得
                features1 = edge1["content"].split('\n')
                features2 = edge2["content"].split('\n')
    
                # 各機能をペアで比較し、類似度が高い組を探す
                for f1 in features1:
                    for f2 in features2:
                        similarity = SentenceTransformers_.calc_sim(f1, f2, cached=False)
                        print(similarity)
                        if similarity > threshold:
                            # 緑線を追加し、説明に類似した機能を表示
                            net.add_edge(
                                edge1["middle_node"],
                                edge2["middle_node"],
                                color="green",
                                title=f"{f1}\n&\n{f2}",
                                width=2
                            )

def remove_lonely_middle_nodes(network):
    nodes = network.get_nodes()
    edges = network.get_edges()
    middle_nodes = [node for node in nodes if node.startswith("middle_")]

    nodes_to_remove = []
    edges_to_remove = []

    for middle_node in middle_nodes:
        # 中間ノードに接続されているエッジを取得
        connected_edges = [edge for edge in edges if edge['from'] == middle_node or edge['to'] == middle_node]
        
        if len(connected_edges) <= 2:  # 接続エッジが2本以下
            nodes_to_remove.append(middle_node)
            edges_to_remove.extend(connected_edges)

            # 2本のエッジが接続されている場合、代わりに直接接続
            if len(connected_edges) == 2:
                edge1, edge2 = connected_edges
                # 直接接続のノードを決定
                node1 = edge1['from'] if edge1['from'] != middle_node else edge1['to']
                node2 = edge2['from'] if edge2['from'] != middle_node else edge2['to']
                # 中間ノードが保持していた情報を引き継ぐ
                combined_title = f"{edge1.get('title', '')} + {edge2.get('title', '')}"
                network.add_edge(node1, node2, title=combined_title, color="blue", length=100)

    # 削除対象をログとして出力
    print("削除されるノード:", nodes_to_remove)
    print("削除されるエッジ:", edges_to_remove)
    
    # エッジを削除
    network.edges = [edge for edge in network.edges if edge not in edges_to_remove]
    
    # ノードを削除
    network.nodes = [node for node in network.nodes if node not in nodes_to_remove]

    # ネットワークを再描画
    network.show("network.html")




# データ読み込みと処理
sections = load_data(file_paths)
process_sections(sections)

# 孤立した中間ノードを削除
remove_lonely_middle_nodes(net)

# 物理シミュレーションを有効化
net.toggle_physics(True)

# HTMLで保存して表示
net.show("network.html")

"""
# ネットワーク設定を詳細に指定
net.set_options('''
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -8000,
      "centralGravity": 0.3,
      "springLength": 150,
      "springConstant": 0.04,
      "damping": 0.09
    }
  },
  "nodes": {
    "shape": "dot",
    "scaling": {
      "min": 10,
      "max": 30
    }
  }
}
''')
"""