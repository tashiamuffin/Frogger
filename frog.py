import pygame
import random as Random
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 1102
SCREEN_HEIGHT = 804
pygame.init()

screen = pygame.display.set_mode((1102,804), 0, 0) ###background ma 1102x804, width, depth 
pygame.display.set_caption('Frogger')
##ładowanie obrazków

background = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\bg.jpg').convert()
frog_up = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\up.png').convert_alpha()
frog_done = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
frog_left = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\lef.png').convert_alpha()
frog_right = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\right.png').convert_alpha()
frpg_down = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\down.png').convert_alpha()
car1 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\car1.png').convert_alpha()
car2 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\car2.png').convert_alpha()
car3 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\car3.png').convert_alpha()
car4 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\car4.png').convert_alpha()
car5 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\car5.png').convert_alpha()
log = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\tronco.png').convert_alpha()


class Frog(pygame.sprite.Sprite):
    def __init__(self):
        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.position = [SCREEN_WIDTH/2,SCREEN_HEIGHT-25]
        self.rect.center = (self.position[0],self.position[1]) #pozycja początkowa
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.rect.center = (self.position[0],self.position[1])#move in-place

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= SCREEN_HEIGHT*1/10: #bez dwóch pasów u góry
            self.rect.top = SCREEN_HEIGHT*1/10
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

frog_sprite = pygame.sprite.RenderClear() #kontener na żabe
frog = Frog()                       #stwórz żabe
frog_sprite.add(frog) 

##generowanie tła 
sit = True
while sit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sit = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                frog.position[0] = frog.position[0]-40
            elif event.key == K_RIGHT:
                frog.position[0] = frog.position[0] + 40
            elif event.key == K_UP:
                frog.position[1] = frog.position[1] - 40
            elif event.key == K_DOWN:
                frog.position[1] = frog.position[1] + 40
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                frog.position[0] = frog.position[0] - 40
            elif event.key == K_RIGHT:
                frog.position[0] = frog.position[0] + 40
            elif event.key == K_UP:
                frog.position[1] = frog.position[1] - 40
            elif event.key == K_DOWN:
                frog.position[1] = frog.position[1] + 40
        screen.blit(background, (0, 0))
        frog_sprite.draw(screen)
        pygame.display.update()
  
    #Aktualizuj wszystkie sprite'y
    frog_sprite.update()

    #Wyczyść ekran
    frog_sprite.clear(screen, background)

    #Rysuj sprite'y na ekranie
    frog_sprite.draw(screen)
pygame.quit()
