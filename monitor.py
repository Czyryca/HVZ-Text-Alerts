"""
Main file.
Gets the number of humans and zombies in the game, 
then posts changes to a specified GroupMe chat.
Also logs stats at stats.txt.
"""

from __future__ import print_function
import urllib2
from time import sleep
from os import system
from pprint import pprint
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

    seconds_between_checks = settings['seconds_between_checks']

    #No ID provided? Defaults to current game
    game_id = settings['game_id'].strip()


    #file for logging human and zombie counts
    f = open('stats.txt','a')
    old_players = {}

    #Use API to get json dict, retrieve stats
    if settings['game_id']== "":
        url = 'https://umbchvz.com/api/longGamePlayerList.php'
    else:
        url = 'https://umbchvz.com/api/longGamePlayerList.php?gameID='+game_id


    while True:
        got_data = False

        while not got_data:
            try:
                #the server tries to send a cached page, which is NOT ok for us
                request = urllib2.Request(url)
                request.add_header('Pragma','no-cache')
                content = urllib2.build_opener().open(request)
                site_data = json.loads(content.read())

                got_data = True
                try:
                    new_players = site_data['players']
                    humans = site_data['humans']
                    zombies = site_data['zombies']
                    ozs = site_data['ozs']
                except KeyError:
                    print("Dict is missing keys at "+getDate())
                    print(site_data)
                    new_players = {}
            except urllib2.URLError:
                print("Unable to get players. Server is down? "+getDate())
                sleep(5*60)
    
        #pprint(new_players)
        print(getDate())
        #if it's not the first time, check for deaths
        #if it's the first time through the loop, initialize old_human_count
        
        change,humans_count,zombies_count = compareDict(old_players,new_players)
        
        if change and not first_run:
            print(change)
            stats = 'at '+getDate()+': '+str(humans)+' Humans, and '+str(zombies)+' Zombies\n'
            f.write(stats) 
            print(stats)

            #send message in groupme
            if int(ozs) > 0:            
                message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)+' with '+str(ozs)+' hidden OZs.'
            else:
                message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)
    
            sendMessage(message,bot_id)

        else:
            first_run = False



        old_players = new_players
        sleep(seconds_between_checks) 

    f.close()

main()
