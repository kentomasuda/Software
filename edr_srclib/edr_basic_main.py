# -*- coding: utf-8 -*-
"""
EDR basic sample

@author: MURAKAMI Tamotsu
@date: 2023-12-06
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_lib.concept import Concept
from edr_lib.concept import EdrClsf
from edr_lib.edr import Edr
from edr_lib.j_word import JWord
from edr_srclib.jwpos import JwPos
from text_lib.lang import Lang
from text_srclib.simplepos import SimplePos

"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-12-06
"""

if __name__ == "__main__":
    print('* Start *')
    
    """
    目的の語が見出し語にあるかどうかの確認
    """

    print(Edr.check_headword.__doc__) # Print information about the method.
    
    """
    有無の判定のみ
    """
    ret = Edr.check_headword('きれい',
                             lang=Lang.JPN,
                             pos=SimplePos.all_(),
                             suggest=False)
    print(ret)
    
    """
    ない場合に、似た文字列を提示。
    """
    ret = Edr.check_headword('きれい',
                             lang=Lang.JPN,
                             pos=SimplePos.all_(),
                             suggest=True)
    print(ret)
    
    ret = Edr.check_headword('きれい',
                             lang=Lang.JPN,
                             pos=JwPos.all_(), # Edrの日本語品詞を使用。
                             suggest=True)
    print(ret)
    
    ret = Edr.check_headword('きれいだ',
                             lang=Lang.JPN,
                             pos=SimplePos.ADJ,
                             suggest=True)
    print(ret)
    
    ret = Edr.check_headword('きれいだ',
                             lang=Lang.JPN,
                             pos=JwPos.all_(),
                             suggest=True)
    print(ret)
    
    # ret = Edr.check_headword('clean',
    #                          lang=Lang.ENG,
    #                          suggest=True)
    # print(ret)
    
    """
    語から概念識別子を取得する。
    """
    
    print(Edr.headword_conceptids.__doc__)
    
    cidset1 = Edr.headword_conceptids('みかん', lang=Lang.JPN, pos=SimplePos.N)
    
    print(cidset1)
    
    cidset2 = Edr.headword_conceptids('りんご', lang=Lang.JPN, pos=SimplePos.N)
    
    print(cidset2)
    
    """
    概念識別子から語を取得する。
    """

    print(Edr.conceptid_headwords.__doc__)
    
    ret = Edr.conceptid_headwords(cidset1[0], lang=Lang.JPN)
    
    print(ret)
    
    ret = JWord.conceptid_headwords('3ce6c0', pos=SimplePos.N)  # 日本語の場合
    
    print(ret)
    
    ret = JWord.conceptid_headwords('3ce6c0', pos=SimplePos.V)  # 日本語の場合
    
    print(ret)
    
    """
    概念識別子の上位の概念識別子を取得する。
    """

    print(Edr.conceptids_of_classification.__doc__)
    
    cidset3 = Edr.conceptids_of_classification(cidset2[0], clsf=EdrClsf.SUPER)
    
    print(cidset3)

    ret = Edr.conceptid_headwords(cidset3[0], lang=Lang.JPN)
    print(ret)
    
    """
    概念識別子の説明を取得する。
    """
    
    print(Concept.concept_expl(cidset3[0]))

    """
    概念識別子の下位の概念識別子を取得する。
    """

    cidset4= Edr.conceptids_of_classification(cidset3[0], clsf=EdrClsf.SUB)
    
    print(cidset4)
    
    for cid in cidset4:
        print(Edr.conceptid_headwords(cid, lang=Lang.JPN | Lang.ENG))

    print('* End *')       

# End of file