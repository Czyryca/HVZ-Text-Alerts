from urllib2 import urlopen
import sys
import re
import datetime
from time import sleep
from bs4 import BeautifulSoup
import smtplib

LIVE = False

mailing_list = ['4438049290@messaging.sprintpcs.com']

#date format sample: 13 April 2015 02:43AM
def getDate():
    str(datetime.datetime.now().strftime('%d %B %Y %I:%M%p'))

#prepare to send texts through emails
def setUpEmail():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login('umbchvzdeath@gmail.com',str(sys.argv[1]))
    return server
    #TODO prompt for password instead of hardcoding in plaintext


#assumes connection is set up 
def sendMessage(recipient,deaths):
    try:
        server = setUpEmail()
        server.sendmail('umbchvzdeath@gmail.com',recipient,str(deaths)+" human(s) died! Don't forget to ask if people are clean! umbchvz.com/playerList.php")
    except Exception:
        server = setUpEmail()
        try:
            print 'Trying once more to send to '+str(recipient)
            server.sendmail('umbchvzdeath@gmail.com',recipient,str(deaths)+" human(s) died! Don't forget to ask if people are clean! umbchvz.com/playerList.php")
            print 'And succeeded.'

        except:
            print "But still couldn't"
    

server = setUpEmail()

#file for logging human and zombie counts
f = open('UMBCHVZ_stats','a')
old_human_count = 0

while True:
    #retrieve stats    
    date = getDate()
    site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read())
    stats = re.findall('[0-9]+ Humans*, and [0-9]+ Zombies*', site.get_text()) 

    #log stats to file and console
    f.write('at '+date+': '+str(stats[0])+'\n')
    print 'wrote: at '+date+': '+str(stats[0]) 

    #Check humans alive
    #if the number has gone down, alert everyone
    regex_pat =  '[0-9]+'
    new_human_count = int((re.search(regex_pat, str(stats[0]))).group(0))
    #if it's not the first time, check for deaths
    #if it's the first time through the loop, initialize old_human_count
    if old_human_count != 0:
        deaths = old_human_count - new_human_count
        new_human_count = old_human_count
    else:
        old_human_count = new_human_count
        deaths = -1 * new_human_count #negative deaths = births?
    print "DEBUG: old: "+str(old_human_count)+"new: "+str(new_human_count)+"deaths: "+str(deaths)


    respondToDeaths();
    old_human_count = new_human_count
        
    #check again in 5 minutes
    sleep(5*60) 
#args: int dead -- the number of people who've died since last update
def respondToDeaths(deaths):
    if deaths > 0: #DED 
        print str(deaths)+" deaths!"
        server = setUpEmail()
        server.sendmail('umbchvzdeath@gmail.com','4438049290@messaging.sprintpcs.com',str(deaths)+" human(s) died! "+str(new_human_count)+" humans left. Ask if people are clean! umbchvz.com/playerList.php")

        if live:
            for number in mailing_list:
                sendMessage(number,deaths)
        deaths = 0

    elif deaths < 0: #explains 'births', either players joining or initializing
        print 'There are now '+str(new_human_count)+' players.'


#I guess unreachable right now. Probably shouldn't run this on Windows
#TODO add a proper interupt
f.close()
