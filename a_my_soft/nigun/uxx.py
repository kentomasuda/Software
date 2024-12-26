# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:17:56 2024

@author: masuda1379
"""

import openai
from tqdm import tqdm

# OpenAI APIキーの設定
api_key = "
openai.api_key = api_key

def fetch_camera_data(year):
    """特定の年のカメラに関するデータを取得する"""
    try:
        #question = f"{year}年発売のカメラで新しいユーザ体験を提供し、注目された製品とその内容を3つ教えて。結果はjson型式で製品名、発売日、新しい体験の名前、新しい体験の内容の四項目書いて"
        #question = f"{year}年発売のカメラにおいて、新しい特徴的な機能や仕組みを提案してください。この機能は、従来の技術的な性能向上ではなく、ユーザーがその製品を使う際に実用性を感じられるものを目指しています。その内容を3つ教えて。結果はjson型式でその機能を持つ具体的な製品名、その製品の発売日、新しい機能の名前、新しい機能の内容の四項目書いて"
        question = f"""
魅力的（Attractiveness） 製品の全体的な印象。ユーザーはそれを好きか嫌いか？
明瞭さ（Perspicuity） 製品を使い始めるのは簡単か、使い方を学ぶのは容易か？
効率性（Efficiency） ユーザーは余計な努力なしにタスクを解決できるか？反応は速いか？
信頼性（Dependability） ユーザーはインタラクションをコントロールできていると感じるか？安全で予測可能か？
刺激（Stimulation） 製品を使うことは刺激的でモチベーションが上がるか？楽しさを感じるか？
新規性（Novelty） 製品のデザインは創造的か？ユーザーの興味を引くか？

{year}年発売のカメラに関して。上記の六項目を意識して、その年に初めて登場した機能、ユーザ体験を教えて。
生成結果は
具体的な機能・ユーザ体験名
その機能・ユーザ体験を持つ具体的な製品名
その製品名の具体的な発売日
その機能・ユーザ体験の説明
その機能・ユーザ体験が六項目のどれに属するか
の五つの項目でjson形式で20個記述して。
        """
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=4095,
            temperature=1
        )
        # 応答のテキストを取得
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching data for year {year}: {e}")
        return None

def main():
    # 年代を指定
    start_year = 2005
    end_year = 2010
    
    # 結果を格納するリスト
    results = []
    
    for year in tqdm(range(start_year, end_year + 1)):
        data = fetch_camera_data(year)
        results.append(f"{year}年の結果:\n{data}\n")
    
    # 結果をテキスト形式で保存
    with open("camera_ux.txt", "w", encoding="utf-8") as f:
        f.writelines(results)
    
    print("データ収集が完了しました。結果は camera_ux.txt に保存されています。")

if __name__ == "__main__":
    main()
