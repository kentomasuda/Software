# -*- coding: utf-8 -*-
"""
Collection basic sample

@author: MURAKAMI Tamotsu
@date: 2022-10-13
"""

import sys
import os
sys.path.append(os.pardir)

# Library
from container_lib.collection import Collection_
from math_srclib.calc_type import CalcType


print('start')

print(Collection_.compare.__doc__)

list1 = ['a', 'b', 'c']
list2 = ['d', 'c', 'b', 'a']

print('単純な比較の例。要素対の類似度のリストのみ返す。')
print(Collection_.compare(list1, list2, simtype=CalcType.ONE_TO_ONE, pairs=True))

print('要素をどのように対応させたかの情報も返す例。')
print('返す値は、要素対の類似度のリスト、list1の要素順、list2の要素順、のtuple。')
print('list1の要素順の第i要素とlist2の要素順の第i要素を対として対応させたことを表す。')
print(Collection_.compare(list1, list2, simtype=CalcType.ONE_TO_ONE, pairs=True))

list2 = ['d', 'b', 'e', 'a']

print('最大でも2対しか対応しない場合の例。')
print(Collection_.compare(list1, list2, simtype=CalcType.ONE_TO_ONE))

print('要素をどのように対応させたかの情報も返す例。')
print(Collection_.compare(list1, list2, simtype=CalcType.ONE_TO_ONE, pairs=True))

def mysimf(x, y):
    """
    Similarity function
    """
    if x == y:
        return 0.0
    else:
        return 1.0
    
print('要素の適合と値の大小を逆にすると、できるだけ要素が一致しない対応付けを返すことになる。')    
print(Collection_.compare(list1, list2, simf=mysimf, simtype=CalcType.ONE_TO_ONE, pairs=True))

set1 = {('a', 1), ('a', 2), ('b', 1), ('b', 2), ('c', 1), ('c', 2)}
set2 = {('d', 1), ('d', 2), ('b', 1), ('b', 2), ('a', 1), ('a', 2)}

print('要素は構造を持っていても可。')
print(Collection_.compare(set1, set2, simtype=CalcType.ONE_TO_ONE, pairs=True))

def mysimf2(x, y):
    """
    Element pair similarity function
    """
    if x == y:
        return 1.0 # 同じものなら 1。
    elif x[1] == y[1]: # 第2要素が同じなら 0.5。
        return 0.5
    else:
        return 0.0

print("要素比較関数の定義により、比較の仕方が異なる。('c',1)と('d',1)の対に0.5が与えられている。")
print(Collection_.compare(set1, set2, simf=mysimf2, simtype=CalcType.ONE_TO_ONE, pairs=True))

print('end')

# End of file