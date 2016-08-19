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
import os



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
    #password = (sys.argv[1])
    pass
else: 
    pass
    #password = getpass()
    
def main():
    first_run = True

    #file for logging human and zombie counts
    f = open('stats','a')
    old_players = {}


    while True:
        #Parse site, retrieve stats    
        site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read())
        my_parser = parser()
        my_parser.feed(str(site))
        new_players = my_parser.getPlayers()

        #if it's not the first time, check for deaths
        #if it's the first time through the loop, initialize old_human_count
        
        change,humans,zombies = compareDict(old_players,new_players)
        
        if change and not first_run:
            print change
            stats = 'at '+getDate()+': '+str(humans)+' Humans, and '+str(zombies)+' Zombies\n'
            f.write(stats) 
            print stats 
            #send message in groupme
            message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)
            command = "curl -d '{\"text\" : \"" + message + "\", \"bot_id\" : \"6aff2df273686bb5c617d7aff7\"}' https://api.groupme.com/v3/bots/post"
            os.system(command)
        else:
            first_run = false

        old_players = new_players
        #check again in 60 seconds
        sleep(60) 

    f.close()

main()
