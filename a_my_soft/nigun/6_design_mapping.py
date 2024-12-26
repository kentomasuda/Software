# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:28:20 2024

@author: masuda1379
"""
from pyvis.network import Network

# ネットワークオブジェクトを作成
net = Network(height="750px", width="100%", notebook=True)

# カメラのノード（画像を使用）
net.add_node(1, label="Camera 1", shape="image", image="https://free-icons.net/wp-content/uploads/2020/07/pcsp019.png")
net.add_node(2, label="Camera 2", shape="image", image="https://free-icons.net/wp-content/uploads/2020/07/pcsp019.png")
net.add_node(3, label="Camera 3", shape="image", image="https://free-icons.net/wp-content/uploads/2020/07/pcsp019.png")

# 腕時計のノード（画像を使用）
net.add_node(4, label="Watch 1", shape="image", image="https://nureyon.com/sample/66/wrist_watch-2-p2.svg?1601963557")
net.add_node(5, label="Watch 2", shape="image", image="https://nureyon.com/sample/66/wrist_watch-2-p2.svg?1601963557")
net.add_node(6, label="Watch 3", shape="image", image="https://nureyon.com/sample/66/wrist_watch-2-p2.svg?1601963557")

# エッジ（リンク）を追加（例: カメラと腕時計の関係を示すリンク）
net.add_edge(1, 4, title="Camera 1 ↔ Watch 1")
net.add_edge(2, 5, title="Camera 2 ↔ Watch 2")
net.add_edge(3, 6, title="Camera 3 ↔ Watch 3")
net.add_edge(1, 2, title="Camera 1 ↔ Camera 2")
net.add_edge(4, 5, title="Watch 1 ↔ Watch 2")

# 物理シミュレーション（レイアウト調整）を有効化
net.toggle_physics(True)

# HTMLで保存し、ブラウザで表示
net.show("camera_watch_network.html")
