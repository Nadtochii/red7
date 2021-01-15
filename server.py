import json
import random
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

connected = []
player_id_count = 0
new_game_id = 1

colors = ['R', 'O', 'Y', 'G', 'B', 'I', 'V']
numbers = [i for i in range(1, 8)]
deck = [{'color': c, 'number': n} for c, n in zip(colors, numbers)]
random.shuffle(deck)


def send(client, data):
    client.send(str.encode(json.dumps(data)))


class Player:
    def __init__(self, player_id, conn):
        self.id = player_id
        self.conn = conn
        self.hand = None
        self.deck = None


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.players = []

    def join_game(self, player) -> None:
        self.players.append(player)

    def get_players(self):
        return len(self.players)


games: dict[int, Game] = {}


def threaded_client(conn, player_id):
    global new_game_id
    print(f'player_id {player_id}')
    player = Player(player_id, conn)
    connected.append(conn)
    send(conn, {'msg': 'lobby', 'player_id': player_id, 'game_ids': list(games.keys())})

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                data = json.loads(data)
                msg = data['msg']

                if msg == "create":
                    new_game = Game(new_game_id)
                    games[new_game_id] = new_game
                    print(f'Create game {new_game_id}')
                    data = {'msg': 'lobby', 'game_ids': list(games.keys())}
                    for c in connected:
                        send(c, data)
                    new_game_id += 1

                if msg == "join":
                    game_id = int(data['game_id'])
                    game = games.get(game_id)
                    if not game:
                        print(f"Game {data} does not exist")
                    else:
                        if game.get_players() >= 4:
                            print('full room')
                        else:
                            print(f'Try to connect to game {game_id}')
                            for p in game.players:
                                data = {'msg': 'new player', 'game': game_id, 'new_player': player.id}
                                send(p.conn, data)

                            games[game_id].join_game(player)
                            player_ids = [p.id for p in games[game_id].players]
                            data = {'msg': 'join', 'players': player_ids}
                            send(conn, data)

                if msg == 'play':
                    game_id = int(data['game_id'])
                    game = games.get(game_id)
                    if not game:
                        print(f'Game error: {game_id}')
                    else:
                        n = 0
                        for p in game.players:
                            p.hand = deck[n:7]
                            p.deck = deck[n+7]
                            n += 8
                            data = {'msg': 'start cards', 'cards hand': p.hand, 'cards deck': p.deck}
                            send(p.conn, data)

        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    player_id_count += 1
    start_new_thread(threaded_client, (conn, player_id_count))
