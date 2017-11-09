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
    
    # Takes a subroot of mapping_span tags
    mapping_span_subroot = m.iter('mapping_span')
    
    for n in mapping_span_subroot:
        span_lrg_start = n.attrib['lrg_start']
        span_lrg_end = n.attrib['lrg_end']
        span_other_start = n.attrib['other_start']
        span_other_end = n.attrib['other_end']
    
    #Search by coord system
    if coord_system == currentbuild:
        # Create current build dictionary
        currentbuilddict = {}
        
        # Populate current build dictionary
        currentbuilddict['span_lrg_start'] = span_lrg_start
        currentbuilddict['span_lrg_end'] = span_lrg_end
        currentbuilddict['span_other_start'] = span_other_start
        currentbuilddict['span_other_end'] = span_other_end
        currentbuilddict['mapping_other_start'] = m.attrib['other_start']
        currentbuilddict['mapping_other_end'] = m.attrib['other_end']
    elif coord_system == previousbuild:
        # Create previous build dictionary
        previousbuilddict = {}
        
        # Populate previous build dictionary
        previousbuilddict['span_lrg_start'] = span_lrg_start
        previousbuilddict['span_lrg_end'] = span_lrg_end
        previousbuilddict['span_other_start'] = span_other_start
        previousbuilddict['span_other_end'] = span_other_end
        previousbuilddict['mapping_other_start'] = m.attrib['other_start']
        previousbuilddict['mapping_other_end'] = m.attrib['other_end']
            
print(currentbuilddict)
print(previousbuilddict)