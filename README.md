[![Build Status](https://img.shields.io/travis/sotetsuk/memozo.svg)](https://travis-ci.org/sotetsuk/memozo)
[![Coverage Status](https://img.shields.io/coveralls/sotetsuk/memozo.svg)](https://coveralls.io/github/sotetsuk/memozo)
[![python3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://github.com/sotetsuk/memozo)
[![LICENCE](https://img.shields.io/github/license/sotetsuk/memozo.svg)](https://github.com/sotetsuk/memozo)

# memozo
Python decorator for memoization to disk.

## Motivating example
Imagene that now you have tremendous number of sentences and you have to filter the sentences which includes a given keyword.
You will create a filtering generator which take a argument as keyword,
and you may want to **cache** the filtered sentences to disk if you plan to reuse the filtered sentences again,

**memozo** greatly helps such a situation !

```py
import codecs
from memozo import Memozo

m = Memozo('./data')


@m.generator(file_name='filtered_sentences', ext='txt')
def filter_data(keyword):
    path_to_raw_data = './data/sentences.txt'
    with codecs.open(path_to_raw_data, 'r', 'utf-8') as f:
        for line in f:
            if keyword in line:
                yield line

if __name__ == '__main__':
    # This generator will filter sentences of original data ('./data/sentences.txt')
    # and save filtered sentences to './data/filtered_sentences_1fec01f.txt'.
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
```

## How it works
**Memozo** decorator will create a ```.memozo``` log file at the path determined by ```Memozo``` constructor.
When the created data is successflly cached, the log is added to ```.memozo``` file:

```
2017-01-20 18:32:36	1fec01f	filtered_sentences	filter_data	'keyword': 'pen'
```

where each column indicates (```datetime```, ```hash```, ```file name```, ```function name```, ```parameters```).
The log includes sha1 hash created by the triplet of (```file name``` (if not specified, equal to function name), ```function name```, ```parameters```).
The hash is also used in cached file name (```{file name}_{hash}.{extension}```).
Memozo will reuse the cashed data if **the same hash exists in ```.memozo``` log file and actually the cached file exists**.
That is, if (at least) one of the (```file name```, ```function name```, ```parameters```) is changed, cached files are not used.

## Installation

```sh
$ pip install memozo
```

## APIs

The methods of ```Memozo``` includes:

- ```___call___``` (analogous to ```open```)
- ```codecs``` (analogous to ```codecs```)
- ```pickle``` (analogous to ```pickle.load``` and ```pickle.dump```)
- ```generator``` (caching generator outputs)

## LICENSE
MIT
