
import json
import operator
import random
import Levenshtein

class LunaroPlayers:
    def __init__(self):
        self.lunaroset = None
        self.lunarosetraw = None

    def load(self):
        """
        Load the json players to active memory.
        (self.lunaroset; self.lunarosetraw;)
        :return: Dict of all players
        """

        lunarosetraw = open("Dependencies/Lunaro Player Datasheet/Lunaro Players.json")
        lunarosetraw = lunarosetraw.read()

        self.lunarosetraw = json.loads(lunarosetraw)['Lunaro Players']
        self.lunaroset = list(self.lunarosetraw.values())
        #print(str(list(self.lunaroset.values())[random.randint(0, len(self.lunaroset) - 1)]))

        #Returns list of players, raw dict only useful when searching for specific players
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

        for player in self.lunaroset:
            diff[player['Name']] = Levenshtein.ratio(name, player['Name'])
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
            return {'Name': name, 'Shortn': name, 'Rank': None, 'Rankint': None}