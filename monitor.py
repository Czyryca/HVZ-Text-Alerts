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
from library import *

#if LIVE: activates mailing list
LIVE = False
if LIVE:
    mailing_list = []
else:
    mailing_list = ['k.czyryca@gmail.com']


#Prompts for password if not given.
#Prompt is much safer than passing it as a command line arg,
#but command line arg is supported.
if (len(sys.argv) == 2) :
    password = (sys.argv[1])
else: 
    password = getpass()      



    

    
def main():
    server = setUpEmail()

    #file for logging human and zombie counts
    f = open('stats','a')
    old_human_count = 0
    old_players = {}


    while True:
        #Parse site, retrieve stats    
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

main()
