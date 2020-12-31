from flask import Flask, redirect, url_for, abort, request, json
from flask_socketio import SocketIO, join_room, leave_room, emit
import os
import random
import string
from game import Game
from flask_cors import CORS

#use socketio rooms for each game

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
CORS(app)
socketio = SocketIO(app) #set up the flask app to use the socket io library

#gamesId = set() #a set that will contain the ids of all active games
games = {}
cards = None

@app.before_first_request
def startup():
    global cards    
    cards = json.load(open(os.path.abspath("./public/cards.json"))) #this is going to be problamatic

@app.route('/api/test')
def test():
    print(cards) 

@app.route('/api/games/') #the rendering for the home screen, just renders it and rwith a list of all active games
def getGame():
    return {"games": list(games.keys())}

@app.route('/api/newGame/') #the link that is give to create a ne games
def newGame():
    newGameId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while newGameId in games.keys():
        newGameId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) #generate a new game idea and keep doing that until it is unique (not in teh gamesId set)
    games[newGameId] = Game(newGameId) #adds that ID to games id
    return {"gameId" : newGameId} #redirects to that game page
 
@app.route('/api/game/<gameID>') #loads a game give a specefic game id
def load_game(gameID):
    print("a")
    if gameID in games.keys():
        return {"valid": True, "gameId": gameID, "cards": cards}
        #render_template('game.html', gameID=gameID, cards=cards)
    else:
        return {"valid": False}
        #abort(404) #if the game is not created, aborts

# def intiateGame(): #may not need
#     #handling of starting game
#     pass

@socketio.on('join') #what to do when a user joins the game
def add_user(data):
    join_room(data['game']) #add the user to the room with their socketid
    inUseGame = games[data['game']]
    if data['player']:
        inUseGame.addPlayer(data['name'], request.sid) #also add the player's name as a variable in the game, there might be a problem with 2 players with the same name
    emit('playerUpdate', {'players': inUseGame.players}, room=data['game']) #have all players update their list
    return "added" #confirmation

@socketio.on('startGame')
def startGame(data): #starts the game by sending the game state to each player, each player recieves their updates and own deck through the SID, however this SID needs to be updated to handle reocnnects
    game = games[data['game']]
    game.startGame()
    update = game.getState()
    #will want to emit with everyone to send them the game state
    for player in update['players']:
        #print(type(update['sids'][player]))
        emit('handUpdate', {'hand': list(update['hands'][player])}, room=update['sids'][player]) #need to actually fix this to send something reasonable in the json (lk a card id might be best and just have an external json file with all card info and ids for all cards nad just do it all by ID)

if __name__ == "__main__":
    socketio.run(app, debug=True)
