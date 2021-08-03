import pygame 
from pygame.locals import *
from sys import exit


##### Aula 04 
##### Link: https://www.youtube.com/watch?v=oppoAp5yuv4&list=PLJ8PYFcmwFOxtJS4EZTGEPxMEo4YdbxdQ&index=6

## Iniciando o Game
pygame.init()

largura = 640
altura = 480
x = largura/2
y = altura/2


tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Meu primeiro jogo")
relogio = pygame.time.Clock()

while True: 
    relogio.tick(10)
    tela.fill((0,0,0))
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
        x = x +20
    if pygame.key.get_pressed()[K_d]:
        x = x -20
    if pygame.key.get_pressed()[K_s]:
        y = y +20
    if pygame.key.get_pressed()[K_w]:
        y = y -20
    
    #Desenhar retângulo: 
    pygame.draw.rect(tela, (255,0,0), (x,y,40,50))
    
    
    
    pygame.display.update()
    