import pygame
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\images\\spaceship.png").convert_alpha()
        self.rect = self.image.get_frect(center = (width/2 , height/2))
        self.player_direction = pygame.math.Vector2()
        self.player_speed  = 500
        
        #cooldown
        self.laser_shooting = True
        self.cooldown = 400
        self.shooting_time = 0

        #mask
        self.mask = pygame.mask.from_surface(self.image)
        

    def laser_timer(self):
        if not  self.laser_shooting:
            current_time = pygame.time.get_ticks()
            if current_time - self.shooting_time >= self.cooldown:
                self.laser_shooting = True
                
            
    def update(self, dt):
        self.keys = pygame.key.get_pressed()
        self.recent_keys = pygame.key.get_just_pressed()
        self.player_direction.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
        self.player_direction.y = int(self.keys[pygame.K_DOWN]) - int(self.keys[pygame.K_UP])
        self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.player_speed * dt

        if self.keys[pygame.K_SPACE] and self.laser_shooting:
            Laser(laser_surf, (all_sprites, laser_sprites), (self.rect.midtop[0] - 5, self.rect.midtop[1]))
            Laser(laser_surf, (all_sprites, laser_sprites), (self.rect.midtop[0] + 5, self.rect.midtop[1]))
            self.laser_shooting = False
            self.shooting_time = pygame.time.get_ticks()
            laser_sound.play() 
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf, width, height):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0,width), randint(0,height)))

class Laser(pygame.sprite.Sprite):

    def __init__(self, surf, groups, pos):
        super().__init__(groups)
        
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 350 * dt
        if self.rect.bottom <0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf,pos):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.lifetime = 3000
        self.time_of_creation = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(300, 500)
        #mask
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
    def update(self, dt):
        self.rotation += randint(10,50) *dt
        self.rect.center += self.speed * dt * self.direction
        self.image = pygame.transform.rotozoom(self.original_surf , self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        
        if pygame.time.get_ticks() >= self.time_of_creation + self.lifetime:
            self.kill()

class AnimatedExpressions(pygame.sprite.Sprite):
    def __init__(self, groups, pos, frames):
        super().__init__(groups)
        self.image = frames[0]
        self.images = frames
        self.index = 0
        self.rect = self.image.get_frect(center  = pos)  
    
    def update(self, dt):
        self.index += 20 * dt
        if int(self.index) < len(self.images):
            self.image = self.images[int(self.index)]
        else:
            self.kill()

def check_collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask):  #dont need to create self.mask, because collide_mask can create it itself
        running = False
        

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            
            laser.kill()
            AnimatedExpressions(all_sprites , laser.rect.midtop, explosions_surf)
            explosion_sound.play()
            
def calculate_score():
    score = pygame.time.get_ticks() / 1000
    score_surf = font.render(str(score), True, "white")
    score_rect = score_surf.get_frect(center = (width / 2, height - 50 ))
    
    screen.blit(score_surf, score_rect)
    pygame.draw.rect(screen, "white",score_rect.inflate(20,20).move(0,-3), 5, 10)

#generat setup
width, height = 1280, 720
running = True
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
bcgrnd_clr = "#c8c8c8"

#import
star_surf = pygame.image.load("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\images\\sparkler.png").convert_alpha()
laser_surf = pygame.image.load("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\images\\technology.png").convert_alpha()
meteor_surf = pygame.image.load("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\images\\meteor.png").convert_alpha()
explosions_surf = [pygame.image.load("C:\\Users\Filip\\Documents\\Projects\\games\\spaceshooter\\images\\explosion\\" + f"{i}.png").convert_alpha() for i in range(21)]
font = pygame.font.Font(None, 50)

laser_sound = pygame.mixer.Sound("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\audio\\laser.wav")
game_music_sound = pygame.mixer.Sound("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\audio\\game_music.wav")
explosion_sound = pygame.mixer.Sound("C:\\Users\\Filip\\Documents\\Projects\\games\\spaceshooter\\audio\\explosion.wav")
#spirtes
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

player = Player(all_sprites)

for i in range(20):
    Star(all_sprites, star_surf, width, height)
game_music_sound.play()
 #custom events -> meteor event
meteor_event  = pygame.event.custom_type()          
pygame.time.set_timer(meteor_event,500) 

while running:
    dt = clock.tick(60) / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
             x,y = randint(0,width), randint(-100, -50)
             Meteor((all_sprites, meteor_sprites), meteor_surf,(x,y))
    
    all_sprites.update(dt) 
    check_collisions()
 
    #draw game
    screen.fill(bcgrnd_clr)
    all_sprites.draw(screen) 
    calculate_score()
    
    pygame.display.update()
    
pygame.quit() 