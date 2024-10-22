# -*- coding: utf-8 -*-
"""
String comparison

@author: MURAKAMI Tamotsu
@date: 2021-11-26
"""

# For directory access
import os
import sys
sys.path.append(os.pardir)

# Python
import difflib

# Library
from string_srclib.string import String

class Comparison:
    """
    String comparison
    
    http://pixelbeat.jp/text-matching-3-approach-with-python/
    
    @author: MURAKAMI Tamotsu
    @date: 2020-07-23
    """
    
    @staticmethod
    def gestalt_pattern_match(s1: str,
                              s2: str
                              ) -> float:
        """
        Calculate similarity between two strings and retun similarity between 0 and 1.

        http://pixelbeat.jp/text-matching-3-approach-with-python/
        
        def gestalt_pattern_match(s1: str,
                                  s2: str
                                  ) -> float:

        @author: MURAKAMI Tamotsu
        @date: 2020-07-23
        """
        
        return difflib.SequenceMatcher(None, s1, s2).ratio()
    
"""
Test

@author: MURAKAMI Tamotsu
@date: 2020-12-22
"""

if __name__ == '__main__':
    print('* Start *')
    
    STRING_PAIRS = (
            ('低額', '低額だ'),
            ('低額', '低い'),
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
    
    for s1, s2 in STRING_PAIRS:
        sim1 = String.similarity(s1, s2)
        sim2 = Comparison.gestalt_pattern_match(s1, s2)
        print('"{}", "{}": {}'.format(s1, s2, (sim1, sim2)))
        
    print('* End *')
    
# End of file