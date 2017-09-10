"""
Main file.
Gets the number of humans and zombies in the game, 
then posts changes to a specified GroupMe chat.
Also logs stats at stats.txt.
"""

from __future__ import print_function
from urllib2 import urlopen
from sys import argv
from time import sleep
from bs4 import BeautifulSoup
from parser import parser
from HTMLParser import HTMLParser
from library import *
from os import system

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

        if not(new_players): #if dict is empty
            print("Didn't find any players")
            

        #if it's not the first time, check for deaths
        #if it's the first time through the loop, initialize old_human_count
        
        change,humans,zombies = compareDict(old_players,new_players)
        
        if change and not first_run:
            print(change)
            stats = 'at '+getDate()+': '+str(humans)+' Humans, and '+str(zombies)+' Zombies\n'
            f.write(stats) 
            print(stats)
            #send message in groupme
            message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)
            command = "curl -d '{\"text\" : \"" + message + "\", \"bot_id\" : \"f9d93ab901d96ee9532da9142c\"}' https://api.groupme.com/v3/bots/post"
            #command += ' | at now +1 hour '
            system(command)
        else:
            first_run = False


        old_players = new_players
        #check again in 60 seconds
        sleep(60) 

    f.close()

main()
