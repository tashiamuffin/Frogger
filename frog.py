import pygame
import random as Random
from pygame.locals import *
from sys import exit
import random


### dodać poziomy

SCREEN_WIDTH = 1102
SCREEN_HEIGHT = 804
WHITE = (255,255,255)
pygame.init()

screen = pygame.display.set_mode((1102,804), 0, 0) ###background ma 1102x804, width, depth 
pygame.display.set_caption('Frogger')
programIcon = pygame.image.load(r'images/zaba.png')
pygame.display.set_icon(programIcon)
##ładowanie obrazków

background = pygame.image.load('images/bg.jpg').convert()
frog_up = pygame.image.load(r'images/zaba.png').convert_alpha()
frog_left = pygame.image.load(r'images/zaba_left.png').convert_alpha()
frog_right = pygame.image.load(r'images/zaba_right.png').convert_alpha()
frpg_down = pygame.image.load(r'images/zaba_down.png').convert_alpha()
car1 = pygame.image.load(r'images/auto1.png').convert_alpha()
car2 = pygame.image.load(r'images/auto2.png').convert_alpha()
car3 = pygame.image.load(r'images/auto3.png').convert_alpha()
car4 = pygame.image.load(r'images/auto4.png').convert_alpha()
car5 = pygame.image.load(r'images/police.png').convert_alpha()
log = pygame.image.load(r'images/lg.png').convert_alpha()
logl = pygame.image.load(r'images/logl.png').convert_alpha()

pygame.mixer.init()

boing = pygame.mixer.Sound(r"images\boing.mp3")
car_crash = pygame.mixer.Sound(r"images\car_crash.mp3")
water_fall = pygame.mixer.Sound(r"images\water_fall.mp3")
game_over = pygame.mixer.Sound(r"images\game_over.wav")
jingle = pygame.mixer.Sound(r"images\jingle.mp3")
pygame.mixer.Sound.set_volume(jingle, 0.1)

file = r"l.txt"

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        # Inicjalizuj klasę bazową Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = frog_up
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.position = [SCREEN_WIDTH/2, SCREEN_HEIGHT - 25]
        self.rect.center = (self.position[0], self.position[1]) #pozycja początkowa
        self.ability = 1 ###umiejętność poruszania się, gdy jest -1 to nie może się ruszać (jest już na górze szczęsliwa i czeka na inne żabki)

    def update(self):
        if self.ability == 1: ##jeśli może się poruszać to
            self.rect.center = (self.position[0],self.position[1])#move in-place

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

        elif self.ability == 0: ## jej ostatni skok na bezpieczne miejsce
            self.rect.center = (self.position[0], self.position[1])#move in-place

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

            self.ability -=1

### ----------------auta---------------
class cars(pygame.sprite.Sprite):
  
    def __init__(self):
        #730, 660, 600, 540, 470
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([car1, car2, car3, car4, car5])
        self.rect = self.image.get_rect()
        self.position = random.choice([[0, 730], [0, 660], [0, 600], [0, 540], [0, 470]])
        self.rect.center = (self.position[0], self.position[1])
        self.x_velocity = 0.5

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: ##gdy wyjdzie poza ekran to znika
            self.kill()

### ------------- kłody -----------

class logsl(pygame.sprite.Sprite): ###kłody płynące w lewo
  
    def __init__(self):
        #360, 300, 240, 180, - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = log
        self.rect = self.image.get_rect()
        self.position = [SCREEN_WIDTH, random.choice([300, 180])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = -0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class logsr(pygame.sprite.Sprite): ###kłody płynące w prawo
  
    def __init__(self):
        #360, 300, 240, 180 - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = logl
        self.rect = self.image.get_rect()
        self.position = [0, random.choice([360,240,120])]
        self.rect.center = (self.position[0], self.position[1])
        self.x_velocity = 0.4

    def update(self):
        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

#-------------------tablice z wynikami------

class LiveBoard(pygame.sprite.Sprite):
    def __init__(self):
        #inicjalizuj klasę bazową
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.text = "lives: %4d" % self.lives
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = (50, 5)

    def update(self):
        self.lives -= 1
        self.text = "Lives: %4d" % self.lives
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = (50, 5)


class WinBoard(pygame.sprite.Sprite):
    def __init__(self,time, text):
        #inicjalizuj klasę bazową
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.text = ("YOU {} with time: %4d s" % int(self.time)).format(text)
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = (300, 410)

class LossBoard(pygame.sprite.Sprite):
    def __init__(self):
        #inicjalizuj klasę bazową
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.text = "YOU LOST :c TRY AGAIN"
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = (300, 410)

class MusicBoard(pygame.sprite.Sprite):
    def __init__(self, text):
        #inicjalizuj klasę bazową
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = (955, 220)

##-----------------funkcje do obsługi pliku do leaderboardu
def leaderboard_top(file):
    try:
        leaderboard_file = open(file, 'r')
        leaderboard = leaderboard_file.readlines()
        leaderboard_file.close()
        lead_list = [int(leaderboard[i][:-1]) for i in range(0, len(leaderboard))]
        lead_list.sort()

        if len(leaderboard) < 5:
            return lead_list
        else:
            return lead_list[:5]
    except FileNotFoundError:
        return []

def leaderboard_add(file, text):
    leaderboard_file = open(file, 'a')
    leaderboard_file.write(text + "\n")
    leaderboard_file.close()
    
## ----------------main -------------
def main():
    frog_sprite = pygame.sprite.RenderClear() #kontener na żabe
    frog = Frog()                       #stwórz żabe
    frog_sprite.add(frog) 

    # Inicjalizuj obiekty
    cars_sprites = pygame.sprite.RenderClear() #kontener dla aut
    cars_sprites.add(cars())
    logs_sprites = pygame.sprite.RenderClear() # kontener dla logs

    ## ilość żyć
    scoreboardSprite = pygame.sprite.RenderClear()
    scoreboardSprite.add(LiveBoard())
    scoreboardSprite.draw(screen)
    pygame.display.flip()

    musicSprite = pygame.sprite.RenderClear()

    ##zmienne
    sit = True
    addenemyfighterCounter = 0
    addlogsl = 0
    addlogsr = 0
    lives = 3
    frogs_arrived = -1
    time = 0
    end_time = 0
    win_am = 1
    music = 1
    #file = r"l.txt"

    while sit:
        ## -------strona startowa ---------------------

        if frogs_arrived == -1: #obsługa muzyki w tle
            if music == 1:
                jingle.play(-1)

            ###zasady, o autorze, exit, leaderboard, konfig
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                    if event.key == pygame.K_RETURN:
                        frogs_arrived += 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    if button.collidepoint(mouse_pos): #przycisk startu
                        frogs_arrived += 1

                    elif ex_but.collidepoint(mouse_pos): #exit
                        sit = False

                    elif music_but.collidepoint(mouse_pos): #muzyka on/off
                        if music == 1:
                            music = 0
                            jingle.stop()
                        elif music == 0:
                            music = 1
                            jingle.play(-1)

                screen.blit(background, (0, 0))
                
                ##obsługa przycisku do muzyki
                if music == 1:
                    off_t = MusicBoard("on")
                    musicSprite.empty()
                    musicSprite.add(off_t)
                            
                elif music == 0:
                    on_t = MusicBoard("off")
                    musicSprite.empty()
                    musicSprite.add(on_t)
                
                ##logo
                frog_im = pygame.image.load(r'images/frogger.png').convert_alpha()
                screen.blit(frog_im, (310, 300))

                ##budowa przycisku start
                button = pygame.Rect(300, 400, 450, 50) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], button)  # draw button
                font = pygame.font.SysFont(None, 24)
                img = font.render('PRESS ENTER OR THIS BUTTON TO START THE GAME', True, (255, 244, 244))
                screen.blit(img, (310, 420))
                
                ###labelki
                font3 = pygame.font.SysFont("comicsansms", 40)
                title = font3.render('LEADERBOARD', True, (0, 50, 50))
                screen.blit(title, (20, 30))

                title = font3.render('AUTHOR:', True, (0, 50, 50))
                screen.blit(title, (820, 30))

                title = font3.render('CONFIG', True, (0, 50, 50))
                screen.blit(title, (820, 150))

                title = font3.render('THE RULES:', True, (255, 221, 0))
                screen.blit(title, (400, 510))

                font4 = pygame.font.SysFont(None, 30)
                title = font4.render('Natalia Lach', True, (0, 100, 100))
                screen.blit(title, (820, 90))

                fontL = pygame.font.SysFont(None, 30)
                title = fontL.render('NORMAL:', True, (0, 50, 50))
                screen.blit(title, (20, 90))

                ##leaderboard:
                leaderboard_list = leaderboard_top(file)
                y = 120
                n = 1
                for i in leaderboard_list:
                    title = font4.render(str(i), True, (0,100,100))
                    screen.blit(title, (50, y))
                    title = font4.render(str(n) + ".", True, (0, 50, 50))
                    screen.blit(title, (30, y))
                    n += 1
                    y += 30
                
                ##zasady
                title = font4.render('This is a classic arcade game, in which your goal is to lead the frog family across the street and river.', True, (200,200,200))
                screen.blit(title, (80, 575))
                title = font4.render('Attention! The frog dies when it is hit by the car or when it falls to the water.', True, (200,200,200))
                screen.blit(title, (150, 610))
                title = font4.render('Once all the five frogs are safe on the lily pads, you win.', True, (200,200,200))
                screen.blit(title, (250, 645))
                title = font4.render('You steer the frog with key arrows.', True, (200,200,200))
                screen.blit(title, (350, 700))

                ##przycisk exit
                ex_but = pygame.Rect(1000, 760, 102, 40) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], ex_but)  # draw button
                font5 = pygame.font.SysFont(None, 40)
                title = font5.render('EXIT', True, (0,100,100))
                screen.blit(title, (1015, 770))

                ##label do muzyki i przycisk
                music_but = pygame.Rect(950, 215, 50, 40) ##left top wifth height
                pygame.draw.rect(screen, [255,255,255], music_but) # draw button
            
                title = font5.render('MUSIC:', True, (0, 100, 100))
                screen.blit(title, (820, 220))
                
                musicSprite.update()
                musicSprite.draw(screen)

                pygame.display.flip()

        #------------------------gra właściwa---------------------
        elif 0 <= frogs_arrived <= 5:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sit = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False

                    elif event.key == K_LEFT:
                        frog.position[0] = frog.position[0] - 60
                        frog.image = frog_left
                        pygame.mixer.Channel(0).play(boing)

                    elif event.key == K_RIGHT:
                        frog.position[0] = frog.position[0] + 60
                        frog.image = frog_right
                        pygame.mixer.Channel(0).play(boing)

                    elif event.key == K_UP:
                        ####gdy żaba jest u samej góry i chce wejść na bezpieczną lilię
                        pygame.mixer.Channel(0).play(boing)
                        if frog.position[1] < 130 and 520<frog.position[0]<570:
                            frog.position[1] = 60
                            frog.position[0] = 545
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frpg_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 150<frog.position[0]<220:
                            frog.position[1] = 60
                            frog.position[0] = 185
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frpg_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 335<frog.position[0]<400:
                            frog.position[1] = 60
                            frog.position[0] = 365
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frpg_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 690<frog.position[0]<760:
                            frog.position[1] = 60
                            frog.position[0] = 725
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frpg_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        elif frog.position[1] < 130 and 880<frog.position[0]<930:
                            frog.position[1] = 60
                            frog.position[0] = 905
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frpg_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        ### zwyczajny ruch w górę
                        elif frog.position[1] > 130:
                            frog.position[1] = frog.position[1] - 60
                            frog.image = frog_up

                    elif event.key == K_DOWN:
                        frog.position[1] = frog.position[1] + 60
                        frog.image = frpg_down
                        pygame.mixer.Channel(0).play(boing)


                screen.blit(background, (0, 0))
                scoreboardSprite.draw(screen)
                frog_sprite.draw(screen)
                pygame.display.update()
            
            ###update liczników do generowania obiektów
            addenemyfighterCounter += 1
            addlogsl += 1
            addlogsr += 1
            time +=1

            ###render aut i logów
            if addenemyfighterCounter >= 300:
                cars_sprites.add(cars())
                cars_sprites.add(cars())
                addenemyfighterCounter = 0

            if addlogsl >= 360:
                logs_sprites.add(logsl())
                addlogsl = 0

            if addlogsr >= 300:
                logs_sprites.add(logsr())
                addlogsr = 0

            
            #Aktualizuj wszystkie sprite'y
            
            cars_sprites.update()
            logs_sprites.update()
            frog_sprite.update()
            
            ### wpadniecie do wody
            if frog.position[1] < 400 and len(pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0)) == 0:
                frog.kill()
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)
                pygame.mixer.Channel(2).play(water_fall)

            ## uderzenie autem
            for hit in pygame.sprite.groupcollide(cars_sprites,frog_sprite,False, True):
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)
                pygame.mixer.Channel(2).play(car_crash)

            ###wejście na kłodę
            for log_travel in pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0):
                frog.position[0] += log_travel.x_velocity
                frog_sprite.update()
                frog_sprite.draw(screen)

            ####wygrana
            if frogs_arrived == 5:
                frogs_arrived +=1
                end_time = pygame.time.get_ticks()
                time_sec = round(end_time/1000)
                leaderboard_add(file, str(time_sec))


            #Wyczyść ekran
            
            cars_sprites.clear(screen, background)
            logs_sprites.clear(screen, background)
            frog_sprite.clear(screen, background)

            #Rysuj sprite'y na ekranie
            cars_sprites.draw(screen)
            logs_sprites.draw(screen)
            frog_sprite.draw(screen)
            
            ###koniec gry
            if lives <= 0:
                    print("Koniec gry")
                    frogs_arrived = 6
                    end_time = pygame.time.get_ticks()
                    win_am = 0

            pygame.display.flip()

        # ------------- poza główną akcją, ekran końcowy-------------
        else:
            cars_sprites.clear(screen, background)
            logs_sprites.clear(screen, background)
            frog_sprite.clear(screen, background)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                    if event.key == pygame.K_RETURN:
                        main()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    if button.collidepoint(mouse_pos): ##restart gry
                        main()

                    if ex_but.collidepoint(mouse_pos): ##wyjście
                        sit = False
                
                ###render wiadomości
                if win_am:
                    win_table = WinBoard(end_time/1000,"WON")
                else:  
                    win_table = LossBoard()
                
                
                ##przycisk restartu
                button = pygame.Rect(300, 480, 420, 50) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], button)  # draw button
                font = pygame.font.SysFont(None, 24)
                img = font.render('PRESS ENTER OR THIS BUTTON TO START AGAIN', True, (255,244,244))
                screen.blit(img, (310, 500))

                ##przycisk wyjścia
                ex_but = pygame.Rect(1000, 760, 102, 40) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], ex_but)  # draw button
                font5 = pygame.font.SysFont(None, 40)
                title = font5.render('EXIT', True, (0, 100, 100))
                screen.blit(title, (1015, 770))

                scoreboardSprite.add(win_table)
                scoreboardSprite.draw(screen)
                                    
                pygame.display.flip()
    

    pygame.quit()

main()

