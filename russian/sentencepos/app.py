#!/usr/bin/env python


from flask import Flask, request, render_template

from yandexmystem import mystem


app = Flask(__name__)


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


@app.route('/russian/sentencepos/mystem', methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        text = request.form.get('text')
        output = mystem(text)
    else:
        text = open('schooltask.txt').read()
        output = mystem(text)

    return render_template('mystem.html', text=text, output=output) 


if __name__ == '__main__':
    app.run(debug=True)
