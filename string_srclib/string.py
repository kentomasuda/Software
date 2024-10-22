# -*- coding: utf-8 -*-
"""
String library

@author: MURAKAMI Tamotsu
@date: 2021-11-26
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
from typing import Collection
from typing import Union
import unicodedata

# Library
from string_srclib.strrel import StrRel

class String:
    """
    String（文字列）
    @author: MURAKAMI Tamotsu
    @date: 2019-11-07
    """
    
    UTF_8 = 'utf-8' 
    
    @staticmethod
    def _num_float(x: str): # -> float, None
        """
        x が float を表す str であればその float を、そうでなければ None を返す。
        
        @author: MURAKAMI Tamotsu
        @date: 2019-01-10
        """
        
        try:
            y = float(x)
            return y
        except:
            return None
        
    @staticmethod
    def _num_int(x: str): # -> int, None
        """
        x が int を表す str であればその int を、そうでなければ None を返す。
        
        @author: MURAKAMI Tamotsu
        @date: 2019-01-10
        """
        
        try:
            y = int(x)
            return y
        except:
            return None
        
    @staticmethod
    def camel_upper_to_lower(s: str) -> str:
        """
        Convert upper camel case to lower camel case.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        return s[:1].lower() + s[1:]
    
    @staticmethod
    def compact_str(x) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-11-07
        """
        
        table = (
                ('\n', ''),
                ('\r', ''),
                ('\t', ''),
                ('  ', ' ')
                )
     
        org = None  # Dummy
        rpl = x
        
        while org != rpl:
            org = rpl
            for pair in table:
                if pair[0] in rpl:
                    rpl = rpl.replace(pair[0], pair[1])
        
        return rpl

    @staticmethod
    def compare(str1: str,
                str2: str,
                case: bool = True,
                width: bool = True,
                zenhan: bool = True,
                match: bool = False,
                unmatch: bool = False
                ): # -> StrRel or tuple
        """
        Compare two strings and returns the relationship between the strings.
        
        def compare(str1: str,
                    str2: str,
                    case: bool = True,
                    zenhan: bool = True,
                    match: bool = False,
                    unmatch: bool = False
                    ): # -> StrRel or tuple
            
            case: Case-sensitive or not.
            
            zenhan: Full- and half- width sensitive or not.

            match: Returns matched strings or not.

            unmatch: Returns unmatched strings in str1 and str2  or not.
            
            returns:
                match = False, Unmatch = False: StrRel
                match = True, Unmatch = False: (StrRel, [match-strings])
                match = False, Unmatch = True: (StrRel, [unmatch-strings1], [unmatch-strings2])
                match = True, Unmatch = True: (StrRel, [match-strings], [unmatch-strings1], , [unmatch-strings2])
        
        @author: MURAKAMI Tamotsu
        @date: 2021-11-26
        """
        
        if case:
            s1 = str1
            s2 = str2
        else:
            s1 = str1.lower()
            s2 = str2.lower()
            
        if zenhan:
            str1x = s1
            str2x = s2
        else:
            str1x = String.zen_to_han(s1)
            str2x = String.zen_to_han(s2)
        
        # rel = StrRel.NONE
        rel = None
        m = []
        um1 = []
        um2 = []
        
#        if set(str1) & set(str2): # Share some characters
        if str1x == str2x:
            rel = StrRel.EQUALS
            if match:
                m.append(str1x)
        elif str1x.startswith(str2x):
            rel = StrRel.STARTS_WITH
            if match:
                m.append(str2x)
            if unmatch:
                um1.append(str1x[len(str2x):])
        elif str1x.endswith(str2x):
            rel = StrRel.ENDS_WITH
            if match:
                m.append(str2x)
            if unmatch:
                um1.append(str1x[:-len(str2x)])
        elif str2x.startswith(str1x):
            rel = StrRel.STARTS
            if match:
                m.append(str1x)
            if unmatch:
                um2.append(str2x[len(str1x):])
        elif str2x.endswith(str1x):
            rel = StrRel.ENDS
            if match:
                m.append(str1x)
            if unmatch:
                um2.append(str2x[:-len(str1x)])
        elif str1x in str2x:
            rel = StrRel.CONTAINED_BY
            if match:
                m.append(str1x)
            if unmatch:
                um2.extend(str2x.split(str1x))
        elif str2x in str1x:
            rel = StrRel.CONTAINS
            if match:
                m.append(str2x)
            if unmatch:
                um1.extend(str1x.split(str2x))
        else:
            ns, ne = String.share_start(str1x, str2x), String.share_end(str1x, str2x)
            if ns > 0:
                if match:
                    m.append(str1x[:ns])
                if ne > 0:
                    rel = StrRel.SHARE_START_END
                    if match:
                        m.append(str1x[-ne:])
                    if unmatch:
                        um1.append(str1x[ns:-ne])
                        um2.append(str2x[ns:-ne])
                else:
                    rel = StrRel.SHARE_START
                    if unmatch:
                        um1.append(str1x[ns:])
                        um2.append(str2x[ns:])
            elif ne > 0:
                rel = StrRel.SHARE_END
                if match:
                    m.append(str1x[-ne:])
                if unmatch:
                    um1.append(str1x[:ne])
                    um2.append(str2x[:ne])
            else:
                # ns == 0 and ne == 0
                n = String.precedes(str1x, str2x)
                if n >= 0:
                    rel = StrRel.PRECEDES
                    if match:
                        m.append(str1x[-n:])
                    if unmatch:
                        um1.append(str1x[:-n])
                        um2.append(str2x[n:])
                else:
                    n = String.precedes(str2x, str1x)
                    if n >= 0:
                        rel = StrRel.SUCCEEDS
                        if match:
                            m.append(str2x[-n:])
                        if unmatch:
                            um2.append(str2x[:-n])
                            um1.append(str1x[n:])
                    else:
                        n, i, j = String.share_middle(str1x, str2x)
                        if n >=0:
                            rel = StrRel.SHARE_MIDDLE
                            if match:
                                s = str1x[i:i+n]  # Shared string
                                m.append(s)
                            if unmatch:
                                um1.extend(str1x.split(s))
                                um2.extend(str2x.split(s))
                        else:
                            rel = StrRel.DIFFERS
                            if unmatch:
                                um1.append(str1x)
                                um2.append(str2x)
        # Return
        if match:
            if unmatch:
                return (rel, m, um1, um2)
            else:
                return (rel, m)
        elif unmatch:
            return (rel, um1, um2)
        else:
            return rel
    
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
    def equal(s1: str,
              s2: str,
              case: bool = True,
              zenhan: bool = True
              ) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-03-02
        """
        
        if case:
            if zenhan:
                return s1 == s2
            else:
                x1 = String.zen_to_han(s1)
                x2 = String.zen_to_han(s2)
                return x1 == x2
        else:
            x1 = s1.lower()
            x2 = s2.lower()
            if zenhan:
                return x1 == x2
            else:
                y1 = String.zen_to_han(x1)
                y2 = String.zen_to_han(x2)
                return y1 == y2
        
    @staticmethod
    def escape_sqlite(s: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """

        esc = s.replace("'", "''")
        return esc

    @staticmethod
    def export_str_with_double_quote(s: str
                                     ) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-03-21
        """
        
        #return s.replace('"', '\\"')
        return s
    
    @staticmethod
    def import_str_with_double_quote(s: str
                                     ) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-12-23
        """
        
        if '"""' in s:
            si = s.replace('"""', '"')
        else:
            si = s
        
        #si = s.replace('\\', '')
        #si = s.replace('""', '"')
        
        return si
    
    @staticmethod
    def ishiragana(c: str) -> bool:
        """
        Returns True if the character is a hiragana.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        return 'HIRAGANA' in unicodedata.name(c)
    
    @staticmethod
    def iskanji(c: str) -> bool:
        """
        Returns True if the character is a kanji.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        return 'CJK UNIFIED' in unicodedata.name(c)
    
    @staticmethod
    def iskatakana(c: str) -> bool:
        """
        Returns True if the character is a hiragana.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        return 'KATAKANA' in unicodedata.name(c)
    
    @staticmethod
    def num(x: str): # -> int, float, None
        """
        def num(x: str): # -> int, float, None

        x が int または float を表す str であればその int または float を、
        そうでなければ None を返す。
        
        @author: MURAKAMI Tamotsu
        @date: 2019-01-10
        """
        
        y = String._num_int(x)
        if not y is None:
            return y
        else:
            y = String._num_float(x)
            if not y is None:
                return y
            else:
                return None

    @staticmethod
    def precedes(str1: str, str2: str) -> int:
        """
        Returns shared character numbers.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        i = str1.find(str2[0])
        if i >= 0:
            if str2.startswith(str1[i:]):
                return len(str1) - i
            else:
                return -1
        else:
            return -1
    
    @staticmethod
    def share_end(str1: str, str2: str) -> int:
        """"
        Returns shared character numbers at end.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        n = -min(len(str1), len(str2));
        i = -1;
        end = False
        while i >= n and end == False:
            if str1[i] == str2[i]:
                i -= 1
            else:
                end = True
        return -i - 1
    
    @staticmethod
    def share_middle(str1: str, str2: str) -> (int, int, int, int):
        """
        Returns (shared length, start index in string 1, start index in string 2).
        
        If none is shared, (0, -1, -1) is returned.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-05
        """
        
        n1 = len(str1)
        i1 = 0  # Scan index 1
        s1 = -1  # Start index 1

        while i1 < n1 and s1 < 0:
            s2 = str2.find(str1[i1])
            if s2 >= 0:
                s1 = i1
            else:
                i1 += 1
        
        if s1 < 0:
            return (-1, -1, -1)
        else:
            return (String.share_start(str1[s1:], str2[s2:]), s1, s2)

    @staticmethod
    def share_start(str1: str, str2: str) -> int:
        """"
        Returns shared character numbers at start.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        n = min(len(str1), len(str2));
        i = 0;
        end = False
        while i < n and end == False:
            if str1[i] == str2[i]:
                i += 1
            else:
                end = True
        return i
    
    @staticmethod
    def similarity(str1: str,
                   str2: str,
                   kanji: Union[float, int] = 3,
                   case: bool = True,
                   zenhan: bool = True
                   ) -> Union[float, int]:
        """
        Calculate similarity between the two strings.

        def similarity(str1: str,
                       str2: str,
                       kanji: Union[float, int] = 3,
                       case: bool = True,
                       zenhan: bool = True
                       ) -> Union[float, int]:

        Parameters
        ----------
        str1 : str
        str2 : str
            Strings to be compared.
        kanji : Union[float, int], optional
            ひらがな、半角1文字の適合を1とするとき、漢字1文字の適合の重みづけ。
            省略値は経験的に決めている。
            The default is 3.
        case : bool, optional
        　　　　Case-sensitive or not.
            The default is True.
        zenhan : bool, optional
            Full- and half- width sensitive or not.
            The default is True.

        Returns
        -------
        Union[float, int]
            0 <= similarity <= 1

        @author: MURAKAMI Tamotsu
        @date: 2021-11-26
        """
        
        rel, ml = String.compare(str1,
                                 str2,
                                 case = case,
                                 zenhan = zenhan,
                                 match = True,
                                 unmatch = False)
        if rel == StrRel.DIFFERS:
            return 0.0
        else:
            mkanji = 0  # Match
            mkana = 0  # Match
            melse = 0  # Match
            for s in ml:
                nkanji, nkana, nelse = String.count_char(s)
                mkanji += nkanji
                mkana += nkana
                melse += nelse
            nkanji1, nkana1, nelse1 = String.count_char(str1)
            nkanji2, nkana2, nelse2 = String.count_char(str2)
            ukanji = nkanji1 + nkanji2 - mkanji * 2  # Unmatch
            ukana = nkana1 + nkana2 - mkana * 2  # Unmatch
            uelse = nelse1 + nelse2 - melse * 2  # Unmatch
            return (mkanji * kanji + mkana + melse) / ((mkanji + ukanji) * kanji + mkana + ukana + melse + uelse)

    @staticmethod
    def startswith_any(x: str,
                       starts: Collection,
                       silent: bool = True
                       ) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-02-04
        """
        
        judge = False
        
        for s in starts:
            if x.startswith(s):
                judge = True
                if silent == False:
                    print('String.startswith_any: "{}" starts with "{}".'.format(x, s))
                break
        
        return judge
    
    @staticmethod
    def stdstr(x
               ) -> str:
        """
        Standard string

        @author: MURAKAMI Tamotsu
        @date: 2019-11-07
        """
        
        if isinstance(x, int) or isinstance(x, float):
            return '{:g}'.format(x)
        else:
            return '{}'.format(x)

    @staticmethod
    def strip_quotation(x: str) -> str:
        """
        Remove redundant quotation marks at the ends.
        Redundant quotation marks appear when reading strings from Excel outputs for example.

        @author: MURAKAMI Tamotsu
        @date: 2019-04-17
        """
        
        if (x.startswith('"') and x.endswith('"')) or (x.startswith("'") and x.endswith("'")):
            return x[1:-1]
        else:
            return x
    
    @staticmethod
    def zen_to_han(s: str
                   ) -> str:
        """
        英数全角を英数半角に変換する。
        
        https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf
        
        @author: MURAKAMI Tamotsu
        @date: 2020-03-02
        """
        
        return s.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2021-11-26
"""

if __name__ == '__main__':
    print('* Test start *')
    
    print(String.zen_to_han('東京ＡB'))
    
#    STRING_PAIRS = [('東京', 'とうきょう'),] * 1000
#    print(STRING_PAIRS)
    
    STRING_PAIRS = (
            ('東京', 'とうきょう'),
            ('トウキョウ', 'とうきょう'),
            ('東大', '大学'),
            ('計る', '設計'),
            ('設計研', '設計'),
            ('青', '青い'),
            ('不自由な', '自由な'),
            ('大学', '東京大学'),
            ('等しい', '等しい'),
            ('機械工学科', '工学'),
            ('工学', '機械工学専攻'),
            ('青い', '青く'),
            ('自然科学', '天然素材'),
            ('東京大学', '京都大学'),
            ('阪神タイガース', '阪急ブレーブス'),
            )
    
    sims = []
    for str1, str2 in STRING_PAIRS:
        sims.append(String.similarity(str1, str2))
    print(sims)

    s1 = '他'
    s2 = '他'
    print(String.compare(s1, s2))
    print(String.similarity(s1, s2))
        
    print('* Test end *')
    
# End of file