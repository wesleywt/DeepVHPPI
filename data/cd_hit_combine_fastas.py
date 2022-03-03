from fasta_to_pandas import fasta_to_pandas
from pandas_to_fasta import pandas_to_fasta
import pandas as pd


def concatenate_pandas(df_list):
    concatenated_df = pd.concat(df_list)

    return concatenated_df


if __name__ == '__main__':
    first_novel = fasta_to_pandas('williams_MTB/cd_hit_analysis/first_novel.fasta', 'Uniprot_B', 'Seq2')
    second_novel = fasta_to_pandas('williams_MTB/cd_hit_analysis/second_novel.fasta', 'Uniprot_B', 'Seq2')
    third_novel = fasta_to_pandas('williams_MTB/cd_hit_analysis/third_novel.fasta', 'Uniprot_B', 'Seq2')
    fourth_novel = fasta_to_pandas('williams_MTB/cd_hit_analysis/fourth_novel.fasta', 'Uniprot_B', 'Seq2')
    sixth_novel = fasta_to_pandas('williams_MTB/cd_hit_analysis/sixth_novel.fasta', 'Uniprot_B', 'Seq2')
    missing_examples = fasta_to_pandas('williams_MTB/cd_hit_analysis/missing_novel.fasta', 'Uniprot_B', 'Seq2')
    print(len(first_novel))
    print(len(second_novel))
    print(len(third_novel))
    print(len(fourth_novel))
    print(len(sixth_novel))
    print(len(first_novel) + len(second_novel) + len(third_novel) + len(fourth_novel) + len(sixth_novel) + len(
        missing_examples))
    positive_examples = fasta_to_pandas('williams_MTB/positive_examples.fasta', 'Uniprot_B', 'Seq2')
    print(len(positive_examples))
    df_list = [first_novel, second_novel, third_novel, fourth_novel, sixth_novel, missing_examples]
    negative_examples = concatenate_pandas(df_list)
    print(negative_examples.head())
    print(len(negative_examples))
    pandas_to_fasta(negative_examples, 'williams_MTB/new_negative_examples.fasta', 'Uniprot_B','Seq2')


