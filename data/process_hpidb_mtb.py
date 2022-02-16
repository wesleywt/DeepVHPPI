import time

import pandas as pd
from Bio import Entrez
from tqdm import tqdm
from utils.uniprot_query import UniprotQueryClient
import numpy as np
from sklearn.model_selection import train_test_split
import json
"""parse_hidb formats the datasets downloaded from HPIDB https://hpidb.igbb.msstate.edu/"""

class Models:
    def __init__(self, df):
        self.df = df
        self.taxon_list = []
        self.species_dict = {}
        self.species_list = []

    def uniprot_ref(self, column):
        xref = self.df[column].tolist()
        uniprot_ref = []
        for ID in xref:
            id_sublist = ID.split("|")
            for item in id_sublist:
                if item.split(":")[0] == 'uniprotkb':
                    uniprot_ref.append(item.split(":")[1])

        return uniprot_ref

    def taxid_species_name(self, column):
        taxids = self.df[column].tolist()
        self.taxon_list = [item.split(':')[1].split("(")[0] for item in taxids]

        Entrez.email = 'wesleywt@gmail.com'
        taxons = list(dict.fromkeys(self.taxon_list))
        handle = Entrez.efetch('taxonomy', id=taxons, rettype='xml')
        response = Entrez.read(handle)

        for entry in response:
            sci_name = entry.get('ScientificName')
            taxonid = entry.get('TaxId')
            self.species_dict.update({taxonid: sci_name})
        species_list = []
        for taxonid in self.taxon_list:
            species_list.append(self.species_dict[taxonid])

        return self.taxon_list, species_list

    def sequence(self, column):
        return self.df[column].tolist()


def create_interaction_df(input_csv_file:str)->pd.DataFrame:
    """Creates an interaction dataset from the mitab file downloaded from HPIDB for all bacteria.

        Args:
            input_csv_file (str): The input mitab file that is tab seperated
        Returns:
            output_df (pd.Dataframe): A pandas dataframe containing all the protein information for


    """
    df = pd.read_csv(input_csv_file, sep='\t', encoding='ISO-8859-1')
    db = Models(df)
    protein_id_1 = db.uniprot_ref('protein_xref_1')
    protein_id_2 = db.uniprot_ref('protein_xref_2')
    taxonID_1, speciesName_1 = db.taxid_species_name('protein_taxid_1')
    taxonID_2, speciesName_2 = db.taxid_species_name('protein_taxid_2')
    seq1 = db.sequence('protein_seq1')
    seq2 = db.sequence('protein_seq2')
    # ensure that the interaction df follows bacteria/pathogen (A) info -> human/host (B) info format
    output_df = pd.DataFrame(
        data=zip(protein_id_2, protein_id_1, taxonID_2, taxonID_1, speciesName_2, speciesName_1, seq2, seq1),
        columns=['Uniprot_A', 'Uniprot_B', 'TaxonID_A', 'TaxonID_B', 'Species_A', 'Species_B', 'Seq1', 'Seq2'])
    return output_df


def add_random_negative_entries(input_df, human_id_column, from_random_csv=False, csv_file=None):
    if from_random_csv:
        negative_df = pd.read_csv(csv_file, index_col=0)
        print(negative_df.head())
        input_df.drop(columns=['Uniprot_B', 'Seq2'])
        input_df['Uniprot_B'] = negative_df['Uniprot_B'].values
        input_df['Seq2'] = negative_df['Seq2'].values
    else:
        id_list = input_df[human_id_column].tolist()
        negative_df = pd.DataFrame(columns=['Uniprot_B', 'Seq2'])
        # for i in tqdm(range(0, len(id_list))):
        input_length = len(id_list)
        i = 0
        pbar = tqdm(desc='Uniprot Download', total=input_length)
        while i < input_length:
            time.sleep(0.1)
            query = UniprotQueryClient()
            query.make_random_query(9606, 1)
            query_id = query.get_fasta_uniprot_id()
            query_seq = query.get_fasta_seq_only()
            before_append = len(negative_df)
            if query_id not in id_list:
                query_data = {'Uniprot_B': query_id, 'Seq2': query_seq}

                query_df = pd.DataFrame(data=query_data, index=np.arange(1))

                negative_df = pd.concat([negative_df, query_df], ignore_index=True)

                query.clear()
                if len(negative_df) == before_append + 1:
                    i += 1
                    pbar.update(i)
            else:
                continue
        # save downloaded list

        print(f'Downloaded {len(negative_df)}\{len(id_list)} examples from Uniprot')
        pbar.close()
        negative_df.to_csv('williams_MTB/uniprot_negative.csv')
        input_df.drop(columns=['Uniprot_B', 'Seq2'])
        input_df['Uniprot_B'] = negative_df['Uniprot_B'].values
        input_df['Seq2'] = negative_df['Seq2'].values

    return input_df


def create_split_list(df, split_list, is_interaction):
    for i in range(0, len(df)):
        bacterial_protein = df['Uniprot_A'].iloc[i]
        bacterial_seq = df['Seq1'].iloc[i]
        human_seq = df['Seq2'].iloc[i]
        human_protein = df['Uniprot_B'].iloc[i]

        sample = {'protein_1': {'id': bacterial_protein, 'primary': bacterial_seq},
                  'protein_2': {'id': human_protein, 'primary': human_seq}, 'is_interaction': is_interaction}
        split_list.append(sample)
    return split_list


def train_test(df, split_percent=0.2):
    train, test = train_test_split(df, test_size=split_percent, shuffle=True, random_state=42)
    return train, test


def create_train_test_list(positive_df, negative_df, split_percent=0.2):
    pos_train, pos_test = train_test(positive_df, split_percent=split_percent)
    neg_train, neg_test = train_test(negative_df, split_percent=split_percent)
    train_list = []
    train_list = create_split_list(pos_train, split_list=train_list, is_interaction=1)
    train_list = create_split_list(neg_train, split_list=train_list, is_interaction=0)
    test_list = []
    test_list = create_split_list(pos_test, split_list=test_list, is_interaction=1)
    test_list = create_split_list(neg_test, split_list=test_list, is_interaction=0)

    return train_list, test_list


if __name__ == '__main__':
    input_csv = 'williams_MTB/pathcat_BACTERIA.mitab_plus.txt'
    random_csv = 'williams_MTB/uniprot_negative.csv'
    interactionDF = create_interaction_df(input_csv)
    negative_interaction_df = add_random_negative_entries(interactionDF,
                                                          'Uniprot_B',
                                                          from_random_csv=True,
                                                          csv_file=random_csv)

    list_train, list_test = create_train_test_list(interactionDF, negative_interaction_df)
    with open('williams_MTB/hidb_train.json', 'w') as f:
        json.dump(list_train, f)
    with open('williams_MTB/hidb_test.json', 'w') as f:
        json.dump(list_test, f)
