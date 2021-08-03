import pygame 
from pygame.locals import *
from sys import exit

## Iniciando o Game
pygame.init()

largura = 640
altura = 480


tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Meu primeiro jogo")

while True: 
### Checa se algum evento ocorreu. 
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
    
    #Desenhar retângulo: 
    pygame.draw.rect(tela, (255,0,0), (200,300,40,50))
    #Desenhar circulo:
    pygame.draw.circle(tela, (0,0,255), (300,260), 40) 
    #Desenhar circulo:
    pygame.draw.line(tela, (255,255,0), (390,0), (390,600), 5)
    
    
    
    pygame.display.update()



    