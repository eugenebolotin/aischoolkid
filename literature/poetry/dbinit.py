#!/usr/bin/env python
#
# This script should be called once for each of cmudict files


from cmudb import CmuDb
from config import CMUDICT_DB_FILENAME, CMUDICT_FILENAME


db = CmuDb(CMUDICT_DB_FILENAME)
db.add_cmudict(CMUDICT_FILENAME)


