import pygame, sys, os 
from settings import * 
from tiles import Tile
from level import Level


#Start pygame
pygame.init()
screen = pygame.display.set_mode( (screen_width, screen_height) )
clock_game = pygame.time.Clock()
level = Level( level_map, screen )

test_tile = pygame.sprite.Group(Tile((100,100),200))


#Game
while True:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run()


    pygame.display.update()
    clock_game.tick(60)