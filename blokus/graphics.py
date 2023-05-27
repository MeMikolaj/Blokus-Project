import pygame

from blokus.constants import *

class Graphics:

    # Information Top Banner
    def draw_information(blokus, win, player):
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 20)
        if blokus.num_players == 4:
            pygame.draw.rect(win, WHITESMOKE, (550, 25, 500, 75))
        else:
            pygame.draw.rect(win, WHITESMOKE, (550, 25, 350, 75))
        if blokus.winner_id != "":
            my_font = pygame.font.SysFont('calibri', 30)
            text = my_font.render(blokus.winner_id, True, WINCOLOUR)
            win.blit(text, (560, 32.5))
        else:
            moves = player.possible_moves
            if moves == 0:
                txt1 = "You have 0 possible moves."
                txt2 = "Click mouse to skip your turn."
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
        round_num = blokus.round
        round_txt = "Round: " + str(round_num)
        round_text = my_font.render(round_txt, True, BLACK)
        if blokus.num_players == 4:
            win.blit(round_text, (950, 72.5))
        else:
            win.blit(round_text, (800, 72.5))


    # Current Scores and Player Type
    def draw_points(blokus, win):
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 25)
        if blokus.num_players == 4:
            pygame.draw.rect(win, LIGHTBLACK, (550, 170, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (925, 170, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (925, 710, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (550, 710, 125, 25))
            player1 = my_font.render('Blue: ' + str(blokus.players[0].score), True, BLUE)
            player2 = my_font.render('Yellow: ' + str(blokus.players[1].score), True, YELLOW)
            player3 = my_font.render('Red: ' + str(blokus.players[2].score), True, RED)
            player4 = my_font.render('Green: ' + str(blokus.players[3].score), True, GREEN)
            win.blit(player1, (550,170))
            win.blit(player2, (925,170))
            win.blit(player3, (925,710))
            win.blit(player4, (550,710))
            pygame.draw.rect(win, LIGHTBLACK, (550, 140, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (925, 140, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (925, 740, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (550, 740, 125, 25))
            player1_strategy = my_font.render(str(blokus.players[0].strategy), True, BLUE)
            player2_strategy = my_font.render(str(blokus.players[1].strategy), True, YELLOW)
            player3_strategy = my_font.render(str(blokus.players[2].strategy), True, RED)
            player4_strategy = my_font.render(str(blokus.players[3].strategy), True, GREEN)
            win.blit(player1_strategy, (550,140))
            win.blit(player2_strategy, (925,140))
            win.blit(player3_strategy, (925,740))
            win.blit(player4_strategy, (550,740))
        else:
            pygame.draw.rect(win, LIGHTBLACK, (550, 170, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (775, 560, 125, 25))
            player1 = my_font.render('Blue: ' + str(blokus.players[0].score), True, BLUE)
            player2 = my_font.render('Yellow: ' + str(blokus.players[1].score), True, YELLOW)
            win.blit(player1, (550,170))
            win.blit(player2, (775,560))
            pygame.draw.rect(win, LIGHTBLACK, (550, 140, 125, 25))
            pygame.draw.rect(win, LIGHTBLACK, (775, 590, 125, 25))
            player1_strategy = my_font.render(str(blokus.players[0].strategy), True, BLUE)
            player2_strategy = my_font.render(str(blokus.players[1].strategy), True, YELLOW)
            win.blit(player1_strategy, (550,140))
            win.blit(player2_strategy, (775,590))

    # Buttons Graphic
    def draw_buttons(blokus, win):
        # "New Game" Buttons
        pygame.font.init()
        my_font = pygame.font.SysFont('calibri', 12)
        txt1 = "4 Humans"
        txt2 = "2 Humans"
        txt3 = "4 mix & Human"
        txt4 = "4 mix beginner"
        txt5 = "4 mix advanced"
        txt6 = "Human vs Hybrid"
        txt7 = "2 mix beginner"
        txt8 = "2 mix advanced"
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
        # Reset Hint button
        txt_hint = "Hide hint"
        text_hint = my_font.render(txt_hint, True, BLACK)
        pygame.draw.rect(win, RESETPINK, (1075, 745, 4*SQUARE_SIZE, 20))
        win.blit(text_hint, (1082, 749))
        # "What would strategy play" - Hint Buttons
        txt0_0 = "Advanced hint"
        text0_0 = my_font.render(txt0_0, True, BLACK)
        pygame.draw.rect(win, CLUEPINK, (1075, 545, 4*SQUARE_SIZE, 40))
        win.blit(text0_0, (1082, 559))
        txt1_0 = "Amateur hint"
        text1_0 = my_font.render(txt1_0, True, BLACK)
        pygame.draw.rect(win, CLUEPINK, (1075, 605, 4*SQUARE_SIZE, 40))
        win.blit(text1_0, (1082, 619))
        txt2_0 = "Beginner hint"
        text2_0 = my_font.render(txt2_0, True, BLACK)
        pygame.draw.rect(win, CLUEPINK, (1075, 665, 4*SQUARE_SIZE, 40))
        win.blit(text2_0, (1082, 679))


    # BOARD #

    # Draw the actual state of the board with pieces
    # Takes an array that contains numbers 0-4 that imply what is the colour of each square
    def draw_board(board, win):
        win.fill(VLIGHTGRAY)
        count1 = 0
        for i in board.board:
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

    # Draw the gray grid frame
    def draw_board_frame(board, win):
        for row in range(board.row*SQUARE_SIZE+1):
            for col in range(board.col*SQUARE_SIZE+1):
                if row%25 == 0 or col%25 == 0:
                    pygame.draw.rect(win, SILVER, (550+col, 200+row, 1, 1))

    # Show where selected piece can be placed
    def mark_possible_moves(board, player, position):
        if len(player.pieces) <= position or len(player.pieces) == 0:
            position = -1
        else:
            shape = player.pieces[position]
        if position != -1:
            board.possible_moves(shape, player)
        else:
            board.mark_moves = [[0] * board.col for i in range(board.row)]

    # Draw a dote in the square where one can place their currently marked shape
    def draw_possible_moves(board, win, player, position):
        Graphics.mark_possible_moves(board, player, position)
        count1 = 0
        for i in board.mark_moves:
            count2 = 0
            for j in i:
                if j == 1:
                    win.blit(BLACKDOTE, (559.5+count2*SQUARE_SIZE, 209.5+count1*SQUARE_SIZE))
                count2 = count2 + 1
            count1 = count1 + 1


    def draw_highlight(board, win):
        for pt in board.highlight_board:
                pygame.draw.rect(win, HOTPURPLE, (550+pt[1]*SQUARE_SIZE, 200+pt[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    ## Player ##

    # Draw player's pieces on the left side of the screen
    def draw_pieces(player, win):
        #players colour
        colour = WHITE
        if player.id == 1:
            colour = BLUE
        elif player.id == 2:
            colour = YELLOW
        elif player.id == 3:
            colour = RED
        elif player.id == 4:
            colour = GREEN
        size = len(player.pieces)
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
                shape = player.pieces[pos]
                for point in shape.points:
                    x = point[0]
                    y = point[1]
                    pygame.draw.rect(win, colour, (25+b*SQUARE_SIZE*5 + y*SQUARE_SIZE, 25+a*SQUARE_SIZE*5 + x*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                first = shape.points[0]
                win.blit(DOTE, (32.5+b*SQUARE_SIZE*5 + first[1]*SQUARE_SIZE, 32.5+a*SQUARE_SIZE*5 + first[0]*SQUARE_SIZE))
                pos = pos + 1
        for c in range(count_x):
            pygame.draw.rect(win, BLACK, (25+c*SQUARE_SIZE*5, 25+count_y*SQUARE_SIZE*5, SQUARE_SIZE*5, SQUARE_SIZE*5))
            shape = player.pieces[pos]
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

    # Mark the piece that has been chosen
    def mark_pieces(win, pos):
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
