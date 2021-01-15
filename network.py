import json
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.setblocking(False)
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(json.dumps(data)))
        except socket.error as e:
            print(e)

    def receive(self):
        data = self.client.recv(4096).decode()
        return json.loads(data)
