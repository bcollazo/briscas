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

        p = LocalPlayer('Bryan')
        self._assert_play_pops_card(p)
