import pandas as pd
from Bio import SeqIO
import numpy as np


def fasta_to_pandas(fasta_file, id_column, seq_column):
    """
    Convert a fasta file to a pandas dataframe
    Parameters:
        fasta_file (str): Path to fasta file
        id_column(str): dataframe column name for the sequence id
        seq_column (str): dataframe column name for the sequence column
    """
    seq_dict = dict()
    record = []
    seq_seq = []
    for seq_record in SeqIO.parse(fasta_file, 'fasta'):
        record.append(seq_record.id)
        seq_seq.append(str(seq_record.seq))

    seq_dict.update({id_column: record, seq_column: seq_seq})
    seq_df = pd.DataFrame(data=seq_dict, index=np.arange(len(seq_seq)))
    print(f'Dataframe {seq_df.head()}')
    print(f'Dataframe columns {seq_df.columns}')
    return seq_df


if __name__ == '__main__':
    novel_df = fasta_to_pandas('williams_MTB/negative_novel', 'Uniprot_B', 'Seq2')
    print(len(novel_df))
