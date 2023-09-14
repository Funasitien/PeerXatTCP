# Script du client 

import socket
from threading import Thread


class myThread (Thread):

    def __init__(self, socket, addr):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr

    def run(self):
        self.socket.bind(self.addr)
        while True:
            # On attend un message, quand il arrive on récupère aussi l'adresse de l'expéditeur
            data, addr = self.socket.recvfrom(1024)

            # On décode le message
            message = data.decode('utf-8')
            # Affichage du message
            print("Message de " + str(addr), end=' : ')
            print(message)
        c.close()


def main():
    # On récupère le nom de la machine locale (à remplacer par l'IP locale plus tard)
    host = socket.gethostname()
    # On donne l'IP du serveur (à remplacer par l'IP du serveur distant plus tard)
    host_serveur = socket.gethostname()
    # On choisit le même port que le serveur
    port_serveur = 4000
    # On crée l'adresse
    addr_serveur = (host_serveur, port_serveur)
    # On crée le socket utilisant IPv4 et TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # On choisit un port différent car on est sur la même machine (rien n'empêche de choisir le même que le serveur plus tard)
    port_recept = 4001
    addr_recept = (host, port_recept)
    # On lance un thread pour gérer les messages entrant
    thread = myThread(s, addr_recept)
    thread.start()

    # On demande le message à envoyer
    message = input("-> ")
    while message != 'q':
        # On envoie le message
        s.sendto(message.encode('utf-8'), addr_serveur)
        # On attend un nouveau message
        message = input("-> ")
    s.close()


if __name__ == '__main__':
    main()
