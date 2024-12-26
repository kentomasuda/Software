# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:38:48 2024

@author: masuda1379
"""

import openai
import json

# OpenAI APIの設定
api_key = 
openai.api_key = api_key

# プロダクト名を指定（カメラ、腕時計など）
product_name = "掃除機"  # 必要に応じて変更可能

# ファイルの読み込み
input_file_path = f'{product_name}_features_year.txt'  # 入力ファイル名に製品名を反映
output_file_path = f'{product_name}_features_output.txt'  # 出力ファイル名に製品名を反映
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# セクションごとに分割
sections = content.strip().split('\n\n')

# 各年代の抽出
years = []
for section in sections:
    lines = section.split('\n')
    year = lines[0]  # 最初の行が年代
    years.append(year)

# 抽出した年代を表示
print(years)

# 新機能を取得する関数
def ask_openai(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=9000,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # 最初の行に「-1989年発売のカメラ」を追加
    output_file.write(f"-1989年発売の{product_name}\n")

    # 過去の機能リストを初期化
    past_features = []
    
    # 最初のセクションを処理
    if sections:
        first_section = sections[0].split('\n')
        first_year_line = first_section[0]
        output_file.write(f"{first_year_line}\n")
    
        # 最初の質問を生成
        question = f"""
    魅力的（Attractiveness） 製品の全体的な印象。ユーザーはそれを好きか嫌いか？
    明瞭さ（Perspicuity） 製品を使い始めるのは簡単か、使い方を学ぶのは容易か？
    効率性（Efficiency） ユーザーは余計な努力なしにタスクを解決できるか？反応は速いか？
    信頼性（Dependability） ユーザーはインタラクションをコントロールできていると感じるか？安全で予測可能か？
    刺激（Stimulation） 製品を使うことは刺激的でモチベーションが上がるか？楽しさを感じるか？
    新規性（Novelty） 製品のデザインは創造的か？ユーザーの興味を引くか？
    
    {first_year_line}発売の{product_name}に関して。上記の六項目を意識して、その年に初めて登場した機能、ユーザ体験を教えて。
    生成結果は
    具体的な機能・ユーザ体験名
    その機能・ユーザ体験を持つ具体的な製品名
    その製品名の具体的な発売日
    その機能・ユーザ体験の説明
    その機能・ユーザ体験が六項目のどれに属するか
    の五つの項目で5個記述して。
    """
    
        answer = ask_openai(question)
    
        features = []
        for line in answer.split('\n'):
            if "具体的な機能・ユーザ体験名" in line:
                feature = line.split(":", 1)[-1].strip()
                if feature not in features:  # 重複排除
                    features.append(feature)
                    past_features.append(feature)  # 過去のリストに追加
    
        for feature in features:
            output_file.write(f"{feature}\n")
    
        output_file.write("\n")
    
    # 2つ目以降の年代ブロック処理
    previous_year_line = first_year_line

    
    # 各セクションに対する処理
    previous_year_line = first_year_line  # 最初の年代行を記録
    for section in sections[1:]:
        lines = section.split('\n')
    
        # 年代行を取得
        year_line = lines[0]
    
        # プロンプトに過去の機能を追加
        past_features_str = ', '.join(past_features) if past_features else "なし"
        question = f"""
    魅力的（Attractiveness） 製品の全体的な印象。ユーザーはそれを好きか嫌いか？
    明瞭さ（Perspicuity） 製品を使い始めるのは簡単か、使い方を学ぶのは容易か？
    効率性（Efficiency） ユーザーは余計な努力なしにタスクを解決できるか？反応は速いか？
    信頼性（Dependability） ユーザーはインタラクションをコントロールできていると感じるか？安全で予測可能か？
    刺激（Stimulation） 製品を使うことは刺激的でモチベーションが上がるか？楽しさを感じるか？
    新規性（Novelty） 製品のデザインは創造的か？ユーザーの興味を引くか？
    
    {year_line}発売の{product_name}に関して。上記の六項目を意識して、その年に初めて登場した機能、ユーザ体験を教えてください。
    ただし、以下の機能に含まれていない機能のみに絞って回答してください：
    {past_features_str}
    
    生成結果は
    具体的な機能・ユーザ体験名
    その機能・ユーザ体験を持つ具体的な製品名
    その製品名の具体的な発売日
    その機能・ユーザ体験の説明
    その機能・ユーザ体験が六項目のどれに属するか
    の五つの項目で5個記述して。
    """
        print(f"Question for {year_line}: {question}")
    
        # API呼び出し
        answer = ask_openai(question)
    
        # "具体的な機能・ユーザ体験名"を含む行を抽出
        features = []
        for line in answer.split('\n'):
            if "具体的な機能・ユーザ体験名" in line:
                # ":"以降の内容を取得
                feature = line.split(":", 1)[-1].strip()
                if feature not in features:  # 重複排除
                    features.append(feature)
                    past_features.append(feature)  # 過去機能リストに追加
    
        # ファイルに書き込み
        if previous_year_line:
            output_file.write(f"{previous_year_line}\n")  # 前の年代行を先頭に書き込み
    
        output_file.write(f"{year_line}\n")  # 現在の年代行
    
        for feature in features:
            output_file.write(f"{feature}\n")
    
        output_file.write("\n")  # 各年代ブロックの区切り
    
        previous_year_line = year_line  # 現在の年代行を記録
