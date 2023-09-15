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

if __name__ == '__main__':

  client = TCPClient('localhost', 50101)

  while True:
    msg = input("Enter message to send: ")
    if msg == 'quit':
      break

    client.send(msg)
