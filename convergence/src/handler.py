# import io
# import json
# import numpy as np
# import pickle
import scipy.spatial

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import fileutils
from . import utils

bp = Blueprint('handler', __name__, url_prefix='/')
model = None
kdtree = None

@bp.route('/', methods=('GET', 'POST'))
def index():
  if request.method == 'POST':
      word1 = request.form['word1']
      word2 = request.form['word2']
      word3 = request.form['word3']
      print word1, word2, word3
      if not session['src_filename']:
          flash('No word embeddings found! Please import word embeddings file.')
      else:
          try:
              global model
              # TODO: re-enable kdtree
              # global kdtree
              # print kdtree
              # convergences = utils.get_convergence_kdtree([word1, word2, word3], model[0], model[1], kdtree)
              convergences = utils.get_convergence([word1, word2, word3], model[0], model[1])
              print convergences
              g.word1 = word1
              g.word2 = word2
              g.word3 = word3
              g.converged_word = convergences[0][0]
          except ValueError as err:
              print err
              flash('Error: ' + err.message)
  return render_template('index.html')

@bp.route('/import', methods=('GET', 'POST'))
def import_enbedding():
  # TODO: Fix up clear
  session.clear()
  # TODO: allow input vocab
  vocab_filename = "data/vocab.txt"
  if request.method == 'POST':
      src_filename = request.form['src_filename']
      use_vocab = request.form['use_vocab']
      delimiter = request.form['delimiter'].encode('ascii', 'ignore')
      if not delimiter:
          delimiter = ' '
      session['src_filename'] = src_filename
      session['delimiter'] = delimiter
      global model
      # global kdtree
      if use_vocab:
          model = fileutils.build_embeddings(src_filename, vocab_filename, delimiter)
      else:
          model = fileutils.build_embeddings(src_filename, delimiter)
      session['num_words'] = len(model[1])

      # TODO: re-investigate kdtree for cosine distance
      # kdtree = scipy.spatial.KDTree(model[0])
      # print kdtree

      # TODO: save the model without global var?
      # memfile = io.BytesIO()
      # np.savez_compressed(memfile, model)
      # memfile.seek(0)
      # session['model'] = memfile
  return render_template('import_embeddings.html')