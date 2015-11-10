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
import getpass

#if LIVE: activates mailing list
LIVE = False
if LIVE:
    mailing_list = []
else:
    mailing_list = ['k.czyryca@gmail.com']


#TODO prompt for password if not given

if (len(sys.argv) == 2) :
    password = (sys.argv[1])
else: 
    password = getpass.getpass()

#date format sample: 13 April 2015 02:43AM
def getDate():
    return str(datetime.datetime.now().strftime('%d %B %Y %I:%M%p'))

#prepare to send texts through emails
#Currently hardcoded to log into umbchvzdeath@gmail.com
#returns the smtp server
def setUpEmail():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login('umbchvzdeath@gmail.com',password)
    return server


#assumes connection is set up
def sendMessage(recipient,deaths,status):
    #first, prepare the message
    if deaths > 1:
        msg = str(deaths)+" humans died! "+str(status)+" umbchvz.com/playerList.php"
    elif deaths == 1:
        msg = str(deaths)+" human died! "+str(status)+" umbchvz.com/playerList.php"
    else:
        print "strange # of deaths: "+str(deaths)
        msg = str(deaths)+"? humans died! "+str(status)+" umbchvz.com/playerList.php"

        
    #then send it
    try:
        server = setUpEmail()
        server.sendmail('umbchvzdeath@gmail.com',recipient,msg)
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
def respondToDeaths(deaths,new_human_count):
    if deaths > 0: #DED 
        print str(deaths)+" deaths!"
        for number in mailing_list:
            sendMessage(number,deaths,new_human_count)
    elif deaths < 0: #explains 'births', either players joining or initializing
        print 'There are now '+str(new_human_count)+' players.'

    

server = setUpEmail()

#file for logging human and zombie counts
f = open('stats','a')
old_human_count = 0

while True:
    #retrieve stats    
    date = getDate()
    site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read())
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
        old_human_count = new_human_count
        deaths = -1 * new_human_count #negative deaths = births?
    print "DEBUG: old: "+str(old_human_count)+" new: "+str(new_human_count)+" deaths: "+str(deaths) + " zombies:"+str(zombies) + " OZs: "+str(OZs)


    respondToDeaths(deaths,new_human_count,);
    deaths = 0

    old_human_count = new_human_count
        
    #check again in 60 seconds
    sleep(60) 



f.close()
