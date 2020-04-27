from bs4 import BeautifulSoup, NavigableString, Tag
import urllib2
import string
import sqlite3
import math
from collections import Counter
import time

#conn = sqlite3.connect('/home/palmarg/scripts/data/votecount.db')

#conn.execute('DROP TABLE PLAYERS')
#conn.execute('''CREATE TABLE PLAYERS
#                        (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, VOTE TEXT);''')

gameurl = "http://www.teamliquid.net/forum/mafia/461294-tl-mafia-lxvii-storm-mafia-2-voting-thread?view=all"

fullcontentlist = []
fullposterlist = []

url = gameurl
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)

class player:
    def __init__ (self):
        self.status = "alive"
        self.votes = ""
        self.name = ""
        self.lynchvotes = 0
        self.enemies = []

    def setplayername(self, string):
        self.name = string

    def addvote(self):
        self.lynchvotes = (self.lynchvotes + 1)

    def addenemy(self, playername):
        self.enemies.append(playername)

    def resetvote(self):
        self.lynchvotes = 0

    def votecount(self, votenumber):
        self.lynchvotes = votenumber

    def kill(self):
        self.status = "Dead"

    def setvotes(self, playername):
        self.votes = playername

    def getvotes(self):
        return self.votes

    def getstatus(self):
        if self.statis == "alive":
            print "alive"
        else:
            print "dead"

    def getname(self):
        return self.name


#playerlist = "Vivax","batsnacks","Bill Murray","kushm4sta","ObiWanShinobi","sinani206","prplhz","HaruRH","slOosh","Koshi","VisceraEyes","Corazon","yamato77","layabout","Damdred","ExO_","Toadesstern","HiroPro","mderg","ritoky","iamperfection","Alakaslam","IAmRobik","Forumite","27ninjabunnies","TehPoofter"

playerlist = "Toadesstern","slOosh","ExO_","BillMurray","batsnacks"
modlist = "palmar","marvellosity"
playerlistlower = [x.lower() for x in playerlist]


playerlistclass = []

for item in playerlistlower:
    playername = item
    item = player();
    item.setplayername(playername)
    playerlistclass.append(item)

posters = soup.find_all('span', attrs={ 'class':'forummsginfo'})
for poster in posters:
    allo = poster.get_text()
    bello = allo.encode('ascii', 'ignore')
    cello = bello.split("  ")[0]
    dillo = cello.strip()
    grillo = dillo.lower()
    hollo = grillo.translate(None, ' ')
    fullposterlist.append(hollo)


text = soup.find_all('td', attrs={ 'class':'forumPost'})
for post in text:
    solo = post.find('div', attrs={'class':'quote'})
    if solo:
       solo.replace_with('')
    folo = post.find('b')
    try:
    	yolo = folo.get_text()
    except:
	yolo = ""
	pass
    nolo = yolo.encode('ascii', 'ignore')
    lolo = nolo.lower()
    if "##vote" in lolo:
        trolo = lolo.split("##vote")
        try:
            dmolo = trolo[1]
        except:
            pass
        klolo = dmolo.translate(None, ' :')
        fullcontentlist.append(klolo)
    elif "##unvote" in lolo:
        klol = "unvote"
        fullcontentlist.append(klol)
    else:
	fullcontentlist.append("unrelated")
    posters = set(fullposterlist)
    pairedposts = zip(fullposterlist, fullcontentlist)

for postlol in pairedposts:
    print postlol[0] + " : " + postlol[1]

for pair in pairedposts:
    if pair[0] in playerlistlower:
    	for playerobj in playerlistclass:
            if pair[0] == playerobj.getname():
                if pair[1] in playerlistlower:
                    playerobj.setvotes(pair[1])
                elif pair[1] == "unvote":
                    playerobj.setvotes("")
    elif pair[0] in modlist and pair[1] == "reset":
        for playerobj8 in playerlistclass:
            playerobj8.setvotes("")

#for playerobj2 in playerlistclass:
#    print str(playerobj2.getname()) + " is voting for " + str(playerobj2.getvotes())

print "[b][blue]Official Votecount[/blue][/b]"
print ""
for playerobj3 in playerlistclass:
    for playerobj4 in playerlistclass:
        if playerobj4.getvotes() == playerobj3.getname():
            playerobj3.addenemy(playerobj4.getname());
    if (str(len(playerobj3.enemies)) != "0"):
        print "[b]" + str(playerobj3.getname()) + " (" + str(len(playerobj3.enemies)) + "):[/b] " + ', '.join(playerobj3.enemies)

print ""
print "With " + str(len(playerlistclass)) + " players alive it takes " + str(math.floor((len(playerlistclass)/2) + 1)) + " votes to lynch."
print ""
print "Last update [time]" + time.strftime("%H:%M:%S") + " BST [/time]"
