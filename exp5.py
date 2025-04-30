import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
WHITE, GREEN, RED, BLACK = (255, 255, 255), (34, 139, 34), (255, 0, 0), (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Snake Game")

# Snake properties
snake = [(100, 100), (90, 100), (80, 100)]  # List of segments (x, y)
direction = (GRID_SIZE, 0)  # Moving right initially
food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
clock = pygame.time.Clock()
running = True
score = 0

# Function to draw snake with smooth curves
def draw_snake(snake):
    for i, segment in enumerate(snake):
        size = GRID_SIZE // 2
        pygame.draw.circle(screen, GREEN, (segment[0] + size, segment[1] + size), size)
        if i == 0:  # Add eyes to the snake head
            eye_offset = 5
            pygame.draw.circle(screen, WHITE, (segment[0] + size - eye_offset, segment[1] + size - eye_offset), 3)
            pygame.draw.circle(screen, WHITE, (segment[0] + size + eye_offset, segment[1] + size - eye_offset), 3)

# Function to move snake smoothly
def move_snake():
    global running, food, score
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Check for collisions (wall or self)
    if (
        new_head in snake or
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        running = False

    snake.insert(0, new_head)  # Move forward

    # Check if food is eaten
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
    else:
        snake.pop()  # Remove tail if no food eaten

# Main game loop
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                direction = (GRID_SIZE, 0)

    move_snake()

    # Draw food
    pygame.draw.circle(screen, RED, (food[0] + GRID_SIZE // 2, food[1] + GRID_SIZE // 2), GRID_SIZE // 2)

    # Draw snake with smoother look
    draw_snake(snake)

    pygame.display.flip()
    clock.tick(10)  # Adjust speed

pygame.quit()
print(f"Game Over! Your Score: {score}")
