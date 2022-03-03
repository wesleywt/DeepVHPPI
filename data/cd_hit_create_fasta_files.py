import pandas as pd
import json
from process_hpidb_mtb import create_interaction_df


# 1. Import the csv dataset containing the positive and negative examples
# 2. Extract into two lists the human positive and the human negative examples
# 3. Use CD-HIT-2D in commandline to identify sequences in each dataset that have greater than 80% similarity.
# 4. Remove the sequences from the negative example list and replace them with a new random query


def create_fasta(outputfile, id_col, seq_col, csv_file=None, df_file=None):
    if csv_file:
        df = pd.read_csv(csv_file)
    else:
        df = df_file
    with open(outputfile, 'a') as f:
        for i in range(0, len(df)):
            f.write(f'>{df[id_col].iloc[i]} \n {df[seq_col].iloc[i]}\n')


if __name__ == '__main__':
    input_csv = 'williams_MTB/pathcat_BACTERIA.mitab_plus.txt'
    random_csv = 'williams_MTB/uniprot_negative.csv'
    positive_interaction = create_interaction_df(input_csv)
    print(positive_interaction.head())
    create_fasta('williams_MTB/positive_examples.fasta', 'Uniprot_B', 'Seq2', df_file=positive_interaction)

    create_fasta('williams_MTB/negative_examples.fasta', 'Uniprot_B', 'Seq2', csv_file=random_csv)
