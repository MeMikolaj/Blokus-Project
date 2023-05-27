import pygame
import random

from blokus.constants import SQUARE_SIZE
from blokus.shape import *

class Player:

    def __init__(self, id, strategy):
        self.id = id # player's id
        self.pieces = [] # player's unused game piece, list of Shape
        self.corners = set() # current valid corners on board
        self.score = 0 # player's current score
        self.position = -1 # piece chosen
        self.possible_moves = 1 # num of possible_moves
        self.strategy = strategy # Strategy player is playing
        self.influence = set() # Set of squares it influences


    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        random.shuffle(pieces)
        self.pieces = pieces

    def add_points(self, piece):
        self.score = self.score + piece.size
        if len(self.pieces) == 1: # If the current piece is the last unused piece
            self.score += 15
            if piece.id == 'I1':
                self.score += 5 # bonus for putting the smallest piece last

    # Remove a player's piece (Shape)
    def remove_piece(self, position):
        self.pieces.pop(position)

    # Add corners manually
    def manual_add_corner(self, point):
        corners_set = set()
        corners_set.add(point)
        self.corners = corners_set

##########################

    # Add all pieces to a player's pieces set (Starting set)
    def add_all_pieces(self):
        a = I1()
        b = I2()
        c = I3()
        d = I4()
        e = I5()
        f = V3()
        g = L4()
        h = Z4()
        i = O4()
        j = L5()
        k = T5()
        l = V5()
        m = N()
        n = Z5()
        o = T4()
        p = P()
        r = W()
        s = U()
        t = F()
        u = X()
        w = Y()
        all_pieces = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w]
        random.shuffle(all_pieces)
        for piece in all_pieces:
            piece.set_points(2,2)
        self.pieces = all_pieces

    # Rotate all the pieces
    def rotate_all(self, deg):
        for piece in self.pieces:
            piece.rotate(deg)

    # Flip all the pieces
    def flip_all(self):
        for piece in self.pieces:
            piece.flip()

    # returns the id (in array) of a piece that was chosen (clicked on)
    def which_piece(self, pos):
        x = pos[0]
        y = pos[1]
        piece_chosen = -1
        size = len(self.pieces)
        count_x = size%4
        count_y = int((size - count_x)/4)
        iteration = count_x
        if count_y > 0:
            iteration = 4
        for row in range(count_y):
            for col in range(iteration):
                if x > 25+col*SQUARE_SIZE*5 and y > 25+row*SQUARE_SIZE*5 and x < 25+col*SQUARE_SIZE*5 +SQUARE_SIZE*5 and y < 25+row*SQUARE_SIZE*5 + SQUARE_SIZE*5:
                    piece_chosen = row*4+col
        for col in range(count_x):
            if x > 25+col*SQUARE_SIZE*5 and y> 25+count_y*SQUARE_SIZE*5 and x < 25+col*SQUARE_SIZE*5 +SQUARE_SIZE*5 and y< 25+count_y*SQUARE_SIZE*5 + SQUARE_SIZE*5:
                piece_chosen = count_y*4+col
        return(piece_chosen)
