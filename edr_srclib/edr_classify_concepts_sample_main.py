# -*- coding: utf-8 -*-
"""
EDR classify concepts (words) sample main

@author: MURAKAMI Tamotsu
@date: 2023-11-19
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python

# Library
from edr_srclib.edr_concept_dict import EdrConceptDict
from text_lib.lang import Lang


"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-11-19
"""

if __name__ == '__main__':
   
    print('* Main starts *')
    
    DIR_OUT = './Output'
    
    if not os.path.isdir(DIR_OUT):
        os.mkdir(DIR_OUT)

    concept_dict_path = '../edr_data/edr_concept_dict_blank.json'

    EdrConceptDict.ensure_loaded(concept_dict_path)

    EdrConceptDict.print_word_super_concepts('シリンダー')
    
    count = 0
    
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.set_concept_type('3aa929', st=True, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')

    print('指定した概念識別子（およびその下位）が ST=True と指定された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.set_concept_type('3aa929', st=False, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')

    print('指定した概念識別子（およびその下位）が ST=False と指定された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.set_concept_type('3aa929', st=True, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')
    EdrConceptDict.lock_concept_type('3aa929', st=True, sub=True)

    print('指定した概念識別子（およびその下位）が ST=True と指定され、lock された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.set_concept_type('3aa929', st=False, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')

    print('指定した概念識別子（およびその下位）が ST=False と指定されたが、lock されているので変更されない。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.print_words(st=True, lang=Lang.JPN)

    print('ST=True の概念識別子に対応する語がすべて表示された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.print_word_super_concepts('重さ')

    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.set_concept_type('30f7a6', bh=True, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')
    EdrConceptDict.set_concept_type('3f988d', bh=True, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')
    EdrConceptDict.set_concept_type('3cf921', bh=True, sub=True, date='2023-11-16', author='MURAKAMI Tamotsu')

    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.print_words(bh=True, lang=Lang.JPN)

    print('BH=True の概念識別子に対応する語がすべて表示された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.print_words(st=False, bh=False, fn=False, ux=False, lang=Lang.JPN, num=20)

    print('この時点でST、BH、FN、UX がすべて False の概念識別子に対応する語のうち20個が表示された。')
    input('{}. Enter to continue:'.format(count))
    count += 1

    EdrConceptDict.save(os.path.join(DIR_OUT, 'edr_concept_dict_update.json'), date='2023-11-16', author='MURAKAMI Tamotsu')

    print('* Main ends *')

# End of file