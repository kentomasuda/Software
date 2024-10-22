# -*- coding: utf-8 -*-
"""
Comparison sentence main

@author: MURAKAMI Tamotsu
@date: 2021-02-17
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Libraty
from text_lib.meaning import Meaning
from text_lib.text import Text_
from text_srclib.text_similarity import TextSimilarity

"""
Main

@author: MURAKAMI Tamotsu
@date: 2021-02-17
"""

if __name__ == "__main__":

    print('* start *')

    # S-Vが対応，C-Aが対応
    e01a = '<eng><sen><s><np><t>A</t><m><aj>shining</aj></m><n>light</n></np></s><v><v eng="be">is</v></v><c><aj>beautiful</aj></c><t>.</t></sen></eng>'
    e01b = '<eng><sen><s><t>A</t><n>light</n></s><v><v eng="shine">shines</v></v><a><av>beautifully</av></a><t>.</t></sen></eng>'
    j01a = '<jpn><sen><s><np><m><aj eng="shining">輝く</aj></m><n>照明</n></np></s><v><v eng="be">が</v></v><c><aj>美しい</aj></c><t>。</t></sen></jpn>'
    j01b = '<jpn><sen><s><n>照明</n></s><t>が</t><a><av eng="beautifully">美しく</av></a><v><v>輝く</v></v><t>。</t></sen></jpn>'
    
    # S-Cが対応，S-Aが対応
    e02a = '<eng><sen><s><np><t>A</t><m><aj>fast</aj></m><n>car</n></np></s><v><v eng="run">runs</v></v><t>.</t></sen></eng>'
    e02b = '<eng><sen><s><t>A</t><n>car</n></s><v><v eng="be">is</v></v><c><aj>fast</aj></c><t>.</t></sen></eng>'
    j02a = '<jpn><sen><s><np><m><aj>速い</aj></m><n>自動車</n></np></s><t>が</t><v><v>走る</v></v><t>。</t></sen></jpn>'
    j02b = '<jpn><sen><s><n>自動車</n></s><v><v eng="be">は</v></v><c><aj>速い</aj></c><t>。</t></sen></jpn>'
    
    # V-Oが対応
    e03a = '<eng><sen><s><t>A</t><n>user</n></s><v><v eng="photograph">photographs</v></v><o><t>a</t><n>car</n></o><t>.</t></sen></eng>'
    e03b = '<eng><sen><s><t>A</t><n>user</n></s><v><v eng="take">takes</v></v><o><np><t>a</t><n>photograph</n><m><t>of a</t><n>car</n></m></np></o><t>.</t></sen></eng>'
    j03a = '<jpn><sen><s><n>ユーザ</n></s><t>が</t><o><n>自動車</n></o><t>を</t><v><v>撮影する</v></v><t>。</t></sen></jpn>'
    j03b = '<jpn><sen><s><n>ユーザ</n></s><t>が</t><o><np><m><n>自動車</n><t>の</t></m><n>写真</n></np></o><t>を</t><v><v>撮る</v></v><t>。</t></sen></jpn>'
    
    # V-Oiが対応
    e04a = '<eng><sen><s><t>A</t><n>user</n></s><v><v eng="box">boxes</v></v><o><t>a</t><n>present</n></o><t>.</t></sen></eng>'
    e04b = '<eng><sen><s><t>A</t><n>user</n></s><v><v eng="put">puts</v></v><oi><t>a</t><n>box</n></oi><o><t>a</t><n>present</n></o><t>.</t></sen></eng>'
    j04a = '<jpn><sen><s><n>ユーザ</n></s><t>が</t><o><n>贈り物</n></o><t>を</t><v><v eng="box">箱に入れる</v></v><t>。</t></sen></jpn>'
    j04b = '<jpn><sen><s><n>ユーザ</n></s><t>が</t><oi><n>箱</n></oi><t>に</t><o><n>贈り物</n></o><t>を</t><v><v>入れる</v></v><t>。</t></sen></jpn>'
    
    # V-Cが対応
    e05a = '<eng><sen><s><t>A</t><n>refrigerator</n></s><v><v eng="cool">cools</v></v><o><n>food</n></o><t>.</t></sen></eng>'
    e05b = '<eng><sen><s><t>A</t><n>refrigerator</n></s><v><v eng="keep">keeps</v></v><o><n>food</n></o><c><aj>cool</aj></c><t>.</t></sen></eng>'
    j05a = '<jpn><sen><s><n>冷蔵庫</n></s><t>が</t><o><n>食品</n></o><t>を</t><v><v>冷やす</v></v><t>。</t></sen></jpn>'
    j05b = '<jpn><sen><s><n>冷蔵庫</n></s><t>が</t><o><n>食品</n></o><t>を</t><c><aj jpn="冷たい">冷たく</aj></c><v><v>保つ</v></v><t>。</t></sen></jpn>'
    
    # V-Aが対応
    e06a = '<eng><sen><s><t>A</t><n>car</n></s><v><v eng="outrun">outruns</v></v><o><t>a</t><n>bicycle</n></o><t>.</t></sen></eng>'
    e06b = '<eng><sen><s><t>A</t><n>car</n></s><v><v eng="run">runs</v></v><a><av eng="fast">faster</av><av jpn="より">than</av><t>a</t><n>bicycle</n></a><t>.</t></sen></eng>'
    j06a = '<jpn><sen><s><n>自動車</n></s><t>は</t><o><n>自転車</n></o><v><v eng="outrun">よりよく走る</v></v><t>。</t></sen></jpn>'
    j06b = '<jpn><sen><s><n>自動車</n></s><t>は</t><a><n>自転車</n><av>より</av><av eng="fast">速く</av></a><v><v>走る</v></v><t>。</t></sen></jpn>'
    
    # O-Cが対応
    e07a = '<eng><sen><s><t>An</t><n>automobile</n></s><v><v eng="have">has</v></v><o><np><t>a</t><m><aj>powerful</aj></m><n>engine</n></np></o><t>.</t></sen></eng>'
    e07b = '<eng><sen><s><np><t>An</t><n>engine</n><m><t>of an</t><n>automobile</n></m></np></s><v><v eng="be">is</v></v><c><aj>powerful</aj></c><t>.</t></sen></eng>'
    j07a = '<jpn><sen><s><n>自動車</n></s><t>は</t><o><np><m><aj jpn="強力だ">強力</aj><t>な</t></m><n>エンジン</n></np></o><t>を</t><v><v>持つ</v></v><t>。</t></sen></jpn>'
    j07b = '<jpn><sen><s><np><m><n>自動車</n><t>の</t></m><n>エンジン</n></np></s><t>は</t><c><aj jpn="強力だ">強力</aj></c><v><v eng="be">だ</v></v><t>。</t></sen></jpn>'
    
    # O-Aが対応
    e08a = '<eng><sen><s><t>A</t><n>patient</n></s><v><v eng="catch">caught</v></v><o><np><m><t>a</t><aj>severe</aj></m><n>cold</n></np></o><t>.</t></sen></eng>'
    e08b = '<eng><sen><s><t>A</t><n>patient</n></s><v><v eng="catch">caught</v></v><o><t>a</t><n>cold</n></o><a><av>severely</av></a><t>.</t></sen></eng>'
    j08a = '<jpn><sen><s><n>患者</n></s><t>は</t><o><np><m><aj>ひどい</aj></m><n>風邪</n></np></o><t>を</t><v><v eng="contract">引いた</v></v><t>。</t></sen></jpn>'
    j08b = '<jpn><sen><s><n>患者</n></s><t>は</t><a><av>ひどく</av></a><o><n>風邪</n></o><t>を</t><v><v eng="contract">引いた</v></v><t>。</t></sen></jpn>'
    
    # 語群は類似するが文意は異なる例
    e11a = '<eng><sen><s><t>A</t><n>product</n></s><v><v eng="heal">heals</v></v><o><t>a</t><n>user</n></o><t>.</t></sen></eng>'
    e11b = '<eng><sen><s><t>A</t><n>user</n></s><v><v eng="repair">repairs</v></v><o><t>a</t><n>product</n></o><t>.</t></sen></eng>'
    j11a = '<jpn><sen><s><n>製品</n></s><t>が</t><o><n>ユーザ</n></o><t>を</t><v><v>癒す</v></v><t>。</t></sen></jpn>'
    j11b = '<jpn><sen><s><n>ユーザ</n></s><t>が</t><o><n>製品</n></o><t>を</t><v><v>直す</v></v><t>。</t></sen></jpn>'
    
    xmlstr = '<lm>{}</lm>'.format(j11b)
    words_out = []
    senlm = Text_.xml_parse_string(xmlstr, words_out)
    
    print(senlm)
    
    Meaning.fill_meaning(senlm, TextSimilarity.meaning_id, suggest = sys.stdout)

    for word in words_out:
        print(Meaning.meaning_json_string(word, TextSimilarity.meaning_id))

    print('* end *')

# End of file