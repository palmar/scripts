from bs4 import BeautifulSoup, NavigableString, Tag
import urllib2
import string
import sqlite3
from collections import Counter

#conn = sqlite3.connect('/home/palmarg/scripts/data/yoso.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/lxvi.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/titanic4.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/lxiii.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/titanic.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/heromini.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/lxiv.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/defsus.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/rt.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/xxx.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/guardians.db')
#conn = sqlite3.connect('/home/palmarg/scripts/data/pypint.db')
conn = sqlite3.connect('/home/palmarg/scripts/data/starwars.db')

#conn.execute('DROP TABLE PLAYERS')
conn.execute('''CREATE TABLE PLAYERS
                (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, POSTS INT NOT NULL, WORDS INT NOT NULL, WORDSPERPOST REAL NOT NULL, RATING REAL NOT NULL);''')

startpage = 7
endpage = 35 
#gameurl = "http://www.teamliquid.net/forum/mafia/438132-tl-mafia-lxiv-a-game-of-intrigue?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/443848-default-suspicions-mafia?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/448443-you-only-shoot-once-mafia?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/434275-tl-mafia-lxiii-time-to-die?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/445107-iii-titanic-mini-mafia-ms-paint-edition?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/384953-hero-mini-mafia?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/451310-tl-order-lxvi-mafia?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/462188-iv-titanic-mafia-it-has-been-a-privilege?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/471815-russia-today-mini-mafia?page="
#gameurl = "http://palmar.org/posts/lol.html"
#gameurl = "http://www.teamliquid.net/forum/mafia/479775-xxx-mini-mafia-a-night-of-debauchery-18?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/480042-tl-mafia-lxx-guardians-of-the-galaxy?page="
#gameurl = "http://www.teamliquid.net/forum/mafia/501883-pick-your-power-intriguing?page="
gameurl = "http://www.teamliquid.net/forum/mafia/512849-star-wars-rogue-1-hype-mafia?page="

fullcontentlist = []
fullposterlist = []

for i in range(startpage, endpage):
    url = gameurl + str(i)
    #print url
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "html5lib")

    posters = soup.find_all('div', attrs={ 'class':'fpost-username'})
    for poster in posters:
	spans = poster.find_all('span')
        allo = spans[0]
	bello = allo.get_text()
        #print bello
        #bello = allo.encode('ascii', 'ignore')
        #rppint bello
        #b = str(a)
        #cello = bello.split(" ")[0]
        #dillo = cello.strip()
        #print dillo
        fullposterlist.append(bello)
 
    text = soup.find_all('article', attrs={ 'class':'forumPost'})
    for post in text:
        post2 = post.find('section')
        solo = post2.find_all('div', attrs={'class':'quote'})
        for lolo in solo:
            lolo.replace_with('')
        yolo = post2.get_text()
        nolo = yolo.encode('ascii', 'ignore')
        fullcontentlist.append(nolo)

#print fullposterlist[1]
posters = set(fullposterlist)
pairedposts = zip(fullposterlist, fullcontentlist)

c = Counter(fullposterlist)
idnum = 1
for i in c:
    dbid = idnum
    name = i
    posts = c[i]
    words = 0
    wordsperpost = 0
    rating = 0
    conn.execute('''INSERT INTO PLAYERS (ID, NAME, POSTS, WORDS, WORDSPERPOST, RATING) VALUES (?, ?, ?, ?, ?, ?)''', (dbid, name, posts, words, wordsperpost, rating))
    conn.commit()
    idnum = idnum + 1


for player in posters:
    totalwords = 0
    for pairs in pairedposts:
        if str(pairs[0]) == str(player):
            splitthing = str(pairs[1]).split()
            wordcount = len(splitthing)
            totalwords += wordcount
    conn.execute('''UPDATE PLAYERS SET WORDS = ? WHERE name = ?''', (totalwords, str(player)))
    conn.commit()

cursor = conn.cursor()
cursor.execute('''SELECT NAME, POSTS, WORDS FROM PLAYERS''')
allrows = cursor.fetchall()
for playerrow in allrows:
    wordscalc = float(playerrow[2])/playerrow[1]
    conn.execute('''UPDATE PLAYERS SET WORDSPERPOST = ? WHERE NAME = ?''',(wordscalc, str(playerrow[0])))
    conn.commit()
