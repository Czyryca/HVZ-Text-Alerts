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
        
        if change:
            print change
            stats = 'at '+getDate()+': '+humans+' Humans, and '+zombies+' Zombies\n'
            f.write(stats) 
            print stats 
            #TODO: send message.

        old_players = new_players
        #check again in 60 seconds
        sleep(60) 

    f.close()

main()
