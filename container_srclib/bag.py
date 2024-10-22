# -*- coding: utf-8 -*-
"""
Bag (Multiset)

@author: MURAKAMI Tamotsu
@date: 2023-11-15
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import statistics
from typing import Any
from typing import Callable
from typing import Union

# Library
from math_srclib.calc_type import CalcType


class Bag(dict):
    """
    Bag (Multiset)
    
    class Bag(dict):

    Internally it is a dict whoes keys are elements and values are their frequencies.    
        
    @author: MURAKAMI Tamotsu
    @date: 2022-10-18
    """
    
    def __init__(self,
                 elem: Any = None,
                 elems: Union[list, set, tuple] = None):
        """
        Create an instance.

        Parameters
        ----------
        elem : Any, optional
            An initial element of the bag. The default is None.
        elems : Union[list, set, tuple], optional
            Initial elements of the bag. The default is None.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2022-10-18
        """
        
        super().__init__()
        
        if elem:
            self.add_elem(elem)
    
        if elems:
            self.add_elems(elems)

    def add(self, elem):
        """
        廃止予定。
        
        @author: MURAKAMI Tamotsu
        @date: 2021-12-21
        """
        
        if isinstance(elem, list) or isinstance(elem, set) or isinstance(elem, tuple):
            self.add_elems(elem)
        else:
            self.add_elem(elem)

    def add_elem(self,
                 elem: Any):
        """
        Add an element to the bag.

        Parameters
        ----------
        elem : Any
            An element to be added to the bag.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2023-06-07
        """
        
        if elem in self:
            self[elem] += 1
        elif elem.has_equal():
            new = True
            for x in self.keys():
                if elem.equal(x):
                    self[x] += 1
                    new = False
                    break
            if new:
                self[elem] = 1
        else:
            self[elem] = 1
        
    def add_elems(self,
                  elems: Union[list, set, tuple]):
        """
        Add elements to the bag.

        Parameters
        ----------
        elems : Union[list, set, tuple]
            Elements to be added to the bag.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2021-12-21
        """
        
        for x in elems:
            self.add_elem(x)
    
    @staticmethod
    def calc_sim(bag1, # Bag
                 bag2, # Bag
                 simf: Callable,
                 freq: bool = False,
                 bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                 scalar: bool = False,
                 pairs: bool = False) -> Union[float, int, tuple]:
        """
        Calculate similarity between Bags.
        
        def bag_sim(bag1: Bag,
                    bag2: Bag,
                    simf: Callable,
                    freq: bool = False,
                    bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                    scalar: bool = False,
                    pairs: bool = False) -> Union[float, int, tuple]:

        @author: MURAKAMI Tamotsu
        @date: 2022-12-18
        """
        
        if freq:
            print('Bag.calc_sim: Currently freq=True is not supported.')
        
        elems1 = bag1.get_elems()
        elems2 = bag2.get_elems()
        
        n1 = len(elems1)
        n2 = len(elems2)

        sims_without_freqs1 = [0] * n1
        sims_without_freqs2 = [0] * n2
        
        partners1 = [None] * n1
        partners2 = [None] * n2
        
        i1 = 0
        for elem1 in elems1:
            i2 = 0
            for elem2 in elems2:
                sim = simf(elem1, elem2)
                if sim > sims_without_freqs1[i1]:
                    sims_without_freqs1[i1] = sim
                    partners1[i1] = elem2
                if sim > sims_without_freqs2[i2]:
                    sims_without_freqs2[i2] = sim
                    partners2[i2] = elem1
                i2 += 1
            i1 += 1
        
        if scalar:
            # freqs1 = bag1.get_freqs(freq=freq)
            # freqs2 = bag2.get_freqs(freq=freq)
            # freq_sum1 = sum(freqs1)
            # freq_sum2 = sum(freqs2)
            # sims_with_freqs1 = tuple(map(lambda sim, freq: sim * freq / freq_sum1, sims_without_freqs1, freqs1))
            # sims_with_freqs2 = tuple(map(lambda sim, freq: sim * freq / freq_sum2, sims_without_freqs2, freqs2))

            if bsimtype == CalcType.MAX_MAX_1_TO_M:
                sim = (max(sims_without_freqs1) + max(sims_without_freqs2)) / 2
            elif bsimtype == CalcType.MEAN_MAX_1_TO_M:
                sim = (statistics.mean(sims_without_freqs1) + statistics.mean(sims_without_freqs2)) / 2
            elif bsimtype == CalcType.MEDIAN_MAX_1_TO_M:
                sim = (statistics.median(sims_without_freqs1) + statistics.median(sims_without_freqs2)) / 2
            elif bsimtype == CalcType.MEDIAN_HIGH_MAX_1_TO_M:
                sim = (statistics.median_high(sims_without_freqs1) + statistics.median_high(sims_without_freqs2)) / 2
            else:
                sim = (sum(sims_without_freqs1) * n1 + sum(sims_without_freqs2) * n2) / (n1 + n2) # Old

            if pairs:
                return (sim, tuple(partners1), tuple(partners2))
            else:
                return sim
        elif pairs: # scalar == False, pairs == True
            return (tuple(sims_without_freqs1), tuple(sims_without_freqs2), tuple(partners1), tuple(partners2))
        else: # scalar == False, pairs == False
            return (tuple(sims_without_freqs1), tuple(sims_without_freqs2))

    @staticmethod
    def calc_sim_asym(bag1, # Bag
                      bag2, # Bag
                      simf: Callable,
                      freq: bool = False,
                      bsimtype: CalcType = CalcType.MEAN_MAX_1_TO_M,
                      scalar: bool = False,
                      pairs: bool = False) -> Union[float, int, tuple]:
        """
        Calculate asymmetric similarity between Bags.
        
        @author: MURAKAMI Tamotsu
        @date: 2023-11-15
        """
        
        if freq:
            print('Bag.calc_sim_asym: Currently freq=True is not supported.')
        
        elems1 = bag1.get_elems()
        
        n1 = len(elems1)

        sims_without_freqs1 = [0] * n1
        
        partners1 = [None] * n1
        
        i1 = 0
        for elem1 in elems1:
            for elem2 in bag2.get_elems():
                sim = simf(elem1, elem2)
                if sim > sims_without_freqs1[i1]:
                    sims_without_freqs1[i1] = sim
                    partners1[i1] = elem2
            i1 += 1
        
        if scalar:
            if bsimtype == CalcType.MAX_MAX_1_TO_M:
                sim = max(sims_without_freqs1)
            elif bsimtype == CalcType.MEAN_MAX_1_TO_M:
                sim = statistics.mean(sims_without_freqs1)
            elif bsimtype == CalcType.MEDIAN_MAX_1_TO_M:
                sim = statistics.median(sims_without_freqs1)
            elif bsimtype == CalcType.MEDIAN_HIGH_MAX_1_TO_M:
                sim = statistics.median_high(sims_without_freqs1)
            else:
                sim = statistics.mean(sims_without_freqs1)

            if pairs:
                return (sim, tuple(partners1))
            else:
                return sim
        elif pairs: # scalar == False, pairs == True
            return (tuple(sims_without_freqs1), tuple(partners1))
        else: # scalar == False, pairs == False
            return tuple(sims_without_freqs1)

    def copy(self): # -> Bag:
        """
        Create a copy of the bag.

        Returns
        -------
        Bag
            Copied Bag instance.

        @author: MURAKAMI Tamotsu
        @date: 2021-12-21
        """
        
        bag = Bag()
        
        for k, v in self.elems():
            bag[k] = v
        
        return bag
        
    def get_elem_freq(self) -> Union[int, None]:
        """
        Obtain frequency of the element in the Bag.

        Returns
        -------
        Union[int, None]
            Frequency of the element.
            None if the element is not in the bag.

        @author: MURAKAMI Tamotsu
        @date: 2022-10-18
        """
        
        return tuple(self.keys())
    
    def get_elems(self) -> tuple:
        """
        Obtain elements in the Bag.

        Returns
        -------
        tuple
            Elements in the bag.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-06
        """
        
        return tuple(self.keys())
    
    def get_freqs(self,
                  freq: bool = True,
                  sum_: bool = False) -> Union[tuple, int]:
        """
        Obtain frequencies of elements in the Bag.

        Parameters
        ----------
        freq : bool, optional
            If True, tutple of actual frequencies is returned.
            If False, tuple of 1 for each element is returned.
            The default is True.
        sum_ : bool, optional
            If True, the sum of the frequencies is returned.
            If False, tuple of the frequencies is returned.
            The default is False.

        Returns
        -------
        Union[tuple, int]
            Frequencies or the their sum.

        @author: MURAKAMI Tamotsu
        @date: 2022-06-21
        """
        
        if freq:
            freqs = tuple(self.values())
        else:
            freqs = (1,) * len(self)
        
        if not sum_:
            return freqs
        else:
            return sum(freqs)

    def merge(self,
              bag #: Bag
              ):
        """
        Merge another bag to the bag.

        Parameters
        ----------
        bag # : Bag
            Bag to be merged.

        Returns
        -------
        None.

        @author: MURAKAMI Tamotsu
        @date: 2020-09-06
        """
        
        for elem, freq in bag.items():
            if elem in self:
                self[elem] += freq
            else:
                self[elem] = freq

"""
Test

@author: MURAKAMI Tamotsu
@date: 2022-10-18
"""

if __name__ == '__main__':
    print('* Test starts *')
    
    b = Bag()
    
    b.add_elem('a')
    b.add_elem('b')
    b.add_elem('a')
    b.add_elems((1,2,3))
    
    print(b.get_elems())
    print(b.get_freqs())
   
    print('* Test ends *')

# End of file