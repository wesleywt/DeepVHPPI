import pandas as pd
from fasta_to_pandas import fasta_to_pandas
from create_train_test_list import create_train_test_list
import json


def interaction_df_to_positive_df(interaction_df, uniprot_id_1, uniprot_id_2, sequence_1, sequence_2):
    positive_df = interaction_df[[uniprot_id_1, uniprot_id_2, sequence_1, sequence_2]].copy()
    return positive_df


def fasta_to_negative_interaction_df(fasta_file, positive_df, uniprot_id_1, uniprot_id_2, sequence_1, sequence_2):
    negative_df = fasta_to_pandas(fasta_file, uniprot_id_2, sequence_2)
    negative_df[uniprot_id_1] = positive_df[uniprot_id_1]
    negative_df[sequence_1] = positive_df[sequence_1]
    return negative_df


if __name__ == '__main__':
    interaction_examples = pd.read_csv('williams_MTB/positive_interaction_dataset.csv', index_col=0)
    print(interaction_examples.head())
    positive_examples = interaction_df_to_positive_df(interaction_examples,
                                                      'Uniprot_A',
                                                      'Uniprot_B',
                                                      'Seq1',
                                                      'Seq2')
    negative_examples = fasta_to_negative_interaction_df('williams_MTB/new_negative_examples.fasta',
                                                         positive_examples,
                                                         'Uniprot_A',
                                                         'Uniprot_B',
                                                         'Seq1',
                                                         'Seq2')
    print(len(positive_examples))
    print(len(negative_examples))
    train, test = create_train_test_list(positive_examples, negative_examples)
    with open('williams_MTB/hpidb_train.json', 'w') as f:
        json.dump(train, f)
    with open('williams_MTB/hpidb_test.json', 'w') as f:
        json.dump(test, f)
