from briscas.game import Game
from briscas.models.players import (
    HumanPlayer, RandomPlayer, LocalPlayer
)
from briscas.util import ask_for_input


def choose_player(name):
    i = ask_for_input('Choose %s >>> ' % name, [str(i) for i in range(5)])
    return {
        '0': lambda: HumanPlayer(name),
        '1': lambda: RandomPlayer(name),
        '2': lambda: LocalPlayer(name),
    }[i]()


print('===== Players')
print('0. Human Player')
print('1. Random Player')
print('2. Local Player')
p1 = choose_player('P1')
p2 = choose_player('P2')

# Start game.
game = Game(p1, p2, verbose=True)
game.play()
