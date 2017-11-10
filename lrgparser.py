# -*- coding: utf-8 -*-

# Import Element Tree library
import xml.etree.ElementTree as ET
# Import url library
import urllib

# Prompt user to specify an LRG they wish to download
lrgnumber = input("Please type the LRG number that you wish to extract remotely:")

# url to retrieve XML from
file = 'LRG_' + lrgnumber + '.xml'
path = 'ftp://ftp.ebi.ac.uk/pub/databases/lrgex/'
lrgurl = path + file
# Name of the LRG
lrg_name = 'LRG_' + lrgnumber

# Create HTML Heading
master_html_str = "<html><head>"
master_html_str = master_html_str + "<title>LRG File Analysis of " + lrg_name + "</title>"
master_html_str = master_html_str + "</head>"
master_html_str = master_html_str + "<body>"
master_html_str = master_html_str + "<h1>LRG File Analysis of " + lrg_name + "</h1>"

# Retrieve data and convert to text
response = urllib.request.urlopen(lrgurl)
data = response.read()      # a `bytes` object
lrgtext = data.decode('utf-8') # a `str`; this step can't be used if data is binary

# Extract string as an element tree
root = ET.fromstring(lrgtext)

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

def get_genomic(root):
    '''
    Method to retrieve genomic sequence from XML root table
    
    Input is a root tree for an LRG file in XML format
    
    Output is the genomic sequence in the XML file
    '''
    # Loop for find children under fixed_annotation
    for child in root.findall('fixed_annotation'):

        # Find genomic sequence child
        genomic = child.find('sequence').text
    return genomic

def get_build_information(root):
    '''
    Method to get build information from xml
    
    Root is the root tree produced from the LRG file (in XML format)
    
    Function returns a dictionary containing the LRG start and end positions, the genomic start and end positions, and the strand that the sequence is found in.
    '''
    
    # Create dictionary for output
    d = {}
    
    # Loop through each child in find all
    for child in root.findall('.//annotation_set[@type="lrg"]'):
    
        # Iterate each child in mapping
        for m in child.iter('mapping'):
            
            # Retrieve coordinate system
            coord_system = m.attrib['coord_system']
            
            for span in m.iter("mapping_span"):
                # Sub dictionary
                d1 = {}
                d1['span_lrg_start'] = span.attrib['lrg_start']
                d1['span_lrg_end'] = span.attrib['lrg_end']
                d1['span_other_start'] = span.attrib['other_start']
                d1['span_other_end'] = span.attrib['other_end']
                d1['strand'] = span.attrib['strand']
                
                d[coord_system] = d1
    
    return(d)
    
# Takes a subroot of fixed annotation tags
fixed_annotation_subroot = root.iter('fixed_annotation')

# test compare_build_positions
pos = compare_build_positions(dict)

if pos is True:
    pos = "True"
else:
    pos = "False"

pos_text = 'Is the position of the LRG on each build the same? ' + pos

#print(pos_text)

html_checking = "<p>" + pos_text + "</p>"

#test to return the position shift between builds
shift = find_position_shift(dict)
shift = str(shift)
shift_text = "The new GRCh38 build is shifted by " + shift + " nucleotide positions"

#print(shift_text)

html_checking = html_checking + "<p>" + shift_text + "</p>"

print(output_comparison)
##################### output to html #########################
    #length = compare_build_length(dict) ## everything ok between builds?
position = compare_build_positions(dict) ## check start positions for each build
    #shift = find_position_shift(dict)
length_diff = abs(find_length_difference(dict))

########CH additional bits
for child in root:
    print(child.tag, child.attrib)

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
        
def slice_genomic(seq, exon_dict):
    '''
    slices genomic sequence
    input params: a string of genomic sequence, and a dict of exons
    returns: string of coding sequence
    '''
    fasta_out = ""
    for exon in exon_dict:
        start = exon_dict[exon]['start'] 
        end = exon_dict[exon]['end']
        fasta_temp = seq[int(start):int(end)]
        fasta_out += fasta_temp
        assert containsAny('ATGC', fasta_out)
    return fasta_out


         
    ####### generating output ########
def display_output_text(build_dict, seq):
    '''
    Converts the build dictionaries to HTML tables
    '''
    html_str = ""
    html_str = html_str + "<h1>Comparison of builds</h1>"
    html_str = html_str + "<table border=1>"
    html_str = html_str + "<tr>"
    html_str = html_str + "<th>Build</th>"
    html_str = html_str + "<th>Start Position</th>"
    html_str = html_str + "<th>End Position</th>"
    html_str = html_str + "</tr>"
    
    # Add row to table
    for build in build_dict:
        lrg_start = build_dict[build]['span_lrg_start']
        lrg_end = build_dict[build]['span_lrg_end']
        other_start = build_dict[build]['span_other_start']
        other_end = build_dict[build]['span_other_end']
        strand = build_dict[build]['strand']
        html_str = html_str + "<tr>"
        html_str = html_str + "<td>" + build + "</td>"
        html_str = html_str + "<td>" + other_start + "</td>"
        html_str = html_str + "<td>" + other_end + "</td>"
        html_str = html_str + "</tr>"
    
    # Close table
    html_str = html_str + "</table>"
    
    return html_str

def seq_to_fasta(seq, lrg_name):
    '''
    Method to write a FASTA file containing the coding sequence with the name of the LRG and the sequence from the LRG
    
    Add LRG 
    '''
    header = "> Coding sequence for '%s' \n" % lrg_name
    fasta_out = header + seq
    f = open(lrg_name + ".fasta",'w')
    f.write(fasta_out)
    f.close()

######## Running the tests, if pass, then the code ########
    
def containsAny(str, set):
    '''
    Check whether 'str' contains ANY of the chars in 'set'
    
    Input is a string (str) and the set of characters to confirm (set)
    
    Returns 1 if answer is true
    '''
    return 1 in [c in str for c in set]

######### Running the code ##########
build = get_build_information(root) 
print(build)
exon = get_exon_coordinates(root, lrg_name)
genomic = get_genomic(root)
sliced = slice_genomic(genomic, exon)
build_info_table_html = display_output_text(build, sliced)
seq_to_fasta(sliced, lrg_name)

# Add build information HTML
master_html_str = master_html_str + build_info_table_html

master_html_str = master_html_str + html_checking

# Close HTML
master_html_str = master_html_str + "</body></html>"

Html_file=open("test.html","w")
Html_file.write(master_html_str)
Html_file.close()