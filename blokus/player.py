import pygame
import random

from blokus.constants import BLACK, SQUARE_SIZE, VLIGHTGRAY, WHITE, SILVER, BLUE, YELLOW, RED, GREEN, DIMGRAY, LIGHTPINK, DOTE, NEONCARROT
from blokus.shape import *

class Player:

    def __init__(self, id, strategy):
        self.id = id # player's id
        self.pieces = [] # player's unused game piece, list of Shape
        self.corners = set() # current valid corners on board
        self.score = 0 # player's current score
        self.position = -1 # piece chosen
        self.possible_moves = 1 # num of possible_moves
        self.strategy = strategy
        self.influence = set()


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

    def manual_add_corner(self, point):
        corners_set = set()
        corners_set.add(point)
        self.corners = corners_set

    def draw_pieces(self, win):
        #players colour
        colour = WHITE
        if self.id == 1:
            colour = BLUE
        elif self.id == 2:
            colour = YELLOW
        elif self.id == 3:
            colour = RED
        elif self.id == 4:
            colour = GREEN
        size = len(self.pieces)
        count_x = size%4
        count_y = int((size - count_x)/4)
        iteration = count_x
        if count_y > 0:
            iteration = 4
        pos = 0

        #paint as many black squares as there are pieces + paint pieces in them + print a pink dote in the reference point
        for a in range(count_y):
            for b in range(iteration):
                pygame.draw.rect(win, BLACK, (25+b*SQUARE_SIZE*5, 25+a*SQUARE_SIZE*5, SQUARE_SIZE*5, SQUARE_SIZE*5))
                shape = self.pieces[pos]
                for point in shape.points:
                    x = point[0]
                    y = point[1]
                    pygame.draw.rect(win, colour, (25+b*SQUARE_SIZE*5 + y*SQUARE_SIZE, 25+a*SQUARE_SIZE*5 + x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                first = shape.points[0]
                win.blit(DOTE, (32.5+b*SQUARE_SIZE*5 + first[1]*SQUARE_SIZE, 32.5+a*SQUARE_SIZE*5 + first[0]*SQUARE_SIZE))
                pos = pos + 1
        for c in range(count_x):
            pygame.draw.rect(win, BLACK, (25+c*SQUARE_SIZE*5, 25+count_y*SQUARE_SIZE*5, SQUARE_SIZE*5, SQUARE_SIZE*5))
            shape = self.pieces[pos]
            for point in shape.points:
                x = point[0]
                y = point[1]
                pygame.draw.rect(win, colour, (25+c*SQUARE_SIZE*5 + y*SQUARE_SIZE, 25+count_y*SQUARE_SIZE*5 + x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            first = shape.points[0]
            win.blit(DOTE, (32.5+c*SQUARE_SIZE*5 + first[1]*SQUARE_SIZE, 32.5+count_y*SQUARE_SIZE*5 + first[0]*SQUARE_SIZE))

            pos = pos + 1
        # paint the net so you can see the "squares" of pieces
        for row in range(count_y*5*SQUARE_SIZE+1):
            for col in range(iteration*5*SQUARE_SIZE+1):
                if row%25 == 0 or col%25 == 0:
                    pygame.draw.rect(win, DIMGRAY, (25+col, 25+row, 1, 1))
        if count_x != 0:
            for row in range(count_y*5*SQUARE_SIZE, count_y*5*SQUARE_SIZE+5*SQUARE_SIZE+1):
                for col in range(count_x*5*SQUARE_SIZE+1):
                    if row%25 == 0 or col%25 == 0:
                        pygame.draw.rect(win, DIMGRAY, (25+col, 25+row, 1, 1))
        # paint the white frame for each piece
        for row in range(count_y*5*SQUARE_SIZE+1):
            for col in range(iteration*5*SQUARE_SIZE+1):
                if row%(SQUARE_SIZE*5) == 0 or col%(SQUARE_SIZE*5) == 0:
                    pygame.draw.rect(win, LIGHTPINK, (25+col, 25+row, 1.7, 1.7))
        if count_x != 0:
            for row in range(count_y*5*SQUARE_SIZE, count_y*5*SQUARE_SIZE+5*SQUARE_SIZE+1):
                for col in range(count_x*5*SQUARE_SIZE+1):
                    if row%(SQUARE_SIZE*5) == 0 or col%(SQUARE_SIZE*5) == 0:
                        pygame.draw.rect(win, LIGHTPINK, (25+col, 25+row, 1.7, 1.7))

    def mark_piece(self, win, pos):
        x = pos%4
        y = int((pos - x)/4)
        if pos != -1:
            for row in range(y*SQUARE_SIZE*5, y*SQUARE_SIZE*5+5*SQUARE_SIZE+1):
                for col in range(x*SQUARE_SIZE*5, x*SQUARE_SIZE*5+5*SQUARE_SIZE+1):
                    if row%(SQUARE_SIZE*5) == 0 or col%(SQUARE_SIZE*5) == 0:
                        pygame.draw.rect(win, NEONCARROT, (25+col, 25+row, 1.7, 1.7))
        else:
            for row in range(y*SQUARE_SIZE*5, y*SQUARE_SIZE*5+5*SQUARE_SIZE+1):
                for col in range(x*SQUARE_SIZE*5, x*SQUARE_SIZE*5+5*SQUARE_SIZE+1):
                    if row%(SQUARE_SIZE*5) == 0 or col%(SQUARE_SIZE*5) == 0:
                        pygame.draw.rect(win, LIGHTPINK, (25+col, 25+row, 1.7, 1.7))

##########################

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


    def rotate_all(self, deg):
        for piece in self.pieces:
            piece.rotate(deg)

    def flip_all(self):
        for piece in self.pieces:
            piece.flip()

    # returns the id (in array) of a piece that was chosen (clicked)
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

    def where_on_board(self, pos, board):
        x = pos[0]
        y = pos[1]
        square_chosen = (-1, -1)
        for row in range(board.row):
            for col in range(board.row):
                if x > 550+col*SQUARE_SIZE and y > 200+row*SQUARE_SIZE and x < 550+col*SQUARE_SIZE+SQUARE_SIZE and y < 200+row*SQUARE_SIZE + SQUARE_SIZE:
                    square_chosen = (row, col)
        return(square_chosen)
