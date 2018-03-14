from briscas.models.core import Game
from briscas.models.players import HumanPlayer, RandomPlayer, LocalPlayer, SmartPlayer, KNNPlayer


def choose_player(name):
    print('Choose %s:' % (name))
    print('0. Human Player')
    print('1. Random Player')
    print('2. Local Player')
    print('3. Smart Player')
    print('4. KNN Player')
    i = input('>>> ')
    while i not in [0, 1, 2, 3, 4] and i != exit:
        print('Please enter a number from 0 to 4')
        i = input('>>> ')
    if i == exit:
        exit()
    return {
        0: lambda: HumanPlayer(name),
        1: lambda: RandomPlayer(name),
        2: lambda: LocalPlayer(name),
        3: lambda: SmartPlayer(name),
        4: lambda: KNNPlayer(name, 10),
    }[i]()
p1 = choose_player('P1')
p2 = choose_player('P2')

# Start game.
game = Game(p1, p2, verbose=True)
game.play()
