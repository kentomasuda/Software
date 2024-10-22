# -*- coding: utf-8 -*-
"""
EDR concept dictionaryp

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

# Library
from container_srclib.cons import Cons
from edr_lib.e_word import EwPos
from edr_lib.edr import Edr
from edr_srclib.jwpos import JwPos
from text_lib.lang import Lang
from text_srclib.simplepos import SimplePos

class EdrConceptDict:
    """
    @author: MURAKAMI Tamotsu
    @date: 2023-11-16
    """

    KEY_AUTHOR = 'AUTHOR'
    KEY_BH = 'BH'
    KEY_CONCEPTIDS = 'CONCEPTIDS'
    KEY_DATE = 'DATE'
    KEY_EXPL = 'EXPL'
    KEY_FN = 'FN'
    KEY_LOCK = 'LOCK'
    KEY_ST = 'ST'
    KEY_SUBS = 'SUBS'
    KEY_TYPE = 'TYPE'
    KEY_UX = 'UX'
    KEY_VERSION = 'VERSION'
    
    _concept_dict = None
    _sub_to_supers_dict = {}   
    _super_to_subs_dict = None
    
    @staticmethod
    def _add_type(typelist: list,
                  typekey: str):
        """
        概念識別子の種類を追加する。        

        Parameters
        ----------
        typelist : list
            List of KEY_ST, KEY_BH, KEY_FN and KEY_UX.
        typekey : str
            One of KEY_ST, KEY_BH, KEY_FN or KEY_UX.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """

        # 常に、ST、BH、FN、UXの順を維持する。
        
        if not typekey in typelist:
            if typekey == EdrConceptDict.KEY_ST:
                typelist.insert(0, EdrConceptDict.KEY_ST)
            elif typekey == EdrConceptDict.KEY_BH:
                if EdrConceptDict.KEY_ST in typelist:
                    typelist.insert(1, EdrConceptDict.KEY_BH)
                else:
                    typelist.insert(0, EdrConceptDict.KEY_BH)
            elif typekey == EdrConceptDict.KEY_FN:
                if EdrConceptDict.KEY_ST in typelist:
                    if EdrConceptDict.KEY_BH in typelist:
                        typelist.insert(2, EdrConceptDict.KEY_FN)
                    else:
                        typelist.insert(1, EdrConceptDict.KEY_FN)
                elif EdrConceptDict.KEY_BH in typelist:
                    typelist.insert(1, EdrConceptDict.KEY_FN)
                else:
                    typelist.insert(0, EdrConceptDict.KEY_FN)
            elif typekey == EdrConceptDict.KEY_UX:
                typelist.append(EdrConceptDict.KEY_UX)

    @staticmethod
    def _append_word_type(word_typelist: list,
                          word: str,
                          typelist: set):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        found = False
        
        for word_type in word_typelist:
            if word == word_type[0]:
                for typekey in typelist:
                    if not typekey in word_type[1]:
                        EdrConceptDict._add_type(word_type[1], typekey)
                found = True
                break
        
        if not found:
            word_typelist.append([word, typelist])

    @staticmethod
    def _del_type(typelist: list,
                  typekey: str):
        """
        概念識別子の種類を削除する。        

        Parameters
        ----------
        typelist : list
            List of KEY_ST, KEY_BH, KEY_FN and KEY_UX.
        typekey : str
            One of KEY_ST, KEY_BH, KEY_FN or KEY_UX.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
 
        if typekey in typelist:
            typelist.remove(typekey)

    @staticmethod
    def ensure_loaded(path: str):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-04
        """
        
        if EdrConceptDict._concept_dict is None:
            EdrConceptDict.load(path)
        
    @staticmethod
    def _get_concept_typelist(cid: str) -> Union[list, None]:
        """
        概念識別子の種類のリストを取得する。        

        Parameters
        ----------
        cid : str
            Concept id.

        Returns
        -------
        Union[list, None]
            List of KEY_ST, KEY_BH, KEY_FN and KEY_UX.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        if cid in EdrConceptDict._super_to_subs_dict:
            data = EdrConceptDict._super_to_subs_dict[cid]
            if EdrConceptDict.KEY_TYPE in data:
                return data[EdrConceptDict.KEY_TYPE]
            else:
                return None
        else:
            return None

    @staticmethod
    def _get_sub_paths(tail_cons: Cons) -> list:
        """
        下位の概念識別子を辿る経路のリストを取得する。

        Parameters
        ----------
        tail_cons : Cons
            head 起点となる概念識別子。

        Returns
        -------
        list
            下位の概念識別子を辿る経路のリスト

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        cid = tail_cons.head[0]
        if cid in EdrConceptDict._super_to_subs_dict:
            data = EdrConceptDict._super_to_subs_dict[cid]
            if EdrConceptDict.KEY_SUBS in data:
                sub_paths = []
                for sub in data[EdrConceptDict.KEY_SUBS]:
                    typelist = EdrConceptDict._get_concept_typelist(sub)
                    sub_paths.extend(EdrConceptDict._get_sub_paths(Cons((sub, typelist), tail_cons)))
                return sub_paths
            else:
                return [tail_cons]
        else:
            return [tail_cons]

    @staticmethod
    def _get_super_paths(tail_cons: Cons) -> list:
        """
        上位の概念識別子を辿る経路のリストを取得する。

        Parameters
        ----------
        tail_cons : Cons
            head 起点となる概念識別子。

        Returns
        -------
        list
            上位の概念識別子を辿る経路のリスト

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        cid = tail_cons.head[0]
        if cid in EdrConceptDict._sub_to_supers_dict:
            super_paths = []
            for sup in EdrConceptDict._sub_to_supers_dict[cid]:
                typelist = EdrConceptDict._get_concept_typelist(sup)
                super_paths.extend(EdrConceptDict._get_super_paths(Cons((sup, typelist), tail_cons)))
            return super_paths
        else:
            return [tail_cons]

    @staticmethod
    def _not_locked(data: dict,
                    typekey: str) -> bool:
        """
        ロック（変更不可）の有効/無効を判定する。

        Parameters
        ----------
        data : dict
            判定対象とする概念識別子のデータ。
        typekey : str
            判定対象とする概念識別子の種類。

        Returns
        -------
        bool
            True: ロックされていない（変更可）。
            False: ロックされている（変更不可）。

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        if EdrConceptDict.KEY_LOCK in data:
            locklist = data[EdrConceptDict.KEY_LOCK]
            return not typekey in locklist
        else:
            return True
        
    @staticmethod
    def load(path: str):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-07
        """
        
        print('Loading {}...'.format(path))
        
        with open(path, 'r', encoding='utf-8') as f:
            EdrConceptDict._concept_dict = json.load(f)
            if EdrConceptDict.KEY_CONCEPTIDS in EdrConceptDict._concept_dict:
                EdrConceptDict._super_to_subs_dict = EdrConceptDict._concept_dict[EdrConceptDict.KEY_CONCEPTIDS]
        
        for cid, data in EdrConceptDict._super_to_subs_dict.items():
            if EdrConceptDict.KEY_SUBS in data:
                subs = data[EdrConceptDict.KEY_SUBS]
                for sub in subs:
                    if sub in EdrConceptDict._sub_to_supers_dict:
                        EdrConceptDict._sub_to_supers_dict[sub].add(cid)
                    else:
                        EdrConceptDict._sub_to_supers_dict[sub] = {cid}

    @staticmethod
    def _lock_and_make_message(cid: str,
                               typestr: str,
                               typekey: str,
                               typeval: Union[bool, None],
                               locklist: list,
                               msg: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-18
        """
        
        new_msg = msg

        if typeval == True and not typekey in locklist:
            EdrConceptDict._add_type(locklist, typekey)
            if new_msg:
                new_msg += ', '
            else:
                new_msg = '{}{}: '.format(cid, typestr)
            new_msg += '{}:gets locked'.format(typekey)
        elif typeval == False and typekey in locklist:
            EdrConceptDict._del_type(locklist, typekey)
            if new_msg:
                new_msg += ', '
            else:
                new_msg = '{}{}: '.format(cid, typestr)
            new_msg = '{}:gets unlocked'.format(typekey)
        
        return new_msg

    @staticmethod
    def lock_concept_type(cid: str,
                          st: Union[bool, None] = None,
                          bh: Union[bool, None] = None,
                          fn: Union[bool, None] = None,
                          ux: Union[bool, None] = None,
                          sub: bool = False,
                          indent: str = ' ',
                          _level: int = 0):
        """
        指定した概念識別子の指定した種類の情報をロック（変更不可）/アンロック（変更可）にする。

        Parameters
        ----------
        cid : str
            対象とする概念識別子。
        st : Union[bool, None], optional
            Structure の情報のロック/アンロックの指定。The default is None.
            True: ロックする。
            False: アンロックする。
            None: 現在の状態を維持する。
        bh : Union[bool, None], optional
            Behavior の情報のロック/アンロックの指定。The default is None.
        fn : Union[bool, None], optional
            Function の情報のロック/アンロックの指定。The default is None.
        ux : Union[bool, None], optional
            User experience の情報のロック/アンロックの指定。The default is None.
        sub : bool, optional
            下位の概念識別子への適用の有無。The default is False.
            True: 下位の連鎖的にすべての概念識別子にこの指定を適用する。
            False: この概念識別子のみにこの指定を適用する。
        indent : str, optional
            概念の階層に応じた字下げ。The default is ' '.
        _level : int, optional
            概念階層の深さ。内部使用のみ。The default is 0.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-18
        """
        
        if cid in EdrConceptDict._super_to_subs_dict:
            data = EdrConceptDict._super_to_subs_dict[cid]
            if EdrConceptDict.KEY_LOCK in data:
                locklist = data[EdrConceptDict.KEY_LOCK]
                typelist = data[EdrConceptDict.KEY_TYPE]
                type_now = EdrConceptDict._type_str(typelist)
                
                if st == True and not EdrConceptDict.KEY_ST in locklist:
                    EdrConceptDict._add_type(locklist, EdrConceptDict.KEY_ST)
                    msg = '{}{}: {}:gets locked'.format(cid, type_now, EdrConceptDict.KEY_ST)
                elif st == False and EdrConceptDict.KEY_ST in locklist:
                    EdrConceptDict._del_type(locklist, EdrConceptDict.KEY_ST, EdrConceptDict.KEY_ST)
                    msg = '{}{}: {}:gets unlocked'.format(cid, type_now, EdrConceptDict.KEY_ST)
                else:
                    msg = ''

                msg = EdrConceptDict._lock_and_make_message(cid,
                                                            type_now,
                                                            EdrConceptDict.KEY_BH,
                                                            bh,
                                                            locklist=locklist,
                                                            msg=msg)

                msg = EdrConceptDict._lock_and_make_message(cid,
                                                            type_now,
                                                            EdrConceptDict.KEY_FN,
                                                            fn,
                                                            locklist=locklist,
                                                            msg=msg)

                msg = EdrConceptDict._lock_and_make_message(cid,
                                                            type_now,
                                                            EdrConceptDict.KEY_UX,
                                                            ux,
                                                            locklist=locklist,
                                                            msg=msg)

                if msg:
                    print('{}{}'.format(indent * _level, msg), end='')

                    if EdrConceptDict.KEY_EXPL in data:
                        print(' ', tuple(data[EdrConceptDict.KEY_EXPL].values()))
                    else:
                        print()

                if sub and EdrConceptDict.KEY_SUBS in data:
                    for subcon in data[EdrConceptDict.KEY_SUBS]:
                        EdrConceptDict.lock_concept_type(subcon, st=st, bh=bh, fn=fn, ux=ux, sub=sub, indent=indent, _level=_level+1)

    @staticmethod
    def _new_version(date: Union[str, None] = None,
                     author: Union[str, None] = None) -> Union[dict, None]:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-08
        """

        newver = {}

        if date:
            newver[EdrConceptDict.KEY_DATE] = date
        
        if author:
            newver[EdrConceptDict.KEY_AUTHOR] = author
        
        if newver:
            return newver
        else:
            return None
        
    @staticmethod
    def print_sub_concepts(cid: str,
                           indent: str = ' '):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        typelist = EdrConceptDict._get_concept_typelist(cid)

        sub_paths = [cons.to_list(reverse=True) for cons in EdrConceptDict._get_sub_paths(Cons((cid, typelist), None))]
        
        notnew = set()
        
        for sub_path in sub_paths:
            EdrConceptDict._print_sub_super_concepts(sub_path, indent=indent, level=0, notnew=notnew)

    @staticmethod
    def _print_sub_super_concepts(cid_path: list,
                                  indent: str,
                                  level: int,
                                  notnew: set):
        """
        Common for sub concepts and super concepts.
        
        @author: MURAKAMI Tamotsu
        @date: 2023-11-08
        """
        
        if cid_path:
            cid_type = cid_path[0]
            cid = cid_type[0]
            type_ = cid_type[1]
            print('{}{}{}'.format(indent * level, cid, EdrConceptDict._type_str(type_)), end='')
            if cid in notnew:
                print(' <Not new>')
            else:
                print(' {}'.format(tuple(EdrConceptDict._super_to_subs_dict[cid][EdrConceptDict.KEY_EXPL].values())))
                notnew.add(cid)
            EdrConceptDict._print_sub_super_concepts(cid_path[1:], indent, level=level+1, notnew=notnew)

    @staticmethod
    def print_super_concepts(cid: str,
                             indent: str = ' '):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        typelist = EdrConceptDict._get_concept_typelist(cid)
        
        super_paths = [cons.to_list(reverse=True) for cons in EdrConceptDict._get_super_paths(Cons((cid, typelist), None))]
        
        notnew = set()
        
        for super_path in super_paths:
            EdrConceptDict._print_sub_super_concepts(super_path, indent=indent, level=0, notnew=notnew)

    @staticmethod
    def print_word_super_concepts(w: str,
                                  lang: Lang = Lang.JPN | Lang.ENG,
                                  pos: Union[EwPos, JwPos, SimplePos] = None,
                                  suggest: bool = True,
                                  indent: str = ' '):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        judge, cands = Edr.check_headword(w, lang=lang, pos=pos, suggest=suggest, simmin=0.7, num = 5)
        
        if judge:
            cids = Edr.headword_conceptids(w, lang=lang, pos=pos)
            
            super_paths = []
            
            for cid in cids:
                typelist = EdrConceptDict._get_concept_typelist(cid)
                super_paths.extend([cons.to_list(reverse=True) for cons in EdrConceptDict._get_super_paths(Cons((cid, typelist), None))])
        
            notnew = set()
            
            for super_path in super_paths:
                EdrConceptDict._print_sub_super_concepts(super_path, indent=indent, level=0, notnew=notnew)
        else:
            print(cands)

    @staticmethod
    def _match_typelist(typelist: list,
                        st: Union[bool, None] = None,
                        bh: Union[bool, None] = None,
                        fn: Union[bool, None] = None,
                        ux: Union[bool, None] = None) -> bool:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        if (st == True and not EdrConceptDict.KEY_ST in typelist) or\
           (st == False and EdrConceptDict.KEY_ST in typelist) or\
           (bh == True and not EdrConceptDict.KEY_BH in typelist) or\
           (bh == False and EdrConceptDict.KEY_BH in typelist) or\
           (fn == True and not EdrConceptDict.KEY_FN in typelist) or\
           (fn == False and EdrConceptDict.KEY_FN in typelist) or\
           (ux == True and not EdrConceptDict.KEY_UX in typelist) or\
           (ux == False and EdrConceptDict.KEY_UX in typelist):
            return False
        else:
            return True

    @staticmethod
    def print_words(st: Union[bool, None] = None,
                    bh: Union[bool, None] = None,
                    fn: Union[bool, None] = None,
                    ux: Union[bool, None] = None,
                    lang: Lang = Lang.JPN | Lang.ENG,
                    pos: Union[EwPos, JwPos, SimplePos] = None,
                    num: Union[int, None] = None):
        """
        指定した種類の条件に適合する見出し語を表示する。        

        Parameters
        ----------
        st : Union[bool, None], optional
            Structure の条件指定。The default is None.
            True: Structure に該当するものを対象とする。
            False: Structure に該当しないものを対象とする。
            None: Structure に関しては条件を指定しない。
        bh : Union[bool, None], optional
            Behavior の条件指定。The default is None.
        fn : Union[bool, None], optional
            Function の条件指定。The default is None.
        ux : Union[bool, None], optional
            User experience の条件指定。The default is None.
        lang : Lang, optional
            DESCRIPTION. The default is Lang.JPN | Lang.ENG.
        pos : Union[EwPos, JwPos, SimplePos], optional
            DESCRIPTION. The default is None.
        num : Union[int, None], optional
            表示する語数の上限. The default is None.
            Int: その語数を超えた時点で打ち切る。
            None: 語数に制限を付さない。

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        word_typelist = []
        
        stop = False
        
        for cid, data in EdrConceptDict._super_to_subs_dict.items():
            if stop == False:
                typelist = EdrConceptDict._get_concept_typelist(cid)
                if EdrConceptDict._match_typelist(typelist, st=st, bh=bh, fn=fn, ux=ux):
                    for word in set(Edr.conceptid_headwords(cid, lang=lang, pos=pos)):
                        EdrConceptDict._append_word_type(word_typelist, word, typelist)
                        if not num is None and len(word_typelist) >= num:
                            stop = True
                            break
        
        if word_typelist:
            word_typelist.sort()
            
            print('[', end='')
    
            word_type = word_typelist[0]
            print(word_type[0], end='')
            print(EdrConceptDict._type_str(word_type[1]), end='')
    
            for word_type in word_typelist[1:]:
                print(' ,', end='')
                print(word_type[0], end='')
                print(EdrConceptDict._type_str(word_type[1]), end='')
            print(']')

    @staticmethod
    def save(path: str,
             date: str = None,
             author: str = None):
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-08
        """
        
        if EdrConceptDict._concept_dict:
            newver = EdrConceptDict._new_version(date=date, author=author)

            if newver:
                if EdrConceptDict.KEY_VERSION in EdrConceptDict._concept_dict:
                    vers_now = EdrConceptDict._concept_dict[EdrConceptDict.KEY_VERSION]
                    if newver != vers_now[0]:
                        vers_now.insert(0, newver)
            else:
                # Version を辞書の先頭にするため。
                EdrConceptDict._concept_dict = {EdrConceptDict.KEY_VERSION: [newver]} | EdrConceptDict._concept_dict
    
            print('Saving {}...'.format(path))

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(EdrConceptDict._concept_dict,
                          f, ensure_ascii=False, check_circular=True, indent=1, separators=(',',':'))
        else:
            print('EDR concept dictionary is not loaded.')

    @staticmethod
    def set_concept_type(cid: str,
                         st: Union[bool, None] = None,
                         bh: Union[bool, None] = None,
                         fn: Union[bool, None] = None,
                         ux: Union[bool, None] = None,
                         sub: bool = False,
                         date: Union[str, None] = None,
                         author: Union[str, None] = None,
                         indent: str = ' ',
                         _level: int = 0):
        """
        概念識別子の種類を指定する。        

        Parameters
        ----------
        cid : str
            対象とする概念識別子。
        st : Union[bool, None], optional
            Structure の指定。The default is None.
            True: Structure に該当するものとする。
            False: Structure に該当しないものとする。
            None: Structure に関して状態を変更しない。
        bh : Union[bool, None], optional
            Behavior の指定。The default is None.
        fn : Union[bool, None], optional
            Function の指定。The default is None.
        ux : Union[bool, None], optional
            User experience の指定。The default is None.
        sub : bool, optional
            下位の概念識別子への適用の有無。The default is False.
            True: 下位の連鎖的にすべての概念識別子にこの指定を適用する。
            False: この概念識別子のみにこの指定を適用する。
        date : Union[str, None], optional
            DESCRIPTION. The default is None.
        author : Union[str, None], optional
            DESCRIPTION. The default is None.
        indent : str, optional
            概念の階層に応じた字下げ。The default is ' '.
        _level : int, optional
            概念階層の深さ。内部使用のみ。The default is 0.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-11-18
        """
        
        if cid in EdrConceptDict._super_to_subs_dict:
            data = EdrConceptDict._super_to_subs_dict[cid]
            if EdrConceptDict.KEY_TYPE in data:
                typelist = data[EdrConceptDict.KEY_TYPE]
                type_now = EdrConceptDict._type_str(typelist)
                
                if EdrConceptDict._not_locked(data, EdrConceptDict.KEY_ST) and st == True and not EdrConceptDict.KEY_ST in typelist:
                    st_now = False
                    EdrConceptDict._add_type(typelist, EdrConceptDict.KEY_ST)
                    msg = '{}{}: {}:{}->{}'.format(cid, type_now, EdrConceptDict.KEY_ST, st_now, st)
                elif EdrConceptDict._not_locked(data, EdrConceptDict.KEY_ST) and st == False and EdrConceptDict.KEY_ST in typelist:
                    st_now = True,
                    EdrConceptDict._del_type(typelist, EdrConceptDict.KEY_ST)
                    msg = '{}{}: {}:{}->{}'.format(cid, type_now, EdrConceptDict.KEY_ST, st_now, st)
                else:
                    msg = ''

                msg = EdrConceptDict._set_type_and_make_message(cid,
                                                                type_now,
                                                                data,
                                                                EdrConceptDict.KEY_BH,
                                                                bh,
                                                                typelist=typelist,
                                                                msg=msg)

                msg = EdrConceptDict._set_type_and_make_message(cid,
                                                                type_now,
                                                                data,
                                                                EdrConceptDict.KEY_FN,
                                                                fn,
                                                                typelist=typelist,
                                                                msg=msg)

                msg = EdrConceptDict._set_type_and_make_message(cid,
                                                                type_now,
                                                                data,
                                                                EdrConceptDict.KEY_UX,
                                                                ux,
                                                                typelist=typelist,
                                                                msg=msg)

                # if EdrConceptDict._not_locked(data, EdrConceptDict.KEY_FN) and fn == True and not EdrConceptDict.KEY_FN in typelist:
                #     fn_now = False
                #     EdrConceptDict._add_type(typelist, EdrConceptDict.KEY_FN)
                #     if msg:
                #         msg += ', '
                #     else:
                #         msg = '{}{}: '.format(cid, type_now)
                #     msg += 'fn:{}->{}'.format(fn_now, fn)
                # elif EdrConceptDict._not_locked(data, EdrConceptDict.KEY_FN) and fn == False and EdrConceptDict.KEY_FN in typelist:
                #     fn_now = True
                #     EdrConceptDict._del_type(typelist, EdrConceptDict.KEY_FN)
                #     if msg:
                #         msg += ', '
                #     else:
                #         msg = '{}{}: '.format(cid, type_now)
                #     msg = 'fn:{}->{}'.format(fn_now, fn)

                # if EdrConceptDict._not_locked(data, EdrConceptDict.KEY_UX) and ux == True and not EdrConceptDict.KEY_UX in typelist:
                #     ux_now = False
                #     EdrConceptDict._add_type(typelist, EdrConceptDict.KEY_UX)
                #     if msg:
                #         msg += ', '
                #     else:
                #         msg = '{}{}: '.format(cid, type_now)
                #     msg += 'ux:{}->{}'.format(ux_now, ux)
                # elif EdrConceptDict._not_locked(data, EdrConceptDict.KEY_UX) and ux == False and EdrConceptDict.KEY_UX in typelist:
                #     ux_now = True
                #     EdrConceptDict._del_type(typelist, EdrConceptDict.KEY_UX)
                #     if msg:
                #         msg += ', '
                #     else:
                #         msg = '{}{}: '.format(cid, type_now)
                #     msg = 'ux:{}->{}'.format(ux_now, ux)

                if msg:
                    newver = EdrConceptDict._new_version(date=date, author=author)
        
                    if newver:
                        if EdrConceptDict.KEY_VERSION in data:
                            vers_now = data[EdrConceptDict.KEY_VERSION]
                            if newver != vers_now[0]:
                                vers_now.insert(0, newver)
                        else:
                            data[EdrConceptDict.KEY_VERSION] = [newver]

                    print('{}{}'.format(indent * _level, msg), end='')

                    if EdrConceptDict.KEY_EXPL in data:
                        print(' ', tuple(data[EdrConceptDict.KEY_EXPL].values()))
                    else:
                        print()

                if sub and EdrConceptDict.KEY_SUBS in data:
                    for subcon in data[EdrConceptDict.KEY_SUBS]:
                        EdrConceptDict.set_concept_type(subcon, st=st, bh=bh, fn=fn, ux=ux, sub=sub, indent=indent, _level=_level+1)

    @staticmethod
    def _set_type_and_make_message(cid: str,
                                   typestr: str,
                                   data: dict,
                                   typekey: str,
                                   typeval: Union[bool, None],
                                   typelist: list,
                                   msg: str) -> str:
        """
        @author: MURAKAMI Tamotsu
        @date: 2023-11-18
        """
        
        new_msg = msg

        if EdrConceptDict._not_locked(data, typekey) and typeval == True and not typekey in typelist:
            typeval_now = False
            EdrConceptDict._add_type(typelist, typekey)
            if msg:
                msg += ', '
            else:
                msg = '{}{}: '.format(cid, typestr)
            msg += '{}:{}->{}'.format(typekey, typeval_now, typeval)
        elif EdrConceptDict._not_locked(data, typekey) and typeval == False and typekey in typelist:
            typeval_now = True
            EdrConceptDict._del_type(typelist, typekey)
            if msg:
                msg += ', '
            else:
                msg = '{}{}: '.format(cid, typestr)
            msg = '{}:{}->{}'.format(typekey, typeval_now, typeval)
        
        return new_msg

    @staticmethod
    def _type_str(typelist: list) -> str:
        """
        種類のリストから表示用文字列を作成する。

        Parameters
        ----------
        typelist : list
            List of KEY_ST, KEY_BH, KEY_FN and KEY_UX.

        Returns
        -------
        str
            表示用文字列

        @author: MURAKAMI Tamotsu
        @date: 2023-11-16
        """
        
        type_str = ''
        
        for typekey in (EdrConceptDict.KEY_ST, EdrConceptDict.KEY_BH, EdrConceptDict.KEY_FN, EdrConceptDict.KEY_UX):
            if typekey in typelist:
                if type_str:
                    type_str += ','
                type_str += typekey
        
        return '[' + type_str + ']'


"""
Test

@author: MURAKAMI Tamotsu
@date: 2023-11-16
"""

if __name__ == '__main__':
   
    print('* Test starts *')
    
    concept_dict_path = '../edr_data/edr_concept_dict_blank.json'

    EdrConceptDict.ensure_loaded(concept_dict_path)

    EdrConceptDict.save('../edr_libp/Output/edr_concept_dict_update.json', date='2023-11-09', author='MURAKAMI Tamotsu')

    print('* Test ends *')
        
# End of file