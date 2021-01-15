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
player = 0
new_game_id = 0


class Game:
    def __init__(self, game: int, start_player: int, start_conn):
        self.game = game
        self.player_ids = [start_player]

        self.conns = [start_conn]

    def join_game(self, player_id, conn) -> None:
        self.player_ids.append(player_id)
        self.conns.append(conn)

    def get_players(self):
        return self.player_ids


games: dict[int, Game] = {}


def threaded_client(conn, player):
    global new_game_id
    print(f'idCount {player}')
    # conn.send(str.encode(str(player)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                data = json.loads(data)
                msg = data['msg']

                if msg == "create":
                    new_game = Game(new_game_id, player, conn)
                    games[new_game_id] = new_game
                    print(f'Create game {new_game_id}')
                    conn.send(str.encode(json.dumps({'msg': 'new game created', 'game_id': new_game_id, 'player_id': player})))
                    new_game_id += 1

                if msg == "join":
                    game_id = int(data['game_id'])
                    game = games.get(game_id)
                    if game:
                        print(f'Try to connect to game {game_id}')
                        for c in game.conns:
                            c.send(str.encode(json.dumps({'msg': 'join to game', 'game': game_id, 'new_player': player})))
                        games[game_id].join_game(player, conn)
                        conn.send(str.encode(json.dumps({'msg': 'join', 'players': games[game_id].player_ids})))
                    else:
                        print(f"Game {data} does not exist")
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    player -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    player += 1
    start_new_thread(threaded_client, (conn, player))
