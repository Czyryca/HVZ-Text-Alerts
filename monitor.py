"""
Main file.
Gets the number of humans and zombies in the game, 
then posts changes to a specified GroupMe chat.
Also logs stats at stats.txt.
"""

from __future__ import print_function
from urllib2 import urlopen
from urllib2 import URLError
from time import sleep
from os import system
import json 
from library import *

def main():
    #Skips sending update to GroupMe on first pass
    first_run = True


    with open("config.json") as config_file:
        settings = json.load(config_file)

    #basic checks for bot id from GroupMe
    #get yours from https://dev.groupme.com/bots
    bot_id = settings['bot_id'].strip()
    if bot_id == "FILL THIS IN":
        print("You need to fill in the bot id in config.json")
        exit()
    elif len(bot_id) != 26:
        print("Check your bot_id in config.json. It should be 26 characters.")
        exit()

    #if true, delays the GroupMe post by delay_in_mins
    #Should be unnecessary, but the server-side delay isn't working
    delay_msg = settings['delay_msg']
    delay_in_mins = settings['delay_in_mins']
    seconds_between_checks = settings['seconds_between_checks']

    #No ID provided? Defaults to current game
    game_id = settings['game_id']


    #file for logging human and zombie counts
    f = open('stats.txt','a')
    old_players = {}


    while True:
        #Use API to get json dict, retrieve stats    
        got_data = False
        while not got_data:
            try:
                if settings['game_id']== "":
                    site = urlopen('https://umbchvz.com/api/longGamePlayerList.php')
                else:
                    site = urlopen('https://umbchvz.com/api/longGamePlayerList.php?gameID='+game_id)
                got_data = True
                site_data = json.loads(site.read())
                new_players = site_data['players']
                humans = site_data['humans']
                zombies = site_data['zombies']
                ozs = site_data['ozs']
            except URLError:
                print("Unable to get players. Server is down?")
                sleep(5*60)
    

        if not(new_players): #if dict is empty
            print("Didn't find any players")
            

        #if it's not the first time, check for deaths
        #if it's the first time through the loop, initialize old_human_count
        
        change,humans_count,zombies_count = compareDict(old_players,new_players)
        
        if change and not first_run:
            print(change)
            stats = 'at '+getDate()+': '+str(humans)+' Humans, and '+str(zombies)+' Zombies\n'
            f.write(stats) 
            print(stats)
            #send message in groupme
            message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)+' counting '+str(ozs)+'hidden OZs.'
            sendMessage(message,bot_id,delay_msg,delay_in_mins)

        else:
            first_run = False



        old_players = new_players
        sleep(seconds_between_checks) 

    f.close()

main()
