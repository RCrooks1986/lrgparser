# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import xml.etree.ElementTree as ET

lrg = ET.parse('C:\\Users\chris\Desktop\lrg_parser\LRG_214.xml')
root = lrg.getroot()
print(lrg)
print(root)

for child in root:
    print('hello')
    print(child.tag, child.attrib)
    

