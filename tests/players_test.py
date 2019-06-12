from __future__ import absolute_import
import unittest

from briscas.models import Card, Suit
from briscas.players import RandomPlayer, HumanPlayer, LocalPlayer

import mock


class PlayersTest(unittest.TestCase):
    def _assert_play_pops_card(self, p):
        p.init([Card(4, Suit.GOLD), Card(5, Suit.GOLD), Card(6, Suit.GOLD)])
        p.play(Card(2, Suit.GOLD))
        self.assertEqual(len(p.hand), 2)

    @mock.patch('briscas.players.ask_for_input')
    def test_play_pops_card(self, m):
        p = RandomPlayer('Bryan')
        self._assert_play_pops_card(p)

        p = HumanPlayer('Bryan', print_fn=mock.Mock())
        self._assert_play_pops_card(p)

    def test_play_pops_card_with_thrown(self):
        p = LocalPlayer('Bryan')

        # none is thrown
        p.init([Card(4, Suit.GOLD), Card(5, Suit.GOLD), Card(6, Suit.GOLD)])
        card = p.play(Card(2, Suit.GOLD))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 4)  # weakest card

        # has no better hand
        p.init([Card(4, Suit.GOLD), Card(5, Suit.GOLD), Card(6, Suit.GOLD)])
        card = p.play(Card(2, Suit.GOLD), thrown=Card(3, Suit.GOLD))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 4)  # weakest card

        # has better hand
        p.init([Card(4, Suit.GOLD), Card(6, Suit.GOLD), Card(7, Suit.GOLD)])
        card = p.play(Card(1, Suit.GOLD), thrown=Card(5, Suit.GOLD))
        self.assertEqual(len(p.hand), 2)
        self.assertEqual(card.number, 6)
