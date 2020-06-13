# most recent biopython image as base
FROM biopython/biopython:latest as biopython 

LABEL maintainer="Yogindra Raghav yraghav97@gmail.com"

# set working directory in container 
WORKDIR /usr/src/blast-biopython-challenge/

# copy repo contents to container 
COPY . /usr/src/blast-biopython-challenge/

# run python script 
RUN python3 fastq_stats.py --fasta test_data/test.fna --qual-file test_data/test.qual

# NCBI BLAST
FROM ncbi/blast:2.10.0 

# set working directory 
WORKDIR /usr/src/blast/

# copy contents from previous build 
COPY --from=biopython /usr/src/blast-biopython-challenge/ /usr/src/blast/