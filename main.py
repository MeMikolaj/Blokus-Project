import pygame
import random

from blokus.shape import *
from blokus.player import Player

from blokus.constants import FPS, WIDTH, HEIGHT, SQUARE_SIZE, BLACK
from blokus.board import Board
from blokus.blokus import Blokus

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blokus')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# arraySquares = [[random.randint(0, 4) for col in range(20)] for row in range(20)]


WIN.fill(BLACK)
pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    result = ""

    blokus = Blokus(4, ["human", "human", "human", "human"])
    board = Board(blokus.board_size, blokus.board_size)

    while run:
        player = blokus.players[blokus.current_player]
        clock.tick(FPS)
        player.draw_pieces(WIN)
        if not blokus.finished and blokus.players[blokus.current_player].strategy != "human":
            blokus, board = blokus.play_computer_turn(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                blokus, board = blokus.play_turn(board)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    blokus.players[blokus.current_player].rotate_all(270)
                elif event.key == pygame.K_RIGHT:
                    blokus.players[blokus.current_player].rotate_all(90)
                elif event.key == pygame.K_UP:
                    blokus.players[blokus.current_player].flip_all()
                elif event.key == pygame.K_DOWN:
                    blokus.players[blokus.current_player].flip_all()

        # Draw everything / Display
        blokus.update(blokus.players[blokus.current_player], player.position, board, WIN)
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main()
