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
3. Primer Sequence
4. Adaptor Sequence

**Outputs** 

1. Total number of reads in the dataset
2. Total number of reads greater than 100 bp
3. Total number of reads with average quality scores greater than 20

In addition, the program generates the following file:

1. Blast output file in m8 format.

**Usage** 

Fetch container from Docker Hub and  
`docker run --rm -it yraghav97/blast-biopython-challenge:1.0`

**Contact Information**

![interests](https://avatars1.githubusercontent.com/u/38919947?s=400&u=49ab1365a14fac78a91e425efd583f7a2bcb3e25&v=4)

Yogindra Raghav  
yraghav97@gmail.com
