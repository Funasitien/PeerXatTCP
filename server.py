import time
import socket
import threading
import os

from config import IP, PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
sock.listen()

clientDict = {}
msgList = []

class ClientClass:
    def __init__(self, clientValue, clientAdress) -> None:
        self.clientValue = clientValue
        self.clientAdress = clientAdress

    def threadInit(self) -> None:
        write(f"{self.clientAdress} joined")
        self.getNickname()
        self.chatLoop()
        
    def chatLoop(self):
        while True:
            msg = self.getMessages()
            msgList.append(msg)

    def getNickname(self):
        self.nickname = self.getMessages()
        write(f"{self.clientAdress}'s nickname is {self.nickname}")

    def getMessages(self):
        try:
            userMsg = self.clientValue.recv(1024).decode("utf-8")
        except ConnectionError as e:
            self.quit()

        return userMsg

    def quit(self):
        write(f"{self.clientAdress} just quit")
        del clientDict[self.clientAdress]
        exit(1)

def write(msg):
    print(msg)

def sendMessages():
    global msgList
    while True:

        msgToSend = msgList.copy()
        clients = clientDict.copy()
        msgList = msgList[len(msgToSend):]

        for key in clients:
            clientObject = clientDict[key]
            for msg in msgToSend:
                encodedMsg = msg.encode("utf-8")

                try:
                    clientObject.clientValue.send(encodedMsg)
                except BrokenPipeError:
                    clientObject.quit()

if __name__ == "__main__":
    os.system("clear")
    threading.Thread(target=sendMessages, daemon=True).start()
    while True:
        newClient, newClientAdress = sock.accept()    
        clientObject = ClientClass(newClient, newClientAdress)
        clientDict[newClientAdress] = clientObject
        threading.Thread(target=clientObject.threadInit, daemon=True).start()
