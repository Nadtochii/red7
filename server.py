import json
import socket
from _thread import start_new_thread

from game import Player, send, handlers


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.games = dict()
        self.player_id = 1
        self.game_id = '1'
        self.player = None
        self.conn = None

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((self.host, self.port))
        except socket.error as e:
            str(e)

        s.listen(1)
        print("Waiting for a connection, Server Started")

        while True:
            self.conn, address = s.accept()
            print("Connected to:", address)
            start_new_thread(threaded_client, (self.conn, self))
            self.player_id += 1

    def get_game_ids(self):
        return list(self.games.keys())

    def get_game(self, game_id):
        try:
            game = self.games[str(game_id)]
        except KeyError:
            print(f"Game {game_id} does not exist")
        else:
            return game


def process_event(message, server):
    try:
        handlers[message['type']](message['body'], server)
    except KeyError:
        pass


def threaded_client(conn, server):
    server.player = Player(server.player_id, conn)
    server.connections.append(conn)

    data = {'msg': 'lobby', 'game_ids': server.get_game_ids()}
    send(conn, data)

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                process_event(json.loads(data), server)
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()


def main():
    server = Server('127.0.0.1', 5555)
    server.start_server()


if __name__ == '__main__':
    main()
