from __future__ import print_function
import sqlite3
from collections import namedtuple
conn = sqlite3.connect('tha-wn.db')
Word = namedtuple('Word', 'synsetid li')
Synset = namedtuple('Synset', 'synset li')

def getWords(wordid):
	words = []
	cur = conn.execute("select * from word_synset where synsetid=?", (wordid,))
	row = cur.fetchone()
	return Word(*cur.fetchone())

def getSynset(synset):
	cursor=conn.execute("select * from word_synset where li=?",(synset,))
	row=cursor.fetchone()
	if row:
		return Synset(*row)
	else:
		return None
        
print(getSynset("สุดยอด"))
print(getWords("02503365-v"))