import unittest

from briscas.models.core import Game, Card, Suite, Deck
from briscas.models.players import RandomPlayer

import mock


TEST_CASES = [
    [Card(1, Suite.ORO), Card(3, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(1, Suite.ORO), Card(2, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(1, Suite.ORO), Card(12, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(1, Suite.ORO), Card(2, Suite.COPA), Card(4, Suite.COPA), False],
    [Card(3, Suite.ORO), Card(12, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(3, Suite.ORO), Card(2, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(4, Suite.ORO), Card(2, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(10, Suite.ORO), Card(7, Suite.ORO), Card(4, Suite.ORO), True],
    [Card(10, Suite.ORO), Card(3, Suite.ESPADA), Card(4, Suite.ORO), True],
    [Card(10, Suite.ORO), Card(12, Suite.ESPADA), Card(4, Suite.ORO), True],
    [Card(2, Suite.ORO), Card(5, Suite.COPA), Card(4, Suite.ORO), True],
    [Card(2, Suite.ORO), Card(5, Suite.COPA), Card(4, Suite.ESPADA), True],
    [Card(10, Suite.ORO), Card(7, Suite.COPA), Card(4, Suite.ESPADA), True],
    [Card(10, Suite.ORO), Card(7, Suite.COPA), Card(4, Suite.COPA), False],
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
            Card(15, Suite.ORO)

    def test_points(self):
        self.assertEqual(Card(1, Suite.ORO).points(), 11)
        self.assertEqual(Card(3, Suite.ORO).points(), 10)
        self.assertEqual(Card(2, Suite.ORO).points(), 0)
        self.assertEqual(Card(11, Suite.ORO).points(), 3)

    def test_cases(self):
        for case in TEST_CASES:
            (a, b, life, result) = case
            self.assertEqual(result, Game.is_better(a, b, life))

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


if __name__ == '__main__':
    unittest.main()
