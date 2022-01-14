from model.embedding import BERTEmbeddingConv

embedding = BERTEmbeddingConv(27, 768, max_len=512, pos='sin')

seq = 'MTGTTGATATAGATAGAYT'

embed,conv_result = embedding(seq)

