import pygame
import random 
from pygame.locals import *

SCREEN_WIDTH = 1102
SCREEN_HEIGHT = 804
pygame.init()

screen = pygame.display.set_mode((1102,804), 0, 0) ###background ma 1102x804, width, depth 
pygame.display.set_caption('Frogger')
programIcon = pygame.image.load(r'images/zaba1.png')
pygame.display.set_icon(programIcon)
##ładowanie obrazków

background = pygame.image.load('images/bg.jpg').convert()
frog_up = pygame.image.load(r'images/zaba1.png').convert_alpha()
frog_left = pygame.image.load(r'images/zaba_left1.png').convert_alpha()
frog_right = pygame.image.load(r'images/zaba_right1.png').convert_alpha()
frog_down = pygame.image.load(r'images/zaba_down1.png').convert_alpha()
car1 = pygame.image.load(r'images/auto1.png').convert_alpha()
car2 = pygame.image.load(r'images/auto2.png').convert_alpha()
car3 = pygame.image.load(r'images/auto3.png').convert_alpha()
car4 = pygame.image.load(r'images/auto4.png').convert_alpha()
car5 = pygame.image.load(r'images/police.png').convert_alpha()
log = pygame.image.load(r'images/lg.png').convert_alpha()
logl = pygame.image.load(r'images/logl.png').convert_alpha()

pygame.mixer.init()

boing = pygame.mixer.Sound(r"sounds\boing.mp3")
car_crash = pygame.mixer.Sound(r"sounds\car_crash.mp3")
water_fall = pygame.mixer.Sound(r"sounds\water_fall.mp3")
game_over = pygame.mixer.Sound(r"sounds\game_over.wav")
jingle = pygame.mixer.Sound(r"sounds\jingle.mp3")
pygame.mixer.Sound.set_volume(jingle, 0.1)

file = "level1.txt"
file2 = "level2.txt"
file3 = "level3.txt"


class Frog(pygame.sprite.Sprite):
    """a class that creates a Frog - the main movable object in a game"""

    def __init__(self):
        """ function initializing the frog """
        
        pygame.sprite.Sprite.__init__(self)
        self.image = frog_up
        self.rect = self.image.get_rect() #rozmiar rysunku
        self.position = [SCREEN_WIDTH/2, SCREEN_HEIGHT - 25]
        self.rect.center = (self.position[0], self.position[1]) #pozycja początkowa
        self.ability = 1 ###umiejętność poruszania się, gdy jest -1 to nie może się ruszać (jest już na górze szczęsliwa i czeka na inne żabki)

    def update(self):
        """ a function updating a location of a frog """

        if self.ability == 1: ##jeśli może się poruszać to
            self.rect.center = (self.position[0],self.position[1])

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

### ----------------auta--------------------
# predkosc normal - 0.5
class cars(pygame.sprite.Sprite):
    """ a class that creates a moving car that can kill the frog"""

    def __init__(self, velocity):
        """ a function initializing the car
        :param velocity (float): a velocity of the car
        """

        #730, 660, 600, 540, 470 - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([car1, car2, car3, car4, car5])
        self.rect = self.image.get_rect()
        self.position = random.choice([[0, 730], [0, 660], [0, 600], [0, 540], [0, 470]])
        self.rect.center = (self.position[0], self.position[1])
        self.x_velocity = velocity

    def update(self):
        """a function updating the location of the car"""

        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: ##gdy wyjdzie poza ekran to znika
            self.kill()

### ------------- kłody -----------

class logsl(pygame.sprite.Sprite): ###kłody płynące w lewo - predkosc -0.4
    """a class that creates a log floating to the left"""
  
    def __init__(self, velocity):
        """ a function initializing the log
        :param velocity (float): a velocity of the log
        """

        #360, 300, 240, 180, - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = log
        self.rect = self.image.get_rect()
        self.position = [SCREEN_WIDTH, random.choice([300, 180])]
        self.rect.center = (self.position[0],self.position[1])
        self.x_velocity = -velocity

    def update(self):
        """a function updating the location of the log"""

        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class logsr(pygame.sprite.Sprite): ###kłody płynące w prawo - predkosc 0.4 na normal
    """a class that creates a log floating to the right"""
  
    def __init__(self, velocity):
        """ a function initializing the log
        :param velocity (float): a velocity of the log
        """

        #360, 300, 240, 180 - pasy
        pygame.sprite.Sprite.__init__(self)
        self.image = logl
        self.rect = self.image.get_rect()
        self.position = [0, random.choice([360, 240, 120])]
        self.rect.center = (self.position[0], self.position[1])
        self.x_velocity = velocity

    def update(self):
        """a function updating the location of the log"""

        self.position[0] += self.x_velocity
        self.rect.center = (self.position[0], self.position[1])#move in-place
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

#-------------------tablice z wynikami------

class LiveBoard(pygame.sprite.Sprite):
    """a class that creates a widget showing amount of lives"""

    def __init__(self):
        """a function initializing the widget"""

        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.text = "Lives: %4d" % self.lives
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, (0,0,0))
        self.rect = (50, 5)

    def update(self):
        """a function updating the amount of lives"""
        
        self.lives -= 1
        self.text = "Lives: %4d" % self.lives
        self.image = self.font.render(self.text, 1, (0,0,0))
        self.rect = (50, 5)


class WinBoard(pygame.sprite.Sprite):
    """a class that creates a widget showing a score if there was a win"""

    def __init__(self,time, text):
        """a function initializing the widget
        :param text (str): a text - time score
        """

        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.text = ("YOU {} with time: %4d s" % int(self.time)).format(text)
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, (255,255,255))
        self.rect = (300, 410)

class LossBoard(pygame.sprite.Sprite):
    """a class that creates a widget showing a score if there was a loss"""

    def __init__(self):
        """a function initializing the widget"""

        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.text = "YOU LOST :c TRY AGAIN"
        self.font = pygame.font.SysFont(None, 50)
        self.image = self.font.render(self.text, 1, (255,255,255))
        self.rect = (300, 410)


class MusicBoard(pygame.sprite.Sprite):
    """a class that creates a widget for handling music configurations"""

    def __init__(self, text):
        """ a function initializing the widget
        :param text (str): a text to display
        """

        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = (955, 220)

class LevelBoard(pygame.sprite.Sprite):
    """a class that creates a widget for handling level configurations"""

    def __init__(self, text, place):
        """ a function initializing the widget
        :param text (str): a text to display
        :param place (tuple): a place to display the text
        """

        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = place

##-----------------funkcje do obsługi pliku do leaderboardu
def leaderboard_top(file):
    """a function that returns a list with top five scores from a given file
    :param file (str): a path to the file with the scores
    """

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
    """"a function adding a given score to the given file
    :param file (str): a path to the file with scores
    :param text (str): a score 
    """

    leaderboard_file = open(file, 'a')
    leaderboard_file.write(text + "\n")
    leaderboard_file.close()
    
def leaderboard_update(x, y, top_list):
    """a function that displays the top 5 scores on the screen
    :param x (int): an x location
    :param y (int): a y location
    :param top_list (list): a list with the scores
    """

    font4 = pygame.font.SysFont(None, 30)
    n = 1
    for i in top_list:
        title = font4.render(str(i), True, (0,100,100))
        screen.blit(title, (x, y))
        title = font4.render(str(n) + ".", True, (0, 50, 50))
        screen.blit(title, (x - 20, y))
        n += 1
        y += 30

        
## -----------------------------------main -------------------------------------------
def main():
    """a main function handling the whole game"""

    frog_sprite = pygame.sprite.RenderClear() #kontener na żabe
    frog = Frog()                       #stwórz żabe
    frog_sprite.add(frog) 

    # Inicjalizuj obiekty
    cars_sprites = pygame.sprite.RenderClear() #kontener dla aut
    logs_sprites = pygame.sprite.RenderClear() # kontener dla logs

    ## ilość żyć
    scoreboardSprite = pygame.sprite.RenderClear()
    scoreboardSprite.add(LiveBoard())
    scoreboardSprite.draw(screen)
    pygame.display.flip()

    musicSprite = pygame.sprite.RenderClear()
    levelSprite = pygame.sprite.RenderClear()

    ##-------zmienne---------
    sit = True
    addcars = 0
    addlogsl = 0
    addlogsr = 0
    lives = 3
    frogs_arrived = -1
    start_time = 0
    end_time = 0
    final_time = 0
    win_am = 1
    music = 1
    level = 2

    while sit:

        ## -------strona startowa ------------------------
        if frogs_arrived == -1: #obsługa muzyki w tle
            if music == 1:
                jingle.play(-1)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sit = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sit = False
                    if event.key == pygame.K_RETURN:
                        frogs_arrived += 1
                        start_time = pygame.time.get_ticks()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    if button.collidepoint(mouse_pos): #przycisk startu
                        frogs_arrived += 1
                        start_time = pygame.time.get_ticks()

                    elif ex_but.collidepoint(mouse_pos): #exit
                        sit = False

                    elif music_but.collidepoint(mouse_pos): #muzyka on/off
                        if music == 1:
                            music = 0
                            jingle.stop()
                        elif music == 0:
                            music = 1
                            jingle.play(-1)

                    elif level_but_1.collidepoint(mouse_pos):
                        level = 1
                    elif level_but_2.collidepoint(mouse_pos):
                        level = 2
                    elif level_but_3.collidepoint(mouse_pos):
                        level = 3
            
                screen.blit(background, (0, 0))
                
                ##-----------obsługa przycisku do muzyki----------
                if music == 1:
                    off_t = MusicBoard("on")
                    musicSprite.empty()
                    musicSprite.add(off_t)
                            
                elif music == 0:
                    on_t = MusicBoard("off")
                    musicSprite.empty()
                    musicSprite.add(on_t)
                
                ##-------------obsługa poziomów----------------
                if level == 1:
                    on_level = LevelBoard("on", (955,270))
                    levelSprite.empty()
                    levelSprite.add(on_level)
                elif level == 2:
                    on_level = LevelBoard("on", (955,315))
                    levelSprite.empty()
                    levelSprite.add(on_level)
                elif level == 3:
                    on_level = LevelBoard("on", (955,360))
                    levelSprite.empty()
                    levelSprite.add(on_level)

                ##----------logo------------
                frog_im = pygame.image.load(r'images/frogger.png').convert_alpha()
                screen.blit(frog_im, (310, 300))

                ##---------budowa przycisku start-------------
                button = pygame.Rect(300, 400, 450, 50) ##left top wifth height
                pygame.draw.rect(screen, [0, 0, 0], button)  # draw button
                font = pygame.font.SysFont(None, 24)
                img = font.render('PRESS ENTER OR THIS BUTTON TO START THE GAME', True, (255, 244, 244))
                screen.blit(img, (310, 420))
                
                ###--------------labelki----------------
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
                title = fontL.render('EASY:', True, (0, 50, 50))
                screen.blit(title, (20, 90))
                title = fontL.render('NORMAL:', True, (0, 50, 50))
                screen.blit(title, (120, 90))
                title = fontL.render('HARD:', True, (0, 50, 50))
                screen.blit(title, (230, 90))
                
                #------- leaderboard-------
                leaderboard_update(150, 120, leaderboard_top(file2))
                leaderboard_update(50, 120, leaderboard_top(file))
                leaderboard_update(260, 120, leaderboard_top(file3))
                
                ##-----------zasady--------------
                title = font4.render('This is a classic arcade game, in which your goal is to lead the frog family across the street and river.', True, (200,200,200))
                screen.blit(title, (80, 575))
                title = font4.render('Attention! The frog dies when it is hit by the car or when it falls to the water.', True, (200,200,200))
                screen.blit(title, (150, 610))
                title = font4.render('Once all the five frogs are safe on the lily pads, you win.', True, (200,200,200))
                screen.blit(title, (250, 645))
                title = font4.render('You steer the frog with key arrows.', True, (200,200,200))
                screen.blit(title, (350, 700))

                ##-----------przycisk exit---------
                ex_but = pygame.Rect(1000, 760, 102, 40) 
                pygame.draw.rect(screen, [0, 0, 0], ex_but) 
                font5 = pygame.font.SysFont(None, 40)
                title = font5.render('EXIT', True, (0,100,100))
                screen.blit(title, (1015, 770))

                ##-------------label do muzyki i przycisk--------------
                music_but = pygame.Rect(950, 215, 50, 40)
                pygame.draw.rect(screen, [255,255,255], music_but)
                
                #-----------przyciski do poziomów---------------
                level_but_1 = pygame.Rect(950, 265, 50, 40) 
                pygame.draw.rect(screen, [255,255,255], level_but_1)
                level_but_2 = pygame.Rect(950, 310, 50, 40)
                pygame.draw.rect(screen, [255,255,255], level_but_2)
                level_but_3 = pygame.Rect(950, 355, 50, 40)
                pygame.draw.rect(screen, [255,250,255], level_but_3) 
            
                title = font5.render('MUSIC:', True, (0, 100, 100))
                screen.blit(title, (820, 220))
                title = font5.render('Level 0', True, (0, 100, 100))
                screen.blit(title, (820, 270))
                title = font5.render('Level 1', True, (0, 100, 100))
                screen.blit(title, (820, 315))
                title = font5.render('Level 2', True, (0, 100, 100))
                screen.blit(title, (820, 360))
                
                #----------update sprite'ów------------------
                musicSprite.update()
                levelSprite.update()
                musicSprite.draw(screen)
                levelSprite.draw(screen)

                pygame.display.flip()

        #------------------------gra właściwa-----------------------------------
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
                        if frog.position[1] < 130 and 520 < frog.position[0] < 570:
                            frog.position[1] = 60
                            frog.position[0] = 545
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frog_down
                            frog = Frog()
                            frog_sprite.add(frog) 

                        elif frog.position[1] < 130 and 150 < frog.position[0] < 220:
                            frog.position[1] = 60
                            frog.position[0] = 185
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frog_down
                            frog = Frog()
                            frog_sprite.add(frog) 

                        elif frog.position[1] < 130 and 335 < frog.position[0] < 400:
                            frog.position[1] = 60
                            frog.position[0] = 365
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frog_down
                            frog = Frog()
                            frog_sprite.add(frog) 

                        elif frog.position[1] < 130 and 690<frog.position[0] < 760:
                            frog.position[1] = 60
                            frog.position[0] = 725
                            frog.ability = 0
                            frogs_arrived +=1
                            frog.image = frog_down
                            frog = Frog()
                            frog_sprite.add(frog) 

                        elif frog.position[1] < 130 and 880 < frog.position[0] < 930:
                            frog.position[1] = 60
                            frog.position[0] = 905
                            frog.ability = 0
                            frogs_arrived += 1
                            frog.image = frog_down
                            frog = Frog()
                            frog_sprite.add(frog) 
                        ### zwyczajny ruch w górę
                        elif frog.position[1] > 130:
                            frog.position[1] = frog.position[1] - 60
                            frog.image = frog_up

                    elif event.key == K_DOWN:
                        frog.position[1] = frog.position[1] + 60
                        frog.image = frog_down
                        pygame.mixer.Channel(0).play(boing)


                screen.blit(background, (0, 0))
                scoreboardSprite.draw(screen)
                frog_sprite.draw(screen)
                pygame.display.update()
            
            ###-----------update liczników do generowania obiektów----------
            addcars += 1
            addlogsl += 1
            addlogsr += 1

            ###---------render aut i logów w zależności od poziomu-------
            if level == 2:
                if addcars >= 300:
                    cars_sprites.add(cars(0.5))
                    cars_sprites.add(cars(0.5))
                    addcars = 0

                if addlogsl >= 360:
                    logs_sprites.add(logsl(0.4))
                    addlogsl = 0

                if addlogsr >= 300:
                    logs_sprites.add(logsr(0.4))
                    addlogsr = 0

            elif level == 1:
                if addcars >= 450:
                    cars_sprites.add(cars(0.4))
                    cars_sprites.add(cars(0.4))
                    addcars = 0

                if addlogsl >= 360:
                    logs_sprites.add(logsl(0.3))
                    addlogsl = 0

                if addlogsr >= 350:
                    logs_sprites.add(logsr(0.3))
                    addlogsr = 0

            elif level == 3:
                if addcars >= 200:
                    cars_sprites.add(cars(0.6))
                    cars_sprites.add(cars(0.6))
                    addcars = 0

                if addlogsl >= 360:
                    logs_sprites.add(logsl(0.5))
                    addlogsl = 0

                if addlogsr >= 350:
                    logs_sprites.add(logsr(0.5))
                    addlogsr = 0
            
            #----------Aktualizuj wszystkie sprite'y-------------
            
            cars_sprites.update()
            logs_sprites.update()
            frog_sprite.update()
            
            ### -----------wpadniecie do wody-----------------
            if frog.position[1] < 400 and len(pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0)) == 0:
                frog.kill()
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)
                pygame.mixer.Channel(2).play(water_fall)

            ## -----uderzenie autem--------------
            for hit in pygame.sprite.groupcollide(cars_sprites,frog_sprite,False, True):
                frog = Frog()
                lives -= 1
                frog_sprite.add(frog)
                scoreboardSprite.update()
                scoreboardSprite.clear(screen, background)
                scoreboardSprite.draw(screen)
                pygame.mixer.Channel(2).play(car_crash)

            ###---------------wejście na kłodę------------------
            for log_travel in pygame.sprite.groupcollide(logs_sprites, frog_sprite, 0, 0):
                frog.position[0] += log_travel.x_velocity
                frog_sprite.update()
                frog_sprite.draw(screen)

            ####---------------wygrana-------------
            if frogs_arrived == 5:
                frogs_arrived +=1
                end_time = pygame.time.get_ticks()
                final_time = end_time - start_time

                time_sec = round(final_time/1000)

                if level == 1:
                    leaderboard_add(file, str(time_sec))
                elif level == 2:
                    leaderboard_add(file2, str(time_sec))
                elif level == 3:
                    leaderboard_add(file3, str(time_sec))

            #---------Wyczyść ekran--------------
            
            cars_sprites.clear(screen, background)
            logs_sprites.clear(screen, background)
            frog_sprite.clear(screen, background)

            #-----------Rysuj sprite'y na ekranie----------------
            cars_sprites.draw(screen)
            logs_sprites.draw(screen)
            frog_sprite.draw(screen)
            
            ###--------------koniec gry-----------------
            if lives <= 0:
                    pygame.mixer.Channel(2).play(game_over)
                    frogs_arrived = 6
                    win_am = 0

            pygame.display.flip()

        # -------------poza główną akcją, ekran końcowy---------------------------
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
                
                ###------------render wiadomości-----------
                if win_am:
                    win_table = WinBoard(final_time/1000, "WON")
                else:  
                    win_table = LossBoard()
                
                
                ##---------------przycisk restartu-------
                button = pygame.Rect(300, 480, 420, 50) 
                pygame.draw.rect(screen, [0, 0, 0], button) 
                font = pygame.font.SysFont(None, 24)
                img = font.render('PRESS ENTER OR THIS BUTTON TO START AGAIN', True, (255,244,244))
                screen.blit(img, (310, 500))

                ##------------przycisk wyjścia----------------
                ex_but = pygame.Rect(1000, 760, 102, 40) 
                pygame.draw.rect(screen, [0, 0, 0], ex_but)  
                font5 = pygame.font.SysFont(None, 40)
                title = font5.render('EXIT', True, (0, 100, 100))
                screen.blit(title, (1015, 770))

                scoreboardSprite.add(win_table)
                scoreboardSprite.draw(screen)
                                    
                pygame.display.flip()
    

    pygame.quit()

main()

