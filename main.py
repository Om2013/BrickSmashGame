import random

# Ask for difficulty
difficulty = input("Select difficulty (E=Easy, M=Medium, H=Hard, R=Random): ")

# Normalize input: remove spaces and make uppercase
difficulty = difficulty.strip().upper()

# If random, pick one
if difficulty == "R":
    difficulty = random.choice(["E", "M", "H"])
    print(f"Random difficulty chosen: {difficulty}")

# Set grid size based on difficulty
if difficulty == "E":
    num_rows, num_cols = 5, 5
elif difficulty == "M":
    num_rows, num_cols = 7, 7
elif difficulty == "H":
    num_rows, num_cols = 10, 10
else:
    print(f"Invalid input '{difficulty}'! Defaulting to Medium.")
    num_rows, num_cols = 7, 7

#------------------------------Main Game--------------------------------
import pygame 
from paddle_design import Paddle  
from ball_design import Ball 
from bricks_design import Bricks

pygame.init()

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Brick Smash Game")
pygame.key.set_repeat(1, 30)  # Continuous paddle movement

# FPS, clock, font
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Colors
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

# Background music
background_music = pygame.mixer.Sound("bricksmash_bgmusic.mp3")
background_music.play(-1)

# Create paddle and ball
paddle = Paddle(WINDOW_WIDTH, WINDOW_HEIGHT)
ball = Ball(WINDOW_WIDTH, WINDOW_HEIGHT)
paddle_group.add(paddle)
ball_group.add(ball)

# Create bricks grid
start_x = 60
start_y = 60
spacing_x = 100
spacing_y = 30
for row in range(num_rows):
    for col in range(num_cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        brick = Bricks(x, y)
        bricks_group.add(brick)

# Game flags
running = True
gamewin = False
gameover = False

# Main loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    paddle.update()  # Update the paddle

    # Update objects
    ball_group.update()
    bricks_group.update()

    # Collision: ball with bricks
    hit_bricks = pygame.sprite.spritecollide(ball, bricks_group, True)
    if hit_bricks:
        ball.speed_y *= -1  # Bounce
        ball.score += 10    # Increase score
        ballhit_sound.play()  # Play hit sound

    # Collision: ball with paddle
    if ball.rect.colliderect(paddle.rect) and ball.speed_y > 0:
        ball.rect.bottom = paddle.rect.top  # Prevent overlap
        ball.speed_y *= -1  # Bounce up
        ballhit_sound.play()  # Play hit sound

    # Win condition
    if ball.score >= num_rows * num_cols * 10:
        gamewin = True
        gamewin_text = font.render("CONGRATULATIONS! YOU WON!", True, WHITE)
        gamewin_text_rect = gamewin_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        background_music.set_volume(0)
        pygame.time.delay(200)
        gamewin_sound.play()  # Play win sound

    # Lose condition
    if ball.rect.top > WINDOW_HEIGHT:
        defeat_text = font.render("You Lost! Game Over!", True, WHITE)
        defeat_text_rect = defeat_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        background_music.set_volume(0)
        pygame.time.delay(200)
        gamelost_sound.play()  # Play lose sound
        gameover = True

    # Draw objects
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

    # Game over screen
    if gameover:
        screen.fill(BLACK)
        screen.blit(defeat_text, defeat_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
        pygame.quit()
        exit()

    # Game win screen
    if gamewin:
        screen.fill(BLACK)
        screen.blit(gamewin_text, gamewin_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
        pygame.quit()
        exit()

    # Update display
    pygame.display.update()
    clock.tick(FPS)

# Quit
pygame.quit()
