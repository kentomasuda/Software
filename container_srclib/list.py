# -*- coding: utf-8 -*-
"""
List library

@author: MURAKAMI Tamotsu
@date: 2022-11-27
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import numpy as np
from operator import itemgetter
from typing import Callable
from typing import Union

# Library
from misc_srclib.time_ import Time_

class List_:
    """
    List library
    
    Avoid conflict with typing.List.
    
    @author: MURAKAMI Tamotsu
    @date: 2018-08-31
    """
    
    @staticmethod
    def _indices2(simtable: tuple,
                  n1: int
                  ) -> list:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-01-03
        """

        sim_idx2_l = [[0, i] for i in range(len(simtable[0]))]

        for row1 in simtable:
            i = 0
            for sim in row1:
                sim_idx2_l[i][0] += sim
                i += 1

        nz_sim_idx2_l = []
        n_nz = 0
        z_idx2_l = []

        for sim_idx2 in sim_idx2_l:
            if sim_idx2[0] > 0: # Non zero
                nz_sim_idx2_l.append(sim_idx2)
                n_nz += 1
            else: # Zero
                z_idx2_l.append(sim_idx2[1])

        nz_sim_idx2_l.sort(key=itemgetter(1))
        nz_idx2_l = [sim_idx2[1] for sim_idx2 in sorted(nz_sim_idx2_l, reverse=True, key=itemgetter(0))]

        if n_nz < n1:
            z_idx2_l.sort()
            nz_idx2_l.extend(z_idx2_l[:n1 - n_nz])

        return nz_idx2_l
    
    @staticmethod
    def _max_list(simtable: tuple
                      ) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-01-03
        """
        
        return tuple(max(l) for l in simtable)
    
    @staticmethod
    def _simtable(list1: list,
                  list2: list,
                  simf: Callable
                 ) -> tuple:
        """
        @author: MURAKAMI Tamotsu
        @date: 2019-12-30
        """
        
        return tuple(tuple(simf(e1, e2) for e2 in list2) for e1 in list1)
    
    @staticmethod
    def append_new(l: list, item):
        """
        Append item if it is not in the list.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-11-27
        """
        
        if item not in l:
            l.append(item)

    @staticmethod
    def argmin(l: list
               ) -> list:
        """
        
        The list can contain None which is ignored and skipped.
        
        @author: MURAKAMI Tamotsu
        @date: 2019-03-11
        """
        
        minval = None
        indices = None
        
        idx = 0
        for x in l:
            if x is None:
                pass # Just ignore and skip.
            elif minval is None:
                minval = x
                indices = [idx]
            elif x == minval:
                indices.append(idx)
            elif x < minval:
                minval = x
                indices = [idx]
            
            idx += 1
        
        return indices
        
    @staticmethod
    def compare(list1: list,
                list2: list,
                simf: Callable,
                one_to_one: bool = True,
                pairs: bool = False
                ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-01-09
        """
        
        simtable = List_._simtable(list1, list2, simf)
        best = [] # [seq2, siml, sim, continue]

        if one_to_one:
            posmax = sum(List_._max_list(simtable))
            indices2 = List_._indices2(simtable, len(list1))
            List_.compare_one_to_one(list(range(len(list1))),
                                     indices2,
                                     simtable,
                                     [],
                                     [],
                                     posmax,
                                     best)
        else:
            List_.compare_one_to_many(simtable, best)
            
        if pairs:
            return (best[1], tuple(list2[i] for i in best[0]))
        else:
            return best[1]

    @staticmethod
    def compare_one_to_many(simtable: tuple,
                            best: list # [seq2, siml, sim, continue]
                            ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-01-09
        """
        
        siml = [max(sims) for sims in simtable]
        sim = sum(siml)
        seq2 = [np.argmax(sims) for sims in simtable]
        best.extend([seq2, siml, sim, False])

    @staticmethod
    def compare_one_to_one(rest1: list,
                           rest2: list,
                           simtable: tuple,
                           seq2: list,
                           siml: list,
                           posmax: float,
                           best: list # [seq2, siml, sim, continue]
                           ):
        """
        @author: MURAKAMI Tamotsu
        @date: 2020-01-09
        """
        
        if rest1 != []:
            simlist = simtable[rest1[0]]
            for i in range(len(rest2)):
                if best == [] or best[3] == True: # Continue
                    r = rest2.copy()
                    i2 = r.pop(i)
                    s = seq2.copy()
                    s.append(i2)
                    sl = siml.copy()
                    sl.append(simlist[i2])
                    List_.compare_one_to_one(rest1[1:], r, simtable, s, sl, posmax, best)
                else:
                    break
        else:
            sim = sum(siml)
            if best == []:
                best.extend([seq2, siml, sim, True])
            elif sim > best[2]:
                best[0] = seq2
                best[1] = siml
                best[2] = sim
            if sim >= posmax:
                best[3] = False

    @staticmethod
    def extend_new(l: list,
                   items: Union[list, set, tuple]):
        """
        Extend items if they are not in the list.
        
        @author: MURAKAMI Tamotsu
        @date: 2022-11-27
        """
        
        for item in items:
            if item not in l:
                l.append(item)

"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-01-09
"""

if __name__ == '__main__':
    print('* Test starts *')
    
    list1 = list(range(9))
#    list2 = list(range(1, 6))
#    list2 = list(reversed(range(6)))
    list2 = list(reversed(range(1, 11)))

    start = Time_.time_now()    
    result = List_.compare(list1,
                           list2,
                           simf = lambda x, y: 1 if x == y else 0,
                           one_to_one = False,
                           pairs = True)
    time = Time_.time_now(start)    
    print(result)
    print(time)
    
    print('* Test ends *')

# End of file