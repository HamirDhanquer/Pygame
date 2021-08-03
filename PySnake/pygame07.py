import pygame 
from pygame.locals import *
from sys import exit
from random import randint


##### Aula 07 - Sons e Música. 
##### Link: https://www.youtube.com/watch?v=oppoAp5yuv4&list=PLJ8PYFcmwFOxtJS4EZTGEPxMEo4YdbxdQ&index=6

## Iniciando o Game
pygame.init()

pygame.mixer.music.set_volume(3)
musica_de_fundo = pygame.mixer.music.load('BoxCat Games - Battle (Boss).mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('smw_egg_hatching.wav')
barulho_colisao.set_volume(9)

largura = 640
altura = 480
x = largura/2
y = altura/2
x_blue = randint(40,600)
y_blue = randint(50,430)
pontos = 0

font = pygame.font.SysFont('arial',40,True,True)
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Meu primeiro jogo")
relogio = pygame.time.Clock()

while True: 
    relogio.tick(10)
    tela.fill((0,0,0))
    msg = f'Pontos: {pontos}'
    texto = font.render(msg,True, (255,255,255))
### Checa se algum evento ocorreu. 
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
        
        '''
        if event.type == KEYDOWN:
            if event.key == K_a:
                x = x -20
            if event.key == K_d:
                x = x + 20
            if event.key == K_w:
                y = y - 20
            if event.key == K_s:
                y = y + 20
        '''
    if pygame.key.get_pressed()[K_a]:
        x = x -20
    if pygame.key.get_pressed()[K_d]:
        x = x +20
    if pygame.key.get_pressed()[K_s]:
        y = y +20
    if pygame.key.get_pressed()[K_w]:
        y = y -20
    
    #Desenhar retângulo: 
    soldier_red = pygame.draw.rect(tela, (255,0,0), (x,y,40,50))
    soldier_blue = pygame.draw.rect(tela, (0,0,255), (x_blue,y_blue,40,50))
    
    if soldier_red.colliderect(soldier_blue):
        x_blue = randint(40,600)
        y_blue = randint(50,430)
        pontos = pontos +1
        barulho_colisao.play()
    
    tela.blit(texto, (450,40))
    pygame.display.update()
    