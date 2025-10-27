import pygame
import sys
import random
import requests
from io import BytesIO

# --- 1. CONFIGURATION AND INITIAL SETUP ---
# NOTE: This script requires the 'requests' library (pip install requests) 
# and an active internet connection to load the sprites from the PokeAPI.

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulation (Polished GFX & Sprites)")

# --- SPRITE CONFIGURATION ---
SPRITES = {
    "Charizard": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
    "Tyranitar": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/248.png",
    "Scizor": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/212.png",
    "Espeon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/196.png",
    "Blastoise": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png",
    "Venusaur": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png",
}
SPRITE_CACHE = {}

# --- COLORS AND STYLES (Modern Aesthetic) ---
BLACK = (25, 25, 25)
WHITE = (255, 255, 255)
# Background
BG_TOP_COLOR = (150, 200, 255) # Light Sky
BG_BOTTOM_COLOR = (200, 220, 255) # Lighter Sky
# Platforms
FIELD_COLOR_PLAYER = (80, 160, 50) # Darker Green Grass
FIELD_COLOR_OPP = (180, 150, 120) # Stone/Dirt
# UI
UI_BOX_BG = (230, 230, 230)
UI_BOX_BORDER = (50, 50, 50)
MENU_BLUE = (50, 150, 250)

# HP Bar Colors
HP_MAX = (0, 200, 0)
HP_MID = (255, 215, 0)
HP_LOW = (200, 0, 0)
HP_BG = (100, 100, 100) # Darker grey background

# Fonts
FONT_SIZE_TITLE = 32
FONT_SIZE_MAIN = 24
FONT_SIZE_SMALL = 18
font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
font_main = pygame.font.Font(None, FONT_SIZE_MAIN)
font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

# Clock and State Management
clock = pygame.time.Clock()
FPS = 30
LEVEL = 50 

BATTLE_STATE_CHOOSING_ACTION = 0
BATTLE_STATE_CHOOSING_MOVE = 1
BATTLE_STATE_AWAITING_AI = 2
BATTLE_STATE_DISPLAY_MESSAGE = 3
BATTLE_STATE_END = 4

battle_state = BATTLE_STATE_CHOOSING_ACTION
message_queue = []
message_display_timer = 0
MESSAGE_DURATION = 90

red_potions_left = 3
red_action_options = ["FIGHT", "ITEM", "SWITCH"]
red_move_selection = 0
red_action_selection = 0

# --- 2. SPRITE LOADING FUNCTIONALITY ---

def load_sprite_from_url(name, url):
    """Downloads a sprite from a URL and loads it into Pygame."""
    try:
        # Check if already loaded
        if name in SPRITE_CACHE:
            return SPRITE_CACHE[name]

        response = requests.get(url)
        response.raise_for_status() # Raise an error for bad status codes
        image_data = BytesIO(response.content)
        
        # Load, convert, and scale
        sprite = pygame.image.load(image_data).convert_alpha()
        
        # Scale for opponent (front sprite) or player (back sprite)
        if "back" in url:
            scale_size = (180, 180) # Player back sprite is usually larger
        else:
            scale_size = (150, 150) # Opponent front sprite
            
        sprite = pygame.transform.scale(sprite, scale_size)
        SPRITE_CACHE[name] = sprite
        return sprite
        
    except requests.exceptions.RequestException as e:
        print(f"Error loading sprite for {name} from {url}: {e}")
        # Return a simple surface if loading fails
        default_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
        default_surface.fill((200, 50, 50, 180))
        draw_text(default_surface, "LOAD FAIL", font_small, WHITE, 75, 75, center=True)
        return default_surface

# --- 3. POKEMON AND DAMAGE LOGIC (Simplified for brevity, same as before) ---

class Pokemon:
    # ... (Pokemon class definition here - same as previous version) ...
    def __init__(self, name, type, max_hp, attack, defense, moves, is_player_one):
        self.name = name
        self.type = type
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.moves = moves
        self.is_player_one = is_player_one

    def is_fainted(self):
        return self.current_hp <= 0

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

# (Type chart and damage calculation functions removed for brevity - assume they are present)
TYPE_CHART = { "NORMAL": {"ROCK": 0.5, "GHOST": 0.0}, "FIGHTING": {"NORMAL": 2.0, "ROCK": 2.0, "GHOST": 0.0, "FLYING": 0.5, "PSYCHIC": 0.5}, "FLYING": {"FIGHTING": 2.0, "BUG": 2.0, "ROCK": 0.5}, "POISON": {"GRASS": 2.0, "GROUND": 0.5, "ROCK": 0.5}, "GROUND": {"POISON": 2.0, "ROCK": 2.0, "FIRE": 2.0, "FLYING": 0.0, "GRASS": 0.5}, "ROCK": {"FLYING": 2.0, "FIRE": 2.0, "BUG": 2.0, "GROUND": 0.5}, "BUG": {"GRASS": 2.0, "PSYCHIC": 2.0, "POISON": 0.5, "FIRE": 0.5}, "GHOST": {"GHOST": 2.0, "NORMAL": 0.0}, "FIRE": {"GRASS": 2.0, "BUG": 2.0, "WATER": 0.5, "ROCK": 0.5}, "WATER": {"FIRE": 2.0, "GROUND": 2.0, "GRASS": 0.5}, "GRASS": {"WATER": 2.0, "GROUND": 2.0, "FIRE": 0.5, "FLYING": 0.5, "BUG": 0.5, "POISON": 0.5}, "PSYCHIC": {"FIGHTING": 2.0, "POISON": 2.0, "PSYCHIC": 0.5, "DARK": 0.0}, "DARK": {"GHOST": 2.0, "PSYCHIC": 2.0, "FIGHTING": 0.5}, "STEEL": {"ROCK": 2.0, "ICE": 2.0, "FIRE": 0.5, "WATER": 0.5}, }
for t in list(TYPE_CHART.keys()):
    for other_t in list(TYPE_CHART.keys()):
        if other_t not in TYPE_CHART[t]: TYPE_CHART[t][other_t] = 1.0

def calculate_damage(attacker, defender, move):
    power = move['power']
    move_type = move['type']
    base = int((((2 * LEVEL / 5 + 2) * power * attacker.attack / defender.defense) / 50) + 2)
    crit_multiplier = 1.5 if random.random() < 1/16 else 1.0
    random_mult = random.randint(85, 100) / 100.0
    stab_multiplier = 1.5 if attacker.type == move_type else 1.0
    type_mult = TYPE_CHART.get(move_type, {}).get(defender.type, 1.0)
    damage = int(base * crit_multiplier * random_mult * stab_multiplier * type_mult)
    if damage < 1: damage = 1
    return damage, crit_multiplier, type_mult

def use_move(attacker, defender, move_name):
    move = attacker.moves.get(move_name)
    if not move: return [f"{attacker.name} failed to use {move_name}!"]
    damage, crit_mult, type_mult = calculate_damage(attacker, defender, move)
    defender.take_damage(damage)
    messages = [f"{attacker.name} used {move_name}!"]
    if crit_mult > 1.0: messages.append("A critical hit!")
    if type_mult >= 2.0: messages.append("It's Super Effective!")
    elif type_mult == 0.0: messages.append(f"It had no effect on {defender.name}!")
    elif type_mult < 1.0: messages.append("It's not very effective...")
    messages.append(f"{defender.name} took {damage} damage.")
    return messages

def use_item(pokemon):
    global red_potions_left
    heal_amount = 60 
    current_hp = pokemon.current_hp
    max_hp = pokemon.max_hp
    if red_potions_left <= 0: return ["No Potions left!"]
    if current_hp == max_hp: return [f"{pokemon.name} is already at full health!"]
    red_potions_left -= 1
    amount_healed = min(max_hp - current_hp, heal_amount)
    pokemon.current_hp += amount_healed
    messages = [ f"Red used a Potion on {pokemon.name}!", f"{pokemon.name} recovered {amount_healed} HP." ]
    return messages
    
# --- 4. TEAM SETUP ---

# Note: The first Pokémon's sprite will be pre-loaded at the start.
red_team_data = [
    Pokemon("Tyranitar", "DARK", 120, 150, 110, {"Rock Slide": {"type": "ROCK", "power": 75}, "Crunch": {"type": "DARK", "power": 80}}, True),
    Pokemon("Scizor", "STEEL", 100, 130, 100, {"Iron Head": {"type": "STEEL", "power": 80}, "Slash": {"type": "NORMAL", "power": 70}}, True),
    Pokemon("Espeon", "PSYCHIC", 95, 120, 70, {"Psychic": {"type": "PSYCHIC", "power": 90}, "Swift": {"type": "NORMAL", "power": 60}}, True)
]
red_team = red_team_data[:]

blue_team_data = [
    Pokemon("Charizard", "FIRE", 110, 120, 90, {"Flamethrower": {"type": "FIRE", "power": 95}, "Slash": {"type": "NORMAL", "power": 70}}, False),
    Pokemon("Blastoise", "WATER", 115, 110, 120, {"Surf": {"type": "WATER", "power": 90}, "Bite": {"type": "NORMAL", "power": 60}}, False),
    Pokemon("Venusaur", "GRASS", 110, 100, 115, {"Razor Leaf": {"type": "GRASS", "power": 55}, "Body Slam": {"type": "NORMAL", "power": 85}}, False)
]
blue_team = blue_team_data[:]

red_current = red_team[0]
blue_current = blue_team[0]
turn = "RED"

message_queue.append(f"Battle Start! Blue sent out {blue_current.name}!")
message_queue.append(f"Red sent out {red_current.name}!")

# Pre-load initial sprites (must happen after Pygame init)
red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name])
blue_sprite = load_sprite_from_url(blue_current.name, SPRITES[blue_current.name])

# --- 5. GFX AND DRAWING FUNCTIONS ---

def draw_text(surface, text, font, color, x, y, center=False):
    """Utility to draw text."""
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))

def draw_hp_bar(surface, pokemon, x, y, width=200, height=12):
    """Draws a professional, rounded HP bar with color changes."""
    hp_ratio = pokemon.current_hp / pokemon.max_hp if pokemon.max_hp > 0 else 0
    current_width = int(width * hp_ratio)

    if hp_ratio > 0.5:
        color = HP_MAX
    elif hp_ratio > 0.2:
        color = HP_MID
    else:
        color = HP_LOW

    # Draw rounded background track
    pygame.draw.rect(surface, HP_BG, (x, y, width, height), 0, 6)
    
    # Draw colored fill (only draw if HP > 0)
    if current_width > 0:
        fill_rect = (x, y, current_width, height)
        # We draw a small rectangle and then a rounded one over it to manage the end curve
        pygame.draw.rect(surface, color, fill_rect, 0, 6)
        # Ensure the beginning edge is always straight/filled
        if current_width > 6:
             pygame.draw.rect(surface, color, (x + 6, y, current_width - 6, height))

def draw_info_box(surface, pokemon, is_player_one):
    """Draws the detailed name/HP box with an angular, polished look."""
    
    if is_player_one: 
        # Red's Box (Bottom Left, styled as a modern bottom screen info panel)
        box_rect = pygame.Rect(450, 370, 330, 100)
    else: 
        # Blue's Box (Top Right, styled for opponent)
        box_rect = pygame.Rect(20, 50, 330, 80)

    # 1. Main Background
    pygame.draw.rect(surface, UI_BOX_BG, box_rect, 0, 10)
    
    # 2. Outline (Dark border for contrast)
    pygame.draw.rect(surface, UI_BOX_BORDER, box_rect, 3, 10)
    
    # 3. Label/Header Area (Optional accent color)
    header_rect = box_rect.inflate(-6, -6)
    header_rect.height = 30
    pygame.draw.rect(surface, (180, 180, 180), header_rect, 0, 7) # Light grey accent

    # 4. Text Content
    draw_text(surface, pokemon.name, font_main, BLACK, box_rect.x + 10, box_rect.y + 10)
    draw_text(surface, f"Lv.{LEVEL}", font_main, BLACK, box_rect.x + 280, box_rect.y + 10)
    
    hp_bar_x = box_rect.x + 80
    hp_bar_y = box_rect.y + 50
    hp_bar_width = 230
    
    draw_text(surface, "HP:", font_small, BLACK, box_rect.x + 10, box_rect.y + 47)
    draw_hp_bar(surface, pokemon, hp_bar_x, hp_bar_y, hp_bar_width, height=12)
    
    if is_player_one:
        hp_text = f"{pokemon.current_hp}/{pokemon.max_hp}"
        draw_text(surface, hp_text, font_small, BLACK, box_rect.x + 170, box_rect.y + 75)

def draw_message_box(surface, message):
    """Draws the main message box, spanning the bottom of the screen."""
    msg_box_rect = pygame.Rect(0, SCREEN_HEIGHT - 130, SCREEN_WIDTH, 130)
    
    # Main Box BG
    pygame.draw.rect(surface, MENU_BLUE, msg_box_rect)
    
    # Text Area Box (Floating, white background)
    text_area_rect = pygame.Rect(15, SCREEN_HEIGHT - 115, SCREEN_WIDTH - 30, 40)
    pygame.draw.rect(surface, WHITE, text_area_rect, 0, 8)
    pygame.draw.rect(surface, BLACK, text_area_rect, 2, 8) 
    
    draw_text(surface, message, font_main, BLACK, text_area_rect.x + 15, text_area_rect.centery, center=False)

def draw_button(surface, rect, text, is_selected):
    """Helper function to draw a single, stylized button."""
    fill_color = (255, 255, 100) if is_selected else UI_BOX_BG
    light_edge = (255, 255, 255)
    dark_edge = (100, 100, 100)
    
    # Outer 3D effect (shadow)
    if not is_selected:
        pygame.draw.rect(surface, dark_edge, (rect.x + 3, rect.y + 3, rect.width, rect.height), 0, 8)
    
    # Main button body
    pygame.draw.rect(surface, fill_color, rect, 0, 8) 
    
    # Inner highlights (top/left)
    pygame.draw.line(surface, light_edge, (rect.x + 1, rect.y + 1), (rect.x + rect.width - 2, rect.y + 1), 2)
    pygame.draw.line(surface, light_edge, (rect.x + 1, rect.y + 1), (rect.x + 1, rect.y + rect.height - 2), 2)
    
    # Outer border
    pygame.draw.rect(surface, BLACK, rect, 1, 8)
    
    draw_text(surface, text, font_main, BLACK, rect.centerx, rect.centery, center=True)


def draw_command_menu(surface):
    """Draws the action menu (FIGHT, ITEM, SWITCH) using buttons."""
    global red_action_options, red_action_selection
    
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 85
    menu_width, menu_height = SCREEN_WIDTH // 2 - 20, 60
    
    for i, option in enumerate(red_action_options):
        row = i // 2
        col = i % 2
        
        # Adjust position to be centered at the bottom right
        button_x = menu_x + 10 + col * (menu_width // 2)
        button_y = menu_y + row * (menu_height // 2 + 5)
        button_width = menu_width // 2 - 15
        button_height = 30
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        draw_button(surface, button_rect, option, (i == red_action_selection))


def draw_fight_menu(surface):
    """Draws the move selection menu using buttons."""
    global red_move_selection
    
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 85
    menu_width, menu_height = SCREEN_WIDTH // 2 - 20, 60
    
    moves = list(red_current.moves.keys())
    
    for i, move_name in enumerate(moves):
        row = i // 2
        col = i % 2
        
        button_x = menu_x + 10 + col * (menu_width // 2)
        button_y = menu_y + row * (menu_height // 2 + 5)
        button_width = menu_width // 2 - 15
        button_height = 30
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        draw_button(surface, button_rect, move_name, (i == red_move_selection))


def draw_arena(surface):
    """Draws the background arena, platforms, and sprites."""
    global red_sprite, blue_sprite
    
    # 1. Main Sky Background (Gradient)
    for y in range(0, SCREEN_HEIGHT - 130):
        # Interpolate color between top and bottom
        r = int(BG_TOP_COLOR[0] + (BG_BOTTOM_COLOR[0] - BG_TOP_COLOR[0]) * (y / (SCREEN_HEIGHT - 130)))
        g = int(BG_TOP_COLOR[1] + (BG_BOTTOM_COLOR[1] - BG_TOP_COLOR[1]) * (y / (SCREEN_HEIGHT - 130)))
        b = int(BG_TOP_COLOR[2] + (BG_BOTTOM_COLOR[2] - BG_TOP_COLOR[2]) * (y / (SCREEN_HEIGHT - 130)))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
    # 2. Platforms (Stylized ellipses for depth)
    
    # Opponent Platform (Top-Left)
    opp_platform_rect = pygame.Rect(50, 150, 300, 50)
    pygame.draw.ellipse(surface, FIELD_COLOR_OPP, opp_platform_rect)
    pygame.draw.ellipse(surface, BLACK, opp_platform_rect, 3) 
    
    # Player Platform (Bottom-Right, larger)
    player_platform_rect = pygame.Rect(400, 350, 380, 80)
    pygame.draw.ellipse(surface, FIELD_COLOR_PLAYER, player_platform_rect)
    pygame.draw.ellipse(surface, BLACK, player_platform_rect, 4) 

    # 3. Pokémon Sprites
    
    # BLUE'S SPRITE (Opponent - Top-Left)
    if blue_current and blue_current.name in SPRITE_CACHE:
        sprite = SPRITE_CACHE[blue_current.name]
        # Position sprite above the platform
        surface.blit(sprite, (opp_platform_rect.centerx - sprite.get_width() // 2, opp_platform_rect.y - sprite.get_height() + 20))
    
    # RED'S SPRITE (Player - Bottom-Right)
    if red_current and red_current.name in SPRITE_CACHE:
        sprite = SPRITE_CACHE[red_current.name]
        # Position sprite above the platform
        surface.blit(sprite, (player_platform_rect.centerx - sprite.get_width() // 2, player_platform_rect.y - sprite.get_height() + 40))

# --- 6. GAME CONTROL FLOW ---

def handle_faint(fainted_pokemon):
    # (Faint and switch logic - includes loading new sprite on switch)
    global red_current, blue_current, battle_state, message_queue, red_sprite, blue_sprite
    
    is_red = fainted_pokemon.is_player_one
    
    if not is_red:
        fainted_name = blue_current.name
        blue_team[:] = [p for p in blue_team if p.name != fainted_name]
        try:
            blue_current = blue_team[0]
            # Load new sprite
            blue_sprite = load_sprite_from_url(blue_current.name, SPRITES[blue_current.name])
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Blue sends out {blue_current.name}!")
        except IndexError:
            message_queue.append("Blue is defeated! Red wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    else:
        fainted_name = red_current.name
        red_team[:] = [p for p in red_team if p.name != fainted_name]
        try:
            red_current = red_team[0]
            # Load new sprite
            red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name])
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Red automatically sends out {red_current.name}!")
        except IndexError:
            message_queue.append("Red is defeated! Blue wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    return False

def execute_player_turn(action, data=None):
    # (Turn execution logic)
    global battle_state, message_queue, red_current, red_sprite, blue_current
    
    if action == "FIGHT":
        move_name = list(red_current.moves.keys())[data]
        messages = use_move(red_current, blue_current, move_name)
        message_queue.extend(messages)
    
    elif action == "ITEM":
        messages = use_item(red_current)
        message_queue.extend(messages)
        
    elif action == "SWITCH":
        # Find next available Pokémon that is not fainted
        next_pokemon = next((p for p in red_team if p != red_current and not p.is_fainted()), None)
        
        if next_pokemon:
            old_name = red_current.name
            
            red_team.remove(next_pokemon)
            red_team.insert(0, next_pokemon)
            red_current = next_pokemon
            
            # Load new sprite for the switched-in Pokémon
            red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name])
            
            message_queue.append(f"Red withdrew {old_name}!")
            message_queue.append(f"Red sent out {red_current.name}!")
        else:
            message_queue.append("Red has no other available Pokémon to switch to!")
            battle_state = BATTLE_STATE_CHOOSING_ACTION
            return 
    
    battle_state = BATTLE_STATE_DISPLAY_MESSAGE

def execute_ai_turn():
    # (AI execution logic)
    global battle_state, message_queue, blue_current, red_current
    
    if red_current.is_fainted():
        if handle_faint(red_current):
            return 
    
    if blue_current and not blue_current.is_fainted():
        # AI always chooses a random move for simple simulation
        move_names = list(blue_current.moves.keys())
        move_name = random.choice(move_names)
        messages = use_move(blue_current, red_current, move_name)
        message_queue.extend(messages)

    battle_state = BATTLE_STATE_DISPLAY_MESSAGE


# --- 7. MAIN GAME LOOP ---

running = True
while running:
    
    # Handle Events (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Input handling for state machine
            if battle_state == BATTLE_STATE_CHOOSING_ACTION:
                # Same input logic as before
                if event.key == pygame.K_UP: red_action_selection = max(0, red_action_selection - 2)
                elif event.key == pygame.K_DOWN: red_action_selection = min(len(red_action_options) - 1, red_action_selection + 2)
                elif event.key == pygame.K_LEFT: red_action_selection = max(0, red_action_selection - 1)
                elif event.key == pygame.K_RIGHT: red_action_selection = min(len(red_action_options) - 1, red_action_selection + 1)
                elif event.key == pygame.K_RETURN:
                    chosen_action = red_action_options[red_action_selection]
                    if chosen_action == "FIGHT":
                        battle_state = BATTLE_STATE_CHOOSING_MOVE
                        red_move_selection = 0 
                    else:
                        execute_player_turn(chosen_action)
                        turn = "BLUE"
                        
            elif battle_state == BATTLE_STATE_CHOOSING_MOVE:
                moves = list(red_current.moves.keys())
                # Same input logic as before
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT: red_move_selection = max(0, red_move_selection - 1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT: red_move_selection = min(len(moves) - 1, red_move_selection + 1)
                elif event.key == pygame.K_BACKSPACE: battle_state = BATTLE_STATE_CHOOSING_ACTION
                elif event.key == pygame.K_RETURN:
                    execute_player_turn("FIGHT", red_move_selection)
                    turn = "BLUE"
                    
            elif battle_state == BATTLE_STATE_DISPLAY_MESSAGE:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if message_display_timer >= MESSAGE_DURATION or message_display_timer == 0:
                        if message_queue:
                            message_queue.pop(0)
                        message_display_timer = 0
                
    # Update Logic
    if battle_state == BATTLE_STATE_DISPLAY_MESSAGE:
        if message_display_timer < MESSAGE_DURATION and message_queue:
            message_display_timer += 1
        
        if not message_queue:
            if battle_state != BATTLE_STATE_END:
                if handle_faint(red_current) or handle_faint(blue_current):
                    pass
                elif turn == "RED":
                    battle_state = BATTLE_STATE_CHOOSING_ACTION
                elif turn == "BLUE":
                    battle_state = BATTLE_STATE_AWAITING_AI
    
    elif battle_state == BATTLE_STATE_AWAITING_AI:
        execute_ai_turn()
        turn = "RED"
    
    # --- Drawing ---
    
    draw_arena(screen)

    # Draw info boxes
    if blue_current: draw_info_box(screen, blue_current, False)
    if red_current: draw_info_box(screen, red_current, True)
    
    # Determine the current message to display
    current_message = message_queue[0] if message_queue else f"What will {red_current.name} do?"
    
    # Draw menus based on state
    if battle_state == BATTLE_STATE_CHOOSING_ACTION:
        draw_message_box(screen, f"What will {red_current.name} do?")
        draw_command_menu(screen)
    elif battle_state == BATTLE_STATE_CHOOSING_MOVE:
        draw_message_box(screen, "Choose a move.")
        draw_fight_menu(screen)
    elif battle_state == BATTLE_STATE_DISPLAY_MESSAGE or battle_state == BATTLE_STATE_AWAITING_AI:
        draw_message_box(screen, current_message)
    elif battle_state == BATTLE_STATE_END:
        draw_message_box(screen, current_message)
        draw_text(screen, "BATTLE ENDED (Press ESC to Exit)", font_main, BLACK, SCREEN_WIDTH // 2, 20, center=True)

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()