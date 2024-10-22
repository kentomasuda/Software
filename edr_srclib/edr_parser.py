# -*- coding: utf-8 -*-
"""
EDR Parser

@author: MURAKAMI Tamotsu
@date: 2023-10-24
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from difflib import SequenceMatcher
from typing import Union
import unicodedata
from xml.etree import ElementTree

# Library
from container_srclib.cons import Cons
from edr_lib.j_word import JWord
from text_srclib.simplepos import SimplePosTag

class EdrParser:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-10-24
    """
    
    ATTR_ALTPOS = 'altpos'
    ATTR_JPN = 'jpn'
    ATTR_SIM = 'sim'
    
    TAG_E = 'e'
    TAG_J = 'j'
    TAG_T = 't'
    
    len_hw_poses_dict = {}
    len_hw_dict = {}
    
    for hw, poses in JWord.get_headwords_poses():
        n = len(hw)
        if n in len_hw_poses_dict:
            len_hw_poses_dict[n].append((hw, poses))
            len_hw_dict[n].append(hw)
        else:
            len_hw_poses_dict[n] = [(hw, poses)]
            len_hw_dict[n] = [hw]
    
    len_hw_poses_list = sorted(len_hw_poses_dict.items(), reverse=True)
    len_hw_poses_dict = None

    @staticmethod
    def are_similar(w: str,
                    hw: str,
                    nw: int) -> Union[float, int]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        n = int(nw / 2)
        
        if nw == 3:
            simmin = 0.66
        elif nw == 4:
            simmin = 0.5
        elif nw == 5:
            simmin = 0.6
        else:
            simmin = 0.9

        if w[:n] == hw[:n]:
            sim = SequenceMatcher(None, hw, w).ratio()
            if sim >= simmin:
                return sim
            else:
                return 0
        else:
            return 0

    @staticmethod
    def calc_score(seq: list) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        nw = 0  # 厳密一致文字数
        nk = 0  # 漢字文字数
        ns = 0  # 類似一致文字数
        ntags = 0
        
        for tagged in seq:
            element = ElementTree.fromstring(tagged)
            tag = element.tag
            if tag == SimplePosTag.AJ or tag == SimplePosTag.AV or tag == SimplePosTag.N or tag == SimplePosTag.V:
                sim = element.get(EdrParser.ATTR_SIM)
                if sim:
                    ns += len(element.text)
                else:
                    nw += len(element.text)
                nk += EdrParser.count_char(element.text)[0]
                ntags += 1
        
        return (nw, nk, ns, -ntags)
        
    @staticmethod
    def contains_punctuation(text: str) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        contains = False
        
        for x in ('、', '。', '，', '．', ',', '.'):
            if x in text:
                contains = True
        
        return contains

    @staticmethod
    def count_char(s: str) -> (int, int, int):
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        nkanji = 0
        nkana = 0
        nelse = 0
        for c in list(s):
            name = unicodedata.name(c)
            if 'CJK UNIFIED' in name:
                nkanji += 1
            elif 'HIRAGANA' in name or 'KATAKANA' in name:
                nkana += 1
            else:
                nelse += 1
        return (nkanji, nkana, nelse)
    
    @staticmethod
    def end_tag(tag: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-15
        """
        
        return '</{}>'.format(tag)
    
    @staticmethod
    def is_tagged(item: str) -> Union[str, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        element = ElementTree.fromstring(item)

        tag = element.tag
        if tag == SimplePosTag.AJ or tag == SimplePosTag.AV or tag == SimplePosTag.N or tag == SimplePosTag.V or tag == EdrParser.TAG_T:
            return tag
        else:
            return None
    
    @staticmethod
    def make_cons(head: str,
                  cons: Union[Cons, None]) -> Cons:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-21
        """
        
        if EdrParser.is_tagged(head) == EdrParser.TAG_T:
            if cons is None:
                return Cons(head, cons)
            elif EdrParser.is_tagged(cons.head) == EdrParser.TAG_T:
                return Cons(EdrParser.tagging(EdrParser.untagged(head) + EdrParser.untagged(cons.head), EdrParser.TAG_T),
                            cons.tail)
            else:
                return Cons(head, cons)
        else:
            return Cons(head, cons)
    
    @staticmethod
    def parse(text: str,
              similar: bool = False) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        conses_cache = {}
        
        conses = EdrParser._parse_scan(text, conses_cache, similar=similar)
        seqs = [cons.to_list() for cons in conses]
        seqs.sort(key=lambda x: EdrParser.calc_score(x))
        
        return seqs
        
    @staticmethod
    def _parse_scan(text: str,
                    conses_cache: dict,
                    similar: bool = False) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        nt = len(text)
        if nt > 0:
            conses = []
            for nw, hw_poses_list in EdrParser.len_hw_poses_list:
                if nw <= nt:
                    w = text[:nw]
                    rest_text = text[nw:]
                    tail_conses = None
                    items = []

                    if not EdrParser.contains_punctuation(w):
                        for hw, poses in hw_poses_list:
                            if text.startswith(hw):
                                items.append(EdrParser.tagging(hw, poses))
                            elif nw >= 3 and similar:
                                sim = EdrParser.are_similar(w, hw, nw)
                                if sim > 0:
                                    items.append(EdrParser.tagging(w, poses, jpn=hw, sim=sim))

                    if nw == 1 and not items:
                        items.append(EdrParser.tagging(text[0], EdrParser.TAG_T))

                    if items:
                        if tail_conses is None:
                            if rest_text in conses_cache:
                                tail_conses = conses_cache[rest_text]
                                print('"{}" hits cache.'.format(rest_text))
                            else:
                                tail_conses = EdrParser._parse_scan(rest_text, conses_cache=conses_cache, similar=similar)
                                conses_cache[rest_text] = tail_conses
                                # print('"{}" is cached.'.format(rest_text))
    
                        for item in items:
                            conses.extend([EdrParser.make_cons(item, cons) for cons in tail_conses])
            
            return conses
        else:
            return [None]
    
    @staticmethod
    def start_tag(tag: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-15
        """
        
        return '<{}>'.format(tag)

    @staticmethod
    def tagging(item: str,
                poses: Union[str, tuple],
                jpn: str = None,
                sim: Union[float, int, None] = None) -> Union[str, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """
        
        if isinstance(poses, str):
            postag = poses
            tagged = '<{}'.format(postag)
        elif isinstance(poses, tuple):
            postag = SimplePosTag.from_pos(poses[0])
            tagged = '<{}'.format(postag)
            if len(poses) > 1:
                altposes = ','.join([SimplePosTag.from_pos(pos) for pos in poses[1:]])            
                tagged += ' {}="{}"'.format(EdrParser.ATTR_ALTPOS, altposes)
        
        if jpn:
            tagged += ' {}="{}"'.format(EdrParser.ATTR_JPN, jpn)
        
        if sim:
            tagged += ' {}="{}"'.format(EdrParser.ATTR_SIM, sim)
        
        return tagged + '>{}</{}>'.format(item, postag)
        
    @staticmethod
    def untagged(tagged: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-10-24
        """

        element = ElementTree.fromstring(tagged)
        
        return element.text

"""
Test

@author: MURAKAMI Tamotsu
@date: 2023-10-24
"""
if __name__ == '__main__':
    print('* Test start *')
    
    # sim = SequenceMatcher(None, '検出する', '検出した').ratio()
    # print(sim)

    text = 'これは、見出し語を検出したテストです。'
    # text = '見出す語です。'
    
    seqs = EdrParser.parse(text, similar=True)
    
    for seq in seqs[-10:]:
        print(seq)

    print('* Test end *')

# End of file