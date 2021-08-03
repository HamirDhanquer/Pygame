import pygame 
from pygame.locals import *
from sys import exit

## Iniciando o Game
pygame.init()

largura = 640
altura = 480
x = largura/2
y = 0


tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Meu primeiro jogo")
relogio = pygame.time.Clock()

while True: 
    relogio.tick(90)
    tela.fill((0,0,0))
### Checa se algum evento ocorreu. 
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
    
    #Desenhar retângulo: 
    pygame.draw.rect(tela, (255,0,0), (x,y,40,50))
    if y >= altura:
        y = 0
    y = y + 1
    
    
    
    pygame.display.update()
    