from HTMLParser import HTMLParser
import copy

class parser(HTMLParser):
    lastData = ''
    players = {}
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
        if(data in ['human','zombie','OZ']):
            self.players[str(self.lastData)] = str(data)
        self.lastData = data

    def getPlayers(self):
        temp = copy.deepcopy(self.players)
        self.players = {}
        return temp
    
