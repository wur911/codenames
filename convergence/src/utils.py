from operator import itemgetter
import numpy as np
import scipy
import scipy.spatial.distance

def euclidean(u, v):
    # Use scipy's method:
    return scipy.spatial.distance.euclidean(u, v)

def cosine(u, v):
    # Use scipy's method:
    return scipy.spatial.distance.cosine(u, v)

def matching(u, v):
    # The scipy implementation is for binary vectors only. This version is more
    # general.
    return np.sum(np.minimum(u, v))

def negative_matching(u, v):
    return -1 * matching(u, v)

def jaccard(u, v):
    # The scipy implementation is for binary vectors only. This version is more
    # general.
    return 1.0 - (matching(u, v) / np.sum(np.maximum(u, v)))

def negative_jaccard(u, v):
    return -1 * jaccard(u, v)


# Brute force
def get_neighbors(word=None, mat=None, rownames=None, distfunc=cosine):
    """
    Gets neighboring words.

    Args:
        word: Word
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        distfunc: Distance function

    Return:
        Returns a list of closest words as determined by distfunc
    Raises:
        Raises ValueError if the word does not occur in rownames
    """
    if word not in rownames:
        raise ValueError('%s is not in this VSM' % word)
    w = mat[rownames.index(word)]
    dists = [(rownames[i], distfunc(w, mat[i])) for i in xrange(len(mat))]
    return sorted(dists, key=itemgetter(1), reverse=False)


def find_distances(w, mat=None, rownames=None, distfunc=cosine):
    """
    Gets words closest to the given vector.

    Args:
        w: Vec representation
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        distfunc: Distance function

    Return:
        Returns a list of closest words as determined by distfunc
    """
    dists = [(rownames[i], distfunc(w, mat[i])) for i in xrange(len(mat))]
    return sorted(dists, key=itemgetter(1), reverse=False)
    

def midpoint(word1=None, word2=None, mat=None, rownames=None):
    """
    Gets the midpoint between two words as a vec.

    Args:
        word1: Word 1
        word2: Word 2
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)

    Return:
        Returns the midpoint of two words as a vec.
    """
    if word1 not in rownames:
        raise ValueError('%s is not in this VSM' % word1)
    if word2 not in rownames:
        raise ValueError('%s is not in this VSM' % word2)
    w1 = mat[rownames.index(word1)]
    w2 = mat[rownames.index(word2)]
    return (w1 + w2) / 2.0


def is_equivalent_word(word1=None, word2=None):
    if word1 in word2 or word2 in word1:
        return True
    return False


# def get_convergence(word1=None, word2=None, mat=None, rownames=None, distfunc=cosine, k=10):
#     """
#     Shows top k closest convergence guesses.
# 
#     Args:
#         word1: Word 1
#         word2: Word 2
#         mat: Distributional matrix
#         rownames: The rownames (labels of matrix rows)
#         distfunc: Distance function
#         k: Number of words to give
# 
#     Return:
#         Returns a list of the k best convergences as determined by distfunc
#     """
#     w_mid = midpoint(word1, word2, mat, rownames)
#     dists = find_distances(w_mid, mat, rownames, distfunc)
#     convergences = []
#     i = 0
#     while len(convergences) < k:
#         if not is_equivalent_word(dists[i][0], word1) and \
#            not is_equivalent_word(dists[i][0], word2):
#             convergences += [(dists[i])]
#         i += 1
#     return convergences

def get_convergence(word1=None, word2=None, mat=None, rownames=None, kdtree=None, k=10):
    """
    Shows top k closest convergence guesses.

    Args:
        word1: Word 1
        word2: Word 2
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        kdtree: Kd tree
        k: Number of words to give

    Return:
        Returns a list of the k best convergences as determined by using the kdtree
    """
    w_mid = midpoint(word1, word2, mat, rownames)
    dists, pt_idx = kdtree.query([w_mid], k*2)
    dists = dists.flatten()
    pt_idx = pt_idx.flatten()
    print dists
    print pt_idx
    convergences = []
    i = 0
    while len(convergences) < k:
        word = rownames[pt_idx[i]]
        dist = dists[i]
        if not is_equivalent_word(word, word1) and \
           not is_equivalent_word(word, word2):
            convergences += [(word, dist)]
        i += 1
    return convergences