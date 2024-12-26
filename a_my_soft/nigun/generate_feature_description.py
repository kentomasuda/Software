
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 00:24:59 2024

@author: 7491939865
"""
import numpy as np
import os
import openai

# OpenAI APIキーの設定
api_key = "
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

# 刻み幅と製品名をユーザーから入力できるように
def get_year_ranges():
    year_ranges = []
    
    # 製品名を手動入力
    product_name = input("製品名を入力してください（例: カメラ）: ")
    # 年の範囲と刻み幅を手動入力
    start_year = int(input("開始年を入力してください（例: 1980）: "))
    end_year = int(input("終了年を入力してください（例: 2020）: "))
    interval = int(input("何年刻みにしますか？（例: 5）: "))
    

    for year in range(start_year, end_year, interval):
        year_ranges.append((year, year + interval))
    
    return year_ranges, product_name

year_ranges, product_name = get_year_ranges()

generated_text = ""

for a, b in year_ranges:
    # 質問に製品名を動的に挿入
    question = f"{a}年から{b}年の{product_name}の基本的な機能、特徴的な機能をすべて箇条書きせよ。ただし{product_name}を主語とする簡潔な能動態の文で羅列にすること。"
    
    
    response = ask_gpt4(question)
    
    print(f"期間 {a}年〜{b}年 の{product_name}の機能:\n{response}\n")
    
    generated_text += response + "\n\n"

# 空行に挟まれた3行以下の段落を削除する
def filter_short_paragraphs(text):
    paragraphs = text.split("\n\n")  # 空行で段落に分割
    filtered_paragraphs = [p for p in paragraphs if len(p.split("\n")) > 3]  # 4行以上の段落を残す
    return "\n\n".join(filtered_paragraphs)  # 残った段落を空行で再度連結

filtered_text = filter_short_paragraphs(generated_text)

# 生成されたテキストを表示
print(filtered_text)

# 生成されたテキストをファイルに保存
with open('filtered_generated_text.txt', 'w', encoding='utf-8') as file:
    file.write(filtered_text)

print("フィルタリングされたテキストがファイルに保存されました。")
