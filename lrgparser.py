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

# create dictionary to hold attributes from both builds
dict = {}

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
        
        # Create temp current build dictionary
        d1 = {}
            
        # Populate current build dictionary
        d1['span_lrg_start'] = span_lrg_start
        d1['span_lrg_end'] = span_lrg_end
        d1['span_other_start'] = span_other_start
        d1['span_other_end'] = span_other_end
        d1['mapping_other_start'] = m.attrib['other_start']
        d1['mapping_other_end'] = m.attrib['other_end']
        # Add to final dict, using the build as the key
    
        # Name sub dictionary as coordinate system
        dict[coord_system] = d1
print(dict)

def check_build_length(dict):
    length_lrg = int(dict['span_lrg_end']) - int(dict['span_lrg_start'])
    length_other = int(dict['span_other_end']) - int(dict['span_other_start'])
    if length_lrg == length_other:
        is_same = True
    else:
        is_same = False
    return is_same
            
# test check_build_length - should print'true' to screen
check_37 = check_build_length(dict['GRCh37'])
check_38 = check_build_length(dict['GRCh38'])
print(check_37)
print(check_38)
