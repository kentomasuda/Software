
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 00:24:59 2024

@author: 7491939865

1、一年ごとの機能記述を生成
"""
import numpy as np
import os
import openai
import json

# OpenAI APIキーの設定
api_key = 
openai.api_key = api_key

def ask_gpt4(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=10000,
            temperature=0,
            top_p = 1.0,
            frequency_penalty = 0,
            presence_penalty = 0
            
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

def get_year_ranges():
    year_ranges = []
    product_name = input("製品名を入力してください（例: カメラ）: ")
    start_year = int(input("開始年を入力してください（例: 1990）: "))
    end_year = int(input("終了年を入力してください（例: 2024）: "))

    for year in range(start_year, end_year + 1):
        year_ranges.append(year)
    
    return year_ranges, product_name

year_ranges, product_name = get_year_ranges()
generated_text = ""

for year in year_ranges:
    question = f"{year}年発売の{product_name}の特徴的な機能を簡潔な能動態の分で羅列しろ。またその機能を持った具体的な製品名とその製品名の具体的な発売日も上げろ。日本語で\n機能\n具体的な製品名\n具体的な発売日\nのようにjson形式で30個上げろ。"
    response = ask_gpt4(question)
    
    print(f"期間 {year}年 の{product_name}の機能:\n{response}\n")
    
    generated_text += response + "\n\n"

# 生成されたJSON形式のテキストから機能を抽出
def extract_features(json_text):
    features = []
    for line in json_text.splitlines():
        # "機能"が含まれる行をチェック
        if '"機能":' in line:
            # "機能": "高解像度液晶を搭載する。" の部分を抽出
            feature = line.split(': ')[1].strip().strip('",')  # ':'の後の部分を取り出し、余分な文字を削除
            features.append(feature)
        
        # "]"が含まれる行が来たら空行を挿入
        elif ']' in line:
            features.append("")  # 空行を挿入
            
    # 最後の空行を削除
    if features and features[-1] == "":
        features.pop()

    return features

# 抽出した機能記述
features = extract_features(generated_text)

# テキストファイルに保存
file_name = f"{product_name}_features.txt"
with open(file_name, 'w', encoding='utf-8') as file:
    for feature in features:
        file.write(feature + '\n')

print(f"{product_name}の特徴的な機能がファイルに保存されました。")