# Make a game against computer.
from models import HumanPlayer, RandomPlayer, Game

player = HumanPlayer()
# Choose computer player.
# print('Choose opponent:')
# print('\t1. Random Player')
# print('\t2. Local Player')
# print('\t3. Smart Player')
# i = raw_input('>>> ')
# while i not in ['1', '2', '3', 'exit']:
#     print('Please enter a number from 1 to 3')
#     i = raw_input('>>> ')
# if i == 'exit':
#     exit()
computer = RandomPlayer()

# Start game.
game = Game(player, computer)
game.play()
