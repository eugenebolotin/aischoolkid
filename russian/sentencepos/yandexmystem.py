#!/usr/bin/env python


import sys
import re

from pymystem3 import Mystem


def mystem(text):
    lines = []
    stem = Mystem()
    for term in stem.analyze(text.replace('ё', 'е')):
        text = term.get('text')
        analysis = term.get('analysis')

        if text and analysis:
            gr = analysis[0].get('gr', '')

            sex = re.search('муж|жен', gr)
            number = re.search('ед|мн', gr)
            case = re.search('[\|\=](\w+),', gr)

            if sex and number and case:
                info = '(%s род, %s число, %s падеж)' % (sex.group(0), number.group(0), case.group(1))
                lines.append('%s %s' % (text.ljust(20), info))
            else:
                lines.append(text)

    return '\n'.join(lines)


if __name__ == '__main__':
    print(mystem(sys.stdin.read()))
