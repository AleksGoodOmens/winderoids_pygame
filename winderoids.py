
import pygame
import random
from os import path
from platform import python_version 
print (python_version())

game_over = True
img_dir = path.join(path.dirname(__file__), 'img')
voice_dir = path.join(path.dirname(__file__), 'voice')
#game variables=============================================================================================
WIDTH = 1920 # WIDTH OF GAME WINDOW
HEIGHT = 1080  # HEIGHT OF GAME WINDOW
FPS = 60 # UPDATES PER SECOND
POWERUP_TIME = 5000 # working time for powerUps
# colors (R, G, B)=============================================================================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
score = 0


# game initialization =======================================================================
pygame.init() 
pygame.mixer.init() # voice in game
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN) # vareable with all screen sizes
pygame.display.set_caption("Winderoids") # game window name

icon = pygame.image.load(path.join(img_dir, "PNG/playerShip1_orange.png")).convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock() # variable for displaying FPS in game


# text =====================================================================================
font_name = pygame.font.match_font('monospace')





def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# player shield
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# player lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# Create new mobs
def newmob(number = 0):
    objs = [Mob() for i in range(number)]
    for obj in objs:
        all_sprites.add(obj)
        mobs.add(obj)

def newmob2():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 76))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 0
        self.speedY = 0
        self.rot = 0
        self.rot_speed = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # hide if not hide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.shoot_delay = 250
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT - 50

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.shoot_delay = 300
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3) 
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                self.shoot_delay = 350
                shoot_sound.play()
            if self.power >= 4:
                self.shoot_delay = 250
                self.power += 1
            if self.power >= 5:
                self.shoot_delay = 100
                self.power += 1
            if self.power > 6:
                self.shoot_delay = 50
                self.power += 1



    def hide(self):
        # temp hide player
        self.hidden = True
        self.shoot_delay = self.hide_timer
        self.hide_timer = pygame.time.get_ticks()
        self.shield = -1
        self.rect.center = (WIDTH / 2, HEIGHT - 50)

# mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.shield = int(self.rect.width * .85 / 2)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

# class powerups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()

# class explosions
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#graphics in the game
background = pygame.image.load(path.join(img_dir, "Backgrounds/starbg.jpg")).convert()
background1 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg1.jpg")).convert()
background2 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg2.jpg")).convert()
background3 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg3.jpg")).convert()
background4 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg4.jpg")).convert()
background5 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg5.jpg")).convert()
background6 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg6.jpg")).convert()
background7 = pygame.image.load(path.join(img_dir, "Backgrounds/starbg7.jpg")).convert()
background_rect = background.get_rect()
background_rect1 = background1.get_rect()
background_rect2 = background2.get_rect()
background_rect3 = background3.get_rect()
background_rect4 = background4.get_rect()
background_rect5 = background5.get_rect()
background_rect6 = background6.get_rect()
background_rect7 = background6.get_rect()
#player battle ship image
player_img = pygame.image.load(path.join(img_dir, "PNG/playerShip1_orange.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
#Bullet image
bullet_img = pygame.image.load(path.join(img_dir, "PNG/Lasers/Assetes-22.png")).convert_alpha()
#mobs images
meteor_images = []
meteor_list = ['PNG/Meteors/1.png',
                'PNG/Meteors/2.png',
                'PNG/Meteors/3.png',
                'PNG/Meteors/4.png',
                'PNG/Meteors/5.png',
                'PNG/Meteors/6.png',
                'PNG/Meteors/7.png',
                'PNG/Meteors/8.png',
                'PNG/Meteors/9.png',
                'PNG/Meteors/10.png',
                'PNG/Meteors/11.png',
                'PNG/Meteors/12.png',
                'PNG/Meteors/14.png',
                'PNG/Meteors/15.png',
                'PNG/Meteors/16.png',
                'PNG/Meteors/17.png',
                'PNG/Meteors/18.png',
                'PNG/Meteors/19.png']
for folder in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, folder)).convert())

#explosion images
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'explosions/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'explosions/sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

#PowerUps images
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerUp/shield_gold.png')).convert_alpha()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'powerUp/bolt_gold.png')).convert_alpha()

#music
shoot_sound = pygame.mixer.Sound(path.join(voice_dir, 'sfx_laser1.mp3'))
shield_sound = pygame.mixer.Sound(path.join(voice_dir, 'powerUp/sfx_shieldUp.ogg'))
power_sound = pygame.mixer.Sound(path.join(voice_dir, 'powerUp/sfx_zap.ogg'))
expl_sounds = []
for voice in ['Explosion2.mp3', 'Explosion5.mp3']:
    expl_sounds.append(pygame.mixer.Sound(path.join(voice_dir, voice)))

pygame.mixer.music.load(path.join(voice_dir, '1.mp3'))
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(loops=-1) 

def show_start_screen ():
    print(show_start_screen)
    screen.blit(background, background_rect)
    draw_text(screen, "Welcome to Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Good luck have fun", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                waiting = False



def show_go_screen():
    print("show_go_screen")
    screen.blit(background, background_rect)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Controls: WASD or ARROWS Shooting: Press Space", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press button from 1 up to 5", 18, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(screen, "To choose level", 18, WIDTH / 2, HEIGHT * 3 / 4 + 26)
    draw_text(screen, "Or press ESC to leave the game", 18, WIDTH / 2, HEIGHT * 3 / 4 + 52)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/background.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                waiting = False
                pygame.quit()
            if pressed_keys[pygame.K_1] or pressed_keys[pygame.K_KP_1]:
                waiting = False
                global level_1
                level_1 = True
            if pressed_keys[pygame.K_2] or pressed_keys[pygame.K_KP_2]:
                waiting = False
                global level_2
                level_1 = False
                level_2 = True
            if pressed_keys[pygame.K_3] or pressed_keys[pygame.K_KP_3]:
                waiting = False
                global level_3
                level_3 = True
            if pressed_keys[pygame.K_4] or pressed_keys[pygame.K_KP_4]:
                waiting = False
                global level_4
                level_4 = True
            if pressed_keys[pygame.K_5] or pressed_keys[pygame.K_KP_5]:
                waiting = False
                global level_5
                level_5 = True

def show_level_1 ():
    print("show_level_1")
    screen.blit(background1, background_rect1)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Level one ", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "6 winderoids comming,", 22,
            WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "You need destroy them, and gain a score of 2500", 22,
            WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/2.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1) 
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                pygame.mixer.music.stop()
                waiting = False

def show_level_2 ():
    print("show_level_2")
    screen.blit(background2, background_rect2)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Level Two ", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "12 winderoids comming,", 22,
            WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "You need destroy them, and gain a score of 5500", 22,
            WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/3.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1) 
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                pygame.mixer.music.stop()
                waiting = False

def show_level_3 ():
    print("show_level_3")
    screen.blit(background3, background_rect3)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Level Three ", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "18 winderoids comming,", 22,
            WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "You need destroy them, and gain a score of 7500", 22,
            WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/4.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1) 
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                pygame.mixer.music.stop()
                waiting = False

def show_level_4 ():
    print("show_level_4")
    screen.blit(background4, background_rect4)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Level Four ", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "24 winderoids comming,", 22,
            WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "You need destroy them, and gain a score of 9500", 22,
            WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/5.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1) 
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                pygame.mixer.music.stop()
                waiting = False

def show_level_5 ():
    print("show_level_5")
    screen.blit(background5, background_rect5)
    draw_text(screen, "Winderoids", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Level Five ", 22,
            WIDTH / 2, HEIGHT / 2 - 60)
    draw_text(screen, "1 winderoids comming,", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "if you take score more then 100 000 == Easter Egg", 22,
            WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "But you won't be able to do it =)", 22,
            WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "To start press \"TAB\"", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_TAB]:
                pygame.mixer.music.stop()
                waiting = False

def show_game_over():
    print("Game over")
    screen.blit(background7, background_rect7)
    draw_text(screen, "Game Over", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "You Loose", 22,
            WIDTH / 2, HEIGHT / 2)

    draw_text(screen, "Press ESC to go menu", 18, WIDTH / 2, HEIGHT * 3 / 4 + 52)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/looser.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                waiting = False
                show_go_screen()


def show_game_won():
    print("Congratulations ")
    screen.blit(background5, background_rect5)
    draw_text(screen, "Congratulations", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "You've killed all the asteroids", 22,
            WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press button from 1 up to 5", 18, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(screen, "To choose Next level", 18, WIDTH / 2, HEIGHT * 3 / 4 + 26)
    draw_text(screen, "Or press ESC to leave the game", 18, WIDTH / 2, HEIGHT * 3 / 4 + 52)
    pygame.display.flip()
    pygame.mixer.music.load(path.join(voice_dir, 'victory/winner.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=1)
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                waiting = False
                pygame.quit()
            if pressed_keys[pygame.K_1] or pressed_keys[pygame.K_KP_1]:
                waiting = False
                global level_1
                level_1 = True

                pygame.mixer.music.stop()
            if pressed_keys[pygame.K_2] or pressed_keys[pygame.K_KP_2]:
                waiting = False
                global level_2
                level_2 = True

                pygame.mixer.music.stop()
            if pressed_keys[pygame.K_3] or pressed_keys[pygame.K_KP_3]:
                waiting = False
                global level_3
                level_3 = True

                pygame.mixer.music.stop()
            if pressed_keys[pygame.K_4] or pressed_keys[pygame.K_KP_4]:
                waiting = False
                global level_4
                level_4 = True

                pygame.mixer.music.stop()
            if pressed_keys[pygame.K_5] or pressed_keys[pygame.K_KP_5]:
                waiting = False
                global level_5
                level_5 = True

                pygame.mixer.music.stop()

running = True
level_1 = False
level_2 = False
level_3 = False
level_4 = False
level_5 = False

song = True


while running:
    show_go_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            running = False
            pygame.quit()
    level_start = True
    while level_1:
        
        #show_level_1()
        if level_start:
            show_level_1()
            level_start = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            
            for i in range(6):
                newmob2()
                    
            score = 0

        screen.blit(background1, background_rect1)
        draw_text(screen, "Level 1",24,WIDTH//2, HEIGHT - 44) 
        if score > 1000 and score < 1100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/firstblood.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 1850 and score < 1950:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/doublekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 2500:
            level_1 = False
            score = 0
            show_game_won()   
    #events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_1 = False
                    show_go_screen()

        

        #check if hit by bullet
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 100 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob(1)

        #check if mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            player.shield -= hit.radius * hit.speedy / 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            pygame.mixer.music.load(path.join(voice_dir, 'victory/hitting.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
            newmob(1)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                pygame.mixer.music.load(path.join(voice_dir, 'victory/death.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=1)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check colusion with powerUps
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        # if player died game end
        if player.lives <= 0 and not death_explosion.alive():
            player.lives = 3
            score = 0
            level_start = True
            level_1 = False
            show_game_over()

        
        #updates
        all_sprites.update() # update sprites
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        all_sprites.draw(screen) #sprites drawing
        #last function for change screen
        clock.tick(FPS)
        pygame.display.flip()
    level_start = True
    while level_2:
        #show_level_1()
        if level_start:
            show_level_2()
            level_start = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            
            for i in range(12):
                newmob2()
                    
            score = 0

        screen.blit(background2, background_rect2)
        draw_text(screen, "Level 2",24,WIDTH//2, HEIGHT - 44)
        if score > 1000 and score < 1100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/firstblood.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 2000 and score < 2100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/doublekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 3000 and score < 3100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/triplekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 4000 and score < 4100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/megakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 5000 and score < 5100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/ultrakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        
        
        if score > 5500:
            level_2 = False
            score = 0
            show_game_won()   
    #events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_2 = False
                    show_go_screen()

        

        #check if hit by bullet
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 100 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob(1)

        #check if mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            player.shield -= hit.radius * hit.speedy / 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            pygame.mixer.music.load(path.join(voice_dir, 'victory/hitting.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
            newmob(1)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                pygame.mixer.music.load(path.join(voice_dir, 'victory/death.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=1)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check colusion with powerUps
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        # if player died game end
        if player.lives <= 0 and not death_explosion.alive():
            player.lives = 3
            score = 0
            level_2 = False
            level_start = True
            show_game_over()
            

        
        #updates
        all_sprites.update() # update sprites
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        all_sprites.draw(screen) #sprites drawing
        #last function for change screen
        clock.tick(FPS)
        pygame.display.flip()
    level_start = True
    while level_3:
        #show_level_1()
        if level_start:
            show_level_3()
            level_start = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            
            for i in range(18):
                newmob2()
                    
            score = 0

        screen.blit(background3, background_rect3)
        draw_text(screen, "Level 3",24,WIDTH//2, HEIGHT - 44)
        if score > 1000 and score < 1100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/firstblood.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 2000 and score < 2100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/doublekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 3000 and score < 3100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/triplekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 4000 and score < 4100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/megakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 5000 and score < 5100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/ultrakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 6000 and score < 6100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/multikill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 7000 and score < 7100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/dominating.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        
        if score > 7500:
            level_3 = False
            score = 0
            show_game_won()   
    #events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_3 = False
                    show_go_screen()

        

        #check if hit by bullet
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 100 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob(1)

        #check if mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            player.shield -= hit.radius * hit.speedy / 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            pygame.mixer.music.load(path.join(voice_dir, 'victory/hitting.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
            newmob(1)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                pygame.mixer.music.load(path.join(voice_dir, 'victory/death.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=1)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check colusion with powerUps
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        # if player died game end
        if player.lives <= 0 and not death_explosion.alive():
            player.lives = 3
            score = 0
            level_3 = False
            show_game_over()

        
        #updates
        all_sprites.update() # update sprites
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        all_sprites.draw(screen) #sprites drawing
        #last function for change screen
        clock.tick(FPS)
        pygame.display.flip()
    level_start = True
    while level_4:
        if level_start:
            show_level_4()
            level_start = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            
            for i in range(24):
                newmob2()
                    
            score = 0

        screen.blit(background4, background_rect4)
        draw_text(screen, "Level 4",24,WIDTH//2, HEIGHT - 44)
        if score > 1000 and score < 1100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/firstblood.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 2000 and score < 2100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/doublekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 3000 and score < 3100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/triplekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 4000 and score < 4100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/megakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 5000 and score < 5100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/ultrakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 6000 and score < 6100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/multikill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 7000 and score < 7100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/dominating.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 8000 and score < 8100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 9000 and score < 9100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        
        if score > 9500:
            level_4 = False
            score = 0
            show_game_won()   
    #events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_4 = False
                    show_go_screen()

        

        #check if hit by bullet
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 100 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob(1)

        #check if mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            player.shield -= hit.radius * hit.speedy / 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            pygame.mixer.music.load(path.join(voice_dir, 'victory/hitting.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
            newmob(1)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                pygame.mixer.music.load(path.join(voice_dir, 'victory/death.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=1)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check colusion with powerUps
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        # if player died game end
        if player.lives <= 0 and not death_explosion.alive():
            player.lives = 3
            score = 0
            level_start = True
            level_4 = False
            show_game_over()

        
        #updates
        all_sprites.update() # update sprites
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        all_sprites.draw(screen) #sprites drawing
        #last function for change screen
        clock.tick(FPS)
        pygame.display.flip()
    
    
        pygame.display.flip()
    level_start = True
    while level_5:
        if level_start:
            show_level_5()
            level_start = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
        
            
            newmob(1)
                    
            score = 0

        screen.blit(background5, background_rect5)
        draw_text(screen, "Level 5",24,WIDTH//2, HEIGHT - 44)
        if score > 1000 and score < 1100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/firstblood.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 2000 and score < 2100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/doublekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 3000 and score < 3100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/triplekill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 4000 and score < 4100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/megakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 5000 and score < 5100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/ultrakill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 6000 and score < 6100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/multikill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 7000 and score < 7100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/dominating.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 8000 and score < 8100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 9000 and score < 9100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 10000 and score < 10100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 12000 and score < 12100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 13000 and score < 13100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 14000 and score < 14100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 15000 and score < 15100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score > 16000 and score < 16100:
            pygame.mixer.music.load(path.join(voice_dir, 'victory/monsterkill.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
        if score >= 20000:
            if song:
                pygame.mixer.music.load(path.join(voice_dir, 'victory/1.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=-1) 
                song = False
            screen.blit(background6, background_rect6)
            draw_text(screen, "For Mother Russia",24,WIDTH//2, HEIGHT - 44)
        if score > 39000:
                level_5 = False
                score = 0
                show_game_won()
        
        if mobs == 0:
            
            show_game_won()   
    #events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_5 = False
                    show_go_screen()

        

        #check if hit by bullet
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 100 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            if score < 100:
                newmob(1)
                print(mobs)
            elif score < 20000:
                newmob(2)
                print(f'spawn 2{mobs}')
            elif score > 20000:
                newmob(-1)
                print(f'spawn 3{mobs}')
            
                

        #check if mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            player.shield -= hit.radius * hit.speedy / 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            pygame.mixer.music.load(path.join(voice_dir, 'victory/hitting.mp3'))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(loops=1)
            newmob(1)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                pygame.mixer.music.load(path.join(voice_dir, 'victory/death.mp3'))
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=1)
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check colusion with powerUps
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        # if player died game end
        if player.lives <= 0 and not death_explosion.alive():
            player.lives = 3
            score = 0
            level_start = True
            level_5 = False
            show_game_over()
        
        
        
        #updates

        all_sprites.update() # update sprites
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
        all_sprites.draw(screen) #sprites drawing
        #last function for change screen
        clock.tick(FPS)
        pygame.display.flip()
pygame.quit()
