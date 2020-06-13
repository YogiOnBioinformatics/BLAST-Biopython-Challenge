# most recent biopython image as base
FROM biopython/biopython:latest as biopython 

LABEL maintainer="Yogindra Raghav yraghav97@gmail.com"

# set working directory in container 
WORKDIR /usr/src/biopython/

# copy repo contents to container 
COPY . /usr/src/biopython/

# run python script 
RUN python3 scripts/fastq_stats.py --fasta test_data/test.fna --qual-file test_data/test.qual --output-dir /usr/src/biopython/output/

# run script to output ncbi blast bash script 
# RUN python3 scripts/make_blast_commands.py --fasta test_data/test.fna --output-dir output/

# NCBI BLAST
FROM ncbi/blast:2.10.0 

# set working directory 
WORKDIR /usr/src/blast/

# copy contents from previous build 
COPY --from=biopython /usr/src/biopython/ /usr/src/blast/

RUN makeblastdb -in test_data/test.fna -out output/db/final_db -parse_seqids -dbtype nucl

