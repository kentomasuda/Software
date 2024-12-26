# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 18:14:28 2024

@author: masuda1379
"""

import re
import openai

# OpenAI APIキーを設定
api_key = 
openai.api_key = api_key

# 「共通性生成リスト.txt」のファイルパスを指定
file_path = "共通性生成リスト.txt"

# ファイルを読み込む
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()


# 製品名と発売年（または年範囲）を抽出する関数
def extract_product_info(line):
    # 製品名と発売年を識別するための正規表現（年範囲も対応）
    pattern = r"(\d{4}-\d{4}年|\d{4}年)発売の([^\n]+?)(?=\d{4}-\d{4}年|\d{4}年|$)"
    matches = re.findall(pattern, line)
    
    products = []
    for year_range, product in matches:
        # 年範囲をそのまま保持し、「と」を削除
        product = product.replace("と", "").strip()
        products.append({"name": product, "release_year": year_range})
    
    # 製品情報を表示（デバッグ用）
    print(products)
    
    return products
# 各行に対してプロンプトを生成
prompts = []
for line in lines:
    # 製品情報を抽出
    products = extract_product_info(line)
    
    # 製品名と発売年を元にプロンプトを生成
    product_descriptions = "と".join([f"{p['release_year']}発売の{p['name']}" for p in products])
    product_names = "、".join([p["name"] for p in products])
    release_years = "、".join([p["release_year"] for p in products])
    
    # プロンプトのテンプレートを更新
    prompt = f"""
    {product_descriptions}の特徴的で共通した機能は何か。
    その機能とその機能を持つ具体的な製品名と発売日について
    特徴的な機能
    その{products[0]['name']}の製品名
    その{products[1]['name']}の製品名
    その{products[0]['name']}の発売日
    その{products[1]['name']}の発売日
    のように五項目でjson形式で日本語で5つ答えろ。
    発売年の整合性が取れているか注意すること。
    また５つこたえること。
    """
    
    prompts.append(prompt)

# 生成されたプロンプトを表示
for prompt in prompts:
    print(prompt)

def generate_info(prompts):
    different_responses = []
    for prompt in prompts:
        # プロンプトを構成してAPIに送信
        question = f"{prompt}"
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=9000,
            temperature=0
        )
        different_responses.append(response.choices[0].message.content)
    return different_responses

results = generate_info(prompts)

# 結果をファイルに保存
output_filename = "別製品間共通性.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    for item in results:
        output_file.write(f"{item}\n")

print(f"結果が {output_filename} に保存されました。")