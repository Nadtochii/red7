import uuid


def join_game():
    return 'NEW'


def create_game():
    game_id = str(uuid.uuid4())
    return game_id

