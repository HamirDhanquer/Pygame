import pygame, sys
import os, random  
from pygame import display
from pygame import transform
from pygame.display import set_caption
from pygame.locals import *

# Trilha de Estudos: Game Developer
# 1) My class: Pygame Tutorial Series (all) 03/32. 
# Current: Aula 03 - 15:00 Min 
# https://www.youtube.com/watch?v=Qdeb1iinNtk&list=PLX5fBCkxJmm3nAalPU6gGfRIFLlghRuYy&index=2

# Funções Utilizadas no Episodio
def collision_test( rect, tiles ):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top':False, 'bottom':False, 'right':False, 'left':False}
    rect.x += movement[0]

    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    
    rect.y += movement[1]   
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top 
            collision_types['bottom'] = True
        
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    return game_map
         

global animation_frames
animation_frames = {}
def load_animation( path, frame_durations ):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0 
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'

        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[ animation_frame_id ] = animation_image.copy()

        for i in range(frame):
            animation_frame_data.append( animation_frame_id )

        n += 1
    return animation_frame_data

def change_action( action_var, frame, new_value ):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() #Inicializar o Pygame. 

Clock = pygame.time.Clock() #Indica o tempo 
#Variaveis 
pygame.display.set_caption("My Pygame Window")
WINDOW_SIZE = (600,400) #Tamanho da tela 
screen = pygame.display.set_mode(WINDOW_SIZE, 0,32) #

display = pygame.Surface((300, 200))

dirAtual = os.getcwd() + '\\Episode06\\assets\\'
#print( dirAtual )

#player_image = pygame.image.load( r'D:\Projects\Pygame\Episode05\assets\player.png')
#player_image = pygame.image.load( 'assets/player.png')
player_image = pygame.image.load( os.path.join( dirAtual, 'player.png'))
player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load(os.path.join(dirAtual,'grass.png'))
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load(os.path.join(dirAtual,'dirt.png'))

animation_database = {}
animation_database['run'] = load_animation(os.path.join(dirAtual, 'player_animations/run'),[7,7])
animation_database['idle'] = load_animation(os.path.join(dirAtual,'player_animations/idle'),[7,7,40])

jump_sound = pygame.mixer.Sound( os.path.join( dirAtual, 'jump.wav') )
grass_sounds = [pygame.mixer.Sound( os.path.join( dirAtual, 'grass_0.wav' ) ), 
                pygame.mixer.Sound( os.path.join( dirAtual, 'grass_1.wav' ) )]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load( os.path.join( dirAtual,'music.wav' ) )
pygame.mixer.music.play( -1 )
grass_sound_timer = 0

player_action = 'idle'
player_frame = 0
player_flip = False

true_scroll = [0,0]

game_map = load_map(os.path.join(dirAtual,'map'))

player_location = [50,50]
moving_right = False 
moving_left = False
player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect( 50, 50, player_image.get_width(), player_image.get_height() )
test_rect = pygame.Rect(100,100,100,50)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


#Loop do Game 
while True:
    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1


# Camera 
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152) /20
    true_scroll[1] += ( player_rect.y - true_scroll[1] -106 ) /20
    scroll = true_scroll.copy()
    scroll[0] = int( scroll[0] )
    scroll[1] = int( scroll[1] )

# Carregar o Background 
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect( background_object[1][0] - scroll[0] * background_object[0], 
                                background_object[1][1] - scroll[1] * background_object[0], 
                                background_object[1][2],
                                background_object[1][3] )
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150), obj_rect)
        else:
            pygame.draw.rect(display, (9,91,85), obj_rect)


# Eventos do Game: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                #player_y_momentum = -5 
                if air_timer < 6:
                    jump_sound.play()
                    player_y_momentum = -5
        
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

# Carregar o Mapa 
    tile_rects = []
    y = 0
    for row in game_map:
        x= 0
        for tile in row:
            x += 1
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_image,(x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect( x* TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

#Movimentação Personagem        
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    
    if moving_left:
        player_movement[0] -= 2
    
    player_movement[1] = player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action( player_action, player_frame, 'run' )
        player_flip = False
    
    if player_movement[0] == 0:
        player_action,player_frame = change_action( player_action, player_frame, 'idle' )

    
    if player_movement[0] < 0:
        player_action,player_frame = change_action( player_action, player_frame, 'run' )
        player_flip = True

    player_rect, collisions = move( player_rect, player_movement, tile_rects )
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30 
                random.choice( grass_sounds ).play()
    else:
        air_timer += 1
    

    player_frame += 1
    if player_frame >= len( animation_database[ player_action ] ):
        player_frame = 0
    player_img_id = animation_database[ player_action ][ player_frame ]
    
    player_image = animation_frames[player_img_id]
    display.blit( pygame.transform.flip( player_image, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]) )


    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    Clock.tick(60)