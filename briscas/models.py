from __future__ import absolute_import
import enum
import random

from six.moves import range

POINTS = {1: 11, 3: 10, 12: 4, 11: 3, 10: 2}


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[01m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    YELLOW = '\033[93m'


class Suite(enum.Enum):
    ORO = 1
    COPA = 2
    ESPADA = 3
    BASTON = 4

    def __str__(self):
        if self == Suite.ORO:
            return Colors.YELLOW + self.name + Colors.RESET
        elif self == Suite.COPA:
            return Colors.RED + self.name + Colors.RESET
        elif self == Suite.ESPADA:
            return Colors.BLUE + self.name + Colors.RESET
        elif self == Suite.BASTON:
            return Colors.GREEN + self.name + Colors.RESET


class Card:
    def __init__(self, number, suite):
        if (suite not in Suite or
                not isinstance(number, int) or
                number < 1 or number > 13):
            raise Exception('Invalid card')
        self.number = number
        self.suite = suite

    def points(self):
        if self.number in POINTS:
            return POINTS[self.number]
        else:
            return 0

    def to_dict(self):
        return {
            'number': self.number,
            'suite': self.suite.name,
        }

    def __repr__(self):
        if self.number in [1, 3]:
            number = Colors.BOLD + str(self.number) + Colors.RESET
        else:
            number = self.number
        return "[%s %s]" % (number, self.suite)


class Deck:
    def __init__(self):
        self._cards = []
        for s in Suite:
            for n in range(1, 13):
                self._cards.append(Card(n, s))
        random.shuffle(self._cards)

    def pop(self):
        return self._cards.pop(0)

    def peek_last_card(self):
        return self._cards[-1]

    def has_cards(self):
        return len(self._cards) > 0
