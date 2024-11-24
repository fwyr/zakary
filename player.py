import pygame 
import time
from settings import *
from support import *
from timer import Clock

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, interaction_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/player/down_idle/down_idle.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.z = LAYERS['main']

        # graphics
        self.import_player_assets()
        self.state = "down"
        self.frame_index = 0
        self.animation_speed = 0.1

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.interacting = False
        self.interact_cooldown = 400
        self.obstacle_sprites = obstacle_sprites
        self.interaction_sprites = interaction_sprites

        # stats
        self.stats = {"depression": 100, "energy": 40}
        self.depression = 0.5 * self.stats["depression"]
        self.energy = self.stats["energy"]
        self.sleep = False

        # timer
        self.start = time.time()
        self.clock = Clock()
        self.day = 1
        self.hour = 8
        self.minute = 0

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = "./graphics/player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.interacting and not self.sleep:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.state = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.state = "left"
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.state = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.state = "down"
            else: 
                self.direction.y = 0

            # interact input
            if keys[pygame.K_SPACE]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction_sprites, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Bed':
                        self.state = 'left_idle'
                        self.sleep = True
                

    def get_state(self):
        # idle state
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.state:
                self.state += "_idle"

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("x")
        self.hitbox.y += self.direction.y * speed
        self.collision("y")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "x":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right  = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "y":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top 
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.interacting:
            if current_time - self.interact_time >= self.interact_cooldown:
                self.interacting = False

    def animate(self):
        animation = self.animations[self.state]
        
        # loop over frame index
        self.frame_index += self.animation_speed 
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def timer(self):
        if time.time() - self.start >= TICK_DURATION:
            self.clock.tick += 1
            self.start = time.time()
        self.day = self.clock.day()
        self.hour = self.clock.hour()
        self.minute = self.clock.minute()

    def update(self):
        self.input()
        self.cooldowns()
        self.get_state()
        self.animate()
        self.move(self.speed)
        self.timer()
            
        