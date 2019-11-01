#!/usr/bin/env python


from flask import Flask, request, render_template
from nltk.corpus import stopwords
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer


app = Flask(__name__)


def build_summarizer(algorithm, stemmer):
    if algorithm == 'lex_rank':
        return LexRankSummarizer(stemmer)
    elif algorithm == 'lsa':
        return LsaSummarizer(stemmer)
    elif algorithm == 'luhn':
        return LuhnSummarizer(stemmer)


def make_summary(text, language, sentence_count, algorithm):
    tokenizer = Tokenizer(language)
    parser = PlaintextParser.from_string(text, tokenizer)
    stemmer = Stemmer(language)

    summarizer = build_summarizer(algorithm, stemmer)
    summarizer.stop_words = stopwords.words(language)

    lines = []
    for sentence in summarizer(parser.document, sentence_count):
        lines.append(str(sentence))

    return '\n'.join(lines)


@app.route('/literature/summary', methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        text = request.form.get('text')
        language = request.form.get('language')
        sentence_count = request.form.get('sentence_count')
        algorithm = request.form.get('algorithm')

        print(text, language, sentence_count, algorithm)
        text_summary = make_summary(text, language, sentence_count, algorithm)
    else:
        text = open('dary_volhvov.txt').read()
        language = 'russian'
        sentence_count = 20
        algorithm = 'lex_rank'
        text_summary = make_summary(text, language, sentence_count, algorithm)

    return render_template('summary.html', text=text, language=language, 
            sentence_count=sentence_count, algorithm=algorithm, 
            text_summary=text_summary)
