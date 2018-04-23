from __future__ import print_function
from __future__ import absolute_import
import random

from briscas.util import is_better, ask_for_input, hand_string

from six.moves import range

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


class HumanPlayer(Player):
    def __init__(self, name, print_fn=print):
        super(HumanPlayer, self).__init__(name)
        self.print_fn = print_fn

    def play(self, life_card, thrown=None):
        self.print_fn(hand_string(self.hand))
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
            if is_better(card, thrown, life_card):
                betters.append(card)
        if len(betters) == 0:
            i = self.least_good_index(self.hand, life_card)
            return self.hand.pop(i)
        j = self.least_good_index(betters, life_card)
        i = self.hand.index(betters[j])
        return self.hand.pop(i)
