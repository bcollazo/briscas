# Make a game against computer.
from models.core import Game
from models.players import HumanPlayer, RandomPlayer, LocalPlayer, SmartPlayer, KNNPlayer

player = HumanPlayer('P1')
# Choose computer player.
print('Choose opponent:')
print('\t1. Random Player')
print('\t2. Local Player')
print('\t3. Smart Player')
print('\t4. KNN Player')
i = raw_input('>>> ')
while i not in ['1', '2', '3', '4', 'exit']:
    print('Please enter a number from 1 to 3')
    i = raw_input('>>> ')
if i == 'exit':
    exit()
computer = {
    '1': lambda: RandomPlayer('P2'),
    '2': lambda: LocalPlayer('P2'),
    '3': lambda: SmartPlayer('P2'),
    '4': lambda: KNNPlayer('P2', 10),
}[i]()

# Start game.
game = Game(player, computer, verbose=True)
game.play()
