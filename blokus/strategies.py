import pygame
import random
from operator import attrgetter

from blokus.strategy_functions import *
from blokus.result import *

class Strategies:

    # Use specific strategy depending on the name
    def play_strategy(blokus, board, strategy_name):
        player = blokus.players[blokus.current_player]
        if player.possible_moves == 0:
            blokus.next_player()
            return(blokus, board)
        else:
            # Call specific strategies, depending on a name
            if strategy_name == "Random":
                Strategies.strategy_random(blokus, board)
            elif strategy_name == "Largest":
                Strategies.strategy_largest(blokus, board)
            elif strategy_name == "Max_moves":
                Strategies.strategy_max_moves(blokus, board)
            elif strategy_name == "Min_moves":
                Strategies.strategy_min_moves(blokus, board)
            elif strategy_name == "Max_min":
                Strategies.strategy_max_min_moves(blokus, board)
            elif strategy_name == "Corners":
                Strategies.strategy_max_corners(blokus, board)
            elif strategy_name == "Corridors":
                Strategies.strategy_corridors(blokus, board)
            elif strategy_name == "Influence":
                Strategies.strategy_max_min_influence(blokus, board)
            elif strategy_name == "Influence +":
                Strategies.strategy_max_influence(blokus, board)
            elif strategy_name == "Hybrid":
                Strategies.strategy_hybrid(blokus, board)
            blokus.find_winner()
        return(blokus, board)

    # Having specific points of a piece that is about to be placed, add it's data to appropriate sets
    def add_and_filter_data(blokus, board, player, piece_points):
        fake_corner_array = []
        for pt in piece_points:
            board.board[pt[0]][pt[1]] = player.id
            fake_corner_array.append((pt[0]+1, pt[1]+1))
            fake_corner_array.append((pt[0]-1, pt[1]+1))
            fake_corner_array.append((pt[0]-1, pt[1]-1))
            fake_corner_array.append((pt[0]+1, pt[1]-1))
        board.add_corners(player, fake_corner_array)
        board.all_filter_corners(blokus)
        board.all_update_influence(blokus)


    ############################################ STRATEGIES ############################################


    # Advanced strategy, combining other strategies depending on the round of the game.
    # Each strategy gives it's preferences that then are summed up and put together in a ranking.
    def strategy_hybrid(blokus, board):
        player = blokus.players[blokus.current_player]
        max_moves_value = 0
        influence_value = 0
        corridors_value = 0
        corners_value   = 0
        infinity_value  = 0
        min_moves_value = 0
        size_value      = 0
        if blokus.num_players == 2:
            if blokus.round <= 4:
                max_moves_value = 1
                influence_value = 3
                corridors_value = 2
                corners_value   = 0.5
                min_moves_value = 2
                size_value      = 3
            elif blokus.round <= 10:
                max_moves_value = 3
                influence_value = 0.5
                corridors_value = 1.5
                corners_value   = 0.5
                min_moves_value = 2
                size_value      = 2
            elif blokus.round <= 13:
                max_moves_value = 2
                influence_value = 0.5
                corridors_value = 1.5
                corners_value   = 0
                min_moves_value = 1
                size_value      = 1
            elif blokus.round <= 16:
                max_moves_value = 2
                influence_value = 0
                corridors_value = 0.5
                corners_value   = 0
                min_moves_value = 3
                size_value      = 1
            else:
                Strategies.strategy_optimal_finish(blokus, board, 21-blokus.round)
                return(blokus, board)
        else:
            if blokus.round <= 4:
                max_moves_value = 0
                influence_value = 3
                corridors_value = 2
                corners_value   = 0.5
                min_moves_value = 0
                size_value      = 3
            elif blokus.round <= 10:
                max_moves_value = 3
                influence_value = 1
                corridors_value = 2
                corners_value   = 0.5
                min_moves_value = 2
                size_value      = 1
            elif blokus.round <= 13:
                max_moves_value = 4
                influence_value = 1
                corridors_value = 2
                corners_value   = 0.5
                min_moves_value = 2
                size_value      = 1
            elif blokus.round <= 16:
                max_moves_value = 3
                influence_value = 1
                corridors_value = 0
                corners_value   = 0
                min_moves_value = 2
                size_value      = 1
            else:
                max_moves_value = 0.5
                influence_value = 0
                corridors_value = 0
                corners_value   = 0
                size_value      = 0.05
                min_moves_value = 0.5
                infinity_value  = 3
        # Max-min Strategy
        if max_moves_value != 0:
            list1 = Strategy_functions.max_moves(board, player, blokus)
            Result.assign_points(list1, max_moves_value)
        else:
            list1 = []
        # Influence Strategy
        if influence_value != 0:
            list2 = Strategy_functions.max_min_influence_area(board, player, blokus)
            Result.assign_points(list2, influence_value)
        else:
            list2 = []
        # Corridors Strategy
        if corridors_value != 0:
            list3 = Strategy_functions.find_corridors(board, player)
            Result.assign_points(list3, corridors_value)
        else:
            list3 = []
        # Corners Strategy
        if corners_value != 0:
            list4 = Strategy_functions.maximise_corners(board, player, blokus)
            Result.assign_points(list4, corners_value)
        else:
            list4 = []
        # Min moves Strategy - blocking
        if min_moves_value != 0:
            list5 = Strategy_functions.min_moves(board, player, blokus)
            Result.assign_points(list5, min_moves_value)
        else:
            list5 = []
        if infinity_value != 0:
            list6 = Strategy_functions.infinite_turns(board, blokus, 21-blokus.round)
            Result.assign_points(list6, infinity_value)
        else:
            list6 = []
        # Combine, assign piece size value and select the winning piece and points
        resultss = [list1, list2, list3, list4, list5, list6]
        best_move = Result.get_top_move(resultss, size_value)
        max_piece = best_move.piece
        max_points = best_move.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Random
    # Choose a random piece from the set of pieces you can play and play it
    def strategy_random(blokus, board):
        player = blokus.players[blokus.current_player]
        choose_pieces = board.valid_pieces(player)
        random_piece  = random.choice(tuple(choose_pieces))
        choose_points = board.valid_points(random_piece, player)
        random_points = random.choice(tuple(choose_points))
        Strategies.add_and_filter_data(blokus, board, player, random_points)
        player.add_points(random_piece)
        player.remove_piece(player.pieces.index(random_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Largest
    # Choose a random piece from the set of largest possible pieces to place
    def strategy_largest(blokus, board):
        player = blokus.players[blokus.current_player]
        choose_pieces = board.valid_pieces(player)
        largest_piece = max(choose_pieces, key=attrgetter('size'))
        choose_points = board.valid_points(largest_piece, player)
        random_points = random.choice(tuple(choose_points))
        Strategies.add_and_filter_data(blokus, board, player, random_points)
        player.add_points(largest_piece)
        player.remove_piece(player.pieces.index(largest_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    ###### All of the Strategies below (that can have it), contain a size constraint. ######
    ###### In case of a same score of 2 different pieces, piece of the larger size will be played. ######


    # Strategy - Max Corners after move
    # Maximise the amount of corners available after move
    def strategy_max_corners(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.maximise_corners(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Find corridors and a piece that will go to them
    def strategy_corridors(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.find_corridors(board, player)
        if len(list_of_results) == 0:
            return(Strategies.strategy_largest(blokus, board))
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Max possible moves for yourself and min for opponents
    # Place a piece that will maximise moves for you and minimise for opponents
    def strategy_max_min_moves(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.max_min_moves(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Man possible moves
    # Maximise the amount of moves for yourself after the move - greedy for self gain
    def strategy_max_moves(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.max_moves(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Min opponents' possible moves
    # Minimise the amount of moves for opponents after out move - blocking only
    def strategy_min_moves(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.min_moves(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Influence Area
    # Maximise Influence Area for yourself and minimise for opponents
    def strategy_max_min_influence(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.max_min_influence_area(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Influence Area
    # Maximise Influence Area for your blokus
    def strategy_max_influence(blokus, board):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.max_influence_area(board, player, blokus)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        max_piece = top_piece.piece
        max_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, max_points)
        player.add_points(max_piece)
        player.remove_piece(player.pieces.index(max_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Best moves if I had 'depth' moves in a row
    def strategy_infinite_moves(blokus, board, depth):
        player = blokus.players[blokus.current_player]
        list_of_results = Strategy_functions.infinite_turns(board, blokus, depth)
        Result.assign_points(list_of_results, 1)
        top_piece = Result.get_top_move([list_of_results], 0.05)
        optimal_piece = top_piece.piece
        optimal_points = top_piece.points
        Strategies.add_and_filter_data(blokus, board, player, optimal_points)
        player.add_points(optimal_piece)
        player.remove_piece(player.pieces.index(optimal_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)


    # Strategy - Optimal finish - Blokus DUO only
    # Specify the depth, finish optimally considering x (depth) moves of player 1 and 2
    def strategy_optimal_finish(blokus, board, depth):
        player = blokus.players[blokus.current_player]
        tupleValues = Strategy_functions.optimal_finish(board, blokus, depth)
        optimal_piece  = tupleValues[0]
        optimal_points = tupleValues[1]
        Strategies.add_and_filter_data(blokus, board, player, optimal_points)
        player.add_points(optimal_piece)
        player.remove_piece(player.pieces.index(optimal_piece))
        blokus.next_player()
        board.count_possible_moves_all(blokus)
        return(blokus, board)
