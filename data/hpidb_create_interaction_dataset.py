import time

import pandas as pd
from Bio import Entrez
from tqdm import tqdm
from local_packages.uniprot_query import UniprotQueryClient
import numpy as np
from sklearn.model_selection import train_test_split
import json
from fasta_to_pandas import fasta_to_pandas


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


def create_interaction_df(input_csv_file: str) -> pd.DataFrame:
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


if __name__ == '__main__':
    input_csv = 'williams_MTB/pathcat_BACTERIA.mitab_plus.txt'
    interactionDF = create_interaction_df(input_csv)
    interactionDF.to_csv('williams_MTB/positive_interaction_dataset.csv')
