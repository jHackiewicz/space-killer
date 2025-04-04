import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frames = [
            pygame.image.load(f"./assets/images/ship_idle_{i}.png").convert_alpha()
            for i in range(4)  
        ]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.animation_speed = 10  # frames per second
        self.last_update = pygame.time.get_ticks()

        self.can_shoot = True
        self.shoot_time = None
    
    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > 1000 // self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = current_time

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 300:
                self.can_shoot = True
    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos 

    def laser_shoot(self): 
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Laser(self.rect.midtop, laser_group)

    def update(self):
        self.animate()
        self.laser_timer()
        self.input_position()
        self.laser_shoot()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./assets/images/red-laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        # self.rect.y -= 1
        

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load("./assets/images/meteor2.png").convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.8)
        self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=pos)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(300, 500)

        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()


class Score:
    def __init__(self):
        self.font = pygame.font.Font('./assets/graphics/Pixeled.ttf', 15)

    def display(self):
         score_text = f'Score: {pygame.time.get_ticks() // 1000}'
         text_surf = self.font.render(score_text, True, (255,255,255))
         text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
         display_surface.blit(text_surf, text_rect)
         pygame.draw.rect(display_surface, (255,255,255), text_rect.inflate(30,30), width = 6, border_radius = 4)




pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid Shooter")

clock = pygame.time.Clock()


background_surf = pygame.image.load("./assets/images/background.png").convert()
# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
# sprite creation
ship = Ship(spaceship_group)

#timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)


score = Score()


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
           meteor_y_pos = randint(-150, -50)
           meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
           Meteor((meteor_x_pos, meteor_y_pos), groups = meteor_group)



    dt = clock.tick() / 1000
        
    display_surface.blit(background_surf, (0, 0))
        
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    score.display()

    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

        
    pygame.display.update()