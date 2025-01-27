import socket
import threading
from config import *
from color import *
import os

os.system('cls||clear')

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
servers = []

# Sending Messages To All Connected Clients
def broadcast(message):
    print("BC:", clients, message)
    for client in clients:
        client.send(message)
        
    #for client in servers:
        #ssd = SCHOOL + ":" + "" + message
        #ssd = ssd.encode('utf-8')
        #client.send(ssd)
        
        
def close():
    server.close()
    

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            print("Received", message)
            
            ## CETTE FONCTION EST BUGGER. DES QUE L'ON CALL CLIENT  OU CLIENT.RADRR, LE CLIENT CRASH
            # Aider moi svp
            if client in clients:
                
                position = clients.index(client)
                name = nickname[position]
                print("DEBUG", position, name, message)
                broadcast(name + " : " + message)
                
            elif client in servers:
                print("DNS")
            
        except Exception as e:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            print(color.r + f'{nickname} left due to', e + color.k)
            nicknames.remove(nickname)
            break
        
# Receiving / Listening Function
def receive():
    print(color.g + "Server Started" + color.k)
    while True:
        # Accept Connection
        client, address = server.accept()
        print(color.g + "Connected with {}".format(str(address)) + color.k)

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
