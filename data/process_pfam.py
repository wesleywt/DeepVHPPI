from local_packages import extract_from_fasta
from functools import partial
from Bio import SeqIO
import pandas as pd

fasta_seq = SeqIO.parse('../data/pfam/Pfam-A.fasta', 'fasta')
# creates a raw file containing  just the sequences from pfam database
with open('../deepvhppi_data/pfam/pfam.raw', 'w') as f:
    for seq in fasta_seq:
        f.writelines(seq.seq + '\n')
