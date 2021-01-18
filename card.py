from typing import Dict


class Card:

    def __init__(self, card_id, number: int, color: int):
        self.card_id = card_id
        self.number = number
        self.color = color


class Deck:

    # colors = ['R', 'O', 'Y', 'G', 'B', 'I', 'V']
    colors = [i for i in range(1, 8)]
    numbers = [i for i in range(1, 8)]

    def __init__(self):
        self.deck: Dict[int, Card] = {}

    def create_deck(self):
        id_count = 0
        for n in self.numbers:
            for c in self.colors:
                self.deck[id_count] = Card(card_id=id_count, number=n, color=c)
                id_count += 1

        return self.deck
