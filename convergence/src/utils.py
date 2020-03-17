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
    

def midpoint(words, mat=None, rownames=None):
    """
    Gets the midpoint between two words as a vec.

    Args:
        words: Array of str
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)

    Return:
        Returns the midpoint of two words as a vec.
    """
    total = np.zeros(np.shape(mat)[1])
    for word in words:
        if word not in rownames:
            raise ValueError('%s is not in this VSM' % word)
        total += mat[rownames.index(word)]
    return total / float(max(len(words), 1))


def is_equivalent_word(word1=None, word2=None):
    if word1 in word2 or word2 in word1:
        return True
    return False


def get_avg_dist(v, other_vs=[], distfunc=cosine):
    return sum(distfunc(v, x) / float(len(other_vs)) for x in other_vs)


def get_convergence(words=[], mat=None, rownames=None, distfunc=cosine, k=10):
    """
    Shows top k closest convergence guesses.

    Args:
        words: Array of str
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        distfunc: Distance function
        k: Number of words to give

    Return:
        Returns a list of the k best convergences as determined by distfunc
    """
    if any(word not in rownames for word in words):
        raise ValueError('%s is not in this VSM' % word)
    word_vectors = [mat[rownames.index(x)] for x in words]
    dists = [(candidate_w, get_avg_dist(candidate_v, word_vectors, distfunc)) for candidate_w, candidate_v in zip(rownames, mat)]
    dists = sorted(dists, key=itemgetter(1), reverse=False)
    convergences = []
    i = 0
    while len(convergences) < k:
        converged_word = dists[i][0]
        if not any(is_equivalent_word(converged_word, w) for w in words):
            convergences += [(dists[i])]
        i += 1
    return convergences

def get_convergence_midpoint(words=[], mat=None, rownames=None, distfunc=cosine, k=10):
    """
    Shows top k closest convergence guesses.

    Args:
        words: Array of str
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        distfunc: Distance function
        k: Number of words to give

    Return:
        Returns a list of the k best convergences as determined by distfunc
    """
    w_mid = midpoint(words, mat, rownames)
    dists = find_distances(w_mid, mat, rownames, distfunc)
    convergences = []
    i = 0
    while len(convergences) < k:
        converged_word = dists[i][0]
        if not any(is_equivalent_word(converged_word, w) for w in words):
            convergences += [(dists[i])]
        i += 1
    return convergences

def get_convergence_kdtree(words=[], mat=None, rownames=None, kdtree=None, k=10):
    """
    Shows top k closest convergence guesses.

    Args:
        words: Array of str
        mat: Distributional matrix
        rownames: The rownames (labels of matrix rows)
        kdtree: Kd tree
        k: Number of words to give

    Return:
        Returns a list of the k best convergences as determined by using the kdtree
    """
    w_mid = midpoint(words, mat, rownames)
    dists, pt_idx = kdtree.query([w_mid], k*2)
    dists = dists.flatten()
    pt_idx = pt_idx.flatten()
    print dists
    print pt_idx
    convergences = []
    i = 0
    while len(convergences) < k:
        converged_word = rownames[pt_idx[i]]
        dist = dists[i]
        if not any(is_equivalent_word(converged_word, w) for w in words):
            convergences += [(converged_word, dist)]
        i += 1
    return convergences