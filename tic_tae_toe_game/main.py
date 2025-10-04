#!/usr/bin/python3
import numpy as np


def create_board():
     """
     This function create the board of the game
     """

     board = np.zeros((3,3), dtype=str)
     return board


game_board = create_board()


def print_board(game_board):
    '''
    This function displays the board
    '''
    for row in game_board:
        print(" | ".join(row))
        print("-" * 9) 

def is_winner():
    pass
    
print_board(game_board)
