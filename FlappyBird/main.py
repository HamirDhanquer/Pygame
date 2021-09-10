'''
https://www.youtube.com/watch?v=UZg49z76cLw&t=527s

***Adding pipes => 00:39:06
'''

import pygame, sys
#from functions import draw_floor

def draw_floor():
    screen.blit( floor_surface, ( floor_x_pos,605) )
    screen.blit( floor_surface, ( floor_x_pos + 576,605) )


pygame.init()
screen = pygame.display.set_mode( (576,698) )
clock = pygame.time.Clock()

#Game Variables: 

gravity = 0.25
bird_movement = 0

backgrd_surface = pygame.image.load('assets/background-day.png').convert()
backgrd_surface = pygame.transform.scale2x( backgrd_surface )

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x( floor_surface )
floor_x_pos = 0

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x( pipe_surface )
pipe_list = []

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x( bird_surface )
bird_rect = bird_surface.get_rect(center=(100,350))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12


    screen.blit(backgrd_surface, (0,-200) )
    
#Gravidade no bird    
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface,bird_rect)

## Animação do chão.    
    floor_x_pos -=1 
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
### 
    pygame.display.update()
    clock.tick(120)