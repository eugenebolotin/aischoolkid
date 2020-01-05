import sqlite3
from collections import defaultdict, OrderedDict


class CmuDb(object):
    def __init__(self, db_filename):
        self.db = sqlite3.connect(db_filename)
        cursor = self.db.cursor()
        try:
            cursor.execute('CREATE TABLE cmu(word varchar(255), pron varchar(255))')
            cursor.execute('CREATE INDEX index_word ON cmu(word)')
            cursor.execute('CREATE INDEX index_pron ON cmu(pron)')
        except sqlite3.OperationalError:
            pass
        cursor.close() 

    def add_cmudict(self, filename):
        cursor = self.db.cursor()

        for line in open(filename):
            parts = line.split()
            word = parts[0]
            pron = '_'.join(reversed(parts[1:]))
            cursor.execute('INSERT INTO cmu(word, pron) VALUES("%s", "%s")' % \
                    (word, pron))

        cursor.close()
        self.db.commit()

    def get_word_pron(self, word):
        cursor = self.db.cursor()
        cursor.execute('SELECT pron FROM cmu WHERE word="%s"' % word)
        data = cursor.fetchone()
        return data[0] if data else None


    def get_rhymes(self, word):
        pron = self.get_word_pron(word)
        if not pron:
            return []

        rhymes = OrderedDict()
        pron_arr = pron.split('_')
        for i in range(int(len(pron_arr)/2)):
            if len(pron_arr) < 2:
                continue

            cursor = self.db.cursor()
            cursor.execute('SELECT word FROM cmu WHERE pron LIKE "%s%%"' % \
                    '_'.join(pron_arr))

            for word in cursor.fetchall():
                rhymes[word[0]] = 1

            cursor.close()
            pron_arr.pop()

        return rhymes.keys()
