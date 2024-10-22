# -*- coding: utf-8 -*-
"""
Multiprocess sample main

@author: MURAKAMI Tamotsu
@date: 2022-12-22
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import math
from multiprocessing import Pool
from time import time
from typing import Union

#global variable
ints2 = range(20, 30)

def compose1(two_ints: tuple) -> str:
    """
    @author: MURAKAMI Tamotsu
    @date: 2022-12-21
    """
    i1, i2 = two_ints
    
    return '{}_{}'.format(i1, i2)

def compose2(i1: int) -> list:
    """
    @author: MURAKAMI Tamotsu
    @date: 2022-12-21
    """
    
    return ['{}_{}'.format(i1, i2) for i2 in ints2] # 内包表記

def is_prime(x: int) -> Union[int, None]:
    """
    @author: MURAKAMI Tamotsu
    @date: 2022-12-22
    """
    
    judge = True

    for i in range(2, math.floor(x / 2)):
        if x % i == 0:
            judge = False
            break
    
    if judge:
        return x
    else:
        return None
"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-12-21
"""
if __name__ == '__main__':
    
    print('* Main starts *')
    
    """
    以下で、problem = 1 or 2 を指定し実行する。
    
    problem = 1 の場合
    multiprocess = True と multiprocess = False の場合で、所要時間とCPU使用率を比較する。

    problem = 2 の場合
    二つの要素の組合せに対する処理の並列化の方法二つ。    
    """
    
    problem = 1
    # problem = 2
    
    multiprocess = True
    # multiprocess = False

    if problem == 1:
        # n1 から n2 までの素数を求める。
        
        n1 = 950000
        n2 = 1000000
        int_range = range(n1, n2)

        if multiprocess:
            start = time()
        
            N_CPU = os.cpu_count()
            print('N_CPU=', N_CPU)
    
            with Pool(processes=N_CPU) as pool:
                for p in pool.imap_unordered(func = is_prime, iterable = int_range):
                    if p:
                        print(p)
                
                pool.close()
                pool.join()
        
            sec = time() - start
            print('Parallel: {} sec.'.format(sec))
    
        else:
            start = time()
            
            for x in int_range:
                p = is_prime(x)
                
                if p:
                    print(x)
            
            sec = time() - start
            print('Serial: {} sec.'.format(sec))
    
    elif problem == 2:
        # 2つのリスト ints1、ints2 中の整数のすべての組合せ文字列を求める。
        # Multiprocess では引数を1つしか渡せないので、引数を2つ渡す二方法を示す。

        ints1 = range(10, 20)
        
        # 方法1
        # すべての組合せのリストを1引数として渡す。

        N_CPU = os.cpu_count()
        print('N_CPU=', N_CPU)
        
        i1i2_list = []
        for i1 in ints1:
            i1i2_list.extend([(i1, i2) for i2 in ints2])

        with Pool(processes=N_CPU) as pool:
            for s in pool.imap_unordered(func = compose1, iterable = i1i2_list):
                print(s)
            
            pool.close()
            pool.join()
        
        # 方法1
        # 一方のリスト ints1 の要素を引数として渡し、他方のリスト ints2 は大域変数としてアクセスする。
 
        N_CPU = os.cpu_count()
        print('N_CPU=', N_CPU)
        
        with Pool(processes=N_CPU) as pool:
            for sl in pool.imap_unordered(func = compose2, iterable = ints1):
                print(sl)
            
            pool.close()
            pool.join()

    print('* Main ends *')

# End of file