import unittest

from briscas.models.core import Card, Suite
from briscas.models.players import RandomPlayer


class PlayersTest(unittest.TestCase):
    def test_play_pops_card(self):
        r = RandomPlayer('Bryan')
        r.init([Card(4, Suite.ORO), Card(5, Suite.ORO), Card(6, Suite.ORO)])
        r.play(Card(2, Suite.ORO))
        self.assertEqual(len(r.hand), 2)
