import socket
import threading
import pickle
import tkinter as tk
class Server:

    def __init__(self, port, server_ip, my_port, my_server_ip):
        self.input = []
        self.header_length = 128
        self.my_port = my_port
        self.my_server_ip = my_server_ip
        self.my_address = (self.my_server_ip, self.my_port)
        self.port = port
        self.server_ip = server_ip
        self.address = (self.server_ip, self.port)
        self.window = tk.Tk()
        self.test = tk.Label(text = "Enter in text to send:")
        self.test.pack()
        self.entry = tk.Entry(foreground = "yellow", bg = "blue", width = 50)
        self.entry.pack()
        self.entry.bind("<Return>", self.load_input_tk)
        self.s = False
    def print_tk(self, m):
        tk.Label(text = m).pack()
    def load_input_tk(self, event):
        self.s = True
        m = self.entry.get()
        self.print_tk(m)
        self.send(m)
        if m.lower() == "disconnect":
            raise SystemExit(0)
    def send(self, msg):
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = pickle.dumps(msg_length)
        send_length += b' ' *  (self.header_length - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


    def handle_client(self, conn, addr):
        connected = True
        while connected:
            msg_length = pickle.loads(conn.recv(self.header_length))
            if msg_length:
                msg_length = int(msg_length)
                msg = pickle.loads(conn.recv(msg_length))
                if msg.lower() == "disconnect":
                    raise SystemExit(0)
                if msg:
                    self.print_tk(msg)
                    
        conn.close()
    def server_loop(self):
        self.server.bind(self.my_address)
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target = self.handle_client, args = (conn, addr))
            thread.start()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_thread = threading.Thread(target = self.server_loop)
        server_thread.start()
        input()
        self.client.connect(self.address)
        self.window.mainloop()
        

