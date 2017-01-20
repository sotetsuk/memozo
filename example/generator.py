import codecs
from memozo import Memozo

m = Memozo('./data')


@m.generator(name='filtered_sentences', ext='txt')
def filter_data(keyword):
    path_to_raw_data = './data/sentences.txt'
    with codecs.open(path_to_raw_data, 'r', 'utf-8') as f:
        for line in f:
            if keyword in line:
                yield line

if __name__ == '__main__':
    # This generator will filter sentences of original data ('./data/sentences.txt')
    # and save filtered sentences to './data/filtered_sentences_.txt'.
    gen_pen_sentences1 = filter_data('pen')
    for line in gen_pen_sentences1:
        print(line, end='')

    # This generator yields sentences from cached data ('./data/filtered_sentences_1fec01f.txt')
    # We do not need to load all of the original sentences again.
    gen_pen_sentences2 = filter_data('pen')
    for line in gen_pen_sentences2:
        print(line, end='')

    # Given a different parameter, sentences are filtered again from raw data.
    gen_apple_sentences = filter_data('apple')
    for line in gen_apple_sentences:
        print(line, end='')


