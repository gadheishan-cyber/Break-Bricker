import pygame
import math
import button
import random

pygame.mixer.init()

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

HEALTH_FONT = pygame.font.SysFont("nunito", 30)
WINNER_FONT = pygame.font.SysFont("nunito", 80)
LEVEL_FONT = pygame.font.SysFont("nunito", 40)
BALL_RADIUS = 12

brick_hit = pygame.mixer.Sound("bk_hit.wav")
wall_hit  = pygame.mixer.Sound("wall_hit.ogg")
pad_hit = pygame.mixer.Sound("pad.ogg")

COLOR = (213,254,230)
BLACK = (0,0,0)

BRICK_WIDTH , BRICK_HEIGHT = 42, 45

YELLOW_BK   = pygame.transform.scale(pygame.image.load("new yellow bk.png"),   (BRICK_WIDTH , BRICK_HEIGHT))
PINK_BK     = pygame.transform.scale(pygame.image.load("new pink bk.png"),     (BRICK_WIDTH , BRICK_HEIGHT))
PURPLE_BK = pygame.transform.scale(pygame.image.load("new purple bk.png"),     (BRICK_WIDTH , BRICK_HEIGHT))
DARK_BK     = pygame.transform.scale(pygame.image.load("new blue bk.png"),     (BRICK_WIDTH , BRICK_HEIGHT))

YELLOW_DAM   = pygame.transform.scale(pygame.image.load("new yellow_dam bk.png"), (BRICK_WIDTH , BRICK_HEIGHT))
PINK_DAM     = pygame.transform.scale(pygame.image.load("new pink_dam bk.png"),   (BRICK_WIDTH , BRICK_HEIGHT))
PURPLE_DAM = pygame.transform.scale(pygame.image.load("new purple_dam bk.png"),   (BRICK_WIDTH , BRICK_HEIGHT))
DARK_DAM     = pygame.transform.scale(pygame.image.load("new blue_dam bk.png"),   (BRICK_WIDTH , BRICK_HEIGHT))

resume_img = pygame.image.load("RESUME - ed.png").convert_alpha()
start_img = pygame.image.load("start_btn.png").convert_alpha()
exit_img = pygame.image.load("exit_btn.png").convert_alpha()

BASE_PAD_IMAGE = pygame.image.load("new pad.png").convert_alpha()

GAME_LOST = WINNER_FONT.render("Game Over!", True, BLACK)
GAME_WIN = WINNER_FONT.render("You Win!", True, BLACK)
VEL = 8

def draw_health(text):
    ball_rem = HEALTH_FONT.render("Lives : " + text, True, BLACK)
    WIN.blit(ball_rem, (10,10))

def draw_level(level):
    level_text = HEALTH_FONT.render("Level : " + str(level), True, BLACK)
    WIN.blit(level_text, (WIDTH - 120, 10))

def score_display(text):
    score_text = HEALTH_FONT.render("Score : " + str(text), True, BLACK)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))

def show_level_transition(level):
    WIN.fill(COLOR)
    level_text = LEVEL_FONT.render(f"Level {level}", True, BLACK)
    WIN.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 - level_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1500)


def build_bricks_level_1():   #  <-- Level 1 : Classic Horizontal Row
    bricks = []
    cols = 22
    step = 39
    start_x = 20

    rows_data = [
        (40,  DARK_BK,     DARK_DAM,     2),
        (110, PURPLE_BK, PURPLE_DAM, 2),
        (190, PINK_BK,     PINK_DAM,     2),
        (270, YELLOW_BK,   YELLOW_DAM,   2),
    ]
    for y, full, crack, hp in rows_data:
        x = start_x
        for _ in range(cols):
            bricks.append(Brick(x, y, full, crack, hp))
            x += step
    return bricks


def build_bricks_level_2():   #  <-- Level 2 : Pyramid Pattern
    bricks = []
    step = 39
    rows_data = [
        (50, 11, DARK_BK, DARK_DAM, 2),      
        (89, 13, PURPLE_BK, PURPLE_DAM, 2), 
        (128, 15, PINK_BK, PINK_DAM, 2),     
        (167, 17, YELLOW_BK, YELLOW_DAM, 2), 
        (206, 19, DARK_BK, DARK_DAM, 2),     
        (245, 21, PURPLE_BK, PURPLE_DAM, 2), 
    ]
    
    for y, cols, full, crack, hp in rows_data:
        start_x = (WIDTH - cols * step) // 2
        x = start_x
        for _ in range(cols):
            bricks.append(Brick(x, y, full, crack, hp))
            x += step
    return bricks


def build_bricks_level_3():    #  <-- Level 3 : Diamond Pattern
    bricks = []
    step = 39
    
    rows_data = [
        (50, 1, YELLOW_BK, YELLOW_DAM, 2),   
        (89, 3, PINK_BK, PINK_DAM, 2),       
        (128, 5, PURPLE_BK, PURPLE_DAM, 2),
        (167, 7, DARK_BK, DARK_DAM, 2),     
        (206, 5, PURPLE_BK, PURPLE_DAM, 2),
        (245, 3, PINK_BK, PINK_DAM, 2),
        (284, 1, YELLOW_BK, YELLOW_DAM, 2), 
    ]
    
    for y, cols, full, crack, hp in rows_data:
        start_x = (WIDTH - cols * step) // 2
        x = start_x
        for _ in range(cols):
            bricks.append(Brick(x, y, full, crack, hp))
            x += step
    return bricks


def get_level_bricks(level):     #  <-- Function To Get Bricks For Any Level
    level_builders = {
        1: build_bricks_level_1,
        2: build_bricks_level_2,
        3: build_bricks_level_3,
    }
    
    if level in level_builders:
        return level_builders[level]()
    else:
        base_level = ((level - 1) % 3) + 1
        return level_builders[base_level]()
    

class Brick:
    def __init__(self, x, y, img_full, img_cracked, health=2):
        self.x, self.y = x, y
        self.full = img_full
        self.cracked = img_cracked
        self.health = health
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    @property
    def alive(self):
        return self.health > 0

    def draw(self, win):
        if not self.alive:
            return
        if self.health >= 2:
            win.blit(self.full, (self.x, self.y))
        else:
            win.blit(self.cracked, (self.x, self.y))

    def hit(self):
        if not self.alive:
            return False
        self.health -= 1
        return self.health <= 0


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


class Ball:
    PURPLE = (159,43,104)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 5
        self.y_vel = -5

    def draw(self):
        pygame.draw.circle(WIN, self.PURPLE, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = -5
        self.x_vel = 5

    def handle_walls(self):
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.y_vel *= -1
            wall_hit.play()

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.x_vel *= -1
            wall_hit.play()

        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.x_vel *= -1 
            wall_hit.play()

    def out_of_bounds(self):
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            return True
        return False

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius) ,
                           self.radius * 2, self.radius * 2)

    def bounce_off_paddle(self, pad: Pad):
        if not self.rect.colliderect(pad.rect):
            return
        if self.y_vel > 0:  
            offset = (self.x - pad.rect.centerx) / (pad.rect.width / 2)
            offset = max(-1, min(1, offset))

            speed = max(6.0, math.hypot(self.x_vel, self.y_vel))
            self.x_vel = speed * 0.75 * offset
            self.y_vel = -abs(math.sqrt(max(speed**2 - self.x_vel**2, 1)))

            self.y = pad.rect.top - self.radius - 1
            pad_hit.play()

    def bounce_off_brick(self, brick_rect: pygame.Rect):
        b = self.rect
        overlap_left   = b.right  - brick_rect.left
        overlap_right  = brick_rect.right - b.left
        overlap_top    = b.bottom - brick_rect.top
        overlap_bottom = brick_rect.bottom - b.top
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            self.x_vel = -abs(self.x_vel)
            self.x = brick_rect.left - self.radius
        elif min_overlap == overlap_right:
            self.x_vel = abs(self.x_vel)
            self.x = brick_rect.right + self.radius
        elif min_overlap == overlap_top:
            self.y_vel = -abs(self.y_vel)
            self.y = brick_rect.top - self.radius
        else:
            self.y_vel = abs(self.y_vel)
            self.y = brick_rect.bottom + self.radius

        brick_hit.play()


class PowerToken:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.y_vel = 2
        self.power_type = power_type

    def move(self):
        self.y += self.y_vel

    def is_off_screen(self):
        return self.y > HEIGHT

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        diamond_points = [
            (center_x, self.y),
            (self.x + self.width, center_y),
            (center_x, self.y + self.height),
            (self.x, center_y),
        ]
        pygame.draw.polygon(WIN, (92, 100, 200), diamond_points)

        if self.power_type == "pad_expand":
            bar_width = self.width // 2
            bar_height = 4
            bar_rect = pygame.Rect(
                center_x - bar_width // 2,
                center_y - bar_height // 2,
                bar_width,
                bar_height
            )
            pygame.draw.rect(WIN, (255, 255, 0), bar_rect)
        
        elif self.power_type == "extra_ball":
            pygame.draw.circle(WIN, (255, 255, 0), (center_x, center_y), 6)


def main():
    clock = pygame.time.Clock()

    pad = Pad(WIDTH // 2.3)
    balls = [Ball(415, int(HEIGHT // 1.3), 12)]

    ball_count = 3
    paused = False
    start = True
    score = 0
    current_level = 1
    
    power_tokens = []
    
    bricks = get_level_bricks(current_level)
    show_level_transition(current_level)

    run = True
    while run:
        clock.tick(60)
        WIN.fill(COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused 
        
        
        if start:
            start_button = button.Button(WIDTH//2 - start_img.get_width()//2 + 2, HEIGHT//2 - 100, 
                                         start_img, 0.8)
            exit_button = button.Button(WIDTH//2 - exit_img.get_width()//2, HEIGHT//2 , 
                                        exit_img, 0.8)
            
            if start_button.draw(WIN):
                start = False
                show_level_transition(current_level)
                
            if exit_button.draw(WIN):
                run = False
            
            pygame.display.update()
            continue

        if paused:
            resume_button = button.Button(WIDTH//2 - 120, HEIGHT//2 - 130, resume_img, 0.135)
            exit_button = button.Button(WIDTH//2 - exit_img.get_width()//2, HEIGHT//2 , exit_img, 0.8)

            if resume_button.draw(WIN):
                paused = False

            if exit_button.draw(WIN):
                run = False

            pygame.display.update()
            continue
        
        balls_to_remove = []
        for i, ball in enumerate(balls):
            ball.move()
            ball.handle_walls()
            
            if ball.out_of_bounds():
                if len(balls) > 1:
                    balls_to_remove.append(i)
                else:            
                    pad.reset()
                    ball.reset()
                    ball_count -= 1
                    pygame.time.delay(1000)
                    
                    if ball_count == 0:
                        run = False
                        WIN.fill(COLOR)
                        WIN.blit(GAME_LOST, (450 - GAME_LOST.get_width()//2, HEIGHT//2 - GAME_LOST.get_height()))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        break
            else:
                ball.bounce_off_paddle(pad)
                ball.draw()

        for i in reversed(balls_to_remove):
            balls.pop(i)

        if ball_count == 0:
            break

        if not bricks:
            current_level += 1
            if current_level == 2:
                ball_count += 1 
            if current_level == 3:
                ball_count += 2

            if current_level > 3:
                run = False
                WIN.fill(COLOR)
                all_levels_text = WINNER_FONT.render("All Levels Complete!", True, BLACK)
                WIN.blit(all_levels_text, (WIDTH//2 - all_levels_text.get_width()//2, 
                                           HEIGHT//2 - all_levels_text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(3000)
                break
            
            show_level_transition(current_level)
            bricks = get_level_bricks(current_level)
            pad.reset()
            balls = [Ball(415, int(HEIGHT // 1.3), 12)]
            power_tokens.clear()
            pygame.time.delay(1000)

        pad.movement()
        pad.handle_collision()
        pad.update_power_up()

        for ball in balls:
            for brick in bricks[:]:
                if not brick.alive:
                    continue

                if ball.rect.colliderect(brick.rect):
                    ball.bounce_off_brick(brick.rect)
                    score += 5
                    destroyed = brick.hit()

                    power_chance = random.randint(1, 8)
                    if power_chance == 1:
                        power_type = random.choice(["pad_expand", "extra_ball"])
                        power_tokens.append(PowerToken(brick.x, brick.y, power_type))
                        print(f"Power-up '{power_type}' spawned at ({brick.x}, {brick.y})")

                    if destroyed:
                        bricks.remove(brick)
                    break

        tokens_to_remove = []
        for i, token in enumerate(power_tokens):
            token.move()
            token.draw()

            if pad.rect.colliderect(token.rect):
                if token.power_type == "pad_expand":
                    pad.activate_power_up(duration_frames=500)
                    print("Pad expansion activated!")
                elif token.power_type == "extra_ball":
                    new_ball = Ball(pad.x + pad.width//2, pad.y - 20, 12)
                    balls.append(new_ball)
                    print("Extra ball added!")
                
                tokens_to_remove.append(i)
            
            elif token.is_off_screen():
                tokens_to_remove.append(i)

        for i in reversed(tokens_to_remove):
            power_tokens.pop(i)

        for brick in bricks:
            brick.draw(WIN)

        draw_level(current_level)
        draw_health(str(ball_count))
        score_display(str(score))
        pad.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()