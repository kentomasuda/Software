# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:06:21 2024

@author: masuda1379
"""

from pyvis.network import Network
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ネットワークオブジェクトを作成
net = Network(height="750px", width="100%", notebook=True)

# ファイルリスト
file_paths = ['\u30ab\u30e1\u30e9_features_output.txt', '\u8155\u6642\u8a08_features_output.txt', '\u30de\u30c3\u30d7\u53cd\u6620\u8981\u7d20.txt']

# ノードの重複を避けるためのセット
added_nodes = set()

# アイコンのURL
camera_icon_url = "https://free-icons.net/wp-content/uploads/2020/07/pcsp019.png"
watch_icon_url = "https://nureyon.com/sample/66/wrist_watch-2-p2.svg?1601963557"

# センテンストランスフォーマーのモデルを読み込む
model = SentenceTransformer('all-MiniLM-L6-v2')

# 年代を抽出する関数
def extract_year_range(text):
    match = re.match(r'-(\d{4})\u5e74\u767a\u58f2', text)
    if match:
        return f"-{match.group(1)}"
    
    match_range = re.match(r'(\d{4})-(\d{4})', text)
    if match_range:
        return f"{match_range.group(1)}-{match_range.group(2)}"

    match_single = re.match(r'(\d{4})\u5e74', text)
    if match_single:
        return match_single.group(1)
    
    return text

# 製品の種類を判断する関数
def get_product_type(text):
    if "\u30ab\u30e1\u30e9" in text:
        return "\u30ab\u30e1\u30e9", camera_icon_url
    elif "\u8155\u6642\u8a08" in text:
        return "\u8155\u6642\u8a08", watch_icon_url
    return None, None

# 類似度を計算する関数
def calculate_similarity(text1, text2):
    embeddings = model.encode([text1, text2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity

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
        source_type, source_icon = get_product_type(lines[0])
        target_type, target_icon = get_product_type(lines[1])
        
        if not source_icon or not target_icon:
            continue
        
        # 製品タイプごとにノード名を一意化
        source_node = f"{source_type}_{source}"
        target_node = f"{target_type}_{target}"
        edge_content = '\n'.join(lines[2:]) if len(lines) > 2 else "\u8aac\u660e\u306a\u3057"
        
        # ノードを追加（重複チェック）
        if source_node not in added_nodes:
            net.add_node(
                source_node,
                label=source,
                size=30,
                shape="image",
                image=source_icon
            )
            added_nodes.add(source_node)
        
        if target_node not in added_nodes:
            net.add_node(
                target_node,
                label=target,
                size=30,
                shape="image",
                image=target_icon
            )
            added_nodes.add(target_node)
        
        # 同じ製品タイプの場合、青い矢印の前後に小さなノードを挿入
        if source_type == target_type:  # 同じ製品の場合
            middle_node = f"middle_{source_node}_{target_node}"
            net.add_node(middle_node, label=" ", size=1, color="blue", shape="dot", opacity=0)
            
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
    threshold = 0.8  # 類似度閾値
    for i in range(len(middle_edges)):
        for j in range(i + 1, len(middle_edges)):
            edge1 = middle_edges[i]
            edge2 = middle_edges[j]
    
            # target_node の製品タイプが異なる場合のみ比較
            product_type1 = edge1["target_node"].split("_")[0]  # カメラまたは腕時計を取得
            product_type2 = edge2["target_node"].split("_")[0]
    
            if product_type1 != product_type2:  # 異なる製品タイプの場合
                similarity = calculate_similarity(edge1["content"], edge2["content"])
    
                if similarity > threshold:
                    net.add_edge(
                        edge1["middle_node"],
                        edge2["middle_node"],
                        color="green",
                        title=f"Similarity: {similarity:.2f}",
                        width=2
                    )

# データ読み込みと処理
sections = load_data(file_paths)
process_sections(sections)

# 物理シミュレーションを有効化
net.toggle_physics(True)

# HTMLで保存して表示
net.show("network.html")
