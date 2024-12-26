# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:28:20 2024

@author: masuda1379
"""
from pyvis.network import Network
import re  # 年代を抽出するために正規表現を使用

# ネットワークオブジェクトを作成
net = Network(height="750px", width="100%", notebook=True)

# データファイルのパス
file_path = 'マップ反映要素.txt'

# ファイル読み込みとデータ処理
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sections = f.read().strip().split('\n\n')  # 空行で区切られたセクションをリストとして取得
    
    return sections

# ノードの重複を避けるためにセットを使用
added_nodes = set()

# アイコンのURL
camera_icon_url = "https://free-icons.net/wp-content/uploads/2020/07/pcsp019.png"
watch_icon_url = "https://nureyon.com/sample/66/wrist_watch-2-p2.svg?1601963557"

# 年代を抽出する関数
def extract_year_range(text):
    # 年代の形式（例: 1998-2002）または単年（例: 2024）を抽出するための正規表現
    match = re.match(r'(\d{4})-(\d{4})', text)  # 年範囲（例: 1998-2002）
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    
    match_single = re.match(r'(\d{4})年', text)  # 単年（例: 2024年）
    if match_single:
        return match_single.group(1)  # 単年の年数（例: 2024）
    
    return text  # 年代が見つからない場合はそのまま返す

# 製品の種類を判断する関数
def get_product_type(text):
    if "カメラ" in text:
        return "カメラ", camera_icon_url
    elif "腕時計" in text:
        return "腕時計", watch_icon_url
    return None, None  # 製品が判別できない場合

# セクションからノードとリンクを追加
def process_sections(sections):
    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) < 8:
            continue  # 行数が不足している場合はスキップ
        
        # ノードの定義（年代だけを抽出）
        node1_year = extract_year_range(lines[0])  # 年代部分を抽出
        node2_year = extract_year_range(lines[1])  # 年代部分を抽出
        relation_type = lines[2]  # "差異性" か "共通性"
        
        # 製品タイプを判別
        node1_type, icon_url1 = get_product_type(lines[0])
        node2_type, icon_url2 = get_product_type(lines[1])
        
        if node1_type is None or node2_type is None:
            continue  # 製品タイプが判別できない場合はスキップ
        
        # リンクの色分け (差異性なら赤、共通性なら緑)
        link_color = 'red' if relation_type == "差異性" else 'blue'
        
        # ノード1の追加（重複チェック）
        if node1_year not in added_nodes:
            net.add_node(node1_year, label=node1_year, image=icon_url1, size=30, shape='image')
            added_nodes.add(node1_year)
        
        # ノード2の追加（重複チェック）
        if node2_year not in added_nodes:
            net.add_node(node2_year, label=node2_year, image=icon_url2, size=30, shape='image')
            added_nodes.add(node2_year)
        
        # リンクの内容を4行目から8行目で結合
        link_content = ' '.join(lines[3:8])  # 4行目から8行目までを結合してリンク内容とする
        
        # リンクの追加
        net.add_edge(node1_year, node2_year, title=link_content, color=link_color)

# データを読み込み、処理してネットワークを作成
sections = load_data(file_path)
process_sections(sections)

# 物理シミュレーション（レイアウト調整）を有効化
net.toggle_physics(True)

# HTMLで保存し、ブラウザで表示
net.show("network.html")

