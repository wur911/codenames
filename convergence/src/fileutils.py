import csv
import numpy as np

def build_embeddings(src_filename,
                     delimiter=',',
                     header=True,
                     quoting=csv.QUOTE_NONE):
    """
    Builds a distributional word-word matrix.

    Args:
        scr_filename: The source filename
        delimiter: delimiter (default: ',')
        header: Whether there is a header line
        quoting: ???

    Return:
        Returns a tuple of (matrix, rownames, colnames)
    """
    reader = csv.reader(file(src_filename), delimiter=delimiter, quoting=quoting)
    colnames = None
    if header:
        colnames = reader.next()
        colnames = colnames[1: ]
    mat = []
    rownames = []
    for line in reader:        
        rownames.append(line[0])            
        mat.append(np.array(map(float, line[1: ])))
    print "Done building embeddings"
    return (np.array(mat), rownames, colnames)