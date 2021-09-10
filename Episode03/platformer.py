import pygame, sys
import os 
from pygame import display
from pygame.display import set_caption
from pygame.locals import *

# Trilha de Estudos: Game Developer
# 1) My class: Pygame Tutorial Series (all) 03/32. 
# Current: Aula 03 - 15:00 Min 
# https://www.youtube.com/watch?v=Qdeb1iinNtk&list=PLX5fBCkxJmm3nAalPU6gGfRIFLlghRuYy&index=2
# 
# 2) Project: Creating a Mario Style Level in Pygame 0/10
# 3) After: Learning Pygame by making FlappyBird
# https://www.youtube.com/c/ClearCode/videos
#

Clock = pygame.time.Clock() #Indica o tempo 
pygame.init() #Inicializar o Pygame. 

#Variaveis 
pygame.display.set_caption("My Pygame Window")
WINDOW_SIZE = (600,400) #Tamanho da tela 
screen = pygame.display.set_mode(WINDOW_SIZE, 0,32) #

display = pygame.Surface((300, 200))

player_image = pygame.image.load('assets/player.png')
player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load(os.path.join('assets/','grass.png'))
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load(os.path.join('assets/','dirt.png'))

#game_map[y][x]
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


player_location = [50,50]
player_y_momentum = 0
moving_right = False 
moving_left = False

player_rect = pygame.Rect( player_location[0], player_location[1], player_image.get_width(), player_image.get_height() )
test_rect = pygame.Rect(100,100,100,50)

#Loop do Game 
while True:
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x= 0
        for tile in row:
            x += 1
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image,(x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect( x* TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        y += 1




    display.blit(player_image,player_location)

    if player_location[1] > WINDOW_SIZE[1] - player_image.get_height():
        player_y_momentum = - player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    
    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4


    player_rect.x = player_location[0]
    player_rect.y = player_location[1]




    for event in pygame.event.get():
        if event.type == QUIT:
            #print('I don\'t want to close' )
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            


    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    Clock.tick(60)