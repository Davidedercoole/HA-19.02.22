import pygame
from pygame.draw import circle
from pygame.version import PygameVersion
import os
import random
import math
from math import sin, cos




class Settings:
    window_width = 800    #fenster breite
    window_height = 500   #fenster höhe
    path_file = os.path.dirname(os.path.abspath(__file__)) #dateien pfad
    path_image = os.path.join(path_file, "images")  #bilder pfad
    fps = 60 #wie viele bilder in einer sekunde
    caption = "Rotate" # Titel
   
    (max_speed_negative, max_speed_positive) = (-10,10)




class Background(object):  # kalsse background
    def __init__(self, filename="background03.png") -> None: # background bild auswählen
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen): #malt den background
        screen.blit(self.image, (0, 0))


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.height = 80
        self.width = 50
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "spacecraft.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) #stellt die größe des sprites ein
        self.image_ = pygame.transform.scale(self.image_orig, (64,64))
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = Settings.window_height / 2
        self.speed_x = 0
        self.speed_y = 0


    def update(self):
        self.rand()
        if self.angle >= 360: self.angle = 0
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.speed_x >= 10:
            self.speed_x = 10
        if self.speed_y >= 10:
            self.speed_y = 10


    def rand(self):     
        if self.angle >= 360: self.angle = 0
        if self.speed_x <= Settings.max_speed_negative: self.speed_x = Settings.max_speed_negative
        elif self.speed_x >= Settings.max_speed_positive: self.speed_x = Settings.max_speed_positive
        if self.speed_y <= Settings.max_speed_negative: self.speed_y = Settings.max_speed_negative
        elif self.speed_y >= Settings.max_speed_positive: self.speed_y = Settings.max_speed_positive
        self.rect.move_ip(self.speed_x, self.speed_y)
        
        if self.rect.bottom <= 0: 
            self.rect.centery += Settings.window_height
            
        if self.rect.right <= 0: 
            self.rect.centerx += Settings.window_width
            
        if self.rect.left >= Settings.window_width: 
            self.rect.centery -= Settings.window_height
            
        if self.rect.top >= Settings.window_height: 
            self.rect.centerx -= Settings.window_height

        

    def draw(self, screen):
        
        screen.blit(self.image, self.rect)

    def RotateL(self):
        self.old_center = self.rect.center
        self.angle += 22.5
        self.image_rotated = pygame.transform.rotate(self.image_,self.angle)
        self.image = self.image_rotated
        self.rect = self.image.get_rect()
        self.rect.center=self.old_center


    def RotateR(self):
        self.old_center = self.rect.center
        self.angle -= 22.5
        self.image_rotated = pygame.transform.rotate(self.image_,self.angle)
        self.image = self.image_rotated
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center


    def gummigeben(self):
        self.rech()
        self.speed_x = self.speed_x - sin(self.grad_rech)
        self.speed_y = self.speed_y - cos(self.grad_rech)

        
    
    def rech(self):
        self.grad_rech = 0
        self.grad_rech = (math.pi/180) * self.angle

    def bremse(self):
        self.speed_x = 0
        self.speed_y = 0






class Astroid(pygame.sprite.Sprite): # The astroids kinda but metalscrap
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "asteroid.png")).convert_alpha()
        self.size = 64
        self.image = pygame.transform.scale(self.image_original, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(80, Settings.window_height - 80)
        self.rect.centerx = random.randint(80, Settings.window_width - 80)
        self.speed_x = 3
        self.speed_y = 3
        self.speed_x_ = random.randint(1,self.speed_x)
        self.speed_y_ = random.randint(1, self.speed_y)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
    def update(self):
        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0
        self.rect.move_ip(self.speed_x_, self.speed_y_)






class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.players = pygame.sprite.GroupSingle() # erstellt die einzel gruppe players
        self.player = Player()
        self.astroids = pygame.sprite.Group() # erstellt die gruppe astroids
        self.astroid = Astroid()
        self.spawn_timer = Timer(3000)



    def run(self):
        
        self.running = True
        self.start()
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            self.collide()            
        pygame.quit()

    def collide(self):
        if pygame.sprite.groupcollide(self.astroids, self.players, False, False):
            self.running = False




    def watch_for_events(self): #hier wird festgellegt was bei welchen tasten druck passiert
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.player.RotateL()
                elif event.key== pygame.K_RIGHT:
                    self.player.RotateR()
                elif event.key == pygame.K_UP:
                    self.player.gummigeben() 
                elif event.key == pygame.K_r:
                    self.spawn()       
                elif event.key == pygame.K_SPACE:
                    self.player.bremse()
                    




    def update(self):
        self.player.update()
        self.astroids.update()
        if len(self.astroids.sprites()) < 5 and self.spawn_timer.is_next_stop_reached():             
            self.astroids.add(Astroid())

    def draw(self): #erstellt die einzeln objekte auf dem bildschirm
            self.background.draw(self.screen)
            self.player.draw(self.screen)
            self.astroids.draw(self.screen)
            pygame.display.flip()

    def start(self):
        self.background = Background()
        self.spawn()
       


    def spawn(self):# spawnt den spieler 
        self.players.add(Player())






if __name__ == "__main__":
    
    game = Game()
    game.run()