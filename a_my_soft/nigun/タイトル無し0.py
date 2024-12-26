# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:58:54 2024

@author: masuda1379
"""

from pyvis.network import Network

# ネットワークを作成
net = Network(directed=True)

# ノードを追加
net.add_node(1, label="Node 1")
net.add_node(2, label="Node 2")
net.add_node(3, label="Node 3")

# 片矢印を設定（Node 1 → Node 2）
net.add_edge(1, 2, arrows="to", color="green", width=2)

# 両矢印を設定（Node 2 ↔ Node 3）
net.add_edge(2, 3, arrows="to;from", color="blue", width=2)

# HTML ファイルを保存
net.write_html("arrows_example.html")
print("グラフが arrows_example.html に保存されました。ブラウザで開いてください。")
