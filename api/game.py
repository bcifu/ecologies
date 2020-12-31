#from cardsEnums import *
import random

class Game: #class for the game
    def __init__(self, gameId): #the set up saved the game id, and creates and empty list for players and creates a deck which i
        self.gameId = gameId
        self.players = list()
        self.deck = list(range(108)) #create a list of all the ids
        random.shuffle(self.deck)
        self.discard = list()
        self.hands = {} #hand will be a dict where each player is a key, set up when the game starts
        self.currentPlayerTurn = 0 #an int to represent the curernt turn. 0 if the first player in self.players, and so on
        self.playersSID = {} # dict that stores the player SID THESE NEED TO BE UPDATED TO HANDLE DISCONNECT
        pass

    def addPlayer(self, player, sid):
        self.players.append(player)
        self.playersSID[player] = sid

    def startGame(self): #star the game by giving all players five cards and setting the turn to 0
        for player in self.players:
            hand = []
            for i in range(5):
                hand.append(self.dealCard())
            self.hands[player] = hand
        self.currentPlayerTurn = 0

    def dealCard(self): #deal a card by popping it from teh deck, return false if there are not enough cards
        if self.deck:
            return self.deck.pop()
        else:
            return False

    def advanceTurnNumber(self): #advance the turn by adding one or going back to zero if everyon has gone
        self.currentPlayerTurn += 1
        if self.currentPlayerTurn == len(self.players):
            self.currentPlayerTurn = 0

    def getState(self): #generate a dictionary which is the current state of the game, for now just each players hands
        return {'hands': self.hands, 'sids': self.playersSID, 'players': self.players}


# class Card:
#     def __init__(self, name, cardType: CardType, description = None, biome = None, tier = None, points = None, eats = None, eatenBy = None): #the name and type are required, the rest should be provided as given on the card, the None is there so they are optional, but please make sure they are all there or ERRORS. Description is what the factor or biom does
#         #eats will be as strings right now that are equal to the name (this is not the best, would be better if it were card, but that woudl require us to set them later probably)
#         #Biome and tier should both by lists
#         self.name = name
#         self.type = cardType
#         if self.type == CardType.Factor:
#             self.description = description
#         elif self.type == CardType.Biome:
#             self.biome = biome[0]
#             self.description = description
#         else:
#             self.biome = biome
#             self.tier = tier
#             self.points = points
#             self.eats = eats
#             self.eatenBy = eatenBy

#     def __eq__(self, other): #to allow easy comparison of cards with ==
#         if type(self) != type(other):
#             return False
#         if self.name == other.name:
#             return True
#         else:
#             return False

#     @classmethod
#     def buildDeck(cls): #returns a list of cards in the deck
#         deck = []
#         deck.append(Card("Desert Biome", CardType.Biome, description="Healthy Biome: No card can interact with any cards in this biome", biome=Biome.Desert))
#         deck.append(Card("Cactus", CardType.Creature, biome=[Biome.Desert], tier=Tier.Producer, points=0.25, eatenBy=["WHOOPS"]))
#         return deck