import csv
import numpy as np

def build_embeddings(embed_filename,
                     vocab_filename=None,
                     delimiter=',',
                     header=True,
                     quoting=csv.QUOTE_NONE):
    """
    Builds a distributional word-word matrix.

    Args:
        emebed_filename: The filename for the word embeddings
        vocab_filename: The filename for the vocab if pruning is desired
        delimiter: delimiter (default: ',')
        header: Whether there is a header line
        quoting: ???

    Return:
        Returns a tuple of (matrix, rownames, colnames)
    """
    reader = csv.reader(file(embed_filename), delimiter=delimiter, quoting=quoting)
    colnames = None
    if header:
        colnames = reader.next()
        colnames = colnames[1: ]
    mat = []
    rownames = []
    vocab = set()
    # If a vocab is provided, create a vocab to filter nonsense words
    if vocab_filename:
        with open(vocab_filename) as f:
            for line in f:
                vocab.add(line.strip().lower())
    print "Vocab has %d words" % len(vocab)
    # Create word embedding matrix
    # TODO: Debug filter
    num_filtered_words = 0
    for line in reader:
        if vocab and line[0] not in vocab:
            a = 1
            num_filtered_words += 1
            # print "Filtering out", line[0]
        else:
            rownames.append(line[0])
            mat.append(np.array(map(float, line[1: ])))
    print "Done building embeddings"
    print "Filtered out %d words" % num_filtered_words
    print "Enbedding has %d words" % len(rownames)
    return (np.array(mat), rownames, colnames)