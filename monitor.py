"""
Main file.
Gets the number of humans and zombies in the game, 
then contacts the mailing list if it changes.
Also logs stats at stats.txt.
"""

from urllib2 import urlopen
import sys
import re
import datetime
from time import sleep
from bs4 import BeautifulSoup
import smtplib
from getpass import getpass
from parser import parser
from HTMLParser import HTMLParser

#if LIVE: activates mailing list
LIVE = True
if LIVE:
    mailing_list = []
else:
    mailing_list = ['k.czyryca@gmail.com']


#TODO prompt for password if not given
if (len(sys.argv) == 2) :
    password = (sys.argv[1])
else: 
    password = getpass()

#date format sample: 13 April 2015 02:43AM
def getDate():
    return str(datetime.datetime.now().strftime('%d %B %Y %I:%M%p'))

#given the dicts of player status,
#returns a string summarizing changes 
def compareDict(old_dict,new_dict):
    joining = []
    dying = []
    revived = []
    revealed_OZs = []
    for player in new_dict:
        if (player not in old_dict.keys()):#new player joining
            joining.append(player)
        elif new_dict[player] == old_dict[player]:#no change, most common case
            continue
        elif (new_dict[player]=='zombie' and old_dict[player]=='human'):#ded 
            dying.append(player)
        elif (new_dict[player]=='human' and old_dict[player]=='zombie'):#ununded
            revived.append(player)
        elif (new_dict[player]=='OZ' and old_dict[player]=='human'):#dirty OZs
            revealed_OZs.append(player)
        else:
            print 'check compare dict' #its 3 AM TODO
    #return the results of the diff
    result = ''
    if (len(joining)>0):
        result += 'Joining: '+(','.join(joining))+' '
    if (len(dying)>0):
        result += 'Dying: '+(','.join(dying))+' '
    if (len(joining)>0):
        result += 'Revived?!?: '+(','.join(revived))+' '
    if (len(revealed_OZs)>0):
        result += 'Revealed OZ: '+(','.join(revealed_OZs))+' '
    print result
    return result 
    
        

#prepare to send texts through emails
#Currently hardcoded to log into umbchvzdeath@gmail.com
#returns the smtp server
def setUpEmail():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login('umbchvzdeath@gmail.com',password)
    return server


#assumes connection is set up
def sendMessage(recipient,deaths,status,change):
    #first, prepare the message
    print change.strip()
    if deaths > 1:
        msg = str(deaths)+" humans died! "+str(change)
    elif deaths == 1:
        msg = str(deaths)+" human died! "+str(change)
    else:
        print "strange # of deaths: "+str(deaths)
        msg = str(deaths)+"? humans died! "+str(change)
    print "change: "+str(change)
    print "sending message: "+str(msg)

        
    #then send it
    try:
        server = setUpEmail()
        server.sendmail('umbchvzdeath@gmail.com',recipient,str(msg))
    except Exception:
        server = setUpEmail()
        try: #this fails randomly sometimes. My apartment has sketchy internet
            sleep(10)
            print 'Trying once more to send to '+str(recipient)
            server.sendmail('umbchvzdeath@gmail.com',recipient,msg)
            print 'And succeeded.'
        except Exception:
            print "But still couldn't"


#args: int deaths -- the number of people who've died since last update
#
def respondToDeaths(deaths,status,change):
    if deaths > 0: #DED 
        print str(deaths)+" deaths!"
        for number in mailing_list:
            sendMessage(number,deaths,status,change)
    elif deaths < 0: #explains 'births', either players joining or initializing
        print 'There are now '+str(new_human_count)+' players.'
    

    

server = setUpEmail()

#file for logging human and zombie counts
f = open('stats','a')
old_human_count = 0

#Parser to determine player status
old_players = {}

while True:
    #retrieve stats    
    date = getDate()
    site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read())
    my_parser = parser()
    my_parser.feed(str(site))
    stats = re.findall('[0-9]+ Humans*, and [0-9]+ Zombies*.*?[.]', site.get_text()) 
    stats = str(stats[0])
    #log stats to file and console
    f.write('at '+date+': '+stats+'\n') 
    print 'wrote: at '+date+': '+stats 


    #Check humans alive
    #if the number has gone down, alert everyone
    counts = [int(number) for number in stats.split() if number.isdigit()]
    new_human_count = counts[0]
    zombies = counts[1]
    new_players = my_parser.getPlayers()

    #handles OZs
    OZs = 0
    if(re.search("the OZ",stats)):
        OZs = 1
    else: 
        try:
            OZs = counts[2]
        except IndexError:
            pass #give up and leave it at 0


    #if it's not the first time, check for deaths
    #if it's the first time through the loop, initialize old_human_count
    if old_human_count != 0:
        deaths = old_human_count - new_human_count

    else:
        old_players = new_players
        old_human_count = new_human_count
        deaths = -1 * new_human_count #negative deaths = births?
    print "DEBUG: old: "+str(old_human_count)+" new: "+str(new_human_count)+" deaths: "+str(deaths) + " zombies:"+str(zombies) + " OZs: "+str(OZs)

    change = str(compareDict(old_players,new_players))
    if deaths!=0:
        respondToDeaths(deaths,stats,change);
        deaths = 0
    
 
    if change:
        print 'Diff: '+change
    old_human_count = new_human_count


    old_players = new_players
        
    #check again in 60 seconds
    sleep(60) 



f.close()
