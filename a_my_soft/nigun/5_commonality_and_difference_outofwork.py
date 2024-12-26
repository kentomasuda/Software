    # -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:46:13 2024

@author: masuda1379

5,似ているものの差異性、似ていないものの共通性を抽出
"""

import openai
import json

# OpenAI APIキーを設定
api_key =  
openai.api_key = api_key

# 読み込むファイル名
file_name = "年代製品間類似度.txt"

# リストの初期化
similar_prompts = []
different_prompts = []

# ファイル読み込み
with open(file_name, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    # 現在のセクション（similar, differentなど）を追跡
    current_section = None
    # 行ごとに処理
    for line in lines:
        line = line.strip()
        
        # セクションの切り替え
        if line == "similar:":
            current_section = "similar"
        elif line == "different:":
            current_section = "different"
        elif line == "middle:":
            current_section = "middle"
        elif line:  # 空行でない場合
            # 現在のセクションに応じてリストに追加
            if current_section == "similar":
                similar_prompts.append(line)
            elif current_section == "different":
                different_prompts.append(line)

# 結果の確認
print("similar_prompts = ", similar_prompts)
print("different_prompts = ", different_prompts)

# OpenAI APIでsimilarセクションを処理
def generate_similar_info(prompts):
    similar_responses = []
    for prompt in prompts:
        # プロンプトを構成してAPIに送信
        question = f"{prompt} の特徴的で異なっている機能は何か。具体的な製品名とその機能について\n特徴的な機能\nその機能が含まれている製品名\nその機能が含まれていない製品名\nのように三項目でjson形式で日本語で5つ答えろ。"
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=4095,
            temperature=0
        )
        similar_responses.append(response.choices[0].message.content)
    return similar_responses

# OpenAI APIでdifferentセクションを処理
def generate_different_info(prompts):
    different_responses = []
    for prompt in prompts:
        # プロンプトを構成してAPIに送信
        question = f"{prompt} の特徴的で共通した機能は何か。具体的な製品名とその機能について\n特徴的な機能\n腕時計の製品名\nカメラの製品名\nのように三項目でjson形式で日本語で5つ答えろ。"
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=4095,
            temperature=0
        )
        different_responses.append(response.choices[0].message.content)
    return different_responses

# 結果を取得
similar_results = generate_similar_info(similar_prompts)
different_results = generate_different_info(different_prompts)

# 結果をファイルに保存
output_filename = "n共通性・差異性.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.write("similar:\n")
    for item in similar_results:
        output_file.write(f"{item}\n")
    
    output_file.write("\ndifferent:\n")
    for item in different_results:
        output_file.write(f"{item}\n")

print(f"結果が {output_filename} に保存されました。")


