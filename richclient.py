import socket
import threading
from config import IP, PORT, PSEUDO, COULEUR
from data import ASCII_ART
from color import color
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.progress import track
from rich.prompt import Prompt
from os import system

console = Console()
chat = Table(show_header=True, header_style="bold cyan")
chat.add_column("Messages", style="dim", justify="center")

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            chat.add_row(data.decode('utf-8'))
            system("clear")
            console.print(ASCII_ART, justify="center", style="bold cyan")
            console.print(chat, justify="center")
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

    # Initialization du fancy fancy GUI
    system("clear")
    console.print(ASCII_ART, justify="center", style="bold cyan")

    # Démarrage d'un thread pour recevoir les messages du serveur
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    uname = getattr(color, COULEUR, color.reset) + PSEUDO + color.reset
    client.send(uname.encode('utf-8'))
    console.print(chat, justify="center")

    while True:
        message = Prompt.ask("Enter your name")
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
