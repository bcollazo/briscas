from __future__ import print_function
from __future__ import absolute_import
import json

from briscas.models import Deck, POINTS
from briscas.players import HumanPlayer
from briscas.util import is_better, hand_string

from six.moves import range


class Game:

    @staticmethod
    def score(pile):
        return sum([c.points() for c in pile])

    def __init__(self, player1, player2, verbose=False, print_fn=print):
        self.verbose = verbose
        self.deck = Deck()
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.plays = []  # list of maps
        self.life_card = self.deck.peek_last_card()  # for recording
        self.print_fn = print_fn

    def _deal(self):
        cards = [self.deck.pop() for i in range(6)]
        self.player1.init([cards[0], cards[2], cards[4]])
        self.player2.init([cards[1], cards[3], cards[5]])

    def _print(self, message):
        if self.verbose:
            self.print_fn(message)

    def log_play(self, commander, c_play, follower, f_play):
        play = {
            commander.name: {
                'hand': [c.to_dict() for c in commander.hand],
                'play': c_play.to_dict()
            },
            follower.name: {
                'hand': [c.to_dict() for c in follower.hand],
                'play': f_play.to_dict()
            },
            'commander': commander.name
        }
        self.plays.append(play)

    def play(self):
        self._deal()

        commander = self.player1
        follower = self.player2
        life_card = self.deck.peek_last_card()
        while self.player1.has_cards() or self.player2.has_cards():
            self._print('\033[2J')
            self._print('%s LIFE CARD: %s %s' % (
                '=' * 11, str(life_card), '=' * 11))
            c_play = commander.play(life_card)
            if not isinstance(commander, HumanPlayer):
                self._print(hand_string([c_play]))
                self._print('\n\n' + '=' * 30)
            f_play = follower.play(life_card, thrown=c_play)
            if not isinstance(commander, HumanPlayer):
                self._print(hand_string([c_play]))
                self._print('\n\n' + '=' * 30)
            self.log_play(commander, c_play, follower, f_play)

            if is_better(c_play, f_play, life_card):
                self._print('%s takes it.' % (commander.name))
                commander.push_to_pile([c_play, f_play])
            else:
                self._print('%s takes it.' % (follower.name))
                follower.push_to_pile([c_play, f_play])
                commander, follower = (follower, commander)

            if self.deck.has_cards():
                commander.take_into_hand(self.deck.pop())
                follower.take_into_hand(self.deck.pop())

        p1_score = Game.score(self.player1.pile)
        p2_score = Game.score(self.player2.pile)
        self._print('%s points: %d [%s]' % (
            self.player1.name, p1_score,
            [c for c in self.player1.pile if c.number in POINTS]))
        self._print('%s points: %d [%s]' % (
            self.player2.name, p2_score,
            [c for c in self.player2.pile if c.number in POINTS]))

        self.set_winner(p1_score, p2_score)
        return self.winner

    def set_winner(self, p1_score, p2_score):
        if p1_score > p2_score:
            self._print('===== %s WINS =====' % (self.player1.name))
            self.winner = self.player1
        elif p1_score == p2_score:
            self._print("Empate!")
        else:
            self._print('===== %s WINS =====' % (self.player2.name))
            self.winner = self.player2

    def to_json(self):
        data = {
            'winner': None if self.winner is None else self.winner.name,
            'plays': self.plays,
            'life_suite': self.life_card.suite.name
        }
        return json.dumps(data)
