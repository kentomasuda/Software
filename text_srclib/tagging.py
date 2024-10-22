# -*- coding: utf-8 -*-
"""
Tagging

@author: MURAKAMI Tamotsu
@date: 2023-12-03
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import json
from typing import Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

# Library
from edr_lib.e_word import EwPos
from edr_lib.edr import Edr
from edr_srclib.jwpos import JwPos
from text_lib.altwording import AltWording
from text_lib.lang import Lang
from text_srclib.simplepos import SimplePos
from text_srclib.textxml import TextXml
from wordnet_lib.wnpos import WnPos
from wordnet_lib.wordnet import WordNet

class Tagging:
    """
    Tagging
    
    Tags:
        <a></a>: Adverbial (副詞語句)
        <aj></aj>: Adjective (形容詞)
        <av></av>: Adverb (副詞)
        <c></c>: Complement (補語)
        <eng></eng>: English (英語)
        <jpn></jpn>: Japanese (日本語)
        <lm></lm>: Language map (言語マップ)
        <m></m>: Modifier(s) (修飾語)
        <n></n>: Noun (名詞)
        <np></np>: Noun phrase (名詞句)
        <o></o>: (Direct) Object ((直接)目的語)
        <oi></oi>: Indirect object (間接目的語)
        <s></s>: Subject (主語)
        <sen></sen>: Sentence (文)
        <t></t>: Text (テキスト) (処理対象外の記述)
        <v></v>: Verb (動詞)
    Attributes:
        eng: English alternative (英語の代替後)
        jpn: Japanese alternative (日本語の代替後)
    
    @author MURAKAMI Tamotsu
    @date 2022-10-21
    """
    
    KEY_ALT = 'alt'
    KEY_HEADWORD = 'headword'
    KEY_TEXT = 'text'
    
    @staticmethod
    def find_edr_headword(text: str,
                          lang: Lang = Lang.JPN|Lang.ENG,
                          pos: Union[SimplePos, JwPos, EwPos] = SimplePos.all_(),
                          suggest: bool = True,
                          simmin: Union[float, int] = 1,
                          nmax: int = 55,
                          progress: bool = False) -> dict:
        """
        テキスト中のEDR電子化辞書の見出し語を探す。
        単純なN-gramアルゴリズムのため時間はかかります。
        目的に応じ、simmin大きく（最大1）、nmaxを小さくすると、探す内容が限定されるので時間は短縮されます。

        Parameters
        ----------
        text : str
            解析対象のテキスト。
        lang : Lang, optional
            解析対象のテキストの言語。
            The default is Lang.JPN|Lang.ENG. (Both Japanese and English)
        pos : Union[SimplePos, JwPos, EwPos], optional
            探す対象の品詞。
            The default is SimplePos.all_(). (品詞を限定せず。)
        suggest : bool, optional
            完全一致するものがない場合、似ている候補を提案するかどうか。
            The default is True.
        simmin : Union[float, int], optional
            提示する候補の類似度の下限。
            The default is 1. (完全一致するもののみ)
        nmax : int, optional
            N-gramのNをいくつから開始するか。
            日本語: 35字（"エレクトロニックコマース・リーガルシステム・ソリューションプロジェクト"）
            英語: 55字（"United Nations Relief and Rehabilitation Administration"）
            The default is 55.
        progress : bool, optional
            進捗の表示をするかどうか。
            The default is False.

        Returns
        -------
        dict
            テキスト中に検出されたEDR電子化辞書の見出し語。

        @author: MURAKAMI Tamotsu
        @date: 2022-12-16
        """
        
        NMAX_J = 35  # "エレクトロニックコマース・リーガルシステム・ソリューションプロジェクト"
        NMAX_E = 55  # "United Nations Relief and Rehabilitation Administration"
        
        nstart = min(len(text), nmax)
        
        checked = set()
        
        result = {}

        for n in range(nstart, 0, -1):
            for i in range(len(text) - n + 1):
                ngram = text[i : i + n]
                if not ngram in checked:
                    if progress:
                        print('Checking {}-gram "{}"...'.format(n, ngram))
                    judge_cands = Edr.check_headword(ngram,
                                                     lang=lang,
                                                     pos=pos,
                                                     suggest=suggest,
                                                     simmin=simmin)
                    altwording = AltWording.check_edr(ngram, simmin)
                    if judge_cands[1]:
                        if ngram in result:
                            result[ngram][Tagging.KEY_HEADWORD] = judge_cands
                        else:
                            result[ngram] = {Tagging.KEY_HEADWORD: judge_cands}

                        if progress:
                            print('"{}" -> {}: {}'.format(ngram, Tagging.KEY_HEADWORD, judge_cands))

                    if altwording:
                        if ngram in result:
                            result[ngram][Tagging.KEY_ALT] = altwording
                        else:
                            result[ngram] = {Tagging.KEY_ALT: altwording}

                        if progress:
                            print('"{}" -> {}: {}'.format(ngram, Tagging.KEY_ALT, altwording))

                    checked.add(ngram)
        
        return result

    @staticmethod
    def find_wordnet_lemma(text: str,
                           lang: Lang = Lang.JPN|Lang.ENG,
                           pos: WnPos = WnPos.ALL,
                           suggest: bool = True,
                           simmin: Union[float, int] = 1):
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-05
        
        """
        
        ngrams = []

        for n in range(len(text), 0, -1):
            for i in range(len(text) - n + 1):
                item = text[i : i + n]
                if not item in ngrams:
                    ngrams.append(text[i : i + n])
        
        for ngram in ngrams:
            judge_cands = WordNet.check_lemma(ngram,
                                              lang = lang,
                                              pos = pos,
                                              suggest = suggest,
                                              simmin = simmin)
            
            if judge_cands[1]:
                print('"{}" -> WN: {}'.format(ngram, judge_cands))

    @staticmethod
    def get_alt_words(elem: Element,
                      altwords: set):
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-10-30
        """
        
        eng = elem.attrib.get(TextXml.ATTR_ENG)
        if eng:
            altwords.add(eng)
        
        jpn = elem.attrib.get(TextXml.ATTR_JPN)
        if jpn:
            altwords.add(jpn)
        
        for child in elem:
            Tagging.get_alt_words(child, altwords=altwords)
        
    @staticmethod
    def ngram(text: str) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-23
        """
        
        ngrams = []

        for n in range(len(text), 0, -1):
            for i in range(len(text) - n + 1):
                item = text[i : i + n]
                if not item in ngrams:
                    ngrams.append(text[i : i + n])

    @staticmethod
    def transform_alt_wording(filein: str, edrout: str, wnout: str):
        """
        @author MURAKAMI Tamotsu
        @date 2022-09-25
        """
        
        edrdict = {}
        wndict = {}
        with open(filein, 'r', encoding='utf-8') as f:
            altdict = json.load(f)
            for w, wlang_wpos_altw_altlang_edrwn in altdict.items():
                for wlang, wpos_altw_altlang_edrwn in wlang_wpos_altw_altlang_edrwn.items():
                    for wpos, altw_altlang_edrwn in wpos_altw_altlang_edrwn.items():
                        for altw, altlang_edrwn in altw_altlang_edrwn.items():
                            for altlang, edrwn in altlang_edrwn.items():
                                for con in edrwn:
                                    if con == 'EDR':
                                        newdict = edrdict
                                    elif con == 'WN':
                                        newdict = wndict
                                    if w in newdict:
                                        w_dict = newdict[w]
                                        if wlang in w_dict:
                                            wlang_dict = w_dict[wlang]
                                            if wpos in wlang_dict:
                                                wpos_dict = wlang_dict[wpos]
                                                if altw in wpos_dict:
                                                    altlangs = wpos_dict[altw]
                                                    if not altlang in altlangs:
                                                        altlangs.append(altlang)
                                                else:
                                                    wpos_dict[altw] = [altlang]
                                            else:
                                                wlang_dict[wpos] = {altw: [altlang]}
                                        else:
                                            w_dict[wlang] = {wpos: {altw: [altlang]}}
                                    else:
                                        newdict[w] = {wlang: {wpos: {altw: [altlang]}}}

        with open(edrout, 'w', encoding='utf-8') as f:
            json.dump(edrdict,
                      f,
                      ensure_ascii=False,
                      check_circular=True,
                      indent=2,
                      sort_keys=True)
            
        with open(wnout, 'w', encoding='utf-8') as f:
            json.dump(wndict,
                      f,
                      ensure_ascii=False,
                      check_circular=True,
                      indent=2,
                      sort_keys=True)
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-09-25
"""

if __name__ == '__main__':

    print('* Test start *')
    
    # Tagging.find_edr_headword('goodな文章。', simmin=0.8)
    # Tagging.find_edr_headword('good lucks.', lang=Lang.ENG, simmin=0.8)
    
    # Tagging.find_wordnet_lemma('goodな文章。', simmin=0.8)
    # Tagging.find_wordnet_lemma('good lucks.', lang=Lang.ENG, simmin=0.8)

    Tagging.transform_altwording('../text_data/alternativeWords.json',
                                 '../text_data/altWordingEdr.json',
                                 '../text_data/altWordingWordNet.json')

    print('* Test end *')
    
# End of file