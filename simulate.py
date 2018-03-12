import os
import uuid
from models import RandomPlayer, Game

# Ensure data dir exists
DATA_DIR = 'data'
try:
    os.mkdir(DATA_DIR)
except:
    pass


player1 = RandomPlayer('P1')
player2 = RandomPlayer('P2')
i = 0
while i < 100:
    game = Game(player1, player2)
    game.play()
    line = game.to_json()
    with open(DATA_DIR + '/' + str(uuid.uuid4()), 'a') as f:
        f.write(line)
    i += 1
