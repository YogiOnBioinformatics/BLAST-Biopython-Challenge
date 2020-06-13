"""
Author: Yogindra Raghav
Email: yraghav@gmail.com
Name: FASTQ Stats
Description: Given FASTQ and Quality Scores file, return metrics including: 

"""

import argparse
import math 

# maintain counter for total reads 
total_reads = 0 
# maintain list for gene ids of those reads greater than 100 bp 
large_genids = []

if __name__ == "__main__":

    """
    Counting Reads
    """

    # create argument parser 
    args = argparse.ArgumentParser() 
    # create flag for path to FASTA input 
    args.add_argument("--fasta", required = True, help = "Path to input FASTA", \
        action = 'store', dest="input_fasta")
    # create flag for path to quality score file 
    args.add_argument("--qual-file", required=True, help= "Path to input Quality \
        File", action = 'store', dest="input_quality")
    # retrieve arguments 
    parse_arguments = args.parse_args() 

    # load in data into massive list 
    with open(parse_arguments.input_fasta, "r") as data: 
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
    
    # open file to write to 
    output_file = open("../output/fastq_stats.txt","w")

    # write to output file 
    output_file.write("Total Reads: "+str(total_reads)+"\n") 
    output_file.write("Reads with more than 100 bp: " +str(len(large_genids))+"\n")


    
    """
    Checking Quality Scores 
    """
    # load in data into massive list 
    with open(parse_arguments.input_quality, "r") as data: 
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
    
    # write to output file  
    output_file.write("Total number of reads with average quality score greater than 20: "+
        str(len(quality_genids))+"\n")

    # close output file 
    output_file.close()