"""
Author: Yogindra Raghav
Python version 3.7
"""

import argparse
import os
import sys
from Bio.Blast import Applications
import math

""" 
Constants 
""" 

PRIMER_SEQUENCE = "CGCCGTTTCCCAGTAGGTCTC"
ADAPTOR_SEQUENCE = "ACTGAGTGGGAGGCAAGGCACACAGGGGATAGG"

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
    # create the makeblastdb command
    make_blast_db = Applications.NcbimakeblastdbCommandline(dbtype = "nucl",
        out = file_dir+"test", input_file = input_fasta, input_type = "fasta",
        parse_seqids = True)
    # add path to binary with command
    cmd = parse_arguments.path +"/"+ str(make_blast_db)
    # run command in current os environment 
    return_code = os.system(cmd)
    # let user know that database files have been made 
    print("Command 'make_blast_db' has created index files.")
    # create the blastn command 
    make_blastn_primer = Applications.NcbiblastnCommandline(
        query ="primer_sequence.fasta", db = file_dir+'test', 
        out = "primer_results.m8", task = "blastn", outfmt = 6)
    make_blastn_adaptor = Applications.NcbiblastnCommandline(
        query = "adaptor_sequence.fasta", db = file_dir+'test', 
        out = "adaptor_results.m8", outfmt =6, task = "blastn")
    # add path to binary with command 
    cmd = parse_arguments.path +"/"+ str(make_blastn_primer) 
    cmd_2 = parse_arguments.path+"/"+str(make_blastn_adaptor) 
    # run command in current os environment 
    return_code = os.system(cmd)
    return_code_2 = os.system(cmd_2)
    # let user know that both files have been created 
    print("Files 'adaptor_results.m8' and 'primer_results.m8' have been created.")

    """
    Counting Reads
    """
    # maintain counter for total reads 
    total_reads = 0 
    # maintain list for gene ids of those reads greater than 100 bp 
    large_genids = []

    # load in data into massive list 
    with open(input_fasta, "r") as data: 
        data_fasta = data.readlines()
    
    # count total reads and those > 100bp
    for line in data_fasta: 
        # if its sequence identifier
        if ">" in line: 
            # update counter for total reads 
            total_reads +=1
            # split line by spaces 
            line = line.split(" ") 
            # access the length tag and split by equal sign 
            length = line[1].split("=")
            # check if length is greater than 100
            if int(length[1])>100:
                # add geneid to large_genids list 
                large_genids.append(line[0].replace(">", ""))
    
    # print out data 
    print("Total Reads: "+str(total_reads)) 
    print("Reads with more than 100 bp: " +str(len(large_genids)))

    """
    Checking Quality Scores 
    """
    # load in data into massive list 
    with open(input_quality, "r") as data: 
        data_quality = data.readlines()

    # maintain list of all genids with high enough average quality
    quality_genids = []
    # save length of quality list 
    qual_len = len(data_quality) 

    # get average of quality scores 
    for num in range(0, qual_len): 
        # get current line 
        line = data_quality[num]
        # if header line 
        if ">" in line:  
            # split line by spaces 
            line = line.split(" ") 
            # access the length tag and split by equal sign 
            length = line[1].split("=")
            # convert length to int 
            length = int(length[1]) 
            # find number of rows to iterate over since each row has 60 entries
            num_rows = math.ceil(length/60)
            # maintain temp list of quality scores per each entry (>)
            all_quality_scores = []
            
            # for each entry (>)
            for num2 in range(num+1,num+num_rows+1): 
                # get line of data quality 
                line2 = data_quality[num2]
                # get individual scores into list  
                line2 = line2.split(' ') 
                # transfer scores

                for thing in line2: 
                    # convert to int 
                    all_quality_scores.append(int(thing))

            # get average of quality scores per entry (>)
            average = sum(all_quality_scores)/len(all_quality_scores)
            # if average is greater than 20  
            if average >20: 
                # append genid to quality_genids list 
                quality_genids.append(line[0].replace(">",""))
    
    # print results 
    print("Total number of reads with average quality score greater than 20: "+
        str(len(quality_genids)))
    
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
     
    
             
            



