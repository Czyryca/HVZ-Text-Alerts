# HVZ-Text-Alerts
Python 2 script that sends messages through GroupMe when the game server (umbchvz.com) reports deaths. Create a GroupMe developer account, edit the bot id in config.json, and then run monitor.py to use. Requires a shell with curl and at (at only required if delaying messages).

File Overview:

monitor.py is the main script to be run during weeklongs. It holds the main logic of the program. Currently, messages have no delay by default because the server has a 1 hour delay. 

config.json must be edited to include your bot id from dev.groupme.com/bots before the script can run. It contains timing preferences as well. The game id can be chaned to test on old games EX: LG0000f .

library.py defines functions used to manipulate data -- it contains no program logic and is separated for testing purposes. test.py contains unit tests for the functions defined in the library.

