import socket
import threading
 
HOST = '0.0.0.0'
PORT = 25631
SERVER = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr)  
 
server.bind(SERVER)
server.listen()
 
Clients =[]
Nicknames =[]
 
def broadcast(message):
    for client in Clients:
        client.send(message)
         
def handle(client):
    while True:
        try:
            message =client.recv(1024)
            print(f'{Nicknames[Clients.index(client)]} says {message}')
            broadcast(message)
             
        except:
            index = Clients.index(client)
            Clients.remove(client)
            client.close()
            nickname =Nicknames[index]
            Nicknames.remove(nickname)
            break
             
def receive():
    while True :
        client ,address = server.accept()
        print(f'Connected with {str(address)} !')
         
        client.send("NICK".encode('utf-8'))
        nickname= client.recv(1024).decode('utf-8')
         
        Nicknames.append(nickname)
        Clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} connected to server\n'.encode("utf-8"))
        client.send("Connected to the server ".encode('utf-8'))
        client.send("".encode('utf-8'))
        thread= threading.Thread(target=handle, args=(client,))
        thread.start()
print('Server running ///')
receive()
        
