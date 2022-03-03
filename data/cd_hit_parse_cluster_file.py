def parse_cluster(input_file):
    with open(input_file, 'r', encoding='UTF-8') as f:
        data = f.readlines()
    not_novel_ids = []
    for item in data:

        if '>' not in item.split('\t')[0]:

            if int(item.split('\t')[0]) > 0:
                not_novel_ids.append(item.split('\t')[1].split('>')[1].split('.')[0])
    print(len(not_novel_ids))
    return len(not_novel_ids)


if __name__ == '__main__':
    uniprot_redo = parse_cluster('williams_MTB/50_novel.fasta.clstr')
