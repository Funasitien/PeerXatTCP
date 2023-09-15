# PeerXat Launcher. Info @ peerxat.eu.org 

from config import *

def peerxat():
    a = input("Voulez vous lancer le client ou le serveur ? [S/C] ")
    if a == "S" or a == "Serveur":
        from server import TCPServer
        name = input("Comment voulez vous appeler votre serveur [exit pour quitter] ")
    
        if name != "exit":
        
            server = TCPServer("Test")
            server.run()
        
        else:
            peerxat()
    else:
        from client import TCPClient
        TCPClient.launch(IP, PORT)

peerxat()
