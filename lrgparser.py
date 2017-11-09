# -*- coding: utf-8 -*-

#Current and previous build, update these if genome build changes
currentbuild = "GRCh38"
previousbuild = "GRCh37"

# Import Element Tree library
import xml.etree.ElementTree as ET

# Parse LRG file into element tree
tree = ET.parse('LRG_1.xml')
root = tree.getroot()
print(tree)
print(root)

# Takes a subroot of annotation_set tags
annotation_set_subroot = root.iter('annotation_set')

# Finds only annotation sets where type="lrg"
for m in annotation_set_subroot:
    if m.attrib['type'] == "lrg":
        # Send to mapping subroot
        mapping_set_subroot = m.iter('mapping')

# Print mapping tags, text and attrib
for m in mapping_set_subroot:
    #Retrieve coord_system and remove .p
    coord_system = m.attrib['coord_system']
    coord_system = coord_system.split('.')[0]
    
    #Search by coord system
    if coord_system == currentbuild:
        currentbuilddict = []
        
        for item in m:
            d = {}
            for a in item.attributes.values():
                d[a.name] = a.value
            currentbuilddict.append(d)
        
        print(m.attrib['other_start'])
        print(m.attrib['other_end'])
    if coord_system == previousbuild:
        previousbuilddict = []
        
        for item in m:
            d = {}
            for a in item.attributes.values():
                d[a.name] = a.value
            previousbuilddict.append(d)
            
        print(m.attrib['other_start'])
        print(m.attrib['other_end'])
            
print(currentbuilddict)
print(previousbuilddict)