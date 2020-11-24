import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests

clients_lock = threading.Lock()

Players = []
def connectionLoop(sock):
    numMatches = 0
    lobbyCount = 0
    numLoops = 0
    while True:
        data, addr = sock.recvfrom(1024)
        data = json.loads(data)
        print(str(data))
        updatePlayerURL = "https://568hf3ns1a.execute-api.us-east-2.amazonaws.com/default/UpdatePlayer" + "/?ELODifference="
        if 'players' in data:
            for count in range(numMatches):
                matchLobby = {'GameID': count + 1, 'players': [], 'PlayerWon' : {}}


                for playerCount in range(3):                    
                    if playerCount + numLoops >= len(data['players']):
                        numLoops = 0
                    matchLobby['players'].append(data['players'].__getitem__(playerCount + numLoops))
                    
                
                
                PlayerWon = random.choice(matchLobby['players'])
                matchLobby['PlayerWon'] = PlayerWon

                for player in matchLobby['players']:
                    if player is PlayerWon:
                        player['ELO'] = str(int(player['ELO']) + 50)
                        requests.get(updatePlayerURL + player['ELO'] + '&PlayerID=' + player['PlayerNames'])
                        PlayerWon = player
                    else:
                        player['ELO'] = str(int(player['ELO']) - 15)
                        requests.get(updatePlayerURL + player['ELO'] + '&PlayerID=' + player['PlayerNames'])
                numLoops += 3
                sock.sendto(bytes(str(matchLobby), "utf-8"), addr)

        else:
            numMatches = data['numMatches']


def main():
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    start_new_thread(connectionLoop, (s,))
    while True:
       time.sleep(1)


if __name__ == '__main__':
   main()