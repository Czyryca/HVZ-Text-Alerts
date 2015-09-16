from urllib2 import urlopen
import sys
import re
import datetime
from time import sleep
from bs4 import BeautifulSoup
import smtplib

mailing_list = [""]

#prepare to send texts through emails
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login('umbchvzdeath@gmail.com',sys.argv[1])
#TODO prompt for password instead of hardcoding in plaintext


#assumes connection is set up 
def sendMessage(recipient):
    server.sendmail('umbchvzdeath@gmail.com',recipient, "You've been added to the mailing list. Please confirm by sending a reply to this number or umbchvzdeaths@gmail.com")

for number in mailing_list:
	sendMessage(number)
