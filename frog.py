import pygame
import random as Random
from pygame.locals import *
from sys import exit

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



##generowanie tła 
sit = True
while sit:
    for event in pygame.event.get():
        if event.type == QUIT:
            sit = False
    screen.blit(background, (0, 0))
    pygame.display.update()

pygame.quit()
