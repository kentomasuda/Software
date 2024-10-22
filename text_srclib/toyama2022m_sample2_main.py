# -*- coding: utf-8 -*-
"""
Toyama2022m sample 2 main

@author: MURAKAMI Tamotsu
@date: 2022-11-21
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from pprint import pprint
from xml.etree import ElementTree

# Library
from edr_lib.edr import Edr
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_ｓｒｃlib.simplepos import SimplePos
from text_srclib.text_similarity import TextSimilarity


"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-11-21
"""

if __name__ == '__main__':

    print('* Main start *')
    
    meaning_id = Edr.ID # EDR
    
    # 以下のいずれか一つを指定し（それ以外はコメントアウト）で実行する。
    # mode = 1 # 見出し語との適合検査
    # mode = 2 # 意味の確認
    mode = 3 # Mode 4 で生成したWord instanceにより類似度計算（大きいものが後ろ）
    # mode = 4 # Word instance 生成のXML表記生成（実行不要）
    
    if mode == 1 or mode == 2 or mode == 4:
        original_words = ['V', '型', 'シリンダー', '左右', '交互', '字', 'エンジン',
                          '気筒', '以上', '多', '化', '直列', '式', '全長',
                          'メリット', '大', '排気量', '比較的', 'ため', '多く',
                          '採用', '年', '代', 'ボディ', '前部', 'クラッシャブルゾーン',
                          '狙い', '直', '部品', '点数', '大衆車', '向け', '小',
                          '不向き', '構造', 'モジュール', '生産', '利点', '内',
                          '爆発', '熱', 'エネルギー', 'ピストン', '上下', '運動',
                          'クランクシャフト', '回転', 'こと', 'タイプ', '基本', '古く',
                          '船舶', '鉄道車両', '航空機', '自動車', '燃料', '燃焼',
                          '作動', '流体', '圧力', '膨張', '力', '往復', '直線',
                          'ついで', 'クランク', '力学', '原動機', '初期', '蒸気',
                          '機関', 'ポンプ', 'よう', '場合', 'まま', 'タービン',
                          'ヴァンケル', 'ロータリーエンジン', '概念', 'レシプロエンジン',
                          '現在', '主流', '中', '吸入', '圧縮', '排気', '行程',
                          'ストローク', 'もの', '内燃', 'ガス', '事', '一連', '動作',
                          'つ', '工程', 'ガソリン', 'おにぎり', 'ローター', '歯車',
                          'エキセントリック', 'シャフト', '際', '吸気', '技術者',
                          'バンケル', '後', '東洋', '工業', '用', '量産', '成功',
                          '長所', '軽量', 'コンパクト', '低', '振動', '騒音', '高',
                          '出力', '走り', '気持ち', '反面', '燃費', '低速', 'トルク',
                          '不足', 'ぎみ', '短所', '英語', 'rotary engine', '動',
                          '機構', '容積', '変化', '動力', '発明', '三角形',
                          '回転子', 'オットーサイクルエンジン', '熱機関', '度', '水平',
                          '対向', '対', '動き', '右', '上死', '点', '左', '使用',
                          '打ち消す', '間', '横', '方向', 'レイアウト', '重心',
                          'Boxer', '理想', 'パワー', 'ユニット', '中心', '左右対称',
                          '互い', '慣性', 'フィール', '提供', 'アクセル', 'ワーク',
                          'レスポンス', 'シーン', 'ドライビング', '他', '形式', '全高',
                          'アドバンテージ', '走行', '安定性', 'ハンドリング', '性能',
                          '約束']
        # 上記の検査結果をふまえ、日本語の表記調整または英語への置き換えを試す。
        original_words.extend(['crushable zone', 'module', 'crankshaft',
                               '鉄道', '車両', 'Wankel', 'reciprocating engine',
                               'エキセントリックだ', '気味', 'Otto cycle engine',
                               '上死点', 'ボクサー', '対称', 'feel', 'work',
                               'driving', 'handling'])
        
        valid_words = []
        invalid_words = []
        
    if mode == 1:
        for word in original_words:
            judge, cands = Edr.check_headword(word, pos=SimplePos.all_(), suggest=True, simmin=0.65)
            pos = cands[0][2]
            if judge and bool(pos & SimplePos.N): # 名詞のみ選択
                lang = cands[0][1]
                print('"{}"({},{}): valid.'.format(word, lang, pos))
                valid_words.append(word)
            else:
                invalid_words.append(word)
                print('"{}": invalid -> {}.'.format(word, cands))
        
        print('valid_words = {}.'.format(valid_words))
        print('invalid_words = {}.'.format(invalid_words))
    
    if mode == 2 or mode == 4:
        for word in original_words:
            judge, cands = Edr.check_headword(word, pos=SimplePos.all_(), suggest=True, simmin=1)
            if judge:
                pos = cands[0][2]
            else:
                pos = None

            if pos and bool(pos & SimplePos.N): # 名詞のみ選択
                lang = cands[0][1]
                print('"{}"({},{}): valid.'.format(word, lang, pos))
                valid_words.append(word)
            else:
                invalid_words.append(word)
                print('"{}": invalid.'.format(word))
        
        print('valid_words = {}'.format(valid_words))
        print('invalid_words = {}'.format(invalid_words))

        for word in valid_words:
            expls = Edr.get_headword_expl(word, pos=SimplePos.N)
            print(word)
            pprint(expls)
            print()
    
    if mode == 3:
        xmlstrs = (
            # '<jpn><n>V</n></jpn>',
            # '<jpn><n>型</n></jpn>',
            '<jpn><n>シリンダー</n></jpn>',
            # '<jpn><n>左右</n></jpn>',
            # '<jpn><n>交互</n></jpn>',
            # '<jpn><n>字</n></jpn>',
            # '<jpn><n>エンジン</n></jpn>',
            '<jpn><n>気筒</n></jpn>',
            # '<jpn><n>以上</n></jpn>',
            # '<jpn><n>多</n></jpn>',
            # '<jpn><n>化</n></jpn>',
            # '<jpn><n>直列</n></jpn>',
            # '<jpn><n>式</n></jpn>',
            # '<jpn><n>全長</n></jpn>',
            # '<jpn><n>メリット</n></jpn>',
            # '<jpn><n>大</n></jpn>',
            # '<jpn><n>排気量</n></jpn>',
            # '<jpn><n>ため</n></jpn>',
            # '<jpn><n>多く</n></jpn>',
            # '<jpn><n>採用</n></jpn>',
            # '<jpn><n>年</n></jpn>',
            # '<jpn><n>代</n></jpn>',
            # '<jpn><n>ボディ</n></jpn>',
            # '<jpn><n>前部</n></jpn>',
            # '<jpn><n>狙い</n></jpn>',
            # '<jpn><n>直</n></jpn>',
            # '<jpn><n>部品</n></jpn>',
            # '<jpn><n>点数</n></jpn>',
            # '<jpn><n>大衆車</n></jpn>',
            # '<jpn><n>向け</n></jpn>',
            # '<jpn><n>小</n></jpn>',
            # '<jpn><n>不向き</n></jpn>',
            # '<jpn><n>構造</n></jpn>',
            # '<jpn><n>生産</n></jpn>',
            # '<jpn><n>利点</n></jpn>',
            # '<jpn><n>内</n></jpn>',
            # '<jpn><n>爆発</n></jpn>',
            # '<jpn><n>熱</n></jpn>',
            # '<jpn><n>エネルギー</n></jpn>',
            # '<jpn><n>ピストン</n></jpn>',
            # '<jpn><n>上下</n></jpn>',
            # '<jpn><n>運動</n></jpn>',
            # '<jpn><n>回転</n></jpn>',
            # '<jpn><n>こと</n></jpn>',
            # '<jpn><n>タイプ</n></jpn>',
            # '<jpn><n>基本</n></jpn>',
            # '<jpn><n>古く</n></jpn>',
            # '<jpn><n>船舶</n></jpn>',
            # '<jpn><n>航空機</n></jpn>',
            # '<jpn><n>自動車</n></jpn>',
            # '<jpn><n>燃料</n></jpn>',
            # '<jpn><n>燃焼</n></jpn>',
            # '<jpn><n>作動</n></jpn>',
            # '<jpn><n>流体</n></jpn>',
            # '<jpn><n>圧力</n></jpn>',
            # '<jpn><n>膨張</n></jpn>',
            # '<jpn><n>力</n></jpn>',
            # '<jpn><n>往復</n></jpn>',
            # '<jpn><n>直線</n></jpn>',
            # '<jpn><n>ついで</n></jpn>',
            # '<jpn><n>クランク</n></jpn>',
            # '<jpn><n>力学</n></jpn>',
            # '<jpn><n>原動機</n></jpn>',
            # '<jpn><n>初期</n></jpn>',
            # '<jpn><n>蒸気</n></jpn>',
            # '<jpn><n>機関</n></jpn>',
            # '<jpn><n>ポンプ</n></jpn>',
            # '<jpn><n>よう</n></jpn>',
            # '<jpn><n>場合</n></jpn>',
            # '<jpn><n>まま</n></jpn>',
            # '<jpn><n>タービン</n></jpn>',
            # '<jpn><n>ロータリーエンジン</n></jpn>',
            # '<jpn><n>概念</n></jpn>',
            # '<jpn><n>現在</n></jpn>',
            # '<jpn><n>主流</n></jpn>',
            # '<jpn><n>中</n></jpn>',
            # '<jpn><n>吸入</n></jpn>',
            # '<jpn><n>圧縮</n></jpn>',
            # '<jpn><n>排気</n></jpn>',
            # '<jpn><n>行程</n></jpn>',
            # '<jpn><n>ストローク</n></jpn>',
            # '<jpn><n>もの</n></jpn>',
            # '<jpn><n>内燃</n></jpn>',
            # '<jpn><n>ガス</n></jpn>',
            # '<jpn><n>事</n></jpn>',
            # '<jpn><n>一連</n></jpn>',
            # '<jpn><n>動作</n></jpn>',
            # '<jpn><n>工程</n></jpn>',
            # '<jpn><n>ガソリン</n></jpn>',
            # '<jpn><n>おにぎり</n></jpn>',
            # '<jpn><n>ローター</n></jpn>',
            # '<jpn><n>歯車</n></jpn>',
            # '<jpn><n>シャフト</n></jpn>',
            # '<jpn><n>際</n></jpn>',
            # '<jpn><n>吸気</n></jpn>',
            # '<jpn><n>技術者</n></jpn>',
            # '<jpn><n>後</n></jpn>',
            # '<jpn><n>東洋</n></jpn>',
            # '<jpn><n>工業</n></jpn>',
            # '<jpn><n>用</n></jpn>',
            # '<jpn><n>量産</n></jpn>',
            # '<jpn><n>成功</n></jpn>',
            # '<jpn><n>長所</n></jpn>',
            # '<jpn><n>軽量</n></jpn>',
            # '<jpn><n>コンパクト</n></jpn>',
            # '<jpn><n>振動</n></jpn>',
            # '<jpn><n>騒音</n></jpn>',
            # '<jpn><n>高</n></jpn>',
            # '<jpn><n>出力</n></jpn>',
            # '<jpn><n>走り</n></jpn>',
            # '<jpn><n>気持ち</n></jpn>',
            # '<jpn><n>反面</n></jpn>',
            # '<jpn><n>燃費</n></jpn>',
            # '<jpn><n>低速</n></jpn>',
            # '<jpn><n>トルク</n></jpn>',
            # '<jpn><n>不足</n></jpn>',
            # '<jpn><n>短所</n></jpn>',
            # '<jpn><n>英語</n></jpn>',
            # '<eng><n>rotary engine</n></eng>',
            # '<jpn><n>動</n></jpn>',
            # '<jpn><n>機構</n></jpn>',
            # '<jpn><n>容積</n></jpn>',
            # '<jpn><n cid="108164,3cf4fd,3cf70c,3cfc8e">変化</n></jpn>', # 指定前の意味は10個
            # '<jpn><n>動力</n></jpn>',
            # '<jpn><n>発明</n></jpn>',
            # '<jpn><n>三角形</n></jpn>',
            # '<jpn><n>回転子</n></jpn>',
            # '<jpn><n>熱機関</n></jpn>',
            # '<jpn><n>度</n></jpn>',
            # '<jpn><n>水平</n></jpn>',
            # '<jpn><n>対向</n></jpn>',
            # '<jpn><n>対</n></jpn>',
            # '<jpn><n>動き</n></jpn>',
            # '<jpn><n>右</n></jpn>',
            # '<jpn><n>点</n></jpn>',
            # '<jpn><n>左</n></jpn>',
            # '<jpn><n>使用</n></jpn>',
            # '<jpn><n>間</n></jpn>',
            # '<jpn><n>横</n></jpn>',
            # '<jpn><n>方向</n></jpn>',
            # '<jpn><n>レイアウト</n></jpn>',
            # '<jpn><n>重心</n></jpn>',
            # '<jpn><n>理想</n></jpn>',
            # '<jpn><n>パワー</n></jpn>',
            # '<jpn><n>ユニット</n></jpn>',
            # '<jpn><n>中心</n></jpn>',
            # '<jpn><n>互い</n></jpn>',
            # '<jpn><n>慣性</n></jpn>',
            # '<jpn><n>提供</n></jpn>',
            # '<jpn><n>アクセル</n></jpn>',
            # '<jpn><n>レスポンス</n></jpn>',
            # '<jpn><n>シーン</n></jpn>',
            # '<jpn><n>他</n></jpn>',
            # '<jpn><n>形式</n></jpn>',
            # '<jpn><n>全高</n></jpn>',
            # '<jpn><n>アドバンテージ</n></jpn>',
            # '<jpn><n>走行</n></jpn>',
            # '<jpn><n>安定性</n></jpn>',
            # '<jpn><n>性能</n></jpn>',
            # '<jpn><n>約束</n></jpn>',
            # '<eng><n>module</n></eng>',
            # '<eng><n>crankshaft</n></eng>',
            # '<jpn><n>鉄道</n></jpn>',
            # '<jpn><n>車両</n></jpn>',
            # '<eng><n>reciprocating engine</n></eng>',
            # '<jpn><n>気味</n></jpn>',
            # '<jpn><n>上死点</n></jpn>',
            # '<jpn><n>ボクサー</n></jpn>',
            # '<jpn><n>対称</n></jpn>',
            # '<eng><n>feel</n></eng>',
            # '<eng><n>work</n></eng>',
            # '<eng><n>driving</n></eng>',
            # '<eng><n>handling</n></eng>',
            )

        words = [Text_.xml_parse_tree(ElementTree.fromstring(xmlstr)) for xmlstr in xmlstrs]
        Meaning.fill_meaning(words, meaning_id=meaning_id)
        print(words)
        n = len(words)
        sim_wordpair_list = []
        for i in range(n):
            print(i)
            wordi = words[i]
            for j in range(i + 1, n):
                wordj = words[j]
                sim = TextSimilarity.word_sim(wordi, wordj, meaning_id=meaning_id)
                sim_wordpair_list.append((sim, wordi.get_text(), wordj.get_text()))
        sim_wordpair_list.sort(reverse=False)
        pprint(sim_wordpair_list)
    
    if mode == 4:
        for text in valid_words:
            _, cands = Edr.check_headword(text, pos=SimplePos.all_(), suggest=True, simmin=1)
            lang = cands[0][1]
            print('<{1}><n>{0}</n></{1}>'.format(text, lang))
    
    # print('words =', words)
    # print('excluded =', excluded)
    
    # words = ('素子', '各', 'ピクセル', '上', '赤', '緑', '青', 'ため', 'RGB', 'フィルター', '配列', '方式', 'こと', 'ほとんど', '人間', '眼', '緑色', '波長', 'g', 'r', 'b', '倍', '数', 'それぞれ', '光', '以外', '色', '近隣', '情報', '演算', '処理', '画像', '実際', '発生', '多く', 'モアレ', 'レンズ', 'センサー', '間', '効果', '同時', '解像度', '欠点', 'メーカー', '補完', '程度', '技術', 'つ', '事実', '変わり', 'カメラ', '無', '加工', '形式', 'RAW', 'データ', 'どおり', '画素', '越し', '三原色', 'うち', '一色', 'フルカラー', '種類', 'ごと', '一般', '全て', 'red', 'green', 'blue', '凡そ', '分', 'CFA', 'カラー', 'color', 'filter', 'array', 'フォト', '正方形', 'グリッド', 'フィルタ', '特定', '配置', 'ビデオカメラ', 'スキャナ', 'パターン', '%', '赤色', '青色', 'イヤー', '法', 'arrangement', '固体', '撮影', '側', '採用', 'ディスプレイ', '利用', '例', '比率', '名称', '社', '所属', '発明者', '名', 'リング', '市松', '模様', '点', '本', '関連', '前面', '単位', '繰り返す', '目', '輝度', 'ほか', 'もの', 'フイルム', 'x', 'CMOS', '全', '取り込める', '層', '構造', 'イメージ', 'ほう', '順', 'シリコン', '特性', '垂直', '方向', 'トップ', 'ミドル', 'ボトム', '短波', '長', '中間', '長波', '主に', 'すべて', '原理', '必要', 'シャープ', '感', '一種', '厚み', 'カラーフィルム', '各層', '位置', '第', '最', '上層', '要素', '下層', 'エンジン', '値', '中層', 'ウエハー', '以下', 'ピント', 'ずれ', '色収差', '部分', '他', '場合', 'いくつ', '電子', '回折', '現象', '領域', '分光', '従来', '約', '化', '置き換え', '半導体', 'デバイス', '製造', '無機', '材料', 'プロセス', '波', '性質', '事', '成功', '実現', '置換', '設計', '適用', '作製')
    # excluded = ('受光', '撮像', 'ベイヤー', '偽色', 'ローパスフィルター', 'ベイヤーフィルタ', '各値', 'デモザイク', 'フォトダイオード', 'シングルチップデジタルイメージセンサ', 'grgb', 'rggb', 'Bayer', 'ブライス', 'ディザ', 'Foveon', 'センサ', '以深', 'μm', '高感度', '色ごと')

    # jpns = []
    # engs = []
    # count = 0
    # for text in words:
    #     judge = Edr.check_headword(text, pos=SimplePos.N, suggest=True, simmin=1, num=1)
    #     if Lang.JPN in judge[1][0]:
    #         jpns.append(text)
    #         print(count, 'JPN')
    #     else:
    #         engs.append(text)
    #         print(count, 'ENG')
    #     count += 1
    
    # print('jpns =', jpns)
    # print('engs =', engs)
    
    # jpns = ['素子', '各', 'ピクセル', '上', '赤', '緑', '青', 'ため', 'RGB', 'フィルター', '配列', '方式', 'こと', 'ほとんど', '人間', '眼', '緑色', '波長', 'g', 'r', 'b', '倍', '数', 'それぞれ', '光', '以外', '色', '近隣', '情報', '演算', '処理', '画像', '実際', '発生', '多く', 'モアレ', 'レンズ', 'センサー', '間', '効果', '同時', '解像度', '欠点', 'メーカー', '補完', '程度', '技術', 'つ', '事実', '変わり', 'カメラ', '無', '加工', '形式', 'RAW', 'データ', 'どおり', '画素', '越し', '三原色', 'うち', '一色', 'フルカラー', '種類', 'ごと', '一般', '全て', '凡そ', '分', 'カラー', 'フォト', '正方形', 'グリッド', 'フィルタ', '特定', '配置', 'ビデオカメラ', 'スキャナ', 'パターン', '%', '赤色', '青色', 'イヤー', '法', '固体', '撮影', '側', '採用', 'ディスプレイ', '利用', '例', '比率', '名称', '社', '所属', '発明者', '名', 'リング', '市松', '模様', '点', '本', '関連', '前面', '単位', '繰り返す', '目', '輝度', 'ほか', 'もの', 'フイルム', 'x', 'CMOS', '全', '取り込める', '層', '構造', 'イメージ', 'ほう', '順', 'シリコン', '特性', '垂直', '方向', 'トップ', 'ミドル', 'ボトム', '短波', '長', '中間', '長波', '主に', 'すべて', '原理', '必要', 'シャープ', '感', '一種', '厚み', 'カラーフィルム', '各層', '位置', '第', '最', '上層', '要素', '下層', 'エンジン', '値', '中層', 'ウエハー', '以下', 'ピント', 'ずれ', '色収差', '部分', '他', '場合', 'いくつ', '電子', '回折', '現象', '領域', '分光', '従来', '約', '化', '置き換え', '半導体', 'デバイス', '製造', '無機', '材料', 'プロセス', '波', '性質', '事', '成功', '実現', '置換', '設計', '適用', '作製']
    # engs = ['red', 'green', 'blue', 'CFA', 'color', 'filter', 'array', 'arrangement']

    # words = []
    # for jpn in jpns:
    #     words.append(Word(text=jpn, lang=Lang.JPN, pos=SimplePos.N))
    # for eng in engs:
    #     words.append(Word(text=eng, lang=Lang.ENG, pos=SimplePos.N))
    # Meaning.fill_meaning(words, meaning_id=meaning_id)
    
    # # print(words)

    # n = len(words)
    # sim_pair_list = []
    
    # for i in range(n):
    #     wordi = words[i]
    #     texti = wordi.get_text()
    #     for j in range(i + 1, n):
    #         wordj = words[j]
    #         textj = wordj.get_text()
    #         sim = TextSimilarity.word_sim(wordi,
    #                                       wordj,
    #                                       meaning_id=meaning_id,
    #                                       # wsimtype=CalcType.MAX_COMBI)
    #                                       # wsimtype=CalcType.MEAN_COMBI)
    #                                       # wsimtype=CalcType.MEAN_MAX_1_TO_M)
    #                                       wsimtype=CalcType.MEDIAN_MAX_1_TO_M)
    #         sim_pair_list.append((sim, texti, textj))
    
    # with open('./Output/toyama2022m.txt', 'w', encoding='utf-8') as f:
    #     for sim_pair in sorted(sim_pair_list, reverse=True):
    #         print(sim_pair)
    #         f.write('{}\n'.format(sim_pair))
 
    
    print('* Main ends *')
    
# End of file