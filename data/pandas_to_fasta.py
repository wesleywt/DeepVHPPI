

def pandas_to_fasta(df, outputfile, id_col, seq_col):
    """
    Convert a pandas dataframe containing an id and sequence to a fasta file
    Parameters:
        df (pd.Dataframe): A pandas dataframe where the export file has pandas imported
        outputfile (str): Output file location
        id_col (str): The name of the id column in the dataframe
        seq_col(str): The name of the sequence column in the dataframe
    """
    with open(outputfile, 'a') as f:
        for i in range(0, len(df)):
            f.write(f'>{df[id_col].iloc[i]} \n {df[seq_col].iloc[i]}\n')