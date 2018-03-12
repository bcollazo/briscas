import enum
import random
import json


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

    def to_dict(self):
        return {
            'number': self.number,
            'suite': self.suite.name,
        }

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

    @staticmethod
    def score(pile):
        return sum([c.points() for c in pile])

    def __init__(self, player1, player2, verbose=False):
        self.verbose = verbose
        self.deck = Deck()
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.plays = []  # list of maps. e.a. map has player1, player2, and commander
        self.life_card = self.deck.peek_last_card()  # for recording

    def _deal(self):
        cards = [self.deck.pop() for i in xrange(6)]
        self.player1.init([cards[0], cards[2], cards[4]])
        self.player2.init([cards[1], cards[3], cards[5]])

    def _print(self, message):
        if self.verbose:
            print(message)

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
        self._print('Life Card: ' + str(life_card))
        while self.player1.has_cards() or self.player2.has_cards():
            self._print("===== Turn: ")
            c_play = commander.play(life_card)
            self._print('%s: %s' % (commander.name, c_play))
            f_play = follower.play(life_card, thrown=c_play)
            self._print('%s: %s' % (follower.name, f_play))
            self.log_play(commander, c_play, follower, f_play)

            if Game.is_better(c_play, f_play, life_card):
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
        self._print('%s points: %d' % (self.player1.name, p1_score))
        self._print('%s points: %d' % (self.player2.name, p2_score))

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
            'winner': self.winner.name,
            'plays': self.plays,
            'life_suite': self.life_card.suite.name
        }
        return json.dumps(data)


class Player:
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

    def play(self, life_card, thrown=None):
        raise Exception('Not yet implemented!')


class HumanPlayer(Player):
    def play(self, life_card, thrown=None):
        print('Hand: ' + str(self.hand))
        playable = [str(i) for i in xrange(len(self.hand))]
        prompt = 'Choose (%s) >>> ' % (', '.join(playable))
        i = raw_input(prompt)
        while i not in playable and i != 'exit':
            i = raw_input(prompt)
        if i == 'exit':
            exit()
        return self.hand.pop(int(i))


class RandomPlayer(Player):
    def play(self, life_card, thrown=None):
        i = random.randint(0, len(self.hand) - 1)
        return self.hand.pop(i)


class LocalPlayer(Player):
    pass


class SmartPlayer(Player):
    pass
