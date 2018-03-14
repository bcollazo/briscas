from briscas.models.core import Game
from briscas.models.players import (
    HumanPlayer, RandomPlayer, LocalPlayer, SmartPlayer, KNNPlayer
)
from briscas.util import ask_for_input


def choose_player(name):
    i = ask_for_input('Choose %s >>> ' % name, [str(i) for i in range(5)])
    return {
        '0': lambda: HumanPlayer(name),
        '1': lambda: RandomPlayer(name),
        '2': lambda: LocalPlayer(name),
        '3': lambda: SmartPlayer(name),
        '4': lambda: KNNPlayer(name, 10),
    }[i]()


print('===== Players')
print('0. Human Player')
print('1. Random Player')
print('2. Local Player')
print('3. Smart Player')
print('4. KNN Player')
p1 = choose_player('P1')
p2 = choose_player('P2')

# Start game.
game = Game(p1, p2, verbose=True)
game.play()
