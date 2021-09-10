import pygame, sys
from pygame.display import set_caption
from pygame.locals import *

# My class: Pygame.
# Current: Aula 03 - https://www.youtube.com/watch?v=Qdeb1iinNtk&list=PLX5fBCkxJmm3nAalPU6gGfRIFLlghRuYy&index=2
# After: https://www.youtube.com/c/ClearCode/videos
#Continuar: 09:00 Min 

Clock = pygame.time.Clock() #Indica o tempo 
pygame.init() #Inicializar o Pygame. 

#Variaveis 
pygame.display.set_caption("My Pygame Window")
WINDOW_SIZE = (400,400) #Tamanho da tela 
screen = pygame.display.set_mode(WINDOW_SIZE, 0,32) #

player_image = pygame.image.load('player.png')
player_location = [50,50]
player_y_momentum = 0
moving_right = False 
moving_left = False

player_rect = pygame.Rect( player_location[0], player_location[1], player_image.get_width(), player_image.get_height() )
test_rect = pygame.Rect(100,100,100,50)

#Loop do Game 
while True:
    screen.fill((146,244,255))
    screen.blit(player_image,player_location)

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

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255,0,0), test_rect)
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)


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
            



    pygame.display.update()
    Clock.tick(60)