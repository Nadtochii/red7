import collections
from typing import List

from card import Card


class Score:

    def __init__(self, score: int, high: Card):
        self.score = score
        self.high = high


def red(cards: List[Card]) -> (int, Card):
    high = Card(None, 0, 0)
    for c in cards:
        if (c.number > high.number) or (c.number == high.number and c.color > high.color):
            high = c

    return high.number, high


def orange(cards: List[Card]) -> (int, Card):
    cards_counter = collections.Counter([c.number for c in cards])
    score = max(cards_counter.values())

    high = Card(None, max([k for k, v in cards_counter if v == score]), 0)

    for c in cards:
        if c.number == high.number and c.color > high.color:
            high.color = c.color
    return score, high


def yellow():
    pass


def green():
    pass


def blue():
    pass


def indigo():
    pass


def violet():
    pass


score_handlers = {
    7: red,
    6: orange,
    5: yellow,
    4: green,
    3: blue,
    2: indigo,
    1: violet,
}