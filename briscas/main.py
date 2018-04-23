from __future__ import print_function
from builtins import input

from briscas.game import Game
from briscas.models.players import (
    HumanPlayer, RandomPlayer, LocalPlayer
)
from briscas.util import ask_for_input


def choose_player(name, input_fn=input):
    i = ask_for_input('Choose %s >>> ' % name, [str(i) for i in range(5)],
                      input_fn=input_fn)
    return {
        '0': lambda: HumanPlayer(name),
        '1': lambda: RandomPlayer(name),
        '2': lambda: LocalPlayer(name),
    }[i]()


def main(print_fn=print, input_fn=input):
    print_fn('===== Players')
    print_fn('0. Human Player')
    print_fn('1. Random Player')
    print_fn('2. Local Player')
    p1 = choose_player('P1', input_fn=input_fn)
    p2 = choose_player('P2', input_fn=input_fn)

    game = Game(p1, p2, verbose=True)
    game.play()
