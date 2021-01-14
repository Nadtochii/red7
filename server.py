import json
import socket
from _thread import start_new_thread


host = '127.0.0.1'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = {}
idCount = 0
new_game_id = 0


class Game:
    def __init__(self, game: int, player: int):
        self.game = game
        self.player_ids = {player}

    def join_game(self, player_id) -> None:
        self.player_ids.add(player_id)

    def get_players(self):
        return self.player_ids


games: dict[int, Game] = {}


def threaded_client(conn):
    global idCount, new_game_id
    conn.send(str.encode("HELLO"))

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                data = json.loads(data)
                if data['msg'] == "join":
                    try:
                        games[int(data['game_id'])]
                    except KeyError:
                        print(f"Game {data} does not exist")
                    else:
                        games[int(data['game_id'])].join_game(idCount)
                        print(f'connected: {games}')

                if data['msg'] == "create":
                    new_game = Game(new_game_id, idCount)
                    games[new_game_id] = new_game
                    print(f'Create game {new_game_id}')
                    conn.send(str.encode(json.dumps({'msg': 'new game created', 'game_id': new_game_id})))
                    new_game_id += 1
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    start_new_thread(threaded_client, (conn, ))
