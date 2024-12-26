# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 17:37:14 2024

@author: masuda1379

３，各製品について年代分けを行って、そのファイルを結合させて一つのファイルにまとめる
"""
def combine_two_files(file1, file2, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in [file1, file2, file3, file4, file5, file6]:
            with open(file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n')  # ファイル間に空行を追加

    print(f"{file1} and {file2} have been combined into {output_file}")


# ファイルを統合する処理


# ユーザーからのファイル名の指定
file1 = '腕時計_features_year.txt'
file2 = 'カメラ_features_year.txt'
file3 = 'テレビ_features_year.txt'
file4 = '音楽プレーヤー_features_year.txt'
file5 = '掃除機_features_year.txt'
file6 = '電話_features_year.txt'
output_file = '腕時計_カメラ_テレビ_音楽プレーヤー_掃除機_電話_features_year.txt'

combine_two_files(file1, file2, output_file)
