# BLAST/Biopython Challenge 

![NCBI Blast](https://blast.ncbi.nlm.nih.gov/images/nucleutide-blast-cover.png)
![Biopython](https://biopython.org/assets/images/biopython_logo_xs.png)

**Challenge** 
The pipelines for different sequencing platforms use BLAST extensively to query sequences against a given database. 
One of the steps, in an earlier version of a pipeline, heavily relied on BLAST to eliminate primer and adaptor sequences from the reads to generate clean and manageable datasets. 
You are provided with FASTA and Quality files from a dataset that were generated using the 454 Sequencing Platform. 
You are required to blast the dataset against the given primer and adaptor sequences and generate output in m8 format. 

**Inputs** 
1. FASTA file
2. Quality file
3. Primer Sequence: CGCCGTTTCCCAGTAGGTCTC
4. Adaptor Sequence: ACTGAGTGGGAGGCAAGGCACACAGGGGATAGG

**Outputs** 

1. Total number of reads in the dataset
2. Total number of reads greater than 100 bp
3. Total number of reads with average quality scores greater than 20
4. Total number of reads with primer sequences
5. Total number of reads with adaptor sequences
6. Total number of reads with both primer and adaptor sequences

In addition, the program generates the following files:

1. Blast output file in m8 format.
2. FASTA file containing reads greater than 100bp, average read quality scores greater than 20, primers and adaptors trimmed.
3. Tab de-limited text file containing the read identifiers along with the starting and end positions of the primer or adaptor sequences.

**Usage** 

There is only one flag for this program: 
`-p`: Gives the absolute path to the BLAST executables for this program to use.

For more information on the program: 
`454_sequencing_pre_processing.py --help` 

Example usage: 
`454_sequencing_pre_processing.py -p /ihome/crc/install/blast+/blast-2.7.1/bin/`

**Contact Information**

Yogindra Raghav 
yraghav97@gmail.com 
Phone: 610-462-4310
