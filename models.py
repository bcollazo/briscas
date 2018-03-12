# Design:
# - Game: to_json()
# - Player Interface: play
# - Hand
# - Card
# - Deck Singleton.

import enum
import random


class Suite(enum.Enum):
    ORO = 1
    COPA = 2
    ESPADA = 3
    BASTON = 4


POINTS = {1: 11, 3: 10, 12: 4, 11: 3, 10: 2}


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

    def __repr__(self):
        return "<%s, %s>" % (self.number, self.suite)


class Deck:
    def __init__(self):
        self._cards = []
        for s in Suite:
            for n in xrange(1, 13):
                self._cards.append(Card(n, s))
        random.shuffle(self._cards)

    def pop(self):
        return self._cards.pop(0)

    def peek_last_card(self):
        return self._cards[-1]

    def has_cards(self):
        return len(self._cards) > 0


class Game:
    @staticmethod
    def is_better(a, b, life):
        if a.suite == life.suite and b.suite != life.suite:
            return True
        elif a.suite != life.suite and b.suite == life.suite:
            return False
        elif a.suite == b.suite:
            return (
                a.number == 1 or
                (a.number == 3 and b.number != 1) or
                (b.number not in [1, 3] and a.number > b.number)
            )
        else:  # different non-life suites. first card wins.
            return True

    def __init__(self, player1, player2):
        self.deck = Deck()
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        # list of maps. e.a. map has player1, player2, and commander
        self.plays = []

    def _deal(self):
        cards = [self.deck.pop() for i in xrange(6)]
        self.player1.init([cards[0], cards[2], cards[4]])
        self.player2.init([cards[1], cards[3], cards[5]])

    def _print(self):
        print("===== GAME =====")
        # Print Player Hands
        print("Player 1:")
        print(self.player1.hand)
        print("Player 2:")
        print(self.player2.hand)
        # Print Life and turns / cards remaining.
        print("LIFE: " + str(self.deck.peek_last_card()))
        print("PLAYS: " + str(self.plays))

    def play(self):
        self._deal()

        commander = self.player1
        follower = self.player2
        life_card = self.deck.peek_last_card()
        print('Life Card: ' + str(life_card))
        while self.deck.has_cards():
            print("===== Turn: ")
            c_play = commander.play(life_card)
            print(c_play)
            f_play = follower.play(life_card, thrown=c_play)
            print(f_play)

            play = {commander: c_play, follower: f_play, 'commander': commander}
            self.plays.append(play)

            if Game.is_better(c_play, f_play, life_card):
                commander.pile([c_play, f_play])
                # commander stays commander
                print('TOP')
            else:
                follower.pile([c_play, f_play])
                commander, follower = (follower, commander)
                print('BOTTOM')

            commander.take_into_hand(self.deck.pop())
            follower.take_into_hand(self.deck.pop())


class Player:
    def __init__(self):
        self._pile = []

    def init(self, hand):
        self.hand = hand

    def pile(self, cards):
        self._pile.extend(cards)

    def take_into_hand(self, card):
        self.hand.append(card)

    def play(self, life_card, thrown=None):
        raise Exception('Not yet implemented!')


class HumanPlayer(Player):
    def play(self, life_card, thrown=None):
        print('Hand: ' + str(self.hand))
        i = raw_input('Your turn (0, 1, 2) >>> ')
        while i not in ['0', '1', '2', 'exit']:
            print('Bad input')
            i = raw_input('Your turn (0, 1, 2) >>> ')
        if i == 'exit':
            exit()
        return self.hand.pop(int(i))


class RandomPlayer(Player):
    def play(self, life_card, thrown=None):
        i = random.randint(0, 2)
        return self.hand.pop(i)
