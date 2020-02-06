#!/usr/bin/env python


from flask import Flask, request, render_template
from nltk.corpus import stopwords
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
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


def make_summary(language, sentence_count, algorithm, text=None, url=None):
    tokenizer = Tokenizer(language)
    if url:
        parser = HtmlParser.from_url(url, tokenizer)
    else:
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

        text_summary = make_summary(language, sentence_count, algorithm, text=text)
    else:
        text = open('dary_volhvov.txt').read()
        language = 'russian'
        sentence_count = 20
        algorithm = 'lex_rank'
        text_summary = make_summary(language, sentence_count, algorithm, text=text)

    return render_template('summary.html', text=text, language=language, 
            sentence_count=sentence_count, algorithm=algorithm, 
            text_summary=text_summary)


@app.route('/literature/summary/url', methods=['GET', 'POST'])
def summary_url():
    if request.method == 'POST':
        url = request.form.get('url')
        language = request.form.get('language')
        sentence_count = request.form.get('sentence_count')
        algorithm = request.form.get('algorithm')

        text_summary = make_summary(language, sentence_count, algorithm, url=url)
    else:
        url = 'https://ru.wikipedia.org/wiki/Теорема_Пифагора'
        language = 'russian'
        sentence_count = 20
        algorithm = 'luhn'
        text_summary = make_summary(language, sentence_count, algorithm, url=url)

    return render_template('summary_url.html', url=url, language=language, 
            sentence_count=sentence_count, algorithm=algorithm, 
            text_summary=text_summary)
