import unittest
from library import *
import os
class TestCoreFunctions(unittest.TestCase):

    def test_getDate(self):
        print "Today's date is "+getDate()

    def test_compareDict(self):
        snapshot1 = {'alice':'human','bob':'human',
                     'carol':'human','dave':'human'}
        snapshot2 = {'alice':'zombie','bob':'human',
                     'carol':'human','dave':'human'}
        snapshot3 = {'alice':'zombie','bob':'zombie',
                     'carol':'human','dave':'OZ'}
        snapshot4 = {'alice':'zombie','bob':'zombie',
                     'carol':'zombie','dave':'OZ'}

        
        str_result,humans,zombies = compareDict(snapshot1,snapshot2)
        self.assertEqual(str_result,'Dying: alice')
        self.assertEqual(humans,3)
        self.assertEqual(zombies,1)
        text = str_result + ' -- Humans: '+str(humans)+' Zombies: '+str(zombies)
        command = "curl -d '{\"text\" : \"" + text + "\", \"bot_id\" : \"6aff2df273686bb5c617d7aff7\"}' https://api.groupme.com/v3/bots/post"
        self.assertEqual(os.system(command),0)


        #no change
        str_result,humans,zombies = compareDict(snapshot2,snapshot2)
        self.assertEqual(str_result,'')
        self.assertEqual(humans,3)
        self.assertEqual(zombies,1)


        str_result,humans,zombies = compareDict(snapshot2,snapshot3)
        self.assertEqual(str_result,'Dying: bob Revealed OZ: dave')
        self.assertEqual(humans,1)
        self.assertEqual(zombies,3)

        str_result,humans,zombies = compareDict(snapshot3,snapshot4)
        self.assertEqual(str_result,'Dying: carol')
        self.assertEqual(humans,0)
        self.assertEqual(zombies,4)

        
    def test_compareDictStrange(self):
        snapshot1 = {'alice':'zombie','bob':'human',
                     'carol':'human','dave':'human'}
        snapshot2 = {'alice':'human','bob':'human',
                     'carol':'human','dave':'human'}
        snapshot3 = {'alice':'human','bob':'human',
                     'carol':'human','dave':'human',
                     'eve':'human'}
        snapshot4 = {'alice':'human','bob':'human',
                     'carol':'human','dave':'human',
                     'eve':'zombie'}

        #test revive
        str_result,humans,zombies = compareDict(snapshot1,snapshot2)
        self.assertEqual(str_result,'Revived: alice')
        self.assertEqual(humans,4)
        self.assertEqual(zombies,0)

        #test join as human
        str_result,humans,zombies = compareDict(snapshot2,snapshot3)
        self.assertEqual(str_result,'Joining as human: eve')
        self.assertEqual(humans,5)
        self.assertEqual(zombies,0)

        #test join as zombie
        str_result,humans,zombies = compareDict(snapshot2,snapshot4)
        self.assertEqual(str_result,'Joining as zombie: eve')
        self.assertEqual(humans,4)
        self.assertEqual(zombies,1)

        #test remove players 
        str_result,humans,zombies = compareDict(snapshot4,snapshot2)
        self.assertEqual(str_result,'Removed: eve')
        self.assertEqual(humans,4)
        self.assertEqual(zombies,0)




if __name__ == '__main__':
    unittest.main()
