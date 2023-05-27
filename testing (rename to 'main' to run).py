import pygame
import random

from blokus.constants import FPS, WIDTH, HEIGHT, BLACK
from blokus.blokus import Blokus
from blokus.board import Board


def main():
    clock = pygame.time.Clock()

    array = ["Influence", "Max_moves"]

    blokus = Blokus(2, array)
    board = Board(14, 14)
    wins_1 = 0
    wins_2 = 0
    draws = 0

    round = 20
    while round > 0:
        if(blokus.finished):
            if((blokus.players[0].score > blokus.players[1].score)):
                if(blokus.players[0].strategy == "Influence"):
                    wins_1 += 1
                else:
                    wins_2 += 1
            elif(blokus.players[1].score > blokus.players[0].score):
                if(blokus.players[1].strategy == "Influence"):
                    wins_1 += 1
                else:
                    wins_2 += 1
            else:
                draws += 1
            print("Points Influence Strategy: ", wins_1)
            print("Points Max_moves Strategy: ", wins_2)
            print("Draws: ", draws)
            print("---------")

            if round > 10:
                array = ["Influence", "Max_moves"]
            else:
                array = ["Max_moves", "Influence"]
            blokus = Blokus(2, array)
            board = Board(14, 14)
            round -= 1
        else:
            blokus, board = blokus.play_computer_turn(board)

    pygame.quit()

if __name__ == "__main__":
    main()
