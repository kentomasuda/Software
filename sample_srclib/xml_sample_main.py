# -*- coding:utf-8 -*-
"""
Xml sample main

@author: MURAKAMI Tamotsu
@date: 2022-09-28
"""

# For directory access
import sys
import os
sys.path.append(os.pardir)

# Python
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

class Xml:
    """
    @author: MURAKAMI Tamotsu
    @date: 2022-09-28
    """
    
    @staticmethod
    def scan_child(element: Element,
                   indent: str):
        """
        @author: MURAKAMI Tamotsu
        @date: 2022-09-28
        """
        
        for child in element:
            tagname = child.tag
            print('{}tag = {}'.format(indent, tagname))

            string = ElementTree.tostring(child, encoding='unicode')
            print('{}string = {}'.format(indent, string))

            text = ''.join(child.itertext())
            print('{}text = {}'.format(indent, text))

"""
Main

@author: MURAKAMI Tamotsu
@date: 2022-09-28
"""

if __name__ == '__main__':
    print('* Main starts *')
    
    TAG_P = 'p'
    
    xmlstring = '<page><p><num>第1</num>段落の<sen>文1</sen>です。</p><t>不要テキスト</t><p><num>第2</num>段落の<sen>文2</sen>です。</p></page>'

    xmltree = ElementTree.fromstring(xmlstring)
    
    print('tag =', xmltree.tag)
    
    string = ElementTree.tostring(xmltree, encoding='unicode')
    
    print('string =', string)

    text = ''.join(xmltree.itertext())
    
    print('text =', text)
    
    for child in xmltree:
        tagname = child.tag
        print('tag =', tagname)

        if tagname == TAG_P:
            string = ElementTree.tostring(child, encoding='unicode')
            print('string =', string)
            
            text = ''.join(child.itertext())
            print('text =', text)

            Xml.scan_child(child, '\t')

    print('* Main ends *')

# End of file