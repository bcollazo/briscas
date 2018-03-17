import random
import os
import json

from briscas.models.core import Game
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
        raise Exception('Not yet implemented!')


class HumanPlayer(Player):
    def play(self, life_card, thrown=None):
        print('Hand: ' + str(self.hand))
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


class SmartPlayer(Player):
    # Uses pile data as well.  To build probabilities.
    pass


# TODO:
class KNNPlayer(Player):
    def __init__(self, name, k, data_dir='data/'):
        super(KNNPlayer, self).__init__(name)
        self.k = k
        # Read games into memory.
        self.games = []
        for file in os.listdir(data_dir):
            with open(data_dir + file, 'rb') as f:
                game = json.loads(f.read())
                self.games.append(game)
        print("Loaded", len(self.games))

    def distance(self, game):
        pass

    def play(self, life_card, thrown=None):
        # Find k closest hands in games won.
        # out of all similar hands in given situation (thrown, life)
        # whats concensus from winners?
        hands = []
        for game in self.games:
            winner = game['winner']
            for play in game['plays']:
                pass
        print(hands, winner)  # TODO:
