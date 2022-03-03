from pandas_to_fasta import pandas_to_fasta
from local_packages.uniprot_query import UniprotQueryClient
import pandas as pd
import numpy as np
import sys


def get_random_sequences(num_sequences: int, id_column_name: str, seq_column_name: str) -> pd.DataFrame():
    """
    Download random uniprot human sequences
    Parameters:
        num_sequences (int): The number of sequences you want to download
        id_column_name (str): The column name you want to give the uniprot ID column
        seq_column_name (str): The column name you want to give the sequence column

    Result:
    A Pandas dataframe with an id column and a sequence column.
    """
    i = 0
    random_sequences = []
    random_sequences_id = []
    while i <= num_sequences:
        sys.stdout.write(f'\rDownloading {i}/{num_sequences} entries')
        get_random_sequence = UniprotQueryClient()
        get_random_sequence.make_random_query(9606, limit=1)
        if get_random_sequence.get_fasta_uniprot_id() not in random_sequences_id:
            random_sequences.append(get_random_sequence.get_fasta_seq_only())
            random_sequences_id.append(get_random_sequence.get_fasta_uniprot_id())
        else:
            continue

        i += 1
        sys.stdout.flush()
    random_sequences_dict = {id_column_name: random_sequences_id, seq_column_name: random_sequences}
    random_sequences_df = pd.DataFrame(data=random_sequences_dict, index=np.arange(len(random_sequences_id)))
    return random_sequences_df


if __name__ == '__main__':
    download_4_sequences = get_random_sequences(4, 'Uniprot_B','Seq2')
    pandas_to_fasta(download_4_sequences,'williams_MTB/missing_examples.fasta','Uniprot_B','Seq2')
