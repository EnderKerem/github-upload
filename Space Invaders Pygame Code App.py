import  pygame # : Importing Pygame//
import time # : Operate Time//
import random  # :Random Number Generations//
from pygame import mixer # Mixer For Background Music//
pygame.font.init() # Font For Bars//

"""              Hello ! Welcome To My Underwater Space Invaders Game !    """
"""              Code Written By: ---> Ender Kerem Yemeniciler <---:          """
"""              Google Project  Document Link : -->     https://docs.google.com/document/d/1dzNqQJcByCjrWTXU33f9fsIb4uJo0Zwv0AJwpkmXZmE/edit  """                                                                    
"""              Sources/Bibliography:  PygameTutorial:https://www.youtube.com/watch?v=jO6qQDNa2UY&t=4599s  <--AND -->   PygameSpaceInvaders:https://www.youtube.com/watch?v=o-6pADy5Mdg&t=150s   """
"""             Music Creator -> Alexander Nakara<- : Link : https://www.free-stock-music.com/alexander-nakarada-space-ambience.html  """

#Set Widht / Height For Window//
WIDHT = 1000
HEIGHT = 800
GAME_SCREEN = pygame.display.set_mode((WIDHT,HEIGHT))
pygame.display.set_caption(" UnderWater SpaceWorld Shooter ")  
#Mp3 Music Setting//
mixer.init()
mixer.music.load("alexander-nakarada-space-ambience.mp3") #Mp3 Audio File(Space Music)//
mixer.music.set_volume(5)
mixer.music .play()
# Import Images//
# Main User Ship//
Main_Space_Submarine = pygame.image.load("Mainship1-removebg-preview_ccexpress.png")
#For Main Blue Ship = Mainship1-removebg-preview_ccexpress.png
#For 2nd Main Ship = 2ND_MAIN_SHIP-removebg-preview_ccexpress.png
# Enemy Ships//
Enemy1_Space_Submarine = pygame.image.load("yellow_pixel_art_ufo_enemy_1-removebg-preview_ccexpress.png")
Enemy2_Space_Submarine = pygame.image.load("Blue_EnemySpaceship2-removebg-preview_ccexpress.png")
Enemy3_Space_Submarine = pygame.image.load("Green_pixel_art_ufo_enemy_3-removebg-preview_ccexpress.png")

# Pixel Laser Beam For All Ships// 
Red_Laser_Space_Submarine = pygame.image.load("Lazer1-removebg-preview_ccexpress.png")  #Red Laser For MainShip Only//
Blue_Laser_Space_Submarine = pygame.image.load("blue_lazer_beam_-removebg-preview_ccexpress.png")  #Blue Laser For Enemy2//
Green_Laser_Space_Submarine = pygame.image.load("Greenlazer-removebg-preview_ccexpress.png") #Green Laer For Enemy3//
Yellow_Laser_Space_Submarine = pygame.image.load("yellow_laser_pixel_art-removebg-preview_ccexpress.png") #Yellow Laser For Enemy1//

# Background Asset//
Background_Space_Submarine = pygame.transform.scale(pygame.image.load("MainBackgroundsea.png"),  (WIDHT,HEIGHT))

#  >>>>>>>>  BACKGROUND AND IMPORTATION OF ASSETS <<<<<<<< #

#Object Classes//

class Beam:
    def __init__ (self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    def move(self, vel):
        self.y+= vel
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    def collision(self,obj):
        return collide(obj,self)
    
class SUBMARINE:
    COOLDOWN = 30
    def __init__(self, x, y,  healths = 100):
        self.x = x
        self.y = y
        self.healths = healths
        self.mainship_img = None
        self.beam_img = None
        self.lasers = []
        self.retreive_shooting = 0
    """  Parent Ship Class Above:-> <-:Deparent User Class Bottom  """
    # Functions For  """ WIDTH & HEIGHT  """ To Set Constant Grid//
    def draw(self, window):
        window.blit(self.mainship_img, (self.x, self.y ))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.healths -= 10
                self.lasers.remove(laser)
            
    def cooldown(self):
        if self.retreive_shooting >= self.COOLDOWN:
            self.retreive_shooting = 0
        elif self.retreive_shooting >0:
            self.retreive_shooting+=1
        
    def shoot(self):
        if self.retreive_shooting ==0:
            laser = Beam(self.x,self.y, self.beam_img)
            self.lasers.append(laser)
            self.retreive_shooting = 1

    def get_width(self):
        return self.mainship_img.get_width()
    def get_height(self):
        return self.mainship_img.get_height()
        
class User(SUBMARINE):
    def __init__(self,x,y, healths=200):
        super().__init__(x,y,health)
        self.mainship_img = Main_Space_Submarine
        self.beam_img = Red_Laser_Space_Submarine
        self.mask = pygame.mask.from_surface(self.mainship_img)
        self.full_health = healths 
    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
    def healthbar(self,window):
        pygame.draw.rect(window, (124,252,0), (self.x,self.y + self.mainship_img.get_height() + 10, self.mainship_img.get_width(), 10))
        pygame.draw.rect(window, (255,0,0), (self.x,self.y + self.mainship_img.get_height() + 10, self.mainship_img.get_width() * (self.healths/self.full_health), 10))


class Enemy(SUBMARINE):
    COLOR_MAP = {
                                        "blue": (Enemy2_Space_Submarine, Blue_Laser_Space_Submarine),
                                        "green":(Enemy3_Space_Submarine,Green_Laser_Space_Submarine),
                                        "yellow":(Enemy1_Space_Submarine,Yellow_Laser_Space_Submarine)
                                        }
    def __init__(self, x,y, color, healths=100):
        super().__init__(x,y,healths)
        self.mainship_img, self.beam_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.mainship_img)

    def move(self, vel):
        self.y+=vel

    def shoot(self):
        if self.retreive_shooting ==0:
            laser = Beam(self.x+30,self.y+30, self.beam_img)
            self.lasers.append(laser)
            self.retreive_shooting = 1
        
def  collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
# Fps Setting//
#Acc Function To Set Window//
acc = True
FPS = 70
health= 5
level = 0
Correct_font = pygame.font.SysFont("Inconsolata",55)
lost_font = pygame.font.SysFont("Inconsolata",70)
enemies = []
wave_length = 5
enemy_vel = 1
user_velocity = 5 #Velocity//
laser_velocity = 4
user  =  User(430,  680) #User Location//
clock = pygame.time.Clock()
lost =  False
lost_count = 0
# Correct Function //
def  Correct():
    return true
   
def  redraw_window():
    GAME_SCREEN.blit(Background_Space_Submarine,  (0,0))
    # Healt_Label_Color  = Maroon RGB ==128,0,0
    health_label = Correct_font.render(f"Health: {health}", 1, (128,0,0))
    # Level_Label_Color = Peacock  RGB  == 51,161,201
    level_label = Correct_font.render(f"Level: {level}", 1, (51,161,201))
    GAME_SCREEN.blit(health_label,  (10,10))
    GAME_SCREEN.blit(level_label,  (WIDHT - level_label.get_width() - 10, 10))
    for enemy in enemies:
        enemy.draw(GAME_SCREEN)

    user.draw(GAME_SCREEN)
    if lost:
        lost_label = lost_font.render("Game Lost !", 1,(128,0,0))
        GAME_SCREEN.blit(lost_label,(WIDHT/2 - lost_label.get_width()/2, 350))
    pygame.display.update()

while acc:
    clock.tick(FPS)
    redraw_window()   
    if health <= 0 or user.healths <= 0:
        lost = True
        lost_count+=1
    if lost:
        if lost_count> FPS * 3:
            acc = False
        else:
            continue
        
    if len(enemies) == 0:
        level+=1
        wave_length+=5
        for i in range(wave_length):
            enemy =  Enemy(random.randrange(50,WIDHT-100), random.randrange(-1500, -100),random.choice(["blue","green","yellow"]))
            enemies.append(enemy)           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    Board_Game_Conduct = pygame.key.get_pressed()
    # Board Key Settings//
    if Board_Game_Conduct[pygame.K_LEFT] and user.x+ user_velocity >0:
        user.x-=user_velocity
    if Board_Game_Conduct[pygame.K_RIGHT] and user.x+ user_velocity+user.get_width()< WIDHT:
        user.x+= user_velocity
    if Board_Game_Conduct[pygame.K_UP] and user.y- user_velocity >0:
        user.y-=user_velocity
    if Board_Game_Conduct[pygame.K_DOWN] and user.y+user_velocity+user.get_height() + 15 < HEIGHT:
        user.y+=user_velocity
    if Board_Game_Conduct[pygame.K_SPACE]:
        user.shoot()
    for enemy in enemies[:]:
        enemy.move(enemy_vel)
        enemy.move_lasers(laser_velocity,user)
        if random.randrange(0, 2*60) ==1:
            enemy.shoot()
        if collide(enemy, user):
            user.healths -= 10
            enemies.remove(enemy)
        elif enemy.y+enemy.get_height()>HEIGHT:
            health-=1
            enemies.remove(enemy)
    user.move_lasers(-laser_velocity, enemies)       
def correct_menu():
    title_font = pygame.font.SysFont("Inconsolata" , 80)
    acc = True
    while acc:
        GAME_SCREEN.blit(Background_Space_Submarine, (0,0))
        title_label = title_font.render("Press The Space Button To Begin", 1,  (128,0,0))
        GAME_SCREEN.blit(title_label, (WIDHT/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                acc = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Correct()
    pygame.quit()

correct_menu()
