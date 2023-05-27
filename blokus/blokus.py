import pygame
import random
import copy
import numpy

from blokus.player import *
from blokus.board import *
from blokus.strategies import *
from blokus.graphics import *

class Blokus:

    # Count possible moves for all the players at the beginnig of the game
    def initialise_moves(self):
        board = Board(self.board_size, self.board_size)
        board.count_possible_moves_all(self)


    def __init__(self, players, strategies):
        if players == 4:
            player1 = Player(1, strategies[0])
            player1.add_all_pieces()
            player1.manual_add_corner((0,0))
            player2 = Player(2, strategies[1])
            player2.add_all_pieces()
            player2.manual_add_corner((0,19))
            player3 = Player(3, strategies[2])
            player3.add_all_pieces()
            player3.manual_add_corner((19,19))
            player4 = Player(4, strategies[3])
            player4.add_all_pieces()
            player4.manual_add_corner((19,0))
            self.players = [player1, player2, player3, player4]
            self.board_size = 20
        else:
            player1 = Player(1, strategies[0])
            player1.add_all_pieces()
            player1.manual_add_corner((4,4))
            player2 = Player(2, strategies[1])
            player2.add_all_pieces()
            player2.manual_add_corner((9,9))
            self.players = [player1, player2]
            self.board_size = 14
        self.initialise_moves()
        self.num_players = players
        self.round = 1
        self.winner_id = ""
        self.current_player = 0
        self.finished = False


    # Start the next player's turn
    def next_player(self):
        if not self.finished and self.current_player == (self.num_players - 1):
            self.round = self.round + 1
        self.current_player = (self.current_player + 1) % self.num_players

    # Find a winner (and if there is one)
    def find_winner(self):
        skips = 0
        for i in range(self.num_players):
            if self.players[i].possible_moves == 0:
                skips = skips + 1
        if skips == self.num_players:
            self.finished = True
            winner = ""
            max_score = 0
            colour = ""
            for i in range(self.num_players):
                if self.players[i].score > max_score:
                    if self.players[i].id == 1:
                        colour = "Blue"
                    elif self.num_players == 4:
                        if self.players[i].id == 2:
                            colour = "Yellow"
                        elif self.players[i].id == 3:
                            colour = "Red"
                        else:
                            colour = "Green"
                    else:
                        colour = "Yellow"
                    winner = colour
                    max_score = self.players[i].score
                elif self.players[i].score == max_score:
                    if self.players[i].id == 1:
                        colour = "Blue"
                    elif self.num_players == 4:
                        if self.players[i].id == 2:
                            colour = "Yellow"
                        elif self.players[i].id == 3:
                            colour = "Red"
                        else:
                            colour = "Green"
                    else:
                        colour = "Yellow"
                    winner = winner + ", " + colour
            txt = "The winner is: " + str(winner)
            self.winner_id = txt

    # Which button has been clicked
    def game_type_clicked(self, pos):
        x = pos[0]
        y = pos[1]
        if x > 1075 and x < 1175:
            # New game buttons
            if y > 25 and y < 65:
                return(1)
            elif y > 85 and y < 125:
                return(2)
            elif y > 145 and y < 185:
                return(3)
            elif y > 205 and y < 245:
                return(4)
            elif y > 265 and y < 305:
                return(5)
            elif y > 325 and y < 365:
                return(6)
            elif y > 385 and y < 425:
                return(7)
            elif y > 445 and y < 485:
                return(8)
            elif y > 545 and y < 585: # "Give a hint" buttons
                return(9)
            elif y > 605 and y < 645:
                return(10)
            elif y > 665 and y < 705:
                return(11)
            elif y > 745 and y < 765: # Hide a hint button
                return(99)
        return(-1)

    # New Game Options (Buttons 1 to 8)
    def new_game(self, board, option_button):
        if option_button == 1:
            return(Blokus(4, ["Human", "Human", "Human", "Human"]), Board(20, 20))
        elif option_button == 2:
            return(Blokus(2, ["Human", "Human"]), Board(14, 14))
        elif option_button == 3:
            array = ["Human", "Hybrid", "Max_min", "Influence"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 4:
            array = ["Largest", "Corridors", "Corners", "Random"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 5:
            array = ["Hybrid", "Max_moves", "Max_min", "Influence"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 6:
            array = ["Human", "Hybrid"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        elif option_button == 7:
            array = ["Min_moves", "Max_moves"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        elif option_button == 8:
            array = ["Influence", "Max_min"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        return(self, board)

    # What would startegy play (clue) (buttons 9+)
    def clue_highlight(self, option_button, board):
        player = self.players[self.current_player]
        if player.possible_moves != 0:
            if option_button == 9:
                blokus_copy = copy.deepcopy(self)
                board_copy  = copy.deepcopy(board)
                Strategies.strategy_hybrid(blokus_copy, board_copy)
                chosen_points = numpy.subtract(board_copy.board, board.board)
                row = column = 0
                points_array = []
                for row in range(board.row):
                    for column in range(board.col):
                        if chosen_points[row][column] != 0:
                            points_array.append((row, column))
                board.reset_highlight()
                board.set_highlight(points_array)
            if option_button == 10:
                blokus_copy = copy.deepcopy(self)
                board_copy  = copy.deepcopy(board)
                Strategies.strategy_max_min_moves(blokus_copy, board_copy)
                chosen_points = numpy.subtract(board_copy.board, board.board)
                row = column = 0
                points_array = []
                for row in range(board.row):
                    for column in range(board.col):
                        if chosen_points[row][column] != 0:
                            points_array.append((row, column))
                board.reset_highlight()
                board.set_highlight(points_array)
            elif option_button == 11:
                choose_pieces = board.valid_pieces(player)
                random_piece  = random.choice(tuple(choose_pieces))
                choose_points = board.valid_points(random_piece, player)
                random_points = random.choice(tuple(choose_points))
                board.reset_highlight()
                board.set_highlight(random_points)
            elif option_button == 99:
                board.reset_highlight()
        return(self, board)

    # Human turn or Creating new game
    def play_turn(self, board):
        pos = pygame.mouse.get_pos()
        player = self.players[self.current_player]
        strategy = player.strategy
        if player.possible_moves == 0:
            self.next_player()
        option_button = self.game_type_clicked(pos)
        if option_button > 8 and strategy == "Human":
            return(self.clue_highlight(option_button, board))
        elif option_button != -1:
            return(self.new_game(board, option_button))
        elif player.which_piece(pos) != -1  and strategy == "Human":
            player.position  = player.which_piece(pos)
            piece = player.pieces[player.position]
            board.possible_moves(piece, player)
        elif board.where_clicked(pos) != (-1, -1) and player.position != -1  and strategy == "Human":
            piece = player.pieces[player.position]
            piece.move_points(board.where_clicked(pos))
            if board.valid_move(piece, player) == True:
                for pt in piece.points:
                    board.board[pt[0]][pt[1]] = player.id
                board.add_corners(player, piece.corners)
                board.all_filter_corners(self)
                board.all_update_influence(self)
                player.add_points(piece)
                player.remove_piece(player.position)
                player.position = -1
                self.next_player()
                board.count_possible_moves_all(self)
                board.reset_highlight()
                self.find_winner()
            else:
                piece.move_points((2,2))
                player.position = -1
        return(self, board)

    # Player computer turn with computer strategies
    def play_computer_turn(self, board):
        strategy_name = self.players[self.current_player].strategy
        return(Strategies.play_strategy(self, board, strategy_name))


    # Update all the graphics
    def update_screen(self, player, position, board, win):
        Graphics.draw_board(board, win)
        Graphics.draw_highlight(board, win)
        Graphics.draw_board_frame(board, win)
        Graphics.draw_possible_moves(board, win, player, position)
        Graphics.draw_pieces(player, win)
        Graphics.mark_pieces(win, position)
        Graphics.draw_points(self, win)
        Graphics.draw_information(self, win, player)
        Graphics.draw_buttons(self, win)
