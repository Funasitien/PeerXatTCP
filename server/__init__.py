import socket
import threading
import time
import os

class TCPServer:
    def __init__(self, name, reachable="on", discoverable="on"):
        self.name = name 
        #self.client_ip = get_hostname() 
        #self.split_ip = list(map(int, self.client_ip[0].split(".")))
        self.peers = {}
        self.discoverable = discoverable
        self.reachable = reachable
    
    def get_port(self):
        port = os.environ.get('PORT')
        if not port:
            os.environ['PORT'] = '50101'
            port = '50101'
    
        self.port = int(port)
    
    def scanner(self):
        threading.Thread(target=self._scanner).start()

    def _scanner(self):
        host_list = self.split_ip
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ping_message = f"ping {self.name} {self.port}".encode()
        for i in range(255):
            host_list[3] = i
            ip = ".".join(map(str, host_list))
            if self.client_ip[0] != ip:
                try:
                    sock.connect((ip, self.port))
                    sock.sendall(ping_message)
                except ConnectionRefusedError:
                    pass
                finally: 
                    sock.close()
            time.sleep(0.05)
    
    
    def run(self):
        TCPServer.get_port(self)
        host = socket.gethostbyname(socket.gethostname())
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, self.port))
        
        print(f"Server listening on {host}:{self.port}")
        
        sock.listen(5)
        
        while True:
            conn, addr = sock.accept()  
            threading.Thread(target=self.handle_connection, args=(conn,addr)).start()
    
    def receiver(self):
        threading.Thread(target=self._receiver).start()

    def _receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", self.port))
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=self._handle_connection, args=(conn,addr)).start()

    def handle_connection(self, conn, addr):
        print(f"Connection from {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            conn.send("back")
    
        conn.close()

    def sender(self, message, ip, port=2236):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        request = message.encode()
        sock.sendall(request)
        sock.close()


if __name__ == '__main__':
    server = TCPServer("Test")
    server.run()
