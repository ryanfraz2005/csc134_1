import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.rotation = 0
    
    def get_shape(self):
        return self.shape
    
    def rotate(self):
        # Rotate the shape 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.board_colors = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
        self.spawn_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.current_piece.x = BOARD_WIDTH // 2 - len(self.current_piece.get_shape()[0]) // 2
        self.current_piece.y = 0
        self.next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
        
        if not self.is_valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True
    
    def is_valid_move(self, piece, x, y):
        shape = piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= BOARD_WIDTH or 
                        new_y >= BOARD_HEIGHT or 
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True
    
    def lock_piece(self):
        shape = self.current_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_piece.x + j
                    y = self.current_piece.y + i
                    if y >= 0:
                        self.board[y][x] = 1
                        self.board_colors[y][x] = self.current_piece.color
        self.clear_lines()
        self.spawn_piece()
    
    def clear_lines(self):
        lines_to_clear = []
        for i in range(BOARD_HEIGHT):
            if all(self.board[i]):
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            del self.board[line]
            del self.board_colors[line]
            self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
            self.board_colors.insert(0, [BLACK for _ in range(BOARD_WIDTH)])
        
        num_lines = len(lines_to_clear)
        if num_lines > 0:
            self.lines_cleared += num_lines
            self.score += [0, 100, 300, 500, 800][num_lines] * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 50)
    
    def move(self, dx, dy):
        if self.is_valid_move(self.current_piece, self.current_piece.x + dx, self.current_piece.y + dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self):
        old_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.is_valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = old_shape
    
    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()
    
    def draw_block(self, x, y, color):
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
    
    def draw_board(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.board[i][j]:
                    self.draw_block(j, i, self.board_colors[i][j])
                else:
                    pygame.draw.rect(self.screen, GRAY, 
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    def draw_current_piece(self):
        shape = self.current_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_piece.x + j, 
                                  self.current_piece.y + i, 
                                  self.current_piece.color)
    
    def draw_next_piece(self):
        x_offset = SCREEN_WIDTH + 50
        y_offset = 150
        
        text = self.small_font.render("Next:", True, WHITE)
        self.screen.blit(text, (x_offset, y_offset - 40))
        
        shape = self.next_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(x_offset + j * 25, y_offset + i * 25, 25, 25)
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
    
    def draw_sidebar(self):
        sidebar_x = SCREEN_WIDTH
        pygame.draw.rect(self.screen, (30, 30, 30), (sidebar_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        
        title = self.font.render("TETRIS", True, WHITE)
        self.screen.blit(title, (sidebar_x + 40, 30))
        
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (sidebar_x + 20, 80))
        
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (sidebar_x + 20, 110))
        
        lines_text = self.small_font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (sidebar_x + 20, 140))
        
        self.draw_next_piece()
        
        controls_y = 300
        controls = [
            "Controls:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space: Hard Drop"
        ]
        for i, line in enumerate(controls):
            text = self.small_font.render(line, True, WHITE)
            self.screen.blit(text, (sidebar_x + 20, controls_y + i * 30))
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        if not self.game_over:
            self.draw_current_piece()
        self.draw_sidebar()
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.small_font.render("Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def reset(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.board_colors = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
        self.spawn_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
    
    def run(self):
        running = True
        
        while running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.reset()
                    
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()
            
            if not self.game_over and self.fall_time >= self.fall_speed:
                if not self.move(0, 1):
                    self.lock_piece()
                self.fall_time = 0
            
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()