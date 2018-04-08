import unittest
import random

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

        p = HumanPlayer('Bryan', print_fn=mock.Mock())
        self._assert_play_pops_card(p)

    def test_play_pops_card_with_thrown(self):
        p = LocalPlayer('Bryan')

        # none is thrown
        p.init([Card(4, Suite.ORO), Card(5, Suite.ORO), Card(6, Suite.ORO)])
        card = p.play(Card(2, Suite.ORO))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 4)  # weakest card

        # has no better hand
        p.init([Card(4, Suite.ORO), Card(5, Suite.ORO), Card(6, Suite.ORO)])
        card = p.play(Card(2, Suite.ORO), thrown=Card(3, Suite.ORO))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 4)  # weakest card

        # has better hand
        p.init([Card(4, Suite.ORO), Card(6, Suite.ORO), Card(7, Suite.ORO)])
        card = p.play(Card(1, Suite.ORO), thrown=Card(5, Suite.ORO))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 6)

    # def test_human_print_hand(self):
    #     print_fn = mock.Mock()

    #     p = HumanPlayer('p', print_fn=print_fn)
    #     SUITES = [Suite.BASTON, Suite.ORO, Suite.ESPADA, Suite.COPA]
    #     for j in range(5, 13):
    #         x = random.randint(0, 3)
    #         y = random.randint(0, 3)
    #         z = random.randint(0, 3)
    #         i = random.randint(1, 12)
    #         p.init([Card(i - 1, SUITES[x]), Card(i - 2, SUITES[y]), Card(i, SUITES[z])])
    #         p.print_hand()
    #     self.assertTrue(print_fn.called)
    #     self.assertFalse(True)
