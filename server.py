# Script du serveur 

import socket


def send_all(socket, data, liste_clients):
    for addr in liste_clients:
        socket.sendto(data, addr)


def main():
    # On récupère le nom de la machine locale
    host = socket.gethostname()
    # On choisi un port entre 1024 et 65535
    port_recept = 4000
    # port_envoi = 4001

    # On crée le socket utilisant IPv4 et TCP
    s_recept = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # On attche le socket au serveur avec le port pour attendre les messages
    s_recept.bind((host, port_recept))

    liste_clients = set()

    print("Server démarré")
    while True:
        # On attend un message, quand il arrive on récupère aussi l'adresse de l'expéditeur
        data, addr = s_recept.recvfrom(1024)
        # On ajoute le client à la liste
        liste_clients.add(addr)
        print("liste_client", liste_clients)
        # On décode le message
        message = data.decode('utf-8')
        # Affichage du message
        print("Message de " + str(addr), end=' : ')
        print(message)

        # s_recept.sendto(data, addr)
        send_all(s_recept, data, liste_clients)
    c.close()


if __name__ == '__main__':
    main()
