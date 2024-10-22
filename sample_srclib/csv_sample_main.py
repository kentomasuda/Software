# -*- coding:utf-8 -*-
"""
Csv sample main

@author: MURAKAMI Tamotsu
@date: 2023-05-17
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
import csv

"""
Main

@author: MURAKAMI Tamotsu
@date: 2023-05-17
"""

if __name__ == '__main__':
    print('* Main starts *')
    
    # Read CSV file
    print('Reading CSV file...')
    with open('./Data/sample_csv.csv', 'r', newline='', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in rows:
            print(row)
            for elem in row:
                if elem:
                    print(elem)

    # Read TSV file
    print('Reading TSV file...')
    with open('./Data/sample_tsv.tsv', 'r', newline='', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter='\t')
        for row in rows:
            print(row)
            for elem in row:
                if elem:
                    print(elem)

    print('* Main ends *')

# End of file