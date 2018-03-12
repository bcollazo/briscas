# Make a game against computer.
from models.core import Game
from models.players import HumanPlayer, RandomPlayer, LocalPlayer, SmartPlayer, KNNPlayer


def choose_player(name):
    print('Choose %s:' % (name))
    print('\t0. Human Player')
    print('\t1. Random Player')
    print('\t2. Local Player')
    print('\t3. Smart Player')
    print('\t4. KNN Player')
    i = raw_input('>>> ')
    while i not in ['0', '1', '2', '3', '4', 'exit']:
        print('Please enter a number from 0 to 4')
        i = raw_input('>>> ')
    if i == 'exit':
        exit()
    return {
        '0': lambda: HumanPlayer(name),
        '1': lambda: RandomPlayer(name),
        '2': lambda: LocalPlayer(name),
        '3': lambda: SmartPlayer(name),
        '4': lambda: KNNPlayer(name, 10),
    }[i]()
p1 = choose_player('P1')
p2 = choose_player('P2')

# Start game.
game = Game(p1, p2, verbose=True)
game.play()
