import socket
import threading
import time
from config import *
import os
from color import color

# Choosing Nickname
print(PSEUDO)
nickname = PSEUDO

os.system('cls||clear')

# Connecting To Server
is_connected = False
while is_connected != True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        is_connected = True
        print(color.g + f"Connected to ({IP}, {PORT})!" + color.k)
    except OSError:
        print(color.r + f"Can't connect to ({IP}, {PORT})" + color.k)
        client.close()
        time.sleep(3)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            if message != None and message != "":
                print(message)
        except Exception as e:
            # Close Connection When Error
            print(color.r + "An error occured:", e + color.k)
            client.close()
            break
        
# Sending Messages To Server
def write():
    while True:
        message = '{}'.format(input(''))
        client.send(message.encode('utf-8'))
        
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
