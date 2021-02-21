import socket
import threading
import pickle

class Server:

    def __init__(self, port, server_ip, my_port, my_server_ip, client, file):
        self.input = []
        self.header_length = 128
        self.my_port = my_port
        self.my_server_ip = my_server_ip
        self.my_address = (self.my_server_ip, self.my_port)
        self.port = port
        self.server_ip = server_ip
        self.address = (self.server_ip, self.port)
        self.c = client
        self.file = file
        
    def send(self, msg):
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = pickle.dumps(msg_length)
        send_length += b' ' *  (self.header_length - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


    def handle_client(self, conn, addr):
        connected = True
        with open(self.file, 'w') as f:
            while connected:
                msg_length = pickle.loads(conn.recv(self.header_length))
                if msg_length:
                    msg_length = int(msg_length)
                    msg = pickle.loads(conn.recv(msg_length))
                    if msg.lower() == "disconnect":
                        connected = False
                    if msg:
                        self.input.append(msg)
                        f.write(str(msg))
        conn.close()
    def server_loop(self):
        self.server.bind(self.my_address)
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target = self.handle_client, args = (conn, addr))
            thread.start()
    def client_loop(self):
        self.client.connect(self.address)
        m = input()
        connected = True
        while connected:
            m = input()
            if m.lower() == "disconnect":
                connected = False
            self.send(m)
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #if (self.c):
        server_thread = threading.Thread(target = self.server_loop)
        server_thread.start()
        input()
        client_thread = threading.Thread(target = self.client_loop)
        client_thread.start()
        

