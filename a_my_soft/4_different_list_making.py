import numpy as np
import sys
import os
import itertools
sys.path.append(os.pardir)

# カスタムモジュールをインポート
sys.path.append('C:/path/to/your/sentence_transformers_srclib')
from sentence_transformers_srclib.sentence_transformers1_ import SentenceTransformers_


# 入力ファイルパスと製品リスト
file_path = "c:\\users\\masuda1379\\documents\\software\\a_my_soft\\"  # ファイルのディレクトリ
products = ["電話", "腕時計", "カメラ", "テレビ", "音楽プレーヤー", "掃除機"]

# ファイルからデータを読み取る関数
def read_features(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read()
    sections = data.split('\n\n')
    features_by_year = {}
    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) > 1:
            year = lines[0].strip()
            features = lines[1:]
            features_by_year[year] = features
    return features_by_year

# すべての製品ファイルのデータをロード
data_by_product = {}
for product in products:
    file_name = os.path.join(file_path, f"{product}_features_year.txt")
    data_by_product[product] = read_features(file_name)

# 製品組み合わせごとの類似度計算
def find_least_similar_pair(data_by_product, products):
    results = []

    for prod1, prod2 in itertools.combinations(products, 2):
        features1 = data_by_product[prod1]
        features2 = data_by_product[prod2]

        lowest_similarity = float('inf')
        lowest_pair = None

        for year1, features_list1 in features1.items():
            for year2, features_list2 in features2.items():
                simmaxs1, simmaxs2 = SentenceTransformers_.calc_texts_sims(features_list1, features_list2)
                combined_sims = simmaxs1 + simmaxs2
                average_similarity = np.mean(combined_sims)

                print(f"年: {year1}と{year2} の特徴量: 類似度={average_similarity:.4f}")

                if average_similarity < lowest_similarity:
                    lowest_similarity = average_similarity
                    lowest_pair = (year1, prod1, year2, prod2)

        results.append((lowest_pair, lowest_similarity))

    return sorted(results, key=lambda x: x[1])

# 結果を計算し出力
results = find_least_similar_pair(data_by_product, products)
for (year1, prod1, year2, prod2), similarity in results:
    print(f"{year1}のと{year2}のの類似度: {similarity:.4f}")

# 最小類似度の組み合わせ
least_similar = results[0]
print("最小類似度の組み合わせ:", least_similar)

# 結果をファイルに書き込む
output_file = "共通性生成リスト.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    output_file.write("\ndifferent:\n")
    for (year1, prod1, year2, prod2), similarity in results:
        f.write(f"{year1}と{year2}\n")


print(f"計算結果が '{output_file}' に出力されました。")
