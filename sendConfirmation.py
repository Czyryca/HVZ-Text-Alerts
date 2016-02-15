from urllib2 import urlopen
import sys
import re
import datetime
from time import sleep
from bs4 import BeautifulSoup
import smtplib
import getpass

mailing_list = ["k.czyryca@gmail.com"]

#prepare to send texts through emails
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
if(len(sys.argv)==2):
    password = sys.argv[1]
else:
    password = getpass.getpass()
server.login('umbchvzdeath@gmail.com',password)


#assumes connection is set up 
def sendMessage(recipient):
    server.sendmail('umbchvzdeath@gmail.com',recipient, "You've been added to the UMBCHVZ Text Alerts mailing list. Please reply to confirm.")

for number in mailing_list:
	sendMessage(number)

