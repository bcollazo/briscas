from models import RandomPlayer, Game

player1 = RandomPlayer('P1')
player2 = RandomPlayer('P2')

game = Game(player1, player2)
game.play()
