import time
import socket
import threading
import os

from config import IP, PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
sock.listen()

msgDict = {}

class ClientClass:
    def __init__(self, clientValue, clientAdress) -> None:
        self.clientValue = clientValue
        self.clientAdress = clientAdress

        self.getNickname()
        threading.Thread(target=self.sendMessages, daemon=True).start()
        self.chatLoop()
        
    def chatLoop(self):
        while True:
            msg = self.getMessages()
            for key in msgDict:
                if key == self.clientAdress:
                    continue
                msgDict[key].append(msg)

    def getNickname(self):
        self.nickname = self.getMessages()
        print("Nickname:", self.nickname)

    def getMessages(self):
        try:
            userMsg = self.clientValue.recv(1024).decode("utf-8")
        except ConnectionError as e:
            self.quit()

        return userMsg

    def sendMessages(self):
        while True:
            index = -1
            for index, msg in enumerate(msgDict[self.clientAdress]):
                encodedMsg = msg.encode("utf-8")
                self.clientValue.send(encodedMsg)

            msgDict[self.clientAdress] = msgDict[self.clientAdress][index+1:]

    def quit(self):
        print(self.clientValue, self.clientAdress, "left")
        del msgDict[self.clientAdress]
        exit(1)

if __name__ == "__main__":
    os.system("clear")
    while True:
        newClient, newClientAdress = sock.accept()    
        threading.Thread(target=ClientClass, args=(newClient, newClientAdress), daemon=True).start()
        msgDict[newClientAdress] = []
