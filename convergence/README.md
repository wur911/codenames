# Convergence game

## TODO LIST
*  Fix up file uploading
*  Move word embedding upload to admin privileges
*  fix UI
*  Kd tree with cosine similarity?

## DONE
*  Get word embeddings
*  Find midpoint algorithm
*  Eliminate duplicate words
*  Set up rudimentary UI using flask
*  Moved to use kd tree
*  extend to allow multiple words
   *  Extend algorithm code
   *  Extend UI
*  Use cosine similarity iterate over english dict
*  Find smaller vocab (~100k words)

### Word embeddings

*   word2vec
*   GloVe
*   Elmo
*   ???

### Find midpoint of words

For n=2 -> midpoint

*   Center of mass / centroid = mean of coordinates = minimize squared distance
*   Geometric media = minimize distance
*   minimize avg distance
*   minimize avg square distance
*   minimize max distance

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