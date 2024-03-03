import pygame
import random

# 初始化 Pygame
pygame.init()

# 定義顏色
DUMMY = (0,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# 定義方塊顏色
COLORS = [DUMMY, CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, GRAY]

# 定義遊戲板寬高
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 25

# 初始化遊戲視窗
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄羅斯方塊")

# 定義方塊形狀
SHAPES = [
    [[]],
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0], [1, 0], [1, 1]]
]

# 定義遊戲板類
class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    def clear_lines(self):
        lines_cleared = 0
        rows_to_clear = [row for row in range(BOARD_HEIGHT) if all(self.grid[row])]
        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * BOARD_WIDTH)
            lines_cleared += 1
        return lines_cleared

    def is_end(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                print(y + row_index)
                if cell and (y + row_index <= 0):
                    print('game_over')
                    return True
        return False
        
    def is_collision(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                r = y + row_index
                c = x + col_index

                # print('BOARD_WIDTH: ', BOARD_WIDTH)
                # print('BOARD_HEIGHT: ', BOARD_HEIGHT)
                # print('r: ', r, ', c: ', c)
                if cell and c < 0:
                    print('c: ', c)
                    c = 0
                    return True
                if cell and c >= BOARD_WIDTH:
                    print('c: ', c)
                    c = BOARD_WIDTH - 1
                    return True
                if cell and r >= BOARD_HEIGHT:
                    print('r: ', r)
                    r = BOARD_HEIGHT - 1
                    return True
                if cell and self.grid[r][c] != 0:
                    return True
        return False

    def add_shape(self, shape, x, y, type):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell:
                    self.grid[y + row_index][x + col_index] = type

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, COLORS[cell], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(surface, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 定義方塊類
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(1,7)
        self.shape = SHAPES[self.type]
        self.color = COLORS[self.type]

    def move_down(self):
        self.y += 1

    def move_side(self, direction):
        self.x += direction

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, surface):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color, ((self.x + col_index) * BLOCK_SIZE, (self.y + row_index) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(surface, BLACK, ((self.x + col_index) * BLOCK_SIZE, (self.y + row_index) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 定義遊戲主程式
def main():
    clock = pygame.time.Clock()
    board = Board()
    tetromino = Tetromino(4, 0)
    print(tetromino.shape)
    game_over = False
    while not game_over:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not board.is_collision(tetromino.shape, tetromino.x - 1, tetromino.y):
                        tetromino.move_side(-1)
                elif event.key == pygame.K_RIGHT:
                    if not board.is_collision(tetromino.shape, tetromino.x + 1, tetromino.y):
                        tetromino.move_side(1)
                elif event.key == pygame.K_UP:
                    tetromino.rotate()
                elif event.key == pygame.K_DOWN:
                    if not board.is_collision(tetromino.shape, tetromino.x, tetromino.y + 1):
                        tetromino.move_down()

        if board.is_collision(tetromino.shape, tetromino.x, tetromino.y + 1):
            if board.is_end(tetromino.shape, tetromino.x, tetromino.y):
                game_over = True
            else:
                board.add_shape(tetromino.shape, tetromino.x, tetromino.y, tetromino.type)
                lines_cleared = board.clear_lines()
                tetromino = Tetromino(4, 0)
        else:
            tetromino.move_down()
            
        

        board.draw(screen)
        tetromino.draw(screen)
        pygame.display.flip()
        clock.tick(10)
    
    # for i in range(1000):
    #     screen.fill(WHITE)
    #     board.draw(screen)
    #     tetromino.draw(screen)
    #     pygame.display.flip()
    #     clock.tick(10)
    pygame.quit()

if __name__ == "__main__":
    main()