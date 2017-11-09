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


#def get_build_summary():
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
        
    dict = {}
    #Search by coord system
    if coord_system == currentbuild:
        # Create current build dictionary
        d = {}
        
        # Populate current build dictionary
        d['span_lrg_start'] = span_lrg_start
        d['span_lrg_end'] = span_lrg_end
        d['span_other_start'] = span_other_start
        d['span_other_end'] = span_other_end
        d['mapping_other_start'] = m.attrib['other_start']
        d['mapping_other_end'] = m.attrib['other_end']
        # Add to final dict
        dict[currentbuild] = d
        
    elif coord_system == previousbuild:
            # Create previous build dictionary
        d = {}
    
        # Populate previous build dictionary
        d['span_lrg_start'] = span_lrg_start
        d['span_lrg_end'] = span_lrg_end
        d['span_other_start'] = span_other_start
        d['span_other_end'] = span_other_end
        d['mapping_other_start'] = m.attrib['other_start']
        d['mapping_other_end'] = m.attrib['other_end']
        dict[previousbuild] = d
        
    print(dict)

#return dict