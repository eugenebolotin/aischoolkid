#!/usr/bin/env python


import re

from flask import Flask, request, render_template

from cmudb import CmuDb
from config import CMUDICT_DB_FILENAME


app = Flask(__name__)


def get_db():
    if not hasattr(get_db, 'db'):
        get_db.db = CmuDb(CMUDICT_DB_FILENAME)
    return get_db.db


def get_last_word(text):
    words = re.findall('[^\W\d]+', text)
    return words[-1] if words else ''

    
def get_rhymes(text):
    word = get_last_word(text).lower()
    return '\n'.join(get_db().get_rhymes(word))


@app.route('/literature/poetry/rhymes', methods=['POST'])
def poetry_rhymes():
    text = request.get_json().get('text', '')

    rhymes = get_rhymes(text)
    return rhymes


@app.route('/literature/poetry', methods=['GET'])
def poetry():
    return render_template('poetry.html')


if __name__ == '__main__':
    app.run(debug=True)
