'''
https://www.youtube.com/watch?v=UZg49z76cLw&t=527s

***Adding pipes => 00:54:29
'''

import pygame, sys, random
#from random import 
#from functions import draw_floor

def draw_floor():
    screen.blit( floor_surface, ( floor_x_pos,605) )
    screen.blit( floor_surface, ( floor_x_pos + 576,605) )

def create_pipe():
    random_pipe_pos = random.choice( pipe_height )
    botton_pipe = pipe_surface.get_rect( midtop = (700,random_pipe_pos) )
    top_pipe = pipe_surface.get_rect( midbottom = (700,random_pipe_pos - 300) )
    return botton_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 698:
            screen.blit( pipe_surface, pipe )
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit( flip_pipe, pipe )

def check_collision(pipes):
    for pipe in pipes: 
        if bird_rect.colliderect(pipe):
            #print( 'collision' )
            return False

    if bird_rect.top <= -100 or bird_rect.bottom > 698:
        #print('collision02')
        return False 
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3 , 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display( game_state ):

    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect) 
    
        high_score_surface = game_font.render(f'High score: {str(int(high_score))}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,550))
        screen.blit(high_score_surface, high_score_rect) 

def update_score( score, high_score ):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode( (576,698) )
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04B_19.ttf',40)

#Game Variables: 

gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

backgrd_surface = pygame.image.load('assets/background-day.png').convert()
backgrd_surface = pygame.transform.scale2x( backgrd_surface )

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x( floor_surface )
floor_x_pos = 0

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x( pipe_surface )
pipe_list = []

bird_downflap = pygame.transform.scale2x( pygame.image.load('assets/bluebird-downflap.png').convert_alpha() )
bird_midflap = pygame.transform.scale2x( pygame.image.load('assets/bluebird-midflap.png').convert_alpha() )
bird_upflap = pygame.transform.scale2x( pygame.image.load('assets/bluebird-upflap.png').convert_alpha() )
bird_frames = [ bird_downflap, bird_midflap, bird_upflap ]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect( center = (100,512) )

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer( BIRDFLAP, 200 )

#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x( bird_surface )
#bird_rect = bird_surface.get_rect(center=(100,350))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [150,400,250]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
            
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,350)
                bird_movement = 0
                score = 0
        
        if event.type == SPAWNPIPE:
            pipe_list.extend( create_pipe() ) 
            #print( pipe_list )
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()


    screen.blit(backgrd_surface, (0,-200) )

    if game_active:
    #Bird    
        bird_movement += gravity
        rotated_bird = rotate_bird( bird_surface )
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        score += 0.01
        score_display( 'main_game' )

    #Pipes 
        pipe_list = move_pipes(pipe_list)
        draw_pipes( pipe_list )
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')

#Floor.    
    floor_x_pos -=1 
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
### 
    pygame.display.update()
    clock.tick(120)