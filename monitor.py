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
    #Skips sending update to GroupMe on first pass
    first_run = True


    with open("config.xml") as config_file:
        settings = config_file.read()
    config = BeautifulSoup(settings, "xml")
    #bot id taken from GroupMe
    bot_id = str(config.GroupMe.bot_id.get_text().strip())
    if bot_id == "FILL THIS IN":
        print("You need to fill in the bot id in config.xml")
        exit()
    #if true, delays the GroupMe post by delay_in_mins
    delay_msg = config.settings.delay_msg.get_text().strip() == "True"
    delay_in_mins = int(config.settings.delay_in_mins.get_text().strip())
    seconds_between_checks= int(config.settings.seconds_between_checks.get_text().strip())
    command = "curl -d '{"
    command+= '"text" : "Starting up", '
    command+= '"bot_id":"'+bot_id+'"}'
    command+= "' https://api.groupme.com/v3/bots/post"

    system(command)



    #file for logging human and zombie counts
    f = open('stats.txt','a')
    old_players = {}


    while True:
        #Parse site, retrieve stats    
        site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read(),features="lxml")
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
            command = "curl -d '{"
            command+= '"text" : "'+message+'", '
            command+= '"bot_id":"'+bot_id+'"}'
            command+= "' https://api.groupme.com/v3/bots/post"
            if delay_msg:
                command += " | at now + " + delay_in_mins + " minutes"
            system(command)
        else:
            first_run = False



        old_players = new_players
        sleep(seconds_between_checks) 

    f.close()

main()
