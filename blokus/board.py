import pygame
import copy

from blokus.constants import SQUARE_SIZE

class Board:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board =  [[0] * col for i in range(row)] # empty board
        self.mark_moves = [[0] * col for i in range(row)]
        self.highlight_board = set()


    # Reset, set (create) and draw highlight - user may ask for a clue
    def reset_highlight(self):
        self.highlight_board.clear()

    def set_highlight(self, points):
        for pt in points:
            self.highlight_board.add(pt)

    # Which square on board did we click on
    def where_clicked(self, pos):
        x = pos[0]
        y = pos[1]
        square_chosen = (-1, -1)
        for row in range(self.row):
            for col in range(self.row):
                if x > 550+col*SQUARE_SIZE and y > 200+row*SQUARE_SIZE and x < 550+col*SQUARE_SIZE+SQUARE_SIZE and y < 200+row*SQUARE_SIZE + SQUARE_SIZE:
                    square_chosen = (row, col)
        return(square_chosen)

    # Is the point in bounds of the board
    def in_bounds(self, point):
        if 0 <= point[0] < self.col and 0 <= point[1] < self.row:
                return(True)
        return(False)

    # Check if a piece placement overlap another piece on the board
    def not_occupied(self, point):
        if self.board[point[0]][point[1]] == 0:
            return (True)
        return (False)

    # Are any same colour points adjacent? (Used for sides)
    # True - they are, can't put
    def adjacent(self, side, player):
        if self.board[side[0]][side[1]] == player.id:
            return(True)
        return(False)

    # Check whether the future corner has any adj points of the same id
    # First check if the checked point will be in bounds (corner isn't in the corner of the board)
    # True - doesn't have any
    def adj_corner(self, corner, player):
        to_pass = 4
        if corner[0] == 0:
            to_pass = to_pass - 1
        elif self.board[corner[0] - 1][corner[1]] != player.id:
            to_pass = to_pass - 1
        if corner[1] == 0:
            to_pass = to_pass - 1
        elif self.board[corner[0]][corner[1] - 1] != player.id:
            to_pass = to_pass - 1
        if corner[0] == self.row - 1:
            to_pass = to_pass - 1
        elif self.board[corner[0] + 1][corner[1]] != player.id:
            to_pass = to_pass - 1
        if corner[1] == self.row - 1:
            to_pass = to_pass - 1
        elif self.board[corner[0]][corner[1] + 1] != player.id:
            to_pass = to_pass - 1
        if to_pass == 0:
            return(True)
        else:
            return(False)

    # Add new corners if they are in_bounds, not_occupied and they have
    def add_corners(self, player, corners):
        corners_set = player.corners
        for corner in corners:
            if self.in_bounds(corner) and self.not_occupied(corner) and self.adj_corner(corner, player):
                    corners_set.add(corner)
        player.corners = corners_set


    #### Analysis - update_influence ####
    # len(player.corners)*20
    # Blokus DUO:     42 + 42 * 20 = 882
    # Blokus CLASSIC: 63 + 63 * 20 = 1,323

    # Update influence set after placing a piece
    def update_influence(self, player):
        influence_set = set()
        potential_influence = set()
        for candidate in player.corners:
            x = candidate[0]
            y = candidate[1]
            potential_influence.add((x-2, y))
            potential_influence.add((x-1, y))
            potential_influence.add((x-2, y+1))
            potential_influence.add((x-1, y+1))
            potential_influence.add((x, y+1))
            potential_influence.add((x+1, y+1))
            potential_influence.add((x+2, y+1))
            potential_influence.add((x-1, y+2))
            potential_influence.add((x, y+2))
            potential_influence.add((x+1, y+2))
            potential_influence.add((x-2, y-1))
            potential_influence.add((x-1, y-1))
            potential_influence.add((x, y-1))
            potential_influence.add((x+1, y-1))
            potential_influence.add((x+2, y-1))
            potential_influence.add((x+1, y))
            potential_influence.add((x+2, y))
            potential_influence.add((x-1, y-2))
            potential_influence.add((x, y-2))
            potential_influence.add((x+1, y-2))
        for potential in potential_influence:
            if self.in_bounds(potential) and self.not_occupied(potential):
                influence_set.add(potential)
        player.influence = influence_set


    #### Analysis - all_update_influence ####
    # num_of_players * update_influence
    # Blokus DUO:     2 * 882 = 1,764
    # Blokus CLASSIC: 4 * 1,323 = 5,292

    # Filter influence set for all players
    def all_update_influence(self, blokus):
        for player in blokus.players:
            self.update_influence(player)

    # Some corners are not corners anymore (we used 1 and might have covered some)
    def filter_corners(self, player):
        corners_set = player.corners.copy()
        for corner in player.corners:
            if not self.not_occupied(corner):
                corners_set.remove(corner)
            elif not self.adj_corner(corner, player):
                corners_set.remove(corner)
        player.corners = corners_set.copy()

    # Filter corners for all players
    def all_filter_corners(self, blokus):
        for player in blokus.players:
            self.filter_corners(player)


    # Find the squares where one can place their currently selected piece
    def possible_moves(self, shape, player):
        self.mark_moves = [[0] * self.col for i in range(self.row)]
        for corner in player.corners:
            for pt in shape.points:
                x = corner[0] - pt[0] + shape.points[0][0]
                y = corner[1] - pt[1] + shape.points[0][1]
                shape.move_points((x, y))
                if self.valid_move(shape, player):
                    self.mark_moves[x][y] = 1
                shape.move_points((2, 2))

    # Analysis of count_possible_moves
    # 8 * pieces * corners * piece.points * function(valid_move)
    # Worst case - Impossible, upper boundary with max corners and all pieces available:
    # Blokus DUO (max of 42 corners):     8 * 21 * 42 * 5 * (21 + 21) = 1,481,760
    # Blokus CLASSIC (max of 63 corners): 8 * 21 * 63 * 5 * (21 + 21) = 2,222,640

    # Update the total number of possible moves for a player
    def count_possible_moves(self, player):
        set_of_moves = set()
        for i in range(8):
            for piece in player.pieces:
                for corner in player.corners:
                    for pt in piece.points:
                        x = corner[0] - pt[0] + piece.points[0][0]
                        y = corner[1] - pt[1] + piece.points[0][1]
                        piece.move_points((x, y))
                        if self.valid_move(piece, player):
                            set_of_moves.add(frozenset(piece.points))
                        piece.move_points((2, 2))
            if i == 3:
                player.rotate_all(90)
                player.flip_all()
            else:
                player.rotate_all(90)
        player.flip_all()
        player.possible_moves = len(set_of_moves)


    # Analysis - Blokus DUO: 2,963,520 ; Blokus CLASSIC: 8,890,560
    # Number of players * count_possible_moves
    # Update the total number of possible moves for ALL players
    def count_possible_moves_all(self, blokus):
        for player in blokus.players:
            self.count_possible_moves(player)


    # Analysis of valid_move
    # len(shape.points) + len(shape.sides) + len(shape.corners)
    # Worst Case: 5 + (12 + 4 or 11 + 5) = 21
    # Returns True if the move is valid, False if it's not
    def valid_move(self, shape, player):
        # Are points in the board frame
        # Are points oen board not occupied
        for pt in shape.points:
            if not self.in_bounds(pt) or not self.not_occupied(pt) :
                return(False)
        # Are sides not connected
        for s in shape.sides:
            if self.in_bounds(s):
                if self.adjacent(s, player):
                    return(False)
        # Is there a corner match, exception = move number 1
        if player.score != 0:
            for cor in shape.corners:
                if self.in_bounds(cor):
                    if self.board[cor[0]][cor[1]] == player.id:
                        return (True)
        else: # If one of the points is in the "starting squre" at round 1
            for pm in shape.points:
                if pm == next(iter(player.corners)):
                    return(True)
        return(False)


    # Pieces that we are able to place right now
    def valid_pieces(self, player):
        pieces_set = set()
        for i in range(8):
            for piece in player.pieces:
                for corner in player.corners:
                    for pt in piece.points:
                        x = corner[0] - pt[0] + piece.points[0][0]
                        y = corner[1] - pt[1] + piece.points[0][1]
                        piece.move_points((x, y))
                        if self.valid_move(piece, player):
                            pieces_set.add(piece)
                        piece.move_points((2, 2))
            if i == 3:
                player.rotate_all(90)
                player.flip_all()
            else:
                player.rotate_all(90)
        player.flip_all()
        return (pieces_set)


    # Different ways in which we can place specific shape on the board at the moment
    def valid_points(self, shape, player):
        points_set = set()
        for i in range(8):
            for corner in player.corners:
                for pt in shape.points:
                    x = corner[0] - pt[0] + shape.points[0][0]
                    y = corner[1] - pt[1] + shape.points[0][1]
                    shape.move_points((x, y))
                    if self.valid_move(shape, player):
                        points_set.add(frozenset(shape.points))
                    shape.move_points((2, 2))
            if i == 3:
                player.rotate_all(90)
                player.flip_all()
            else:
                player.rotate_all(90)
        player.flip_all()
        return (points_set)
