import unittest

from briscas.models.core import Card, Suite
from briscas.models.players import RandomPlayer, HumanPlayer, LocalPlayer

import mock


class PlayersTest(unittest.TestCase):
    def _assert_play_pops_card(self, p):
        p.init([Card(4, Suite.ORO), Card(5, Suite.ORO), Card(6, Suite.ORO)])
        p.play(Card(2, Suite.ORO))
        self.assertEqual(len(p.hand), 2)

    @mock.patch('briscas.models.players.ask_for_input')
    def test_play_pops_card(self, m):
        p = RandomPlayer('Bryan')
        self._assert_play_pops_card(p)

        print_mock = mock.Mock()
        p = HumanPlayer('Bryan', print_fn=print_mock)
        self._assert_play_pops_card(p)

    def test_play_pops_card_with_thrown(self):
        p = LocalPlayer('Bryan')
        p.init([Card(4, Suite.ORO), Card(5, Suite.ORO), Card(6, Suite.ORO)])
        card = p.play(Card(2, Suite.ORO), thrown=Card(3, Suite.ORO))  # has no better hand
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 4)

        p.init([Card(4, Suite.ORO), Card(6, Suite.ORO), Card(7, Suite.ORO)])
        card = p.play(Card(1, Suite.ORO), thrown=Card(5, Suite.ORO))  # has better hand
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 6)
