import socket
import threading
from config import IP, PORT

clients = []  # liste des sockets connectées
lock = threading.Lock()  # pour gérer l'accès concurrent à la liste des clients

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            # On n'envoie pas le message au client qui l'a envoyé
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print("Erreur lors de l'envoi à un client :", e)

def handle_client(client_socket, client_address):
    print("Connexion de", client_address)
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break  # déconnexion du client
            print("Message de", client_address, ":", data.decode('utf-8'))
            broadcast(data, client_socket)
        except Exception as e:
            print("Erreur de communication avec", client_address, ":", e)
            break
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()
    print("Déconnexion de", client_address)

def main():
    host = IP
    port = PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # nombre maximal de connexions en attente
    print("Serveur TCP démarré sur {}:{}".format(host, port))
    
    while True:
        client_socket, client_address = server.accept()
        with lock:
            clients.append(client_socket)
        # Démarrage d'un thread pour gérer la connexion du client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
