#  Initial Testing Of Pad Expand Feature.

import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

COLOR = (40,245,240)
BASE_PAD_IMAGE = pygame.image.load("new pad.png").convert_alpha()

random_bk_x = WIDTH//2
random_bk_y = HEIGHT//2
VEL = 8


class power_token:
    def __init__(self, random_bk_x, random_bk_y):
        self.x = random_bk_x
        self.y = random_bk_y
        self.width = 30
        self.height = 30
        self.gravity = 0.08
        self.y_vel = 0
        
    def draw(self):
        pygame.draw.rect(WIN, (92,108,220), (self.x, self.y, self.width, self.height))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y_vel += self.gravity
        self.y += self.y_vel


class Pad:
    def __init__(self, x):
        self.x = self.original_x = x
        self.vel = VEL
        self.y = int(HEIGHT // 1.2)
        self.base_width = 120
        self.base_height = 100
        self.width = self.base_width
        self.height = self.base_height
        self.image = pygame.transform.scale(BASE_PAD_IMAGE, (self.width, self.height))
        self.power_up_active = False
        self.power_up_timer = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def handle_collision(self):
        if self.x <= 0:
            self.x = 0
        if self.x + self.width >= WIDTH:
            self.x = WIDTH - self.width

    @property
    def rect(self):

        actual_paddle_width = int(self.width * 0.97)
        actual_paddle_height = int(self.height * 0.15)
        
        collision_x = self.x + (self.width - actual_paddle_width) // 2
        
        collision_y = self.y + (self.height - actual_paddle_height) - 50
        
        return pygame.Rect(collision_x, collision_y, actual_paddle_width, actual_paddle_height)
    
    def reset(self):
        self.x = self.original_x
        self.y = int(HEIGHT // 1.2)
        self.width = self.base_width
        self.height = self.base_height
        self.image = pygame.transform.scale(BASE_PAD_IMAGE, (self.width, self.height))
        self.power_up_active = False
        self.power_up_timer = 0

    def activate_power_up(self, duration_frames = 500):
        if not self.power_up_active:
            self.power_up_active = True
            self.power_up_timer = duration_frames
            self.width = 200
            self.image = pygame.transform.scale(BASE_PAD_IMAGE, (self.width, self.height))

    def update_power_up(self):
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up_active = False
                self.width = self.base_width
                self.image = pygame.transform.scale(BASE_PAD_IMAGE, (self.width, self.height))

def main():
    clock = pygame.time.Clock()
    power1 = power_token(random_bk_x, random_bk_y)
    pad = Pad(WIDTH // 2.3)

    run = True
    while run:
        clock.tick(60)
        WIN.fill(COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pad.rect.colliderect(power1.rect):
            pad.activate_power_up()


        pad.movement()
        pad.handle_collision()
        pad.update_power_up()

        power1.draw()
        power1.move()

        pad.draw()

        pygame.display.update()

if __name__ == "__main__":
    main()

