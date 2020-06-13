"""
Author: Yogindra Raghav
Email: yraghav97@gmail.com
"""

import argparse
import os
import sys
from Bio.Blast import Applications
import math

""" 
Constants 
""" 

# if this is the "main" file called on the command line
if __name__ == "__main__": 

    """
    Command Line Arguments
    """
    # create argument parser 
    args = argparse.ArgumentParser() 
    # create flag for path to BLAST executables 
    args.add_argument("-p", required = True, help = "Absolute path to BLAST \
        executables for this program to use.", action = 'store', dest = 'path')
    # retrieve arguments 
    parse_arguments = args.parse_args() 
    
    """
    Validate Command-Line Input, Prepare Paths
    """ 
    # if inputted path is not valid 
    if not os.path.isdir(parse_arguments.path):
        # print error message 
        print("Path (-p) input does not correspond to valid directory")
        # exit program 
        sys.exit(0) 
    # inputted path is valid 
    else: 
        # save absolute path for original directory 
        orig_dir = os.path.abspath(os.curdir)
        # replace any backwards slashes to forward slashes 
        orig_dir = orig_dir.replace("\\","/")
        # save input file location 
        file_dir = orig_dir+ "/Files_for_test/Files_for_test/"
        # create absolute path to input FASTA file 
        input_fasta = file_dir+"test.fna"
        # create absolute path to input quality file 
        input_quality = file_dir +"test.qual"
       
         
    """
    BLAST
    """


    
    """
    Dealing With BLAST Output
    Find Number of Reads With Adaptors, Primers and Both
    """ 
    # open primer results m8 file 
    with open('primer_results.m8', 'r') as data: 
        primer = data.readlines()
    # print number of primer sequences 
    print("Number of reads with primer sequences: "+str(len(primer)))

    # open adaptor results m8 file 
    with open('adaptor_results.m8', 'r') as data:
        adaptor = data.readlines() 
    # print number of adaptor sequences 
    print("Number of reads with adaptor sequences: "+str(len(adaptor)))

    # list for genids that have primer sequence
    primer_genids = []
    # list for genids that have adaptor sequence 
    adaptor_genids = [] 
    # for entry in primer_results.m8 
    for entry in primer: 
        # split row by tab 
        entry = entry.split("\t") 
        # get genid 
        primer_genids.append(entry[1]) 
    # for entry in adaptor_results.m8 
    for entry in adaptor: 
        # split row by tab 
        entry = entry.split("\t") 
        # get genid 
        adaptor_genids.append(entry[1]) 
    
    # list for genids with both primers and adaptors 
    both = []
    # for each genid with primer sequence check against the genids with 
    # adaptor sequences and see if both of them are present for a given genid
    for genid in primer_genids: 
        if genid in adaptor_genids: 
            both.append(genid) 
    
    # print number of reads with both primer and adaptor 
    print("Total number of reads with both primer and adaptor sequences: "+
        str(len(both)))
    
    """
    New FASTA File
    """ 
    # create new file 
    with open("final.fasta", "w+") as out_file: 
        # get length of total input fasta 
        fasta_len = len(data_fasta)
        # for each line 
        for num in range(0, fasta_len): 
            # save the line 
            line = data_fasta[num]
            # if header line 
            if ">" in line: 
                # split elements by spaces 
                line_list = line.split(" ")
                # get genid 
                genid = line_list[0].replace(">", "") 
                # if read associated with genid is > 100bp and average quality > 20
                if genid in large_genids and genid in quality_genids: 
                    # get str version of length of read
                    length = line_list[1].split("=")
                    # convert to int 
                    length = int(length[1]) 
                    # find number of rows since each row has 60 nucleotides 
                    num_rows = math.ceil(length/60)
                    # create string that we can append to for FASTA sequence
                    FASTA_sequence = ""

                    # for each line 
                    for num2 in range(num+1, num+num_rows+1): 
                        # get nucleotide sequence 
                        line2 = data_fasta[num2] 
                        # get rid of newline character 
                        line2 = line2.replace("\n", "")
                        # concat new FASTA sequence 
                        FASTA_sequence = FASTA_sequence+line2

                    # replace primer sequence 
                    FASTA_sequence = FASTA_sequence.replace(PRIMER_SEQUENCE, "")
                    # replace adaptor sequence 
                    FASTA_sequence = FASTA_sequence.replace(ADAPTOR_SEQUENCE, "") 
                    # replace new line character
                    line = line.replace("\n", "") 
                    # write out title 
                    out_file.write(line + "\n") 
                    # write out FASTA sequence 
                    out_file.write(FASTA_sequence+ "\n") 
                    
    # let user know that file has been created 
    print("File 'final.fasta' has been created.") 

    """
    Creating Primer File
    """ 
    # create tab delimited txt file, explains where primers were found in subject
    # sequence for each geneid 
    with open("primer_results.txt", "w") as out_file: 
        # for each line 
        for line in primer: 
            # split line by tab
            line = line.split("\t")
            # write out gene id and tab  
            out_file.write(line[1]+ "\t") 
            # write out beginning position in subject and tab 
            out_file.write(line[8]+"\t") 
            # write out end position in subject and tab 
            out_file.write(line[9]+"\t"+"\n")
    
    print("Created 'primer_results.txt' file.")

    """
    Creating Adaptor File 
    """ 
    # create tab delimited txt file, explains where adaptors were found in 
    # subject sequence for each geneid 
    with open("adaptor_results.txt", "w") as out_file: 
        # for each line 
        for line in adaptor: 
            # split line by tab
            line = line.split("\t")
            # write out gene id and tab  
            out_file.write(line[1]+ "\t") 
            # write out beginning position in subject and tab 
            out_file.write(line[8]+"\t") 
            # write out end position in subject and tab 
            out_file.write(line[9]+"\t"+"\n")
    
    print("Created 'adaptor_results.txt' file.")
     
    
             
            



