import pygame

FPS = 30

WIDTH, HEIGHT   = 1200, 800
ROWS, COLS      = 32,48
SQUARE_SIZE     = WIDTH//COLS

# rgb
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
VLIGHTGRAY = (220,220,220)
LIGHTGRAY  = (211,211,211)
SILVER     = (192,192,192)
GREY       = (128,128,128)
DIMGRAY    = (105,105,105)
LIGHTPINK  = (255, 204,255)
NEONCARROT = (255, 153, 51)
WHITESMOKE = (245, 245, 245)
PINK       = (255, 192, 203)
WINCOLOUR  = (58, 4, 119)
HOTPURPLE  = (203, 0, 245)
CLUEPINK   = (243, 150, 231)
RESETPINK  = (246, 165, 235)
LIGHTBLACK = (25, 25, 25)

# Pieces colours: Blue, Yellow, Red, Green
BLUE       = (51, 153, 255)
YELLOW     = (255, 255, 102)
RED        = (255, 102, 102)
GREEN      = (0, 153, 0)

DOTE = pygame.transform.scale(pygame.image.load('blokus/pinkDote.png'), (10, 10))
BLACKDOTE = pygame.transform.scale(pygame.image.load('blokus/blackDote.png'), (6, 6))
