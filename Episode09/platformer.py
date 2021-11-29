import pygame, sys
import os, random  
from pygame import display
from pygame import transform
from pygame.display import set_caption
from pygame.locals import *
import data.engine as e

# Trilha de Estudos: Game Developer
# 1) My class: Pygame Tutorial Series (all) 03/32. 
# Current: Aula 03 - 15:00 Min 
# https://www.youtube.com/watch?v=Qdeb1iinNtk&list=PLX5fBCkxJmm3nAalPU6gGfRIFLlghRuYy&index=2

CHUNK_SIZE = 8
def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 #nothing 
            if target_y > 10:
                tile_type = 2 #dirt 
            elif target_y == 10:
                tile_type = 1 # grass 
            elif target_y == 9:
                if random.randint(1,5) == 1: 
                    tile_type = 3 # plant 
            
            if tile_type != 0: 
                chunk_data.append( [[ target_x, target_y ], tile_type] )
    return chunk_data

class jumper_obj():
    def __init__(self, loc):
        self.loc = loc
    
    def render(self, surf, scroll):
        surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect( self.loc[0], self.loc[1], 8, 9 )
    
    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)


dir_entities = os.getcwd() + '\\data\\images\\entities\\'   
print(dir_entities)         
e.load_animations(dir_entities)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() #Inicializar o Pygame. 

Clock = pygame.time.Clock() #Indica o tempo 
#Variaveis 
pygame.display.set_caption("My Pygame Window")
WINDOW_SIZE = (600,400) #Tamanho da tela 
screen = pygame.display.set_mode(WINDOW_SIZE, 0,32) #

display = pygame.Surface((300, 200))

dir_images = os.getcwd() + '\\data\\images\\'
dir_audio = os.getcwd() + '\\data\\audio\\'
print( 'Aqui é o ' + dir_images )

#player_image = pygame.image.load( r'D:\Projects\Pygame\Episode05\assets\player.png')
#player_image = pygame.image.load( 'assets/player.png')
player_image = pygame.image.load( os.path.join( dir_images, 'player.png'))
player_image.set_colorkey((255,255,255))

grass_image = pygame.image.load(os.path.join(dir_images,'grass.png'))
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load(os.path.join(dir_images,'dirt.png'))
plant_image = pygame.image.load( os.path.join( dir_images, 'plant.png' ) ).convert()
plant_image.set_colorkey( (255,255,255) )

jumper_img = pygame.image.load( os.path.join(dir_images, 'jumper.png') ).convert()
jumper_img.set_colorkey((255,255,255))

tile_index = {  1:grass_image,
                2:dirt_image,
                3:plant_image}

jump_sound = pygame.mixer.Sound( os.path.join( dir_audio, 'jump.wav') )
grass_sounds = [pygame.mixer.Sound( os.path.join( dir_audio, 'grass_0.wav' ) ), 
                pygame.mixer.Sound( os.path.join( dir_audio, 'grass_1.wav' ) )]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load( os.path.join( dir_audio,'music.wav' ) )
pygame.mixer.music.play( -1 )
grass_sound_timer = 0

true_scroll = [0,0]

#game_map = load_map(os.path.join(dirAtual,'map'))
game_map = {}

player_location = [50,50]
moving_right = False 
moving_left = False
player_y_momentum = 0
air_timer = 0

player = e.entity(100,100,5,13,'player')

enemies = []
for i in range(5):
    enemies.append( [0,e.entity( random.randint(0,600)-300,80,13,13,'enemy' )] )


background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

jumper_objects = []
for i in range(5):
    jumper_objects.append(jumper_obj( (random.randint(0,600)-300, 110 ) ))

#Loop do Game 
while True:
    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1


# Camera 
    true_scroll[0] += (player.x - true_scroll[0] - 152) /20
    true_scroll[1] += ( player.y - true_scroll[1] -106 ) /20
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


    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x -1 + int( round( scroll[0] / ( CHUNK_SIZE*16 ) ) )
            target_y = y -1 + int( round( scroll[1] / ( CHUNK_SIZE*16 ) ) )
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[ target_chunk ] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]: 
                display.blit( tile_index[tile[1]], ( tile[0][0] * 16 -scroll[0], tile[0][1]*16 -scroll[1] ) )
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16,16,16))

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
        player.set_action('run')
        player.set_flip(False)
        #player_action,player_frame = change_action( player_action, player_frame, 'run' )
        #player_flip = False
    
    if player_movement[0] == 0:
        player.set_action('idle')
        #player_action,player_frame = change_action( player_action, player_frame, 'idle' )

    
    if player_movement[0] < 0:
        player.set_action('run')
        player.set_flip(True)
        #player_action,player_frame = change_action( player_action, player_frame, 'run' )
        #player_flip = True

    collision_types = player.move( player_movement, tile_rects )
    #player_rect, collisions = move( player_rect, player_movement, tile_rects )
    if collision_types['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30 
                random.choice( grass_sounds ).play()
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display,scroll)
    #display.blit( pygame.transform.flip( player_image, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]) )

    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            player_y_momentum = -8
        jumper.loc = [ jumper.loc[0]-0.2, jumper.loc[1] ]

    display_r = pygame.Rect( scroll[0], scroll[1], 300, 200 )
    
    for enemy in enemies:
        if display_r.colliderect( enemy[1].obj.rect ):            
            enemy[0] += 0.2
            enemy_movement = [0,enemy[0]]
            if enemy[0] > 3:
                enemy[0] = 3

            if player.x > enemy[1].x - 5:
                enemy_movement[0] = 1

            if player.x < enemy[1].x + 5:
                enemy_movement[0] = -1 
            collision_types = enemy[1].move( enemy_movement, tile_rects )

            if collision_types['bottom'] == True:
                enemy[0] = 0
            
            enemy[1].display(display,scroll)

            if player.obj.rect.colliderect( enemy[1].obj.rect ):
                player_y_momentum = -4


    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    Clock.tick(60)