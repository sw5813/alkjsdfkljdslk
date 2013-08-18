from __future__ import division, print_function
from Game import Game
from bots import *
from Player import Player
from Grace import Grace
from Guy import Guy

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
    players = [Freeloader(), Alternator(), FairHunter(), Random(0.8), Player(), MaxRepHunter(), BoundedHunter(0.5,1)]
    game = Game(players)
    game.play_game()
    
    #for i in range(0,input()):
    #	game.play_round()
