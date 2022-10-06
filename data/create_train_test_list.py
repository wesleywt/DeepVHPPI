from sklearn.model_selection import train_test_split
import random


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
    random.shuffle(train_list)
    test_list = []
    test_list = create_split_list(pos_test, split_list=test_list, is_interaction=1)
    test_list = create_split_list(neg_test, split_list=test_list, is_interaction=0)
    random.shuffle(test_list)
    return train_list, test_list
