
import json
import operator
import random
import sqlite3

import Levenshtein

class LunaroPlayers:
    def __init__(self):
        self.lunaroset = None
        self.lunarosetraw = {}
        self.con = None
        self.cur = None

    def connect(self):
        self.con = sqlite3.connect('lunaroplayers.db')


    def execute(self, toexec):
        self.connect()
        self.cur = self.con.cursor()
        execed = self.cur.execute(toexec)
        return execed

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()



    def load(self):
        """
        Load the json players to active memory.
        (self.lunaroset; self.lunarosetraw;)
        :return: Dict of all players
        """

        #lunarosetraw = open("Dependencies/Lunaro Player Datasheet/Lunaro Players.json")
        #lunarosetraw = lunarosetraw.read()

        #self.lunarosetraw = json.loads(lunarosetraw)['Lunaro Players']
        #self.lunaroset = list(self.lunarosetraw.values())
        #print(str(list(self.lunaroset.values())[random.randint(0, len(self.lunaroset) - 1)]))

        #Returns list of players, raw dict only useful when searching for specific players
        self.connect()
        self.cur = self.con.cursor()
        self.lunaroset = list(self.cur.execute('''SELECT * FROM players'''))

        for i in self.lunaroset:
            self.lunarosetraw[i[0]] = i

        return self.lunaroset

    def findByExactName(self, name):
        """
        Find a player their exact name
        :param name: The player's name
        :return: Player Dict
        """

        if self.lunarosetraw == None:
            self.load()

        try:
            return self.lunarosetraw[name]
        except:
            return None



    def findByName(self, name):
        """
        Find a player by a close approximation of their name
        :param name: Approximation of the name of the player we want to find
        :return: Player Dict
        """

        if self.lunaroset == None:
            self.load()




        diff = {}

        for player in self.lunaroset:
            diff[player['Name']] = Levenshtein.ratio(name, player['Name'])
        #Get levenshtein for all of them

        #Sort by closest
        sorted_d = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))

        #Return the one with the lowest levenshtein
        #Return the json object by finding the closest one by name

        #print(self.lunarosetraw[list(sorted_d.keys())[0]], list(sorted_d.values())[0])
        return self.lunarosetraw[list(sorted_d.keys())[0]]


    def TryFindByName(self, name):
        """
        Find a player by a close approximation of their name
        :param name: Approximation of the name of the player we want to find
        :return: Player Dict
        """

        if self.lunaroset == None:
            self.load()


        print("Finding player " + str(name))

        diff = {}

        for player in self.load():
            #print(player[0])
            diff[player[0]] = Levenshtein.ratio(name, player[0])
        #Get levenshtein for all of them


        #Sort by closest
        sorted_d = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))

        #Return the one with the lowest levenshtein
        #Return the json object by finding the closest one by name

        if list(sorted_d.values())[0] > 0.5:
            #print(f"Returning {str(self.lunarosetraw[list(sorted_d.keys())[0]])}")
            return self.lunarosetraw[list(sorted_d.keys())[0]]
        else:
            #print(f"Returning 'Name': {name}, 'Shortn': None, 'Rank': None, 'Rankint': None")
            return [name, name, None, None]
