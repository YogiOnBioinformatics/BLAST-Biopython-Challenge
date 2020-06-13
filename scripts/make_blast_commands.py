"""
Author: Yogindra Raghav
Email: yraghav@gmail.com
Name: Make BLAST Commands 
Description: Output BLAST Commands using BioPython 
"""

import argparse
from Bio.Blast import Applications

if __name__ =="__main__": 
    
    """
    Command Line Arguments
    """
    # create argument parser 
    args = argparse.ArgumentParser() 
    # create flag for path to BLAST executables 
    args.add_argument("--fasta", required = True, help = "Path to input FASTA file",
        action = 'store', dest = 'input_fasta')
    # create flag for output 
    args.add_argument("--output-dir", required=True, help="Directory to output \
        results (including trailing slash)", action ='store', dest="output_dir")
    # retrieve arguments 
    parse_arguments = args.parse_args() 

    # create the makeblastdb command
    make_blast_db = Applications.NcbimakeblastdbCommandline(dbtype = "nucl",
        out = args.output_dir+"command.sh", input_file = args.input_fasta, 
        input_type = "fasta", parse_seqids = True)

    # # add path to binary with command
    # cmd = parse_arguments.path +"/"+ str(make_blast_db)
    # # run command in current os environment 
    # return_code = os.system(cmd)
    # # let user know that database files have been made 
    # print("Command 'make_blast_db' has created index files.")
    # # create the blastn command 
    # make_blastn_primer = Applications.NcbiblastnCommandline(
    #     query ="primer_sequence.fasta", db = file_dir+'test', 
    #     out = "primer_results.m8", task = "blastn", outfmt = 6)
    # make_blastn_adaptor = Applications.NcbiblastnCommandline(
    #     query = "adaptor_sequence.fasta", db = file_dir+'test', 
    #     out = "adaptor_results.m8", outfmt =6, task = "blastn")
    # # add path to binary with command 
    # cmd = parse_arguments.path +"/"+ str(make_blastn_primer) 
    # cmd_2 = parse_arguments.path+"/"+str(make_blastn_adaptor) 
    # # run command in current os environment 
    # return_code = os.system(cmd)
    # return_code_2 = os.system(cmd_2)
    # # let user know that both files have been created 
    # print("Files 'adaptor_results.m8' and 'primer_results.m8' have been created.")