import pygame
import sys

# Grid settings
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

# Colors
BG_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
BLOCK_COLOR = (0, 200, 200)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Board stores fixed blocks: 0 empty, 1 filled
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Active block positions (list of (x, y))
def spawn_block():
    x = COLS // 2
    # I-block vertical orientation: 4 cells
    return [(x, -i) for i in range(4)]

active = spawn_block()
fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

def move_block(dx, dy):
    global active
    moved = [(x + dx, y + dy) for x, y in active]
    if all(0 <= x < COLS and y < ROWS and (y < 0 or board[y][x] == 0) for x, y in moved):
        active = moved
        return True
    return False

def lock_block():
    for x, y in active:
        if 0 <= y < ROWS:
            board[y][x] = 1
    if any(board[0][x] for x in range(COLS)):
        pygame.quit()
        sys.exit()
    return spawn_block()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == fall_event:
            if not move_block(0, 1):
                active = lock_block()

    screen.fill(BG_COLOR)

    # Draw fixed blocks
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLOCK_COLOR, rect)

    # Draw active block
    for x, y in active:
        if y >= 0:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLOCK_COLOR, rect)

    # Draw grid lines
    for x in range(COLS + 1):
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
