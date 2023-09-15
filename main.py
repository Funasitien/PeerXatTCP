from config import *

a = input("Voulez vous lancer le client ou le serveur ? [S/C]")
if a == "S" or a == "Serveur":
    print("Serveur")
else:
    from client import TCPClient
    TCPClient.launch(IP, PORT)
    
