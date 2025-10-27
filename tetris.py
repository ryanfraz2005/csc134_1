import pygame
import random

# Initialize Pygame
pygame.init()

# Constants - Better proportions
BLOCK_SIZE = 32
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
PADDING = 30
SIDEBAR_WIDTH = 300
PANEL_MARGIN = 15

GAME_AREA_WIDTH = BOARD_WIDTH * BLOCK_SIZE + PADDING * 2
GAME_AREA_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE + PADDING * 2
SCREEN_WIDTH = GAME_AREA_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = GAME_AREA_HEIGHT

# Colors - Modern color scheme
BG_COLOR = (15, 15, 25)
BOARD_BG = (25, 25, 40)
GRID_COLOR = (40, 40, 60)
PANEL_BG = (30, 30, 50)
PANEL_BORDER = (60, 60, 90)
TEXT_PRIMARY = (240, 240, 255)
TEXT_SECONDARY = (150, 150, 180)
ACCENT = (100, 150, 255)

# Piece colors - Vibrant and distinct
CYAN = (0, 240, 240)
YELLOW = (255, 220, 0)
PURPLE = (180, 0, 255)
GREEN = (0, 255, 100)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
ORANGE = (255, 140, 0)

# Tetromino shapes
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
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_index]]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Classic Edition")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.board_colors = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Timing
        self.fall_time = 0
        self.fall_speed = 800
        
        # Fonts - Better hierarchy
        self.title_font = pygame.font.Font(None, 56)
        self.large_font = pygame.font.Font(None, 42)
        self.medium_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
    
    def is_valid_move(self, piece, offset_x=0, offset_y=0):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = piece.x + j + offset_x
                    new_y = piece.y + i + offset_y
                    
                    if (new_x < 0 or new_x >= BOARD_WIDTH or 
                        new_y >= BOARD_HEIGHT):
                        return False
                    
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True
    
    def lock_piece(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell and self.current_piece.y + i >= 0:
                    y = self.current_piece.y + i
                    x = self.current_piece.x + j
                    self.board[y][x] = 1
                    self.board_colors[y][x] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        if not self.is_valid_move(self.current_piece):
            self.game_over = True
    
    def clear_lines(self):
        lines = []
        for i in range(BOARD_HEIGHT):
            if all(self.board[i]):
                lines.append(i)
        
        for line in lines:
            del self.board[line]
            del self.board_colors[line]
            self.board.insert(0, [0] * BOARD_WIDTH)
            self.board_colors.insert(0, [None] * BOARD_WIDTH)
        
        if lines:
            self.lines_cleared += len(lines)
            points = [0, 100, 300, 500, 800][len(lines)]
            self.score += points * self.level
            self.level = min(self.lines_cleared // 10 + 1, 15)
            self.fall_speed = max(100, 800 - (self.level - 1) * 50)
    
    def move(self, dx, dy):
        if self.is_valid_move(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate(self):
        old_shape = [row[:] for row in self.current_piece.shape]
        self.current_piece.rotate()
        
        if not self.is_valid_move(self.current_piece):
            # Try wall kicks
            for offset in [(1, 0), (-1, 0), (0, -1)]:
                if self.is_valid_move(self.current_piece, offset[0], offset[1]):
                    self.current_piece.x += offset[0]
                    self.current_piece.y += offset[1]
                    return
            self.current_piece.shape = old_shape
    
    def hard_drop(self):
        while self.move(0, 1):
            self.score += 2
        self.lock_piece()
    
    def draw_block(self, x, y, color, size=BLOCK_SIZE):
        # Inner block
        inner_size = size - 4
        pygame.draw.rect(self.screen, color, 
                        (x + 2, y + 2, inner_size, inner_size))
        
        # Highlight
        highlight = tuple(min(c + 50, 255) for c in color)
        pygame.draw.line(self.screen, highlight, (x + 2, y + 2), 
                        (x + size - 2, y + 2), 2)
        pygame.draw.line(self.screen, highlight, (x + 2, y + 2), 
                        (x + 2, y + size - 2), 2)
        
        # Shadow
        shadow = tuple(max(c - 50, 0) for c in color)
        pygame.draw.line(self.screen, shadow, (x + size - 2, y + 2), 
                        (x + size - 2, y + size - 2), 2)
        pygame.draw.line(self.screen, shadow, (x + 2, y + size - 2), 
                        (x + size - 2, y + size - 2), 2)
    
    def draw_board(self):
        # Board background with border
        board_x = PADDING
        board_y = PADDING
        board_w = BOARD_WIDTH * BLOCK_SIZE
        board_h = BOARD_HEIGHT * BLOCK_SIZE
        
        pygame.draw.rect(self.screen, BOARD_BG, 
                        (board_x, board_y, board_w, board_h))
        pygame.draw.rect(self.screen, ACCENT, 
                        (board_x - 2, board_y - 2, board_w + 4, board_h + 4), 3)
        
        # Grid lines
        for i in range(BOARD_HEIGHT + 1):
            y = board_y + i * BLOCK_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, 
                           (board_x, y), (board_x + board_w, y), 1)
        
        for j in range(BOARD_WIDTH + 1):
            x = board_x + j * BLOCK_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, 
                           (x, board_y), (x, board_y + board_h), 1)
        
        # Draw locked pieces
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.board[i][j]:
                    x = board_x + j * BLOCK_SIZE
                    y = board_y + i * BLOCK_SIZE
                    self.draw_block(x, y, self.board_colors[i][j])
        
        # Draw current piece
        if not self.game_over and not self.paused:
            for i, row in enumerate(self.current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        x = board_x + (self.current_piece.x + j) * BLOCK_SIZE
                        y = board_y + (self.current_piece.y + i) * BLOCK_SIZE
                        if y >= board_y:
                            self.draw_block(x, y, self.current_piece.color)
    
    def draw_panel(self, x, y, w, h):
        pygame.draw.rect(self.screen, PANEL_BG, (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, PANEL_BORDER, (x, y, w, h), 2, border_radius=8)
    
    def draw_text_centered(self, text, font, color, x, y, w):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x + w // 2, y))
        self.screen.blit(surface, rect)
    
    def draw_sidebar(self):
        sidebar_x = GAME_AREA_WIDTH
        
        # Title
        self.draw_text_centered("TETRIS", self.title_font, ACCENT, 
                               sidebar_x, 40, SIDEBAR_WIDTH)
        
        # Next piece panel
        next_y = 100
        next_h = 160
        self.draw_panel(sidebar_x + PANEL_MARGIN, next_y, 
                       SIDEBAR_WIDTH - PANEL_MARGIN * 2, next_h)
        
        label = self.medium_font.render("NEXT", True, TEXT_SECONDARY)
        label_rect = label.get_rect(center=(sidebar_x + SIDEBAR_WIDTH // 2, next_y + 25))
        self.screen.blit(label, label_rect)
        
        # Draw next piece
        piece_size = 25
        shape = self.next_piece.shape
        total_w = len(shape[0]) * piece_size
        total_h = len(shape) * piece_size
        start_x = sidebar_x + (SIDEBAR_WIDTH - total_w) // 2
        start_y = next_y + 65 + (next_h - 65 - total_h) // 2
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    x = start_x + j * piece_size
                    y = start_y + i * piece_size
                    self.draw_block(x, y, self.next_piece.color, piece_size)
        
        # Stats panel
        stats_y = next_y + next_h + 20
        stats_h = 240
        self.draw_panel(sidebar_x + PANEL_MARGIN, stats_y, 
                       SIDEBAR_WIDTH - PANEL_MARGIN * 2, stats_h)
        
        stats_data = [
            ("SCORE", str(self.score), self.large_font),
            ("LEVEL", str(self.level), self.large_font),
            ("LINES", str(self.lines_cleared), self.large_font)
        ]
        
        stat_y = stats_y + 30
        for label, value, font in stats_data:
            label_surf = self.small_font.render(label, True, TEXT_SECONDARY)
            value_surf = font.render(value, True, TEXT_PRIMARY)
            
            label_rect = label_surf.get_rect(center=(sidebar_x + SIDEBAR_WIDTH // 2, stat_y))
            value_rect = value_surf.get_rect(center=(sidebar_x + SIDEBAR_WIDTH // 2, stat_y + 25))
            
            self.screen.blit(label_surf, label_rect)
            self.screen.blit(value_surf, value_rect)
            stat_y += 75
        
        # Controls panel
        controls_y = stats_y + stats_h + 20
        controls_h = 200
        self.draw_panel(sidebar_x + PANEL_MARGIN, controls_y, 
                       SIDEBAR_WIDTH - PANEL_MARGIN * 2, controls_h)
        
        controls_title = self.medium_font.render("CONTROLS", True, TEXT_SECONDARY)
        title_rect = controls_title.get_rect(center=(sidebar_x + SIDEBAR_WIDTH // 2, controls_y + 20))
        self.screen.blit(controls_title, title_rect)
        
        controls = [
            ("← →", "Move"),
            ("↑", "Rotate"),
            ("↓", "Drop"),
            ("SPACE", "Hard Drop"),
            ("P", "Pause")
        ]
        
        control_y = controls_y + 55
        for key, action in controls:
            key_surf = self.small_font.render(key, True, ACCENT)
            action_surf = self.small_font.render(action, True, TEXT_PRIMARY)
            
            self.screen.blit(key_surf, (sidebar_x + 40, control_y))
            self.screen.blit(action_surf, (sidebar_x + 140, control_y))
            control_y += 28
    
    def draw_game_over(self):
        overlay = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BG_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        y_pos = GAME_AREA_HEIGHT // 2 - 80
        
        game_over = self.title_font.render("GAME OVER", True, RED)
        go_rect = game_over.get_rect(center=(GAME_AREA_WIDTH // 2, y_pos))
        self.screen.blit(game_over, go_rect)
        
        score_text = self.large_font.render(f"Score: {self.score}", True, TEXT_PRIMARY)
        score_rect = score_text.get_rect(center=(GAME_AREA_WIDTH // 2, y_pos + 60))
        self.screen.blit(score_text, score_rect)
        
        restart = self.medium_font.render("Press R to Restart", True, ACCENT)
        restart_rect = restart.get_rect(center=(GAME_AREA_WIDTH // 2, y_pos + 110))
        self.screen.blit(restart, restart_rect)
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_board()
        self.draw_sidebar()
        
        if self.game_over:
            self.draw_game_over()
        
        if self.paused and not self.game_over:
            overlay = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BG_COLOR)
            self.screen.blit(overlay, (0, 0))
            
            paused = self.title_font.render("PAUSED", True, ACCENT)
            paused_rect = paused.get_rect(center=(GAME_AREA_WIDTH // 2, GAME_AREA_HEIGHT // 2))
            self.screen.blit(paused, paused_rect)
        
        pygame.display.flip()
    
    def reset(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.board_colors = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 800
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    
                    if event.key == pygame.K_p and not self.game_over:
                        self.paused = not self.paused
                    
                    if not self.game_over and not self.paused:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            if self.move(0, 1):
                                self.score += 1
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()
            
            if not self.game_over and not self.paused:
                self.fall_time += dt
                if self.fall_time >= self.fall_speed:
                    if not self.move(0, 1):
                        self.lock_piece()
                    self.fall_time = 0
            
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()