# Convergence game

## TODO LIST
*  Use cosine similarity iterate over english dict
*  Find smaller vocab (~100k words)
*  Fix up file uploading
*  extend to allow multiple words
   *  Extend algorithm code
   *  Extend UI
*  Move word embedding upload to admin privileges
*  fix UI

## DONE
*  Get word embeddings
*  Find midpoint algorithm
*  Eliminate duplicate words
*  Set up rudimentary UI using flask
*  Moved to use kd tree

### Word embeddings

*   word2vec
*   GloVe
*   Elmo
*   ???

### Find midpoint of words

For n=2 -> midpoint

*   Center of mass / centroid = mean of coordinates = minimize squared distance
*   Geometric media = minimize distance

### Find nearest point to midpoint

*   brute force
*   kd tree
*   locality sensitive hashing
*   min-hash/shingling

Ensure nearest point is not one of original points

### UI

*   angular js?
*   node js
*   react js
*   django/flask
*   plain js