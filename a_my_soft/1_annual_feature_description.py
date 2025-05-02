# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:15:51 2025

@author: masuda1379
"""

import openai

# OpenAI APIキーの設定
api_key = 
openai.api_key = api_key

import sys
import os
sys.path.append(os.pardir)

def ask_gpt(question):
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


def get_config():
    """
    複数の製品名、開始年、終了年をまとめて入力させる
    カメラ, 腕時計, 音楽プレーヤー, テレビ, 電話, 掃除機
    """
    # カンマ区切りで複数製品を入力 (例: "カメラ, 腕時計, 音楽プレーヤー")
    product_names_input = input("製品名を複数入力してください（例: カメラ, 腕時計）: ")
    # カンマ区切りを分割・strip()で前後空白を除去
    product_names_list = [p.strip() for p in product_names_input.split(",") if p.strip()]

    start_year = int(input("開始年を入力してください（例: 1990）: "))
    end_year = int(input("終了年を入力してください（例: 2024）: "))
    return product_names_list, start_year, end_year

def extract_features(json_text):
    """
    生成されたJSON形式のテキストから機能を抽出する関数
    """
    features = []
    for line in json_text.splitlines():
        if '"機能":' in line:
            # "機能": "具体的な機能内容" の部分を抽出
            feature = line.split(': ', 1)[1].strip().strip('",')
            features.append(feature)
    return features

def main():
    # 1. 入力から設定を取得
    product_names_list, start_year, end_year = get_config()

    # 2. メインループ：入力された複数の製品に対して繰り返し実行
    for product_name in product_names_list:
        # 指定された年範囲をリスト化
        year_ranges = list(range(start_year, end_year + 1))

        generated_text = ""  # 全年分のJSONレスポンスを連結する変数
        all_features = []    # 全年分の機能を保存するリスト

        # 3. 指定の年ごとにGPTへ問い合わせ
        for year in year_ranges:
            question = f"""
            {year}年発売の{product_name}の特徴的な機能を簡潔に羅列してください。
            またその機能を持った具体的な製品名とその製品名の具体的な発売日も上げてください。
            日本語で
            機能
            具体的な製品名
            具体的な発売日
            の三項目でjson形式で可能な限り多く、最大30個上げてください。
            """

            response = ask_gpt(question)
            
            print(f"[DEBUG] {year}年 の {product_name} に関するレスポンス:\n{response}\n")
            
            # レスポンスを連結変数に追加（必要に応じて使うなら）
            generated_text += response + "\n\n"
            
            # 現在の年のレスポンスから特徴を抽出し、リストに追加
            features = extract_features(response)
            all_features.extend(features)
            
            # 年ごとの区切りとして空行
            all_features.append("")

        # 最後の空行を削除（もし余計な空行が気になる場合）
        if all_features and all_features[-1] == "":
            all_features.pop()

        # 4. 出力ファイル名（製品名に合わせる）
        output_filename = f"{product_name}_features.txt"

        # リストの内容をファイルに書き込む
        with open(output_filename, "w", encoding="utf-8") as f:
            for feature in all_features:
                if feature == "":
                    f.write("\n")  # 区切りの空行
                else:
                    f.write(feature + "\n")

        print(f"\n[INFO] {product_name} の機能抽出結果を {output_filename} に出力しました。\n")

if __name__ == "__main__":
    main()
