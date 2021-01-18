import json
import random
from typing import List, Dict

from card import Deck, Card
from score import score_handlers


def send(client, data):
    client.send(str.encode(json.dumps(data)))


class Player:

    def __init__(self, player_id, conn):
        self.id = player_id
        self.conn = conn
        self.hand: List[Card] = []
        self.palette: List[Card] = []


class Game:

    def __init__(self, game_id: str):
        self.id = game_id
        self.players: Dict[int, Player] = {}
        self.canvas = 7
        self.order: List[int] = []
        self.active_player_id: int = None

    def join_game(self, player) -> None:
        self.players[player.id] = player

    def get_players(self):
        return len(self.players)

    def define_leader_id(self) -> int:
        leader = None
        lead_score, lead_high = 0, Card(None, 0, 0)
        for p in self.players.values():
            score, high = score_handlers[self.canvas](p.palette)

            if (score > lead_score) or (score == lead_score and high.number > lead_high.number) or \
                    (score == lead_score and high.number == lead_high.number and high.color > lead_high.color):
                leader = p
                lead_score, lead_high = score, high

        return leader.id


def create_game(body, server):
    print('create game')
    new_game = Game(server.game_id)
    server.games[str(server.game_id)] = new_game

    data = {
        'msg': 'lobby',
        'game_ids': server.get_game_ids()
    }

    for c in server.connections:
        send(c, data)
    server.game_id = str(int(server.game_id) + 1)


def join_game(body, server):
    print('join game')
    game = server.get_game(body['game_id'])
    if game:
        if game.get_players() >= 4:
            send(server.conn, {'msg': 'full room'})
        else:
            for p in game.players:
                data = {'msg': 'new player', 'game': game.id, 'new_player': server.player.id}
                send(p.conn, data)

            server.games[game.id].join_game(server.player)
            player_ids = [p.id for p in server.games[game.id].players]
            data = {'msg': 'join', 'players': player_ids, 'game_id': game.id}
            send(server.conn, data)


def leave_game(body, server):
    game = server.get_game(body['game_id'])
    if game:
        del game.players[server.player.id]
        data = {
            'msg': 'lobby',
            'game_ids': server.get_game_ids()
        }

        send(server.conn, data)
        for p in game.players.values():
            data = {'msg': 'drop', 'game': game.id, 'player': server.player.id}
            send(p.conn, data)


def start_game(body, server):
    print('start game')
    deck = list(Deck().create_deck().values())
    random.shuffle(deck)
    game = server.get_game(body['game_id'])

    if not game:
        return

    n = 0
    players_info = []
    for player_id, p in game.players.items():
        game.order.append(player_id)
        for i in range(n, 7):
            p.hand.append(deck[i])
        p.palette.append(deck[n + 7])
        n += 8

        players_info.append(
            {'player_id': p.id, 'hand': [c.card_id for c in p.hand], 'palette': [c.card_id for c in p.palette]})

    random.shuffle(game.order)
    game.active_player_id = game.define_leader()

    data = {
        'msg': 'play',
        'game_id': game.id,
        'current_player_id': server.player.id,
        'players_info': players_info,
        'active_player_id': game.active_player_id,
        'order': game.order,
    }

    for p in game.players.values():
        send(p.conn, data)


def make_move(body, server):
    print('make move')

    game = server.get_game(body['game_id'])

    if not game:
        return

    to_palette = body.get('to_palette')
    to_canvas = body.get('to_canvas')
    old_canvas = game.canvas

    if to_canvas:
        game.canvas = to_canvas

    if to_palette:
        game.players[server.player.id].pallete.append(to_palette)

    leader_id = game.define_leader()
    if leader_id != server.player.id:
        game.canvas = old_canvas
        if to_palette:
            game.players[server.player.id].palette.remove(to_palette)

        data = {'msg': 'wrong_move'}
        send(server.player.conn, data)
    else:
        game.players[server.player.id].hand.remove(to_palette)

        active_player_id = 0
        if (old_active_player_index := game.order.index(game.active_player_id)) < len(game.order - 1):
            active_player_id = game.order[old_active_player_index + 1]

        players_info = []
        for p in game.players:
            players_info.append(
                {'player_id': p.id, 'hand': [c.card_id for c in p.hand], 'palette': [c.card_id for c in p.palette]})

        for p in game.players:
            data = {
                'msg': 'new_move',
                'game_id': game.id,
                'current_player_id': server.player.id,
                'players_info': players_info,
                'active_player_id': active_player_id,
                'order': game.order,
            }
            send(p.conn, data)


def lose(body, server):
    print('lose')

    game = server.get_game(body['game_id'])

    if not game:
        return

    del game.players[server.player.id]

    if len(game.players) == 1:
        data = {'msg': 'win', 'winner_id': game.players[0].id}
    else:
        data = {'msg': 'lose', 'player_id': server.player.id}

    send(game.players[0].conn, data)


handlers = {
    'create_game': create_game,
    'join_game': join_game,
    'leave_game': leave_game,
    'start_game': start_game,
    'make_move': make_move,
    'lose': lose,
}