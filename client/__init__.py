import socket

class TCPClient:

  def __init__(self, host, port):
    self.host = host
    self.port = port

  def connect(self):  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((self.host, self.port))
    return sock

  def send(self, msg):
    sock = self.connect()
    msg = msg.encode() 
    sock.sendall(msg)
    sock.close()

  def launch(ip, port):
    
    print("Connexion au serveur " + ip + " sur le port " + str(port))
    client = TCPClient(ip, port)

    while True:
      msg = input("Enter message to send: ")
      if msg == 'quit':
        break

      client.send(msg)

