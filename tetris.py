import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 35
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDEBAR_WIDTH = 280
GAME_AREA_WIDTH = BOARD_WIDTH * BLOCK_SIZE
GAME_AREA_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE
SCREEN_WIDTH = GAME_AREA_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = GAME_AREA_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (60, 60, 60)
DARK_GRAY = (25, 25, 25)
CYAN = (0, 240, 240)
YELLOW = (240, 240, 0)
PURPLE = (160, 0, 240)
GREEN = (0, 240, 0)
RED = (240, 0, 0)
BLUE = (0, 0, 240)
ORANGE = (240, 160, 0)
UI_BG = (35, 35, 50)
UI_PANEL = (45, 45, 65)

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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.tiny_font = pygame.font.Font(None, 22)
    
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
    
    def draw_block(self, x, y, color, offset_x=0, offset_y=0):
        rect = pygame.Rect(offset_x + x * BLOCK_SIZE, offset_y + y * BLOCK_SIZE, 
                          BLOCK_SIZE, BLOCK_SIZE)
        
        # Draw main block
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw highlight for 3D effect
        highlight = tuple(min(c + 40, 255) for c in color)
        pygame.draw.rect(self.screen, highlight, rect, 3)
        
        # Draw border
        pygame.draw.rect(self.screen, DARK_GRAY, rect, 2)
    
    def draw_board(self):
        # Draw board background
        board_rect = pygame.Rect(0, 0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, board_rect)
        
        # Draw grid and blocks
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.board[i][j]:
                    self.draw_block(j, i, self.board_colors[i][j])
                else:
                    # Draw grid lines
                    rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, LIGHT_GRAY, rect, 1)
        
        # Draw board border
        pygame.draw.rect(self.screen, WHITE, board_rect, 3)
    
    def draw_current_piece(self):
        shape = self.current_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_piece.x + j, 
                                  self.current_piece.y + i, 
                                  self.current_piece.color)
    
    def draw_panel(self, x, y, width, height, title):
        # Draw panel background
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, UI_PANEL, panel_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect, 2)
        
        # Draw title
        if title:
            title_text = self.small_font.render(title, True, WHITE)
            title_rect = title_text.get_rect(centerx=x + width // 2, top=y + 10)
            self.screen.blit(title_text, title_rect)
    
    def draw_next_piece(self):
        panel_x = GAME_AREA_WIDTH + 20
        panel_y = 100
        panel_width = SIDEBAR_WIDTH - 40
        panel_height = 150
        
        self.draw_panel(panel_x, panel_y, panel_width, panel_height, "NEXT")
        
        # Draw the next piece centered in the panel
        shape = self.next_piece.get_shape()
        piece_width = len(shape[0]) * 30
        piece_height = len(shape) * 30
        start_x = panel_x + (panel_width - piece_width) // 2
        start_y = panel_y + 50 + (panel_height - 50 - piece_height) // 2
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(start_x + j * 30, start_y + i * 30, 28, 28)
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    highlight = tuple(min(c + 40, 255) for c in self.next_piece.color)
                    pygame.draw.rect(self.screen, highlight, rect, 2)
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
    
    def draw_stats(self):
        panel_x = GAME_AREA_WIDTH + 20
        panel_y = 270
        panel_width = SIDEBAR_WIDTH - 40
        panel_height = 180
        
        self.draw_panel(panel_x, panel_y, panel_width, panel_height, "STATS")
        
        # Draw stats
        stats = [
            ("Score", str(self.score)),
            ("Level", str(self.level)),
            ("Lines", str(self.lines_cleared))
        ]
        
        y_offset = panel_y + 50
        for label, value in stats:
            label_text = self.small_font.render(label + ":", True, LIGHT_GRAY)
            value_text = self.font.render(value, True, WHITE)
            
            self.screen.blit(label_text, (panel_x + 20, y_offset))
            value_rect = value_text.get_rect(right=panel_x + panel_width - 20, centery=y_offset + 15)
            self.screen.blit(value_text, value_rect)
            y_offset += 50
    
    def draw_controls(self):
        panel_x = GAME_AREA_WIDTH + 20
        panel_y = 470
        panel_width = SIDEBAR_WIDTH - 40
        panel_height = 220
        
        self.draw_panel(panel_x, panel_y, panel_width, panel_height, "CONTROLS")
        
        controls = [
            ("← →", "Move"),
            ("↑", "Rotate"),
            ("↓", "Soft Drop"),
            ("Space", "Hard Drop"),
            ("R", "Restart")
        ]
        
        y_offset = panel_y + 50
        for key, action in controls:
            key_text = self.tiny_font.render(key, True, CYAN)
            action_text = self.tiny_font.render(action, True, WHITE)
            
            self.screen.blit(key_text, (panel_x + 20, y_offset))
            self.screen.blit(action_text, (panel_x + 110, y_offset))
            y_offset += 32
    
    def draw_sidebar(self):
        # Draw sidebar background
        sidebar_rect = pygame.Rect(GAME_AREA_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, UI_BG, sidebar_rect)
        
        # Draw title
        title = self.title_font.render("TETRIS", True, WHITE)
        title_rect = title.get_rect(centerx=GAME_AREA_WIDTH + SIDEBAR_WIDTH // 2, top=30)
        self.screen.blit(title, title_rect)
        
        # Draw all panels
        self.draw_next_piece()
        self.draw_stats()
        self.draw_controls()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        
        if not self.game_over:
            self.draw_current_piece()
        
        self.draw_sidebar()
        
        if self.game_over:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over text
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart", True, CYAN)
            
            game_over_rect = game_over_text.get_rect(center=(GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2 - 60))
            score_rect = score_text.get_rect(center=(GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2 + 60))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
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
            self.clock.tick(60)  # 60 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
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