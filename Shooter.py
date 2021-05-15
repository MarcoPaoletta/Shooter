# Import
import pygame, random

# Pantalla
widht = 800
height = 600
screen = pygame.display.set_mode((widht, height))
pygame.display.set_caption("Shooter :v")

# Colores
black = (0,0,0)
white = (255,255,255)
green = (0,120,0)

# Init
pygame.init()
pygame.mixer.init()

# Reloj
clock = pygame.time.Clock()
# Zona de fuentes
def draw_text(surface,text,size,x,y):
    font = pygame.font.SysFont("serif",size)
    text_surface = font.render(text,True,white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

def draw_shield_bar(surface,x,y,percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface,green,fill)
    pygame.draw.rect(surface,white,border,3)

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assests/player.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = widht // 2
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.shield = 100


    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > widht:
            self.rect.right = widht
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()


# Meteoro
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(widht - self.rect.width)
        self.rect.y = random.randrange(-140,-100)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-5,5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < 25 \
                or self.rect.right > widht + 25:
            self.rect.x = random.randrange(widht - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,10)

# Balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("Assests/laser1.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Explosion clase
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = explosion_anim[0]
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
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# Escena GO
def show_go_screen():
    pygame.mixer.music.stop()
    screen.blit(background,[0,0])
    draw_text(screen, "SHOOTER by MARCRAFT",65,widht // 2, height // 4)
    draw_text(screen,"Suscribete a MARCRAFT en YOUTUBE",27,widht // 2, height // 2)
    draw_text(screen,"Press Q to BEGIN",20,widht //2, height * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.mixer.music.play(loops=-1)
                    waiting = False

# Elementos meteoros
meteor_images = []
meteor_list = ["Assests/meteorGrey_big1.png", "Assests/meteorGrey_big2.png", "Assests/meteorGrey_big3.png", "Assests/meteorGrey_big4.png",
				"Assests/meteorGrey_med1.png", "Assests/meteorGrey_med2.png", "Assests/meteorGrey_small1.png", "Assests/meteorGrey_small2.png",
				"Assests/meteorGrey_tiny1.png", "Assests/meteorGrey_tiny2.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
# Explosion imagenes
explosion_anim = []
for i in range(9):
    file = "Assests/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(black)
    img_scale = pygame.transform.scale(img,(70,70))
    explosion_anim.append(img_scale)
# Fondo
background = pygame.image.load("Assests/background.png").convert()

# Elementos

    # Sonidos
laser_sound = pygame.mixer.Sound("Assests/laser5.ogg")
explosion_sound = pygame.mixer.Sound("Assests/explosion.wav")
laser_sound.set_volume(0.5)
explosion_sound.set_volume(0.4)
    # Musica
pygame.mixer.music.load("Assests/music.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# Bucle
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        meteor_list = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        score = 0
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.shoot()

    all_sprites.update()

    # Colisiones meteoro / laser
    hits = pygame.sprite.groupcollide(meteor_list,bullets,True,True)
    for hit in hits:
        score += 1
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Colisiones jugador / meteoro
    hits = pygame.sprite.spritecollide(player,meteor_list, True)
    for hit in hits:
        player.shield -= 20
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield == 0:
            game_over = True
    # Poner fondo de pantalla
    screen.blit(background, [0,0])
    # Sprites
    all_sprites.draw(screen)
    # Marcador
    draw_text(screen,str(score),25, widht // 2, 10)
    # Escudo
    draw_shield_bar(screen,5,5,player.shield)
    # Actualizar pantalla
    pygame.display.flip()
    # Salir de pygame
pygame.quit()