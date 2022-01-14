
def get_fasta_seq_only(fasta):
    """Removes the description line from a fast file, leaving only the sequence"""
    if fasta is not None:
        fasta_split = fasta.splitlines()  # splits the fasta file into a list at the '\n' where the first item in the
        # list is the description line
        fasta_seq = ''.join(fasta_split[1:])  # joins the rest of the splitline list to construct the sequence
    else:
        fasta_seq = 'No sequence'

    return fasta_seq


def get_fasta_uniprot_id(fasta):
    """Extracts the Uniprot ID descriptor from the description line of the fasta file"""
    if fasta is not None:
        uniprot_id = fasta.split('|')[1]  # the second item in the list will be the uniprot ID
    else:
        uniprot_id = 'No ID'
    return uniprot_id


def get_fasta_description(fasta):
    """Use the split methods to splice out information"""
    if fasta is not None:

        description = fasta.split('|')[2].split("\n")[0]
    else:
        description = 'No description'
    return description
