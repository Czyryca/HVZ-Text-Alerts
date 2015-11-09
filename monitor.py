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
def sendMessage(recipient,deaths,new_human_count):
    #first, prepare the message
    if deaths > 1:
        msg = str(deaths)+" humans died! "+str(new_human_count)+" humans, "+str(51-new_human_count)+" zombies. Ask if people are clean! umbchvz.com/playerList.php"
    elif deaths == 1:
        msg = str(deaths)+" human died! "+str(new_human_count)+" humans, "+str(51-new_human_count)+" zombies. Ask if people are clean! umbchvz.com/playerList.php"

    else:
        print "strange # of deaths: "+str(deaths)
        msg = str(deaths)+"? human(s) died! Don't forget to ask if people are clean! umbchvz.com/playerList.php"
        
    #then send it
    try:
        server = setUpEmail()
        server.sendmail('umbchvzdeath@gmail.com',recipient,msg)
    except Exception:
        server = setUpEmail()
        try:
            print 'Trying once more to send to '+str(recipient)
            server.sendmail('umbchvzdeath@gmail.com',recipient,msg)
            print 'And succeeded.'
        except:
            print "But still couldn't"


#args: int deaths -- the number of people who've died since last update
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
    stats = re.findall('[0-9]+ Humans*, and [0-9]+ Zombies*', site.get_text()) 
    #log stats to file and console
    f.write('at '+date+': '+stats[0]+'\n') 
    print 'wrote: at '+date+': '+str(stats) 

    #Check humans alive
    #if the number has gone down, alert everyone
    regex_pat =  '[0-9]+'
    new_human_count = int((re.search(regex_pat, str(stats[0]))).group(0))

    #if it's not the first time, check for deaths
    #if it's the first time through the loop, initialize old_human_count
    if old_human_count != 0:
        deaths = old_human_count - new_human_count
        #new_human_count = old_human_count
    else:
        old_human_count = new_human_count
        deaths = -1 * new_human_count #negative deaths = births?
    print "DEBUG: old: "+str(old_human_count)+"new: "+str(new_human_count)+"deaths: "+str(deaths)


    respondToDeaths(deaths,new_human_count);
    deaths = 0

    old_human_count = new_human_count
        
    #check again in 5 minutes
    sleep(5*60) 



f.close()
