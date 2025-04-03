import socket
import threading
from config import IP, PORT
from color import color

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("Message reçu :", data.decode('utf-8'))
        except Exception as e:
            print("Erreur lors de la réception :", e)
            break

def main():
    # Pour se connecter au serveur, ajustez host et port si besoin
    host = IP
    port = PORT

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except Exception as e:
        print("Connexion impossible :", e)
        return

    # Démarrage d'un thread pour recevoir les messages du serveur
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        message = input("-> ")
        if message.lower() == 'q':
            break
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print("Erreur lors de l'envoi :", e)
            break
    client.close()

if __name__ == "__main__":
    main()
