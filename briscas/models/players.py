from __future__ import print_function

import random

from briscas.models.core import Game, Suite, Colors
from briscas.util import ask_for_input

NUMBER_ORDERING = [1, 3] + list(range(12, 3, -1)) + [2]


class Player(object):
    def __init__(self, name):
        self.name = name
        self.pile = []

    def init(self, hand):
        self.hand = hand

    def push_to_pile(self, cards):
        self.pile.extend(cards)

    def take_into_hand(self, card):
        self.hand.append(card)

    def has_cards(self):
        return len(self.hand) > 0

    # TODO: Future to include piles
    def play(self, life_card, thrown=None):
        raise Exception('Not yet implemented!')  # pragma: no cover


def b(i, j):
    """Block coordinates"""
    return [(i, j), (i, j+1), (i+1, j), (i+1, j+1)]


CARD_LENGTH = L = 14
CARD_HEIGHT = H = 10
SYMBOL_LENGTH = SL = 2
SYMBOL = {
    Suite.ORO: Colors.YELLOW + '#' + Colors.RESET,
    Suite.BASTON: Colors.GREEN + '#' + Colors.RESET,
    Suite.ESPADA: Colors.BLUE + '#' + Colors.RESET,
    Suite.COPA: Colors.RED + '#' + Colors.RESET,
}
TOP_BOTTOM_BORDER = [' '] + ['-'] * (L - 2) + [' ']
EMPTY_LINE = ['|'] + [' '] * (L - 2) + ['|']
L2 = int(L / 2) - 1  # HALF LENGTH
H2 = int(H / 2) - 1  # HALF HEIGHT
L4 = int(L2 / 2)
H4 = int(H2 / 2)
SYMBOL_LOCATIONS = {
    1: [b(L2, H2)],
    2: [b(L2, H4), b(L2, H2 + H4)],
    3: [b(L2, H4 - 1), b(L2, H2), b(L2, H2 + H4 + 1)],
    4: [b(L4, H4), b(L4, H2 + H4),
        b(L2 + L4, H4), b(L2 + L4, H2 + H4)],
    5: [b(L4, H4), b(L4, H2 + H4),
        b(L2 + L4, H4), b(L2 + L4, H2 + H4),
        b(L2, H2)],
    6: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1)],
    7: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4)],
    8: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4), b(L2, H2 + H4)],
    9: [b(L4, H4 - 1), b(L4, H2), b(L4, H2 + H4 + 1),
        b(L2 + L4, H4 - 1), b(L2 + L4, H2), b(L2 + L4, H2 + H4 + 1),
        b(L2, H4 - 1), b(L2, H2), b(L2, H2 + H4 + 1)],
    10: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1), (L2 - 2, H2), (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 1, H2 - 2), (L2 + 1, H2 - 1), (L2 + 1, H2), (L2 + 1, H2 + 1), (L2 + 1, H2 + 2),
         (L2 + 2, H2 - 2), (L2 + 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2), (L2 + 3, H2 + 1), (L2 + 3, H2 + 2),],
    11: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1), (L2 - 2, H2), (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2), (L2 + 3, H2 + 1), (L2 + 3, H2 + 2),],
    12: [(L2 - 2, H2 - 2), (L2 - 2, H2 - 1), (L2 - 2, H2), (L2 - 2, H2 + 1), (L2 - 2, H2 + 2),
         (L2 + 1, H2 - 2), (L2 + 1, H2), (L2 + 1, H2 + 1), (L2 + 1, H2 + 2),
         (L2 + 2, H2 - 2), (L2 + 2, H2), (L2 + 2, H2 + 2),
         (L2 + 3, H2 - 2), (L2 + 3, H2 - 1), (L2 + 3, H2), (L2 + 3, H2 + 2),],
}
# Flatten blocks.
for i in range(1, 10):
    SYMBOL_LOCATIONS[i] = [t for block in SYMBOL_LOCATIONS[i] for t in block]


class HumanPlayer(Player):
    def __init__(self, name, print_fn=print):
        super(HumanPlayer, self).__init__(name)
        self.print_fn = print_fn

    def print_hand(self, print_fn=print):
        # Create empty matrix
        matrix = []
        matrix.append(TOP_BOTTOM_BORDER * len(self.hand))
        for i in range(H - 2):
            matrix.append(EMPTY_LINE * len(self.hand))
        matrix.append(TOP_BOTTOM_BORDER * len(self.hand))

        # Insert symbols
        o = 0  # offset
        for card in self.hand:
            s = SYMBOL[card.suite]
            matrix[1][o + L - 2] = str(card.number)[-1]
            matrix[H - 2][o + 1] = str(card.number)[0]
            if len(str(card.number)) > 1:  # Then add other digit
                matrix[1][o + L - 3] = str(card.number)[0]
                matrix[H - 2][o + 2] = str(card.number)[1]
            for (i, j) in SYMBOL_LOCATIONS[card.number]:
                matrix[j][o + i] = s
            o += CARD_LENGTH

        # Build into string
        string = '\n'.join([''.join(line) for line in matrix])
        self.print_fn(string)

    def play(self, life_card, thrown=None):
        self.print_hand()
        playable = [str(i + 1) for i in range(len(self.hand))]
        prompt = 'Choose (%s) >>> ' % (', '.join([i for i in playable]))
        i = ask_for_input(prompt, playable)
        return self.hand.pop(int(i) - 1)


class RandomPlayer(Player):
    def play(self, life_card, thrown=None):
        i = random.randint(0, len(self.hand) - 1)
        return self.hand.pop(i)


class LocalPlayer(Player):
    def least_good_index(self, cards, life_card):
        min_index = None
        min_rank = None
        for i, card in enumerate(cards):
            card_rank = 0
            if card.suite == life_card.suite:
                card_rank += 36
            card_rank += (12 - NUMBER_ORDERING.index(card.number))

            if min_rank is None or min_rank > card_rank:
                min_index = i
                min_rank = card_rank
        return min_index

    def play(self, life_card, thrown=None):
        if thrown is None:
            i = self.least_good_index(self.hand, life_card)
            return self.hand.pop(i)

        betters = []
        for i, card in enumerate(self.hand):
            if Game.is_better(card, thrown, life_card):
                betters.append(card)
        if len(betters) == 0:
            i = self.least_good_index(self.hand, life_card)
            return self.hand.pop(i)
        j = self.least_good_index(betters, life_card)
        i = self.hand.index(betters[j])
        return self.hand.pop(i)
