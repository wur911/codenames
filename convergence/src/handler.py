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
    print word1, word2
    if not session['src_filename']:
      flash('No word embeddings found! Please import word embeddings file.')
    else:
      try:
        global model, kdtree
        print kdtree
        convergences = utils.get_convergence([word1, word2], model[0], model[1], kdtree)
        print convergences
        g.word1 = word1
        g.word2 = word2
        g.converged_word = convergences[0][0]
      except ValueError as err:
        print err
        flash('Error: ' + err.message)
  return render_template('index.html')

@bp.route('/import', methods=('GET', 'POST'))
def import_enbedding():
  # TODO: Fix up clear
  session.clear()
  if request.method == 'POST':
    src_filename = request.form['src_filename']
    delimiter = request.form['delimiter'].encode('ascii', 'ignore')
    if not delimiter:
      delimiter = ' '
    session['src_filename'] = src_filename
    session['delimiter'] = delimiter
    global model, kdtree
    model = fileutils.build_embeddings(src_filename, delimiter)
    kdtree = scipy.spatial.KDTree(model[0])
    print kdtree
    # memfile = io.BytesIO()
    # np.savez_compressed(memfile, model)
    # memfile.seek(0)
    # session['model'] = memfile
  return render_template('import_embeddings.html')