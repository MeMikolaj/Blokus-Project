import pygame
import random
from operator import attrgetter

from blokus.player import Player
from blokus.shape import *
from blokus.constants import BLUE, YELLOW, RED, GREEN, BLACK, WHITESMOKE, PINK, SQUARE_SIZE, WINCOLOUR
from blokus.board import *

class Blokus:

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

    def next_player(self):
        if not self.finished and self.current_player == (self.num_players - 1):
            self.round = self.round + 1
        self.current_player = (self.current_player + 1) % self.num_players

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

    def game_type_clicked(self, pos):
        x = pos[0]
        y = pos[1]

        if x > 1075 and x < 1175:
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
        return(-1)

    def new_game(self, board, option_button):
        if option_button == 1:
            return(Blokus(4, ["human", "human", "human", "human"]), Board(20, 20))
        elif option_button == 2:
            return(Blokus(2, ["human", "human"]), Board(14, 14))
        elif option_button == 3:
            array = ["random", "random", "human", "human"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 4:
            array = ["random", "corners"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        elif option_button == 5:
            array = ["random", "largest"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        elif option_button == 6:
            array = ["random", "largest", "random", "largest"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 7:
            array = ["max_min", "large+cor", "largest", "random"]
            random.shuffle(array)
            return(Blokus(4, array), Board(20, 20))
        elif option_button == 8:
            array = ["max_min", "largest"]
            random.shuffle(array)
            return(Blokus(2, array), Board(14, 14))
        return(self, board)

    def play_turn(self, board):
        pos = pygame.mouse.get_pos()
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        elif player.which_piece(pos) != -1:
            player.position  = player.which_piece(pos)
            piece = player.pieces[player.position]
            board.possible_moves(piece, player)
        elif player.where_on_board(pos, board) != (-1, -1) and player.position != -1:
            piece = player.pieces[player.position]
            piece.move_points(player.where_on_board(pos, board))
            if board.valid_move(piece, player) == True:
                for pt in piece.points:
                    board.board[pt[0]][pt[1]] = player.id
                board.add_corners(player, piece.corners)
                board.all_filter_corners(self)
                player.add_points(piece)
                player.remove_piece(player.position)
                player.position = -1
                self.next_player()
                board.count_possible_moves_all(self)
            else:
                piece.move_points((2,2))
                player.position = -1
        return(self, board)


    def strategy_random(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            choose_pieces = board.valid_pieces(player)
            random_piece  = random.choice(tuple(choose_pieces))
            choose_points = board.valid_points(random_piece, player)
            random_points = random.choice(tuple(choose_points))
            fake_corner_array = []
            for pt in random_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(random_piece)
            player.remove_piece(player.pieces.index(random_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)

    def strategy_largest(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            choose_pieces = board.valid_pieces(player)
            largest_piece = max(choose_pieces, key=attrgetter('size'))
            choose_points = board.valid_points(largest_piece, player)
            random_points = random.choice(tuple(choose_points))
            fake_corner_array = []
            for pt in random_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(largest_piece)
            player.remove_piece(player.pieces.index(largest_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)

    # BAD STRATEGY - slow
    def strategy_most_moves(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            tupleIDs = board.maximise_moves(player)
            choose_pieces = board.valid_pieces(player)
            max_piece = tupleIDs[0]
            max_points = tupleIDs[1]
            fake_corner_array = []
            for pt in max_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(max_piece)
            player.remove_piece(player.pieces.index(max_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)


    # Largest piece, most corners for first 6 rounds, then most corners
    def strategy_combined(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            tupleIDs = board.maximise_moves_largest_piece(player, self)
            max_piece = tupleIDs[0]
            max_points = tupleIDs[1]
            fake_corner_array = []
            for pt in max_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(max_piece)
            player.remove_piece(player.pieces.index(max_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)

    # Largest piece, most corners for first 6 rounds, then most corners
    def strategy_max_min_moves(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            tupleIDs = board.max_min_moves_largest_piece(player, self)
            max_piece = tupleIDs[0]
            max_points = tupleIDs[1]
            fake_corner_array = []
            for pt in max_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(max_piece)
            player.remove_piece(player.pieces.index(max_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)

    # Most corners available after move
    def strategy_max_corners(self, board):
        pos = pygame.mouse.get_pos()
        option_button = self.game_type_clicked(pos)
        if option_button != -1:
            return(self.new_game(board, option_button))
        player = self.players[self.current_player]
        if self.finished == False:
            self.find_winner()
        if player.possible_moves == 0:
            self.next_player()
            return(self, board)
        else:
            tupleIDs = board.maximise_avail_corners(player, self)
            max_piece = tupleIDs[0]
            max_points = tupleIDs[1]
            fake_corner_array = []
            for pt in max_points:
                board.board[pt[0]][pt[1]] = player.id
                fake_corner_array.append((pt[0]+1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]+1))
                fake_corner_array.append((pt[0]-1, pt[1]-1))
                fake_corner_array.append((pt[0]+1, pt[1]-1))
            board.add_corners(player, fake_corner_array)
            board.all_filter_corners(self)
            player.add_points(max_piece)
            player.remove_piece(player.pieces.index(max_piece))
            self.next_player()
            board.count_possible_moves_all(self)
        return(self, board)

    def play_computer_turn(self, board):
        strategy = self.players[self.current_player].strategy
        if strategy == "random":
            self.strategy_random(board)
        elif strategy == "largest":
            self.strategy_largest(board)
        elif strategy == "max_move":
            self.strategy_most_moves(board)
        elif strategy == "large+cor":
            self.strategy_combined(board)
        elif strategy == "max_min":
            self.strategy_max_min_moves(board)
        elif strategy == "corners":
            self.strategy_max_corners(board)
        return(self, board)



    def draw_points(self, win):
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 25)
        if self.num_players == 4:
            pygame.draw.rect(win, BLACK, (550, 170, 95, 25))
            pygame.draw.rect(win, BLACK, (937, 170, 113, 25))
            pygame.draw.rect(win, BLACK, (963, 710, 87, 25))
            pygame.draw.rect(win, BLACK, (550, 710, 112, 25))
            player1 = my_font.render('Blue: ' + str(self.players[0].score), True, BLUE)
            player2 = my_font.render('Yellow: ' + str(self.players[1].score), True, YELLOW)
            player3 = my_font.render('Red: ' + str(self.players[2].score), True, RED)
            player4 = my_font.render('Green: ' + str(self.players[3].score), True, GREEN)
            win.blit(player1, (550,170))
            win.blit(player2, (937,170))
            win.blit(player3, (963,710))
            win.blit(player4, (550,710))

            pygame.draw.rect(win, BLACK, (550, 140, 95, 25))
            pygame.draw.rect(win, BLACK, (937, 140, 113, 25))
            pygame.draw.rect(win, BLACK, (963, 740, 87, 25))
            pygame.draw.rect(win, BLACK, (550, 740, 112, 25))
            player1_strategy = my_font.render(str(self.players[0].strategy), True, BLUE)
            player2_strategy = my_font.render(str(self.players[1].strategy), True, YELLOW)
            player3_strategy = my_font.render(str(self.players[2].strategy), True, RED)
            player4_strategy = my_font.render(str(self.players[3].strategy), True, GREEN)
            win.blit(player1_strategy, (550,140))
            win.blit(player2_strategy, (937,140))
            win.blit(player3_strategy, (963,740))
            win.blit(player4_strategy, (550,740))
        else:
            pygame.draw.rect(win, BLACK, (550, 170, 95, 25))
            pygame.draw.rect(win, BLACK, (787, 560, 113, 25))
            player1 = my_font.render('Blue: ' + str(self.players[0].score), True, BLUE)
            player2 = my_font.render('Yellow: ' + str(self.players[1].score), True, YELLOW)
            win.blit(player1, (550,170))
            win.blit(player2, (787,560))

            pygame.draw.rect(win, BLACK, (550, 140, 95, 25))
            pygame.draw.rect(win, BLACK, (787, 590, 113, 25))
            player1_strategy = my_font.render(str(self.players[0].strategy), True, BLUE)
            player2_strategy = my_font.render(str(self.players[1].strategy), True, YELLOW)
            win.blit(player1_strategy, (550,140))
            win.blit(player2_strategy, (787,590))

    def draw_information(self, win, player):
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 20)
        if self.num_players == 4:
            pygame.draw.rect(win, WHITESMOKE, (550, 25, 500, 75))
        else:
            pygame.draw.rect(win, WHITESMOKE, (550, 25, 350, 75))
        if self.winner_id != "":
            my_font = pygame.font.SysFont('calibri', 30)
            text = my_font.render(self.winner_id, True, WINCOLOUR)
            win.blit(text, (560, 32.5))
        else:
            moves = player.possible_moves
            txt1 = ""
            txt2 = ""
            txt3 = ""
            if moves == 0:
                txt1 = "You have 0 possible moves."
                txt2 = "Click to skip your turn."
                txt3 = "Score = " + str(player.score)
            else:
                txt1 = "You have " + str(moves) + " possible moves."
                txt2 = "Place a piece."
                txt3 = "Score = " + str(player.score)
            text1 = my_font.render(txt1, True, BLACK)
            text2 = my_font.render(txt2, True, BLACK)
            text3 = my_font.render(txt3, True, BLACK)
            win.blit(text1, (560, 32.5))
            win.blit(text2, (560, 52.5))
            win.blit(text3, (560, 72.5))
        my_font = pygame.font.SysFont('calibri', 20)
        round_num = self.round
        round_txt = "Round: " + str(round_num)
        round_text = my_font.render(round_txt, True, BLACK)
        if self.num_players == 4:
            win.blit(round_text, (950, 72.5))
        else:
            win.blit(round_text, (800, 72.5))

    def draw_buttons(self, win):
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 12)
        txt1 = "4 players game"
        txt2 = "2 players game"
        txt3 = "2 rand 2 human"
        txt4 = "1 rand 1 cor"
        txt5 = "1 rand 1 largest"
        txt6 = "2 rand 2 largest"
        txt7 = "4 player mix"
        txt8 = "1v1 max_min - large"
        text1 = my_font.render(txt1, True, BLACK)
        text2 = my_font.render(txt2, True, BLACK)
        text3 = my_font.render(txt3, True, BLACK)
        text4 = my_font.render(txt4, True, BLACK)
        text5 = my_font.render(txt5, True, BLACK)
        text6 = my_font.render(txt6, True, BLACK)
        text7 = my_font.render(txt7, True, BLACK)
        text8 = my_font.render(txt8, True, BLACK)

        pygame.draw.rect(win, PINK, (1075, 25, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 85, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 145, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 205, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 265, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 325, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 385, 4*SQUARE_SIZE, 40))
        pygame.draw.rect(win, PINK, (1075, 445, 4*SQUARE_SIZE, 40))

        win.blit(text1, (1082, 39))
        win.blit(text2, (1082, 99))
        win.blit(text3, (1082, 159))
        win.blit(text4, (1082, 219))
        win.blit(text5, (1082, 279))
        win.blit(text6, (1082, 339))
        win.blit(text7, (1082, 399))
        win.blit(text8, (1082, 459))

    def update(self, player, position, board, win):
        board.update_possible_moves(player, position)
        board.draw_board(win)
        board.draw_possible_moves(win)
        player.draw_pieces(win)
        player.mark_piece(win, position)
        self.draw_points(win)
        self.draw_information(win, player)
        self.draw_buttons(win)
