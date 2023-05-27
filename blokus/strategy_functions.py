import pygame
import copy
from operator import attrgetter

from blokus.result import *
from blokus.shape import *

class Strategy_functions:

    ######################################### STRATEGY HELPING FUNCTIONS #########################################


    # Search for "corridors" and try to place there a piece
    def find_corridors(board, player):
        return_list = []
        corridors   = set()
        # Find "corridors"
        for row in range(board.row-1):
            for col in range(board.col-1):
                if board.board[col][row] == 0 and board.board[col+1][row+1] == 0 and board.board[col+1][row] != 0 and board.board[col][row+1] != 0:
                    corridors.add((col, row))
                    corridors.add((col+1, row+1))
                elif board.board[col][row] != 0 and board.board[col+1][row+1] != 0 and board.board[col+1][row] == 0 and board.board[col][row+1] == 0:
                    corridors.add((col+1, row))
                    corridors.add((col, row+1))
        if len(corridors) == 0:
            return(return_list)
        setOfPieces  = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                for corridor in corridors:
                    if corridor in points:
                        return_list.append(Result(piece, points, piece.size))
        return(return_list)


    # Max moves possible for yourself
    def max_moves(board, player, blokus):
        return_list = []
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(board)
                player1 = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.all_filter_corners(blokus_copy)
                player1.remove_piece(player.pieces.index(piece))
                copyBoardObj.count_possible_moves(player1)
                resultMoves = player1.possible_moves
                return_list.append(Result(piece, points, resultMoves))
        return(return_list)


    # Min moves possible for opponents
    def min_moves(board, player, blokus):
        return_list = []
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(board)
                player1 = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.all_filter_corners(blokus_copy)
                player1.remove_piece(player.pieces.index(piece))
                copyBoardObj.count_possible_moves_all(blokus_copy)
                resultMoves = 300
                for opponent in blokus_copy.players:
                    if opponent != player1:
                        resultMoves = resultMoves - opponent.possible_moves
                return_list.append(Result(piece, points, resultMoves))
        return(return_list)


    #### Analysis - Max_min_moves ####
    # setOfPieces(max 21) * setOfPoints(max 8 rotated/flipped per each corner = 8*len(corners)) *
    # *(piece_size + add_corners + all_filter_corners + count_possible_moves_all + num_of_players)
    # Blokus DUO:     21 * 8 * 42 * (5 + 42 + 2 * 42 + 2,963,520 + 2) = 20,911,535,568 operations
    # Blokus CLASSIC: 21 * 8 * 63 * (5 + 63 + 4 * 63 + 8,890,560 + 4) = 94,101,116,256 operations

    # Max possible moves for you/Min possible for opponents
    def max_min_moves(board, player, blokus):
        return_list = []
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(board)
                player1 = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.all_filter_corners(blokus_copy)
                player1.remove_piece(player.pieces.index(piece))
                copyBoardObj.count_possible_moves_all(blokus_copy)
                resultMoves = player1.possible_moves*blokus_copy.num_players/2
                for opponent in blokus_copy.players:
                    if opponent != player1:
                        resultMoves = resultMoves - opponent.possible_moves
                return_list.append(Result(piece, points, resultMoves))
        return(return_list)


    # Algorithm to maximise the amount of corners available after the move
    def maximise_corners(board, player, blokus):
        return_list  = []
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                player1 = copy.deepcopy(player)
                copyBoardObj = copy.deepcopy(board)
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                player1.remove_piece(player.pieces.index(piece))
                return_list.append(Result(piece, points, len(player1.corners)))
        return(return_list)


    ############## MAXIMISE INFLUENCE AREA for yourself ##############
    # max min influence area, check it for all the pieces all the points. Decision for present, not future
    def max_influence_area(board, player, blokus):
        return_list = []
        setOfPieces = board.valid_pieces(player)
        player1 = copy.deepcopy(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(board)
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.filter_corners(player1)
                copyBoardObj.update_influence(player1)
                resultMoves = len(player1.influence)
                return_list.append(Result(piece, points, resultMoves))
                player1 = copy.deepcopy(player)
        return(return_list)


    #### Analysis - max_min_influence_area ####
    # setOfPieces(max 21) * setOfPoints(max 8 rotated/flipped per each corner = 8*len(corners)) *
    # * (piece_size + add_corners + all_filter_corners + all_update_influence + num_of_players)
    # Blokus DUO:     21 * 8 * 42 * (5 + 42 + 2 * 42 + 1,764 + 2) = 13,385,232 operations
    # Blokus CLASSIC: 21 * 8 * 63 * (5 + 63 + 4 * 63 + 5,292 + 4) = 59,439,744 operations

    ############## MAXIMISE INFLUENCE AREA for yourself and MINIMISE FOR THE OPPONENT ##############
    # max min influence area, check it for all the pieces all the points. Decision for present, not future
    def max_min_influence_area(board, player, blokus):
        return_list = []
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            for points in setOfPoints:
                blokus_copy = copy.deepcopy(blokus)
                copyBoardObj = copy.deepcopy(board)
                player1 = blokus_copy.players[blokus_copy.current_player]
                fake_corner_array = []
                for pt in points:
                    copyBoardObj.board[pt[0]][pt[1]] = player1.id
                    fake_corner_array.append((pt[0]+1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]+1))
                    fake_corner_array.append((pt[0]-1, pt[1]-1))
                    fake_corner_array.append((pt[0]+1, pt[1]-1))
                copyBoardObj.add_corners(player1, fake_corner_array)
                copyBoardObj.all_filter_corners(blokus_copy)
                copyBoardObj.all_update_influence(blokus_copy)
                resultMoves = len(player1.influence)*blokus_copy.num_players/2
                for opponent in blokus_copy.players:
                    if opponent != player:
                        resultMoves = resultMoves - len(opponent.influence)
                return_list.append(Result(piece, points, resultMoves))
                player1 = copy.deepcopy(player)
        return(return_list)


    ####### Find best moves, If one player had infinite moves in a row #######
    def infinite_turns(board, blokus, depth):
        return_list = []
        player      = blokus.players[blokus.current_player]
        setOfPieces = board.valid_pieces(player)
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                board_copy = copy.deepcopy(board)
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
                temp_score = Strategy_functions.infinite_turns_recursion(board_copy, blokus_copy, depth-1, piece.size)
                return_list.append(Result(piece, piece_pts, temp_score))
        return (return_list)

    # Follow up to the function above
    def infinite_turns_recursion(board, blokus, depth, score):
        if depth == 0:
            return score
        player      = blokus.players[blokus.current_player]
        setOfPieces = board.valid_pieces(player)
        max_score   = score
        if len(setOfPieces) != 0:
            temp_score  = score
            max_element = Shape()
            max_points  = frozenset()
            for piece in setOfPieces:
                setOfPoints = board.valid_points(piece, player)
                piece_index = player.pieces.index(piece)
                for piece_pts in setOfPoints:
                    board_copy = copy.deepcopy(board)
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
                    temp_score += Strategy_functions.infinite_turns_recursion(board_copy, blokus_copy, depth-1, piece.size)
                    if(temp_score > max_score):
                        max_score = temp_score
                    temp_score = score
        return (max_score)


    ############## Optimal finish for 2 players ##############
    # Optimal finish for last moves in 2 players game
    def optimal_finish(board, blokus, depth):
        player      = blokus.players[blokus.current_player]
        setOfPieces = board.valid_pieces(player)
        temp_score  = 0
        max_score   = -9999
        max_element = Shape()
        max_points  = frozenset()
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                board_copy  = copy.deepcopy(board)
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
                board_copy.all_filter_corners(blokus_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_score = Strategy_functions.optimal_player_2(board_copy, blokus_copy, piece.size, depth)
                if(temp_score > max_score):
                    max_score   = temp_score
                    max_element = piece
                    max_points  = piece_pts
        return (max_element, max_points)

    # Optimal Finish - Player's turn
    def optimal_player_1(board, blokus, temp_score, depth):
        player = blokus.players[blokus.current_player]
        setOfPieces = board.valid_pieces(player)
        if depth <= 0:
            return temp_score
        elif len(setOfPieces) == 0:
            blokus.next_player()
            temp_score -= Strategy_functions.optimal_player_2(board, blokus, temp_score, depth)
            return temp_score
        set_of_scores_pieces = set()
        set_of_scores_pts = set()
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                temp_solution = temp_score
                board_copy = copy.deepcopy(board)
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
                board_copy.all_filter_corners(blokus_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_solution += Strategy_functions.optimal_player_2(board_copy, blokus_copy, temp_score + piece.size, depth)
                set_of_scores_pts.add(temp_solution)
            set_of_scores_pieces.add(max(set_of_scores_pts))
            set_of_scores_pts.clear
        return max(set_of_scores_pieces)

    # Optimal Finish - Opponent's turn
    def optimal_player_2(board, blokus, temp_score, depth):
        player = blokus.players[blokus.current_player]
        setOfPieces = board.valid_pieces(player)
        if len(setOfPieces) == 0:
            blokus.next_player()
            temp_score += Strategy_functions.optimal_player_1(board, blokus, temp_score, depth-1)
            return temp_score
        set_of_scores_pieces = set()
        set_of_scores_pts = set()
        for piece in setOfPieces:
            setOfPoints = board.valid_points(piece, player)
            piece_index = player.pieces.index(piece)
            for piece_pts in setOfPoints:
                temp_solution = temp_score
                board_copy = copy.deepcopy(board)
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
                board_copy.all_filter_corners(blokus_copy)
                player_copy.remove_piece(piece_index)
                blokus_copy.next_player()
                temp_solution += Strategy_functions.optimal_player_1(board_copy, blokus_copy, temp_score - piece.size, depth-1)
                set_of_scores_pts.add(temp_solution)
            set_of_scores_pieces.add(min(set_of_scores_pts))
            set_of_scores_pts.clear
        return min(set_of_scores_pieces)
