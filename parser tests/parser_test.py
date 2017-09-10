from parser import parser
from bs4 import BeautifulSoup
from urllib2 import urlopen
from library import compareDict
#given the dicts of player status,
#returns a string summarizing changes 

parser = parser()


#site = str(BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read()))



file_orig = open("source2h2z.txt",'r')
text_orig = file_orig.read()
parser.feed(text_orig)
dict_orig = parser.getPlayers()

file_new= open("source1h3z.txt",'r')
text_new = file_new.read()
parser.feed(text_new)
dict_new = parser.getPlayers()


print dict_orig

print dict_new

print compareDict(dict_orig,dict_new)
