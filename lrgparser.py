# -*- coding: utf-8 -*-

#Current and previous build, update these if genome build changes
currentbuild = "GRCh38"
previousbuild = "GRCh37"

# Import Element Tree library
import xml.etree.ElementTree as ET

# Parse LRG file into element tree
tree = ET.parse('LRG_214.xml')
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
    '''
    Method to check the length of each build, returns a bool
    Input params: A dictionary of dictionaries contain build attributes
    Return: Bool 
    '''
    length_lrg = int(dict['span_lrg_end']) - int(dict['span_lrg_start'])
    length_other = int(dict['span_other_end']) - int(dict['span_other_start'])
    if length_lrg == length_other:
        is_same = True
    else:
        is_same = False
    return is_same

def compare_build_positions(dict):
    '''
    Method to compare build positions, returns a bool
    Input params: A dictionary of dictionaries contain build attributes
    Return: Bool 
    '''
    pos37 = dict['GRCh37']['span_other_start']
    pos38 = dict['GRCh38']['span_other_start']
    
    if pos37 == pos38:
        is_same = True
    else:
        is_same = False
    return is_same

def find_position_shift(dict):
    '''
    Method to display differences in lrg position between builds, will return difference in GRCh37 - GRCh38 position 
    Input params: A dictionary of dictionaries contain build attributes
    Return: int
    '''
    pos37_start = int(dict['GRCh37']['span_other_start'])
    pos38_start = int(dict['GRCh38']['span_other_start'])
    
    shift = pos37_start - pos38_start # different between two
    return shift
    
# Takes a subroot of fixed annotation tags
fixed_annotation_subroot = root.iter('fixed_annotation')

# Create transcripts dictionary
transcripts = {}

# Loop through fixed annotations
for m in fixed_annotation_subroot:
    # Subroot of transcripts
    transcript_subroot = m.iter('transcript')
    for n in transcript_subroot:
        # Get transcript name
        transcriptname = n.attrib['name']
        
        # Subroot of exons
        exons_subroot = n.iter('exon')
        for o in exons_subroot:
            # Get transcript name
            transcriptname = n.attrib['name']

# test check_build_length - should print'true' to screen
check_37 = check_build_length(dict['GRCh37'])
check_38 = check_build_length(dict['GRCh38'])

print(check_37)
print(check_38)
print('###############')
# test compare_build_positions
pos = compare_build_positions(dict)

print(pos)
print('********************')

#test to return the position shift between builds

shift = find_position_shift(dict)
print("The new GR38 build is shifted by", shift, "nucleotide positions")