import math
import sqlite3

#conn = sqlite3.connect('/home/palmarg/scripts/data/lxvi.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/titanic4.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/lxiii.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/titanic.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/djinn.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/yoso.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/heromini.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/lxiv.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/defsus.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/rt.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/xxx.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/guardians.db')
conn = sqlite3.connect('/home/palmarg/scripts/data/pypint.db')

cursor = conn.cursor()
cursor.execute('SELECT NAME, POSTS, WORDS, WORDSPERPOST FROM PLAYERS')
allrows = cursor.fetchall()
for row in allrows:
    name = row[0]
    posts = row[1]
    words = row[2]
    wordsperpost = row[3]
#    mafiarating = math.log((posts**3 * math.sqrt(words) / wordsperpost), 10)
    try:
	mafiarating = math.log((posts**3 * math.sqrt(words) * wordsperpost**2), 10)
    except:
	mafiarating = 0
    print str(name) + " : " + str(mafiarating)

    conn.execute('UPDATE PLAYERS SET RATING = ? WHERE NAME = ?', (mafiarating, name))
    conn.commit()
