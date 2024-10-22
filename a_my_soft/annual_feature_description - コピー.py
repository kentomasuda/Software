
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 00:24:59 2024

@author: 7491939865
"""
import numpy as np
import os
import openai

# OpenAI APIキーの設定
api_key = "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"
openai.api_key = api_key

def ask_gpt4(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=4095,
            temperature=0
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error: {str(e)}"

# 刻み幅を一年に固定し、製品名をユーザーから入力できるように
def get_year_ranges():
    year_ranges = []
    
    # 製品名を手動入力
    product_name = input("製品名を入力してください（例: カメラ）: ")
    # 年の範囲を手動入力
    start_year = int(input("開始年を入力してください（例: 1980）: "))
    end_year = int(input("終了年を入力してください（例: 2020）: "))
    

    for year in range(start_year, end_year + 1):  # 終了年も含めて1年刻みで範囲を設定
        year_ranges.append(year)
    
    return year_ranges, product_name

year_ranges, product_name = get_year_ranges()

# 年ごとの機能を格納する辞書
features_by_year = {}

for year in year_ranges:
    # 質問に製品名を動的に挿入
    question = f"{year}年の{product_name}の基本的な機能、特徴的な機能をすべて箇条書きせよ。ただし{product_name}を主語とする簡潔な能動態の文で羅列にすること。またその年に発売されたその機能を持つ具体的な製品名も答えろ。"
    
    response = ask_gpt4(question)
    
    print(f"{year}年 の{product_name}の機能:\n{response}\n")
    
    # 年ごとの機能をリストとして保存
    features_by_year[year] = response.split('\n')

# フィルタリング処理を行う
filtered_text = ""

for year, features in features_by_year.items():
    # 「カメラは」で始まる文だけを抽出
    filtered_features = [feature.strip() for feature in features if feature.strip().startswith(f"{product_name}は")]
    
    # 年ごとに出力し、空行を挿入
    filtered_text += f"{year}年 の{product_name}の機能:\n"
    filtered_text += "\n".join(filtered_features) + "\n\n"  # 年の境界に空行を追加

# フィルタリングされたテキストを表示
print("フィルタリングされた機能:\n")
print(filtered_text)

# フィルタリングされたテキストをファイルに保存
with open('generated_text.txt', 'w', encoding='utf-8') as file:
    file.write(filtered_text)

print("フィルタリングされたテキストがファイルに保存されました。")
