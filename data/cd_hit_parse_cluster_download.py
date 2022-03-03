from uniprot_get_random_sequences import get_random_sequences

from cd_hit_parse_cluster_file import parse_cluster
from pandas_to_fasta import pandas_to_fasta


if __name__ == '__main__':
    download = parse_cluster('williams_MTB/cd_hit_analysis/fourth_novel.fasta.clstr')
    print(f'Number of non-unique entries is: {download}')
    new_random = get_random_sequences(download, "Uniprot_B", 'Seq2')
    pandas_to_fasta(df=new_random, outputfile='williams_MTB/fifth_random.fasta', id_col='Uniprot_B', seq_col='Seq2')
