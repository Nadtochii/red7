import collections
from typing import List

from card import Card


class Score:

    def __init__(self, score: int, high: Card):
        self.score = score
        self.high = high


def red(cards: List[Card]) -> (int, Card):
    """Highest card"""
    high = Card(None, 0, 0)
    for c in cards:
        if (c.number > high.number) or (c.number == high.number and c.color > high.color):
            high = c

    return high.number, high


def orange(cards: List[Card]) -> (int, Card):
    """Cards of one number"""
    cards_counter = collections.Counter([c.number for c in cards])
    score = max(cards_counter.values())

    high = Card(None, number=max([k for k, v in cards_counter if v == score]), color=0)

    for c in cards:
        if c.number == high.number and c.color > high.color:
            high = c
    return score, high


def yellow(cards: List[Card]) -> (int, Card):
    """Cards of one color"""
    cards_counter = collections.Counter([c.color for c in cards])
    score = max(cards_counter.values())

    high = Card(None, number=0, color=max([k for k, v in cards_counter if v == score]))

    for c in cards:
        if c.color == high.color and c.number > high.number:
            high = c
    return score, high


def green(cards: List[Card]) -> (int, Card):
    """Most even cards"""
    score = 0
    for c in cards:
        if c.number % 2 == 0:
            score += 1
        else:
            cards.remove(c)

    high = Card(None, number=0, color=0)

    for c in cards:
        if (c.number > high.number) or (c.number == high.number and c.color > high.color):
            high = c

    return score, high


def blue(cards: List[Card]) -> (int, Card):
    """Cards of all different colors"""
    score = len(set(c.color for c in cards))

    high = Card(None, number=0, color=0)
    for c in cards:
        if (c.number > high.number) or (c.number == high.number and c.color > high.color):
            high = c

    return score, high


def indigo(cards: List[Card]) -> (int, Card):
    """Cards that form a run"""
    run_length = [1]
    cards.sort(key=lambda x: x.number)

    current_number = cards[0].number
    for i in range(1, len(cards)):
        if cards[i].number == current_number + 1:
            run_length.append(run_length[-1] + 1)
        else:
            run_length.append(1)
        current_number = cards[i].number

    score = max(run_length)
    high = cards[run_length.index(score)]

    return score, high


def violet(cards: List[Card]) -> (int, Card):
    """Most cards below 4"""
    score = 0
    for c in cards:
        if c.number < 4:
            score += 1
        else:
            cards.remove(c)

    high = Card(None, number=0, color=0)

    for c in cards:
        if (c.number > high.number) or (c.number == high.number and c.color > high.color):
            high = c

    return score, high


score_handlers = {
    7: red,
    6: orange,
    5: yellow,
    4: green,
    3: blue,
    2: indigo,
    1: violet,
}