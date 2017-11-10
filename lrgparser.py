# -*- coding: utf-8 -*-

#LRG variables
lrg = '214'
lrg_name= 'LRG_' + lrg 
lrgfilename = 'LRG_' + lrg + '.xml'

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
    Method to check the length within each build, returns a bool
    Input params: A dictionary containing build attributes
    Return: Bool 
    '''
    length_lrg = int(dict['span_lrg_end']) - int(dict['span_lrg_start'])
    length_other = int(dict['span_other_end']) - int(dict['span_other_start'])
    if length_lrg == length_other:
        is_same = True
    else:
        is_same = False
    return is_same

def compare_build_length(dict):
    '''
    Method to compare the length between build, returns a bool
    Input params: A dictionary of dictionaries contain build attributes
    Return: Bool 
    '''
    length37 = int(dict['GRCh37']['span_other_end']) - int(dict['GRCh37']['span_other_start'])
    length38 = int(dict['GRCh38']['span_other_end']) - int(dict['GRCh38']['span_other_start'])
    
    if length37 == length38:
        is_same = True
    else:
        is_same = False
    return is_same

def find_length_difference(dict):
    '''
    Method to find the differences in length between builds (length of GRCh38 - GRCh37)
    Input params: A dictionary of dictionaries contain build attributes
    Return: Int
    '''
    length37 = int(dict['GRCh37']['span_other_end']) - int(dict['GRCh37']['span_other_start'])
    length38 = int(dict['GRCh38']['span_other_end']) - int(dict['GRCh38']['span_other_start'])
    
    diff = length38 - length37
    return diff
    
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

def output_comparison(dict):
    '''
    Method to output the build comparisons
    Input params: A dictionary of dictionaries contain build attributes
    Return: String 
    '''
    #length = compare_build_length(dict) ## everything ok between builds?
    position = compare_build_positions(dict) ## check start positions for each build
    #shift = find_position_shift(dict)
    length_diff = abs(find_length_difference(dict))
    
    print("Difference in lrg length:", length_diff, "Start position is shifted by:", position)
    
# Takes a subroot of fixed annotation tags
fixed_annotation_subroot = root.iter('fixed_annotation')

# Create transcripts dictionary
transcript = {}

# Loop through fixed annotations
for m in fixed_annotation_subroot:    
    # Sequence sub root
    sequence_subroot = m.iter('sequence')
    loopcount = 0        
    
    # Lift Genomic sequence from Genomic subroot
    for n in sequence_subroot:
        if loopcount == 0:
            genomicsequence = n.text
        
        loopcount = loopcount+1
    
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
            exonnumber = o.attrib['label']
            
            # Exon coordinates dictionary
            exon = {}
            
            # Subset of coordinates
            coordinates_subset = o.iter('coordinates')
            for p in coordinates_subset:
                exonstart = p.attrib['start']
                exonend = p.attrib['end']
                coord_system = p.attrib['coord_system']
                
                # If statement for assigning coordinates
                if coord_system == lrgfilename:
                    exon['genomicstart'] = exonstart
                    exon['genomicend'] = exonend
                elif coord_system == transcriptname:
                    exon['transcriptstart'] = exonstart
                    exon['transcriptend'] = exonend
               # elif coord_system == lrgproteinname:
                #    exon['proteinstart'] = exonstart
                 #   exon['proteinend'] = exonend
            
            # Add coordinates to that exon
            transcript[exonnumber] = exon
        
        # Subroot of cDNA
        cdna_subroot = n.iter('cdna')
        for o in cdna_subroot:
            # Subroot of sequence
            sequence_subroot = o.iter('sequence')
            
            # Lift cDNA from cDNA subroot
            for p in sequence_subroot:
                cdna = p.text
                
                transcript['cDNA'] = cdna

        # Subroot of cDNA
        coding_region_subroot = n.iter('coding_region')
        for o in coding_region_subroot:
            # Subroot of coding region
            translation_subroot = o.iter('translation')
            
            # Subroot of translation
            for p in translation_subroot:
                # Subroot of sequence
                sequence_subroot = p.iter('sequence')
                
                # Lift protein sequence from coding region subroot
                for q in sequence_subroot:
                    protein = q.text
                    
                    transcript['protein'] = protein
            
        # Add transcript to the transcripts dictionary
        transcript[transcriptname] = transcript

# test check_build_length - should print'true' to screen
check_37 = check_build_length(dict['GRCh37'])
check_38 = check_build_length(dict['GRCh38'])


print(check_37)
print(check_38)
print('###############')
# test compare_build_positions
pos = compare_build_positions(dict)

print('Is the position of the LRG on each build the same?', pos)

#test to return the position shift between builds

shift = find_position_shift(dict)
print("The new GR38 build is shifted by", shift, "nucleotide positions")

print(output_comparison)
##################### output to html #########################
    #length = compare_build_length(dict) ## everything ok between builds?
position = compare_build_positions(dict) ## check start positions for each build
    #shift = find_position_shift(dict)
length_diff = abs(find_length_difference(dict))


html_str = """
<h1>Comparison of builds </h1>

<table border=1>
     <tr>
     <th>Build</th>
       <th>Start Position</th>
       <th>End Position</th>
     </tr>
     <indent>
       <tr>
         <td><%= position %></td>
         <td><%= length_diff %></td>
         <td>hello3</td>
       </tr>
     </indent>
</table>
"""

Html_file= open("test.html","w")

Html_file.write(html_str)
Html_file.close()



########CH additional bits

for child in root:
    print(child.tag, child.attrib)
    
def get_genomic(root):
    for child in root.findall('fixed_annotation'):   
        genomic = child.find('sequence').text
    return genomic

def get_exon_coordinates(root, lrg_name):
    d = {}
    
    for child in root.findall('.//transcript[@name="t1"]'):
        for exon in child.findall('exon'):
        #print(exon.tag, exon.attrib)
           # d['label'] = exon.get('label')
            for c in exon.findall("coordinates[@coord_system='%s']" % lrg_name ):
                d1 = {}
            #start = c['start'].value  
            #print(c.tag, c.attrib)
                d1['start'] = c.get('start')
                d1['end'] = c.get('end')
                d[exon.get('label')] = d1
        return(d)


def get_build_information(root):
    '''
    Method to get build information from xml
    '''
    d = {}
    for child in root.findall('.//annotation_set[@type="lrg"]'):
        print(child.tag, child.attrib)
        for m in child.iter('mapping'):
            coord_system = m.attrib['coord_system']
            coord_system = coord_system.split('.')[0]
            for span in m.iter("mapping_span"):
                d1 = {}
                d1['span_lrg_start'] = span.attrib['lrg_start']
                d1['span_lrg_end'] = span.attrib['lrg_end']
                d1['span_other_start'] = span.attrib['other_start']
                d1['span_other_end'] = span.attrib['other_end']
                d1['strand'] = span.attrib['strand']
                print("-----CH----")
                print(d1)
                d[coord_system] = d1
    return(d)
            
            
    
build = get_build_information(root)        
exon = get_exon_coordinates(root, lrg_name)
genomic = get_genomic(root)
print("***************")
print(build)
print("***************")
print(exon)

 