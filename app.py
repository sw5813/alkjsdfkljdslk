from __future__ import division, print_function
from Game import Game
from bots import *
from Player import Player
from Grace import Grace
from Test import Test

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
    players = [Grace(), Player(), Freeloader(), Test(), BoundedHunter(0.5,0.8)]
    game = Game(players)
    #game.play_game()
    for i in range(0,input()):
    	game.play_round()
