import unittest
import json
from models import Game, Card, Suite, Deck


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


class Test(unittest.TestCase):

    def test_deck(self):
        d = Deck()
        self.assertEquals(120, Game.score(d._cards))

    def test_serializable(self):
        json.dumps(Card(1, Suite.ORO))
        self.assertTrue(True)

    def test_cases(self):
        for case in TEST_CASES:
            (a, b, life, result) = case
            self.assertEquals(result, Game.is_better(a, b, life))

if __name__ == '__main__':
    unittest.main()
