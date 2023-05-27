import pygame
import random

from blokus.constants import FPS, WIDTH, HEIGHT, BLACK
from blokus.blokus import Blokus
from blokus.board import Board

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blokus')

WIN.fill(BLACK)
pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    blokus = Blokus(4, ["Human", "Human", "Human", "Human"])
    board = Board(blokus.board_size, blokus.board_size)

    while run:
        clock.tick(FPS)

        if not blokus.finished and blokus.players[blokus.current_player].strategy != "Human":
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
        blokus.update_screen(blokus.players[blokus.current_player], blokus.players[blokus.current_player].position, board, WIN)
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main()
