from __future__ import absolute_import
import unittest

from briscas.models import Card, Suit, Deck
from briscas.players import RandomPlayer
from briscas.game import Game
from briscas.util import is_better

import mock


TEST_CASES = [
    [Card(1, Suit.GOLD), Card(3, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(1, Suit.GOLD), Card(2, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(1, Suit.GOLD), Card(12, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(1, Suit.GOLD), Card(2, Suit.CUP), Card(4, Suit.CUP), False],
    [Card(3, Suit.GOLD), Card(12, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(3, Suit.GOLD), Card(2, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(4, Suit.GOLD), Card(2, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(10, Suit.GOLD), Card(7, Suit.GOLD), Card(4, Suit.GOLD), True],
    [Card(10, Suit.GOLD), Card(3, Suit.SWORD), Card(4, Suit.GOLD), True],
    [Card(10, Suit.GOLD), Card(12, Suit.SWORD), Card(4, Suit.GOLD), True],
    [Card(2, Suit.GOLD), Card(5, Suit.CUP), Card(4, Suit.GOLD), True],
    [Card(2, Suit.GOLD), Card(5, Suit.CUP), Card(4, Suit.SWORD), True],
    [Card(10, Suit.GOLD), Card(7, Suit.CUP), Card(4, Suit.SWORD), True],
    [Card(10, Suit.GOLD), Card(7, Suit.CUP), Card(4, Suit.CUP), False],
]


class ModelTest(unittest.TestCase):

    def test_deck(self):
        d = Deck()
        self.assertEqual(120, Game.score(d._cards))

    def test_deck_methods(self):
        d = Deck()
        card = d.peek_last_card()

        self.assertTrue(d.has_cards())
        while d.has_cards():
            popped = d.pop()

        self.assertEqual(card, popped)

    def test_invalid_card_number(self):
        with self.assertRaises(Exception):
            Card(15, Suit.GOLD)

    def test_points(self):
        self.assertEqual(Card(1, Suit.GOLD).points(), 11)
        self.assertEqual(Card(3, Suit.GOLD).points(), 10)
        self.assertEqual(Card(2, Suit.GOLD).points(), 0)
        self.assertEqual(Card(11, Suit.GOLD).points(), 3)

    def test_cases(self):
        for case in TEST_CASES:
            (a, b, life, result) = case
            self.assertEqual(result, is_better(a, b, life))

    def test_game(self):
        p1 = RandomPlayer('P1')
        p2 = RandomPlayer('P2')
        g = Game(p1, p2)
        g.play()
        self.assertFalse(g.deck.has_cards())

    def test_verbose_game(self):
        p1 = RandomPlayer('P1')
        p2 = RandomPlayer('P2')
        print_mock = mock.Mock()
        g = Game(p1, p2, verbose=True, print_fn=print_mock)
        g.play()
        self.assertFalse(g.deck.has_cards())
        self.assertTrue(print_mock.called)
        self.assertNotEqual(g.to_json(), '')

    def test_set_winner(self):
        p1 = RandomPlayer('P1')
        p2 = RandomPlayer('P2')
        g = Game(p1, p2)

        g.set_winner(60, 60)
        self.assertIsNone(g.winner)

        g.set_winner(61, 59)
        self.assertEqual(g.winner, p1)

        g.set_winner(59, 61)
        self.assertEqual(g.winner, p2)


if __name__ == '__main__':
    unittest.main()
