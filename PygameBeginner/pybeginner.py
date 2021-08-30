import pygame, sys
from pygame.display import set_caption
from pygame.locals import *



Clock = pygame.time.Clock()
pygame.init() #Inicializar o Pygame. 

#Variaveis 
pygame.display.set_caption("My Pygame Window")
WINDOW_SIZE = (400,400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0,32)


#Loop do Game 
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            print('I don\'t want to close' )
            
            #pygame.quit()
            #sys.exit()

    
    pygame.display.update()
    Clock.tick(60)