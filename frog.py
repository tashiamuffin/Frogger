import pygame
import random as Random
from pygame.locals import *
from sys import exit
import random

SCREEN_WIDTH = 1102
SCREEN_HEIGHT = 804
pygame.init()

screen = pygame.display.set_mode((1102,804), 0, 0) ###background ma 1102x804, width, depth 
pygame.display.set_caption('Frogger')
##ładowanie obrazków

background = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\bg.jpg').convert()
frog_up = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
frog_done = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
frog_left = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
frog_right = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
frpg_down = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
car1 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto1.png').convert_alpha()
car2 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto2.png').convert_alpha()
car3 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto3.png').convert_alpha()
car4 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\auto4.png').convert_alpha()
car5 = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\police.png').convert_alpha()
log = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\lg.png').convert_alpha()
logl = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\logl.png').convert_alpha()


class Frog(pygame.sprite.Sprite):
    def __init__(self):
        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.position = [SCREEN_WIDTH/2, SCREEN_HEIGHT - 25]
        self.rect.center = (self.position[0], self.position[1]) #pozycja początkowa
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

###auta
class cars(pygame.sprite.Sprite):
  
    def __init__(self):
        #730, 660, 600, 540, 470
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([car1, car2, car3, car4, car5])
        self.rect = self.image.get_rect()
        self.position = random.choice([[0,730], [0,660], [0,600], [0,540],[0,470]])
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = 0.5

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class logsl(pygame.sprite.Sprite):
  
    def __init__(self):
        #360, 300, 240, 180, - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = log
        self.rect = self.image.get_rect()
        self.position = [SCREEN_WIDTH,random.choice([300,180])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = -0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class logsr(pygame.sprite.Sprite):
  
    def __init__(self):
        #360, 300, 240, 180 - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = logl
        self.rect = self.image.get_rect()
        self.position = [0,random.choice([360,240,120])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = 0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0],self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

frog_sprite = pygame.sprite.RenderClear() #kontener na żabe
frog = Frog()                       #stwórz żabe
frog_sprite.add(frog) 

# Inicjalizuj statki wroga
cars_sprites = pygame.sprite.RenderClear() #kontener dla statków
cars_sprites.add(cars())


logs_sprites = pygame.sprite.RenderClear()


clock = pygame.time.Clock()
##generowanie tła 
sit = True
addenemyfighterCounter = 0
addlogsl = 0
addlogsr = 0
while sit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sit = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                frog.position[0] = frog.position[0] - 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
            elif event.key == K_RIGHT:
                frog.position[0] = frog.position[0] + 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
            elif event.key == K_UP:
                frog.position[1] = frog.position[1] - 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
            elif event.key == K_DOWN:
                frog.position[1] = frog.position[1] + 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                frog.position[0] = frog.position[0] - 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_left.png').convert_alpha()
            elif event.key == K_RIGHT:
                frog.position[0] = frog.position[0] + 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_right.png').convert_alpha()
            elif event.key == K_UP:
                frog.position[1] = frog.position[1] - 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba.png').convert_alpha()
            elif event.key == K_DOWN:
                frog.position[1] = frog.position[1] + 60
                frog.image = pygame.image.load(r'C:\Users\admin\OneDrive\Pulpit\informatyka\gra\zaba_down.png').convert_alpha()
        screen.blit(background, (0, 0))
        frog_sprite.draw(screen)
        pygame.display.update()
    
    addenemyfighterCounter += 1
    addlogsl += 1
    addlogsr += 1

    if addenemyfighterCounter >= 200:
        cars_sprites.add(cars())
        cars_sprites.add(cars())
        addenemyfighterCounter = 0
    if addlogsl >= 350:
        logs_sprites.add(logsl())
        addlogsl = 0
    if addlogsr >= 260:
        logs_sprites.add(logsr())
        addlogsr = 0

    #Aktualizuj wszystkie sprite'y
    frog_sprite.update()
    cars_sprites.update()
    logs_sprites.update()

    #Wyczyść ekran
    frog_sprite.clear(screen, background)
    cars_sprites.clear(screen, background)
    logs_sprites.clear(screen, background)

    #Rysuj sprite'y na ekranie
    frog_sprite.draw(screen)
    cars_sprites.draw(screen)
    logs_sprites.draw(screen)

    pygame.display.flip()
    
pygame.quit()
