import socket
import time
from threading import Thread
import os
import sys
from rich.table import Table
from rich import print

table = Table(expand=True)
table.add_column("PeerXat - Messages", justify="left", no_wrap=True)

class myThread (Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            client.send(a.encode("utf-8"))
            # On attend un message, quand il arrive on récupère aussi l'adresse de l'expéditeur
            response = client.recv(1024).decode('utf-8')

            table.add_row(response)
            os.system("clear")
            os.system('cls')
            print(table)
            a = input(">> ")
            client.send(a.encode("utf-8"))
            
        c.close()


is_connected = False
while is_connected != True:
    try:
        client = socket.socket()
        client.connect(('omega.forcehost.net', 25631))
        is_connected = True
    except OSError:
        print("Can't connect")
        client.close()
        time.sleep(3)

thread = myThread()
thread.start()


client.close()
