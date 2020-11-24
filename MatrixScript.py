import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests

def GameInfo(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(str(data))



def main():
    addr = "3.139.89.132"
    port = 12345


    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, port))
    start_new_thread(GameInfo, (s, ))
    numGames = int(input("How Many Games? : "))
    getPlayersURL = "https://b3g27lvea5.execute-api.us-east-2.amazonaws.com/default/RetrievePlayerInfo"

    players = requests.get(getPlayersURL)
    playersBody = json.loads(players.content)

    serverInfo = {"players": playersBody['Items']}

    s.send(bytes(json.dumps({'numMatches': numGames}), "utf-8"))
    s.send(bytes(json.dumps(serverInfo), "utf-8"))



    while True:
        time.sleep(0)



main()        