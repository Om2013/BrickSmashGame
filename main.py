

# --------------------- Difficulty ---------------------
difficulty = input("Select difficulty (E=Easy, M=Medium, H=Hard, R=Random): ").strip().upper()

# Random difficulty if chosen
if difficulty == "R":
    import random 
    difficulty = random.choice(["E", "M", "H"])
    print(f"Random difficulty chosen: {difficulty}")

# Set grid size and ball speed based on difficulty
if difficulty == "E":
    num_rows, num_cols = 5, 5
    speed_x, speed_y = 3, -3
elif difficulty == "M":
    num_rows, num_cols = 7, 7
    speed_x, speed_y = 5, -5
elif difficulty == "H":
    num_rows, num_cols = 10, 10
    speed_x, speed_y = 7, -7
else:
    print(f"Invalid input '{difficulty}', defaulting to Medium")
    num_rows, num_cols = 7, 7
    speed_x, speed_y = 5, -5

# Print only speed_x
print(f"Difficulty: {difficulty}")
print(f"Grid: {num_rows} rows x {num_cols} cols")
print(f"Ball speed x: {speed_x}")

# --------------------- Game Setup ---------------------

import pygame
import random
from paddle_design import Paddle
from ball_design import Ball
from bricks_design import Bricks

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Brick Smash Game")
pygame.key.set_repeat(1, 30)

FPS = 60
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Sprite groups
paddle_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

# Sounds
gamelost_sound = pygame.mixer.Sound("game_over_sound_bricksmash.mp3")
gamewin_sound = pygame.mixer.Sound("game_win_bricksmash.mp3")
ballhit_sound = pygame.mixer.Sound("ball_hit_sound_bricksmash.mp3")
background_music = pygame.mixer.Sound("bricksmash_bgmusic.mp3")
background_music.play(-1)

# Create paddle and ball
paddle = Paddle(WINDOW_WIDTH, WINDOW_HEIGHT)
ball = Ball(WINDOW_WIDTH, WINDOW_HEIGHT)
ball.speed_x = speed_x
ball.speed_y = speed_y
paddle_group.add(paddle)
ball_group.add(ball)

# Create bricks
start_x, start_y = 60, 60
spacing_x, spacing_y = 100, 30
for row in range(num_rows):
    for col in range(num_cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        brick = Bricks(x, y)
        bricks_group.add(brick)

# --------------------- Game Loop ---------------------
running = True
gamewin = False
gameover = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    paddle.update()
    ball_group.update()
    bricks_group.update()

    # ------------------ Collision Checks ------------------
    # Ball hits bricks
    hit_bricks = pygame.sprite.spritecollide(ball, bricks_group, True)
    if hit_bricks:
        ball.speed_y *= -1
        ball.score += 10
        ballhit_sound.play()

    # Ball hits paddle
    if ball.rect.colliderect(paddle.rect) and ball.speed_y > 0:
        ball.rect.bottom = paddle.rect.top
        ball.speed_y *= -1
        ballhit_sound.play()

    # Win/Lose conditions
    total_score = num_rows * num_cols * 10
    if ball.score >= total_score:
        gamewin = True
        gamewin_text = font.render("CONGRATULATIONS! YOU WON!", True, WHITE)
        gamewin_text_rect = gamewin_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        background_music.set_volume(0)
        pygame.time.delay(200)
        gamewin_sound.play()

    if ball.rect.top > WINDOW_HEIGHT:
        gameover = True
        defeat_text = font.render("You Lost! Game Over!", True, WHITE)
        defeat_text_rect = defeat_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        background_music.set_volume(0)
        pygame.time.delay(200)
        gamelost_sound.play()

    # ------------------ Drawing ------------------
    screen.fill(BLACK)
    paddle_group.draw(screen)
    ball_group.draw(screen)
    bricks_group.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {ball.score}", True, WHITE)
    score_rect = score_text.get_rect(centerx=WINDOW_WIDTH // 2, top=20)
    screen.blit(score_text, score_rect)

    # Draw boundaries
    pygame.draw.line(screen, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
    pygame.draw.line(screen, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)

    # Game over/win screens
    if gameover:
        screen.fill(BLACK)
        screen.blit(defeat_text, defeat_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
        pygame.quit()
        exit()

    if gamewin:
        screen.fill(BLACK)
        screen.blit(gamewin_text, gamewin_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
