# most recent biopython image as base
FROM biopython/biopython:latest as biopython 

LABEL maintainer="Yogindra Raghav yraghav97@gmail.com"

# set working directory in container 
WORKDIR /usr/src/biopython/

# copy repo contents to container 
COPY . /usr/src/biopython/

# run python script 
RUN python3 scripts/python/fastq_stats.py --fasta test_data/test.fna --qual-file test_data/test.qual --output-dir /usr/src/biopython/output/

# run script to output ncbi blast bash script 
# RUN python3 scripts/make_blast_commands.py --fasta test_data/test.fna --output-dir output/

# NCBI BLAST
FROM ncbi/blast:2.10.0 

# set working directory 
WORKDIR /usr/src/blast/

# copy contents from previous build 
COPY --from=biopython /usr/src/biopython/ /usr/src/blast/

# allow most open permissions 
RUN chmod -R 777 /usr/src/blast/

# run bash command to make blast db 
RUN makeblastdb -in /usr/src/blast/test_data/test.fna -parse_seqids -dbtype nucl -out /usr/src/blast/output/db/final_db

# run blastn commands 
RUN blastn -db output/db/final_db -query test_data/primer.fa -out output/blastn/primer.m8 -outfmt 6  

RUN blastn -db output/db/final_db -query test_data/adaptor.fa -out output/blastn/adaptor.m8 -outfmt 6  

