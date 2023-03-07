import pygame
import copy
from operator import attrgetter

from blokus.constants import SQUARE_SIZE, VLIGHTGRAY, WHITE, SILVER, BLUE, YELLOW, RED, GREEN, BLACKDOTE
from blokus.shape import *

class Board:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board =  [[0] * col for i in range(row)] # empty board
        self.selected_piece = None
        self.mark_moves = [[0] * col for i in range(row)]

    # Draw the actual state of the board with pieces
    # Takes an array that contains numbers 0-4 that imply what is the colour of each square
    def draw_board(self, win):
        win.fill(VLIGHTGRAY)
        count1 = 0
        for i in self.board:
            count2 = 0
            for j in i:
                if j == 0:
                    pygame.draw.rect(win, WHITE, (550+count2*SQUARE_SIZE, 200+count1*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif j == 1:
                    pygame.draw.rect(win, BLUE, (550+count2*SQUARE_SIZE, 200+count1*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif j == 2:
                    pygame.draw.rect(win, YELLOW, (550+count2*SQUARE_SIZE, 200+count1*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif j == 3:
                    pygame.draw.rect(win, RED, (550+count2*SQUARE_SIZE, 200+count1*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif j == 4:
                    pygame.draw.rect(win, GREEN, (550+count2*SQUARE_SIZE, 200+count1*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                count2 = count2 + 1
            count1 = count1 + 1
        for row in range(self.row*SQUARE_SIZE+1):
            for col in range(self.col*SQUARE_SIZE+1):
                if row%25 == 0 or col%25 == 0:
                    pygame.draw.rect(win, SILVER, (550+col, 200+row, 1, 1))

    # Draw a dote in the square where one can place their currently marked shape
    def draw_possible_moves(self, win):
        count1 = 0
        for i in self.mark_moves:
            count2 = 0
            for j in i:
                if j == 1:
                    win.blit(BLACKDOTE, (559.5+count2*SQUARE_SIZE, 209.5+count1*SQUARE_SIZE))
                count2 = count2 + 1
            count1 = count1 + 1


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

    # are any same colour points adjacent? (Used for sides)
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

    def add_corners_and_influence(self, player, corners):
        corners_set = player.corners
        influence_set = player.influence
        influence_candidate = set()
        for corner in corners:
            if self.in_bounds(corner) and self.not_occupied(corner) and self.adj_corner(corner, player):
                    corners_set.add(corner)
                    x = corner[0]
                    y = corner[1]
                    influence_candidate.add((x-2, y))
                    influence_candidate.add((x-1, y))
                    influence_candidate.add((x-2, y+1))
                    influence_candidate.add((x-1, y+1))
                    influence_candidate.add((x, y+1))
                    influence_candidate.add((x+1, y+1))
                    influence_candidate.add((x+2, y+1))
                    influence_candidate.add((x-1, y+2))
                    influence_candidate.add((x, y+2))
                    influence_candidate.add((x+1, y+2))
                    influence_candidate.add((x-2, y-1))
                    influence_candidate.add((x-1, y-1))
                    influence_candidate.add((x, y-1))
                    influence_candidate.add((x+1, y-1))
                    influence_candidate.add((x+2, y-1))
                    influence_candidate.add((x+1, y))
                    influence_candidate.add((x+2, y))
                    influence_candidate.add((x-1, y-2))
                    influence_candidate.add((x, y-2))
                    influence_candidate.add((x+1, y-2))
                    for candidate in influence_candidate:
                        if self.in_bounds(candidate) and self.not_occupied(candidate) and self.adj_corner(candidate, player):
                            influence_set.add(candidate)
                    influence_candidate.clear()
        player.corners = corners_set
        player.influence = influence_set

    # Filter influence set after placing a piece
    def filter_influence(self, player):
        influence_set = player.influence.copy()
        for influence in player.influence:
            if not self.not_occupied(influence):
                influence_set.remove(influence)
            elif not self.adj_corner(influence, player):
                influence_set.remove(influence)
        player.influence = influence_set.copy()

    # Filter influence set for all players
    def all_filter_influence(self, blokus):
        for player in blokus.players:
            self.filter_influence(player)

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
        else:
            for pm in shape.points:
                if pm == next(iter(player.corners)):
                    return(True)
        return(False)

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

    # Update the number of possible moves with resepect to the selected piece
    def update_possible_moves(self, player, position):
        if len(player.pieces) <= position or len(player.pieces) == 0:
            position = -1
        else:
            shape = player.pieces[position]
        if position != -1:
            self.possible_moves(shape, player)
        else:
            self.mark_moves = [[0] * self.col for i in range(self.row)]

    # Update the total number of possible moves for a player
    def num_of_possible_moves(self, player):
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

    # Update the total number of possible moves for ALL players
    def count_possible_moves_all(self, blokus):
        for player in blokus.players:
            self.num_of_possible_moves(player)

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

    ############# BAD STRATEGY - Long time to compute
    # Return the ID of piece and it's rotation that maximises possible moves
    def maximise_moves(self, player):
        copyBoardObj = copy.deepcopy(self)
        saveIdPieces = Shape()
        saveIdPoints = set()
        save_score = 0
        setOfPieces = self.valid_pieces(player)
        tempIdPc = Shape()
        player1 = copy.deepcopy(player)
        for x in setOfPieces:
            tempIdPc = x
            setOfPoints = self.valid_points(x, player)
            tempIdPt = set()
            for y in setOfPoints:
                tempIdPt = y
                copyBoardObj = copy.deepcopy(self)
                fake_corner_array = []
                for pt in y:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                player1.remove_piece(player.pieces.index(x))
                copyBoardObj.num_of_possible_moves(player1)
                if player1.possible_moves > save_score:
                    save_score = player1.possible_moves
                    saveIdPieces = tempIdPc
                    saveIdPoints = tempIdPt
                player1 = copy.deepcopy(player)
        return(saveIdPieces, saveIdPoints)


    def max_size(self, blokus, max_size, piece):
        if blokus.round >= 10:
            return True
        elif blokus.round >= 8:
            if(piece.size < max_size-2):
                return False
        elif blokus.round >= 6:
            if(piece.size < max_size-1):
                return False
        else:
            if(piece.size < max_size):
                return False
        return True

    def maximise_moves_largest_piece(self, player, blokus):
        copyBoardObj = copy.deepcopy(self)
        saveIdPieces = Shape()
        saveIdPoints = set()
        save_score = -1
        setOfPieces = self.valid_pieces(player)
        max_attr = max(setOfPieces, key=attrgetter('size'))
        largest_pieces = list(filter(lambda x: self.max_size(blokus, max_attr.size, x), setOfPieces))
        tempIdPc = Shape()
        player1 = copy.deepcopy(player)
        for x in largest_pieces:
            tempIdPc = x
            setOfPoints = self.valid_points(x, player)
            tempIdPt = set()
            for y in setOfPoints:
                tempIdPt = y
                copyBoardObj = copy.deepcopy(self)
                fake_corner_array = []
                for pt in y:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                player1.remove_piece(player.pieces.index(x))
                copyBoardObj.num_of_possible_moves(player1)
                if player1.possible_moves > save_score:
                    save_score = player1.possible_moves
                    saveIdPieces = tempIdPc
                    saveIdPoints = tempIdPt
                player1 = copy.deepcopy(player)
        return(saveIdPieces, saveIdPoints)


    ### !!!!! CHNGE IT - SHOULD FILTER ALL THE CORNERS!!!!!
    def max_min_moves_largest_piece(self, player, blokus):
        copyBoardObj = copy.deepcopy(self)
        saveIdPieces = Shape()
        saveIdPoints = set()
        save_score = -9999
        setOfPieces = self.valid_pieces(player)
        max_attr = max(setOfPieces, key=attrgetter('size'))
        largest_pieces = list(filter(lambda x: self.max_size(blokus, max_attr.size, x), setOfPieces))
        tempIdPc = Shape()
        player1 = copy.deepcopy(player)
        for x in largest_pieces:
            tempIdPc = x
            setOfPoints = self.valid_points(x, player)
            tempIdPt = set()
            for y in setOfPoints:
                tempIdPt = y
                copyBoardObj = copy.deepcopy(self)
                fake_corner_array = []
                for pt in y:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                player1.remove_piece(player.pieces.index(x))
                copyBoardObj.count_possible_moves_all(blokus)
                resultMoves = player1.possible_moves*blokus.num_players/2
                for z in blokus.players:
                    if z != player:
                        resultMoves = resultMoves - z.possible_moves
                if resultMoves > save_score:
                    save_score = resultMoves
                    saveIdPieces = tempIdPc
                    saveIdPoints = tempIdPt
                player1 = copy.deepcopy(player)
        return(saveIdPieces, saveIdPoints)

    def maximise_avail_corners(self, player, blokus):
        copyBoardObj = copy.deepcopy(self)
        saveIdPieces = Shape()
        saveIdPoints = set()
        save_score = -1
        setOfPieces = self.valid_pieces(player)
        tempIdPc = Shape()
        player1 = copy.deepcopy(player)
        for x in setOfPieces:
            tempIdPc = x
            setOfPoints = self.valid_points(x, player)
            tempIdPt = set()
            for y in setOfPoints:
                tempIdPt = y
                copyBoardObj = copy.deepcopy(self)
                fake_corner_array = []
                for pt in y:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                player1.remove_piece(player.pieces.index(x))
                if len(player1.corners) > save_score:
                    save_score = len(player1.corners)
                    saveIdPieces = tempIdPc
                    saveIdPoints = tempIdPt
                player1 = copy.deepcopy(player)
        return(saveIdPieces, saveIdPoints)



    ############## Recursion for 2 players ##############

    def recu_1(self, blokus, temp_score, depth):
        self.count_possible_moves_all(blokus)
        player = blokus.players[blokus.current_player]
        setOfPieces = self.valid_pieces(player)
        blokus.find_winner()
        if blokus.finished or depth <= 0:
            return temp_score
        elif len(setOfPieces) == 0:
            blokus.next_player()
            temp_score -= self.recu_2(blokus, temp_score, depth)
            return temp_score
        set_of_scores_pieces = set()
        set_of_scores_pts = set()
        for piece in setOfPieces:
            setOfPoints = self.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                temp_solution = temp_score
                board_copy = copy.deepcopy(self)
                blokus_copy = copy.deepcopy(blokus)
                player_copy = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in piece_pts:
                    board_copy.board[pt[0]][pt[1]] = player_copy.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                board_copy.add_corners(player_copy, fake_corner_array)
                board_copy.filter_corners(player_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_solution += piece.sizeboard_copy.recu_2(blokus_copy, temp_score + piece.size, depth)
                set_of_scores_pts.add(temp_solution)
            set_of_scores_pieces.add(max(set_of_scores_pts))
            set_of_scores_pts.clear
        return max(set_of_scores_pieces)

    def recu_2(self, blokus, temp_score, depth):
        self.count_possible_moves_all(blokus)
        player = blokus.players[blokus.current_player]
        setOfPieces = self.valid_pieces(player)
        blokus.find_winner()
        if blokus.finished:
            return temp_score
        elif len(setOfPieces) == 0:
            blokus.next_player()
            temp_score += self.recu_1(blokus, temp_score, depth-1)
            return temp_score
        set_of_scores_pieces = set()
        set_of_scores_pts = set()
        for piece in setOfPieces:
            setOfPoints = self.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                temp_solution = temp_score
                board_copy = copy.deepcopy(self)
                blokus_copy = copy.deepcopy(blokus)
                player_copy = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in piece_pts:
                    board_copy.board[pt[0]][pt[1]] = player_copy.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                board_copy.add_corners(player_copy, fake_corner_array)
                board_copy.filter_corners(player_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_solution += board_copy.recu_1(blokus_copy, temp_score - piece.size, depth-1)
                set_of_scores_pts.add(temp_solution)
            set_of_scores_pieces.add(min(set_of_scores_pts))
            set_of_scores_pts.clear
        return min(set_of_scores_pieces)

    # Recu depth excided! Mby try to do depth 3 or 4
    def recu_start(self, blokus, depth):
        self.count_possible_moves_all(blokus)
        player = blokus.players[blokus.current_player]
        setOfPieces = self.valid_pieces(player)
        temp_score = 0
        max_score   = -9999
        max_element = Shape()
        max_points  = frozenset()
        for piece in setOfPieces:
            setOfPoints = self.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                board_copy = copy.deepcopy(self)
                blokus_copy = copy.deepcopy(blokus)
                player_copy = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in piece_pts:
                    board_copy.board[pt[0]][pt[1]] = player_copy.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                board_copy.add_corners(player_copy, fake_corner_array)
                board_copy.filter_corners(player_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_score = board_copy.recu_2(blokus_copy, piece.size, depth)
                if(temp_score > max_score):
                    max_score   = temp_score
                    max_element = piece
                    max_points  = piece_pts
                    print("-- New top value found --")
        return (max_element, max_points)



    ### !!!! I NEED TO PEEEE, MAYBW IT DOESN'T REALLY FILTERS ALL THE INFLUCE AREAS, DOUBLE CHECK IT PLS AND TEST IT
    ############## MAXIMISE INFLUENCE AREA for yourself and MINIMISE FOR THE OPPONENT ##############

    # max min influence area, check it for all the pieces all the points. Decision for present, not future
    def max_min_influence_area(self, player, blokus):
        copyBoardObj = copy.deepcopy(self)
        saveIdPieces = Shape()
        saveIdPoints = set()
        save_score = -9999
        setOfPieces = self.valid_pieces(player)
        max_attr = max(setOfPieces, key=attrgetter('size'))
        largest_pieces = list(filter(lambda x: self.max_size(blokus, max_attr.size, x), setOfPieces))
        tempIdPc = Shape()
        player1 = copy.deepcopy(player)
        for x in largest_pieces:
            tempIdPc = x
            setOfPoints = self.valid_points(x, player)
            tempIdPt = set()
            for y in setOfPoints:
                tempIdPt = y
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(self)
                fake_corner_array = []
                for pt in y:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners_and_influence(player1, fake_corner_array)
                copyBoardObj.all_filter_influence(blokus)
                resultMoves = len(player1.influence)*blokus_copy.num_players/2
                for z in blokus_copy.players:
                    if z != player:
                        resultMoves = resultMoves - len(z.influence)
                if resultMoves > save_score:
                    save_score = resultMoves
                    saveIdPieces = tempIdPc
                    saveIdPoints = tempIdPt
                player1 = copy.deepcopy(player)
        return(saveIdPieces, saveIdPoints)
