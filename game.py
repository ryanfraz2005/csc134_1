import pygame
import sys
import random
import requests
from io import BytesIO

# --- 1. CONFIGURATION AND INITIAL SETUP ---
# NOTE: This script requires:
#   1. The 'requests' library (pip install requests) for sprites.
#   2. An active internet connection to load the sprites.
#   3. A MIDI music file (e.g., 'hgss_lance_red.mid') in the same directory for music.

pygame.init()
pygame.mixer.init() # Initialize the mixer for music and sound effects

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulation (Final Polished GFX & Music)")

# --- SPRITE CONFIGURATION ---
SPRITES = {
    # Blue's Team (Opponent - Front Sprites, will be flipped horizontally)
    "Charizard": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
    "Blastoise": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png",
    "Venusaur": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png",
    
    # Red's Team (Player - Back Sprites, default orientation)
    "Tyranitar": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/248.png",
    "Scizor": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/212.png",
    "Espeon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/196.png",
}
SPRITE_CACHE = {}

# --- MUSIC CONFIGURATION ---
MUSIC_FILE = 'hgss_lance_red.mid' # <<< Make sure you have this file in your script's directory!
try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play(-1) # Play indefinitely
except pygame.error as e:
    print(f"Could not load music file '{MUSIC_FILE}'. Ensure it's in the same directory. Error: {e}")
    print("Music will not play in this session.")

# --- COLORS AND STYLES ---
BLACK = (25, 25, 25)
WHITE = (255, 255, 255)

# Background Gradient
SKY_BLUE_LIGHT = (150, 200, 255) 
SKY_BLUE_DARK = (100, 150, 220)

# Platforms
PLAYER_PLATFORM_COLOR_LIGHT = (90, 180, 60)
PLAYER_PLATFORM_COLOR_DARK = (50, 120, 30)
OPPONENT_PLATFORM_COLOR_LIGHT = (180, 150, 120)
OPPONENT_PLATFORM_COLOR_DARK = (120, 90, 70)

# UI Boxes
UI_PRIMARY_BG = (230, 230, 230)
UI_SECONDARY_BG = (200, 200, 200)
UI_BORDER_DARK = (40, 40, 40)
UI_BORDER_LIGHT = (255, 255, 255)
MENU_ACCENT_BLUE = (50, 150, 250)

# HP Bar Colors
HP_MAX = (0, 200, 0)
HP_MID = (255, 215, 0)
HP_LOW = (200, 0, 0)
HP_BG = (100, 100, 100)

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

def load_sprite_from_url(name, url, flip_horizontally=False):
    """Downloads a sprite from a URL, loads it, scales it, and optionally flips it."""
    try:
        if (name, flip_horizontally) in SPRITE_CACHE: # Cache also by flip status
            return SPRITE_CACHE[(name, flip_horizontally)]

        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        
        sprite = pygame.image.load(image_data).convert_alpha()
        
        if "back" in url:
            scale_size = (180, 180) # Player back sprite
        else:
            scale_size = (150, 150) # Opponent front sprite
            
        sprite = pygame.transform.scale(sprite, scale_size)

        if flip_horizontally:
            sprite = pygame.transform.flip(sprite, True, False) # Flip horizontally

        SPRITE_CACHE[(name, flip_horizontally)] = sprite
        return sprite
        
    except requests.exceptions.RequestException as e:
        print(f"Error loading sprite for {name} from {url}: {e}")
        default_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
        default_surface.fill((200, 50, 50, 180))
        draw_text(default_surface, "LOAD FAIL", font_small, WHITE, 75, 75, center=True)
        return default_surface

# --- 3. POKEMON AND DAMAGE LOGIC ---

class Pokemon:
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

TYPE_CHART = {
    "NORMAL": {"ROCK": 0.5, "GHOST": 0.0},
    "FIGHTING": {"NORMAL": 2.0, "ROCK": 2.0, "GHOST": 0.0, "FLYING": 0.5, "PSYCHIC": 0.5},
    "FLYING": {"FIGHTING": 2.0, "BUG": 2.0, "ROCK": 0.5},
    "POISON": {"GRASS": 2.0, "GROUND": 0.5, "ROCK": 0.5},
    "GROUND": {"POISON": 2.0, "ROCK": 2.0, "FIRE": 2.0, "FLYING": 0.0, "GRASS": 0.5},
    "ROCK": {"FLYING": 2.0, "FIRE": 2.0, "BUG": 2.0, "GROUND": 0.5},
    "BUG": {"GRASS": 2.0, "PSYCHIC": 2.0, "POISON": 0.5, "FIRE": 0.5},
    "GHOST": {"GHOST": 2.0, "NORMAL": 0.0},
    "FIRE": {"GRASS": 2.0, "BUG": 2.0, "WATER": 0.5, "ROCK": 0.5},
    "WATER": {"FIRE": 2.0, "GROUND": 2.0, "GRASS": 0.5},
    "GRASS": {"WATER": 2.0, "GROUND": 2.0, "FIRE": 0.5, "FLYING": 0.5, "BUG": 0.5, "POISON": 0.5},
    "PSYCHIC": {"FIGHTING": 2.0, "POISON": 2.0, "PSYCHIC": 0.5, "DARK": 0.0},
    "DARK": {"GHOST": 2.0, "PSYCHIC": 2.0, "FIGHTING": 0.5},
    "STEEL": {"ROCK": 2.0, "ICE": 2.0, "FIRE": 0.5, "WATER": 0.5},
}
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

# Pre-load initial sprites with correct flipping
red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name], flip_horizontally=False)
blue_sprite = load_sprite_from_url(blue_current.name, SPRITES[blue_current.name], flip_horizontally=True) # Blue's sprite is flipped

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

    pygame.draw.rect(surface, HP_BG, (x, y, width, height), 0, 6)
    
    if current_width > 0:
        fill_rect = (x, y, current_width, height)
        pygame.draw.rect(surface, color, fill_rect, 0, 6)
        if current_width > 6:
             pygame.draw.rect(surface, color, (x + 6, y, current_width - 6, height))

def draw_info_box(surface, pokemon, is_player_one):
    """Draws the detailed name/HP box with an angular, polished look."""
    
    if is_player_one: 
        box_rect = pygame.Rect(20, 370, 330, 100) # Player (Red) - Bottom Left
    else: 
        box_rect = pygame.Rect(450, 50, 330, 80) # Opponent (Blue) - Top Right

    pygame.draw.rect(surface, UI_PRIMARY_BG, box_rect, 0, 10)
    pygame.draw.rect(surface, UI_BORDER_DARK, (box_rect.x + 3, box_rect.y + 3, box_rect.width, box_rect.height), 0, 10)
    pygame.draw.rect(surface, UI_PRIMARY_BG, box_rect, 0, 10)

    pygame.draw.rect(surface, UI_BORDER_DARK, box_rect, 2, 10)
    
    pygame.draw.line(surface, UI_BORDER_LIGHT, (box_rect.x + 2, box_rect.y + 2), (box_rect.x + box_rect.width - 3, box_rect.y + 2), 2)
    pygame.draw.line(surface, UI_BORDER_LIGHT, (box_rect.x + 2, box_rect.y + 2), (box_rect.x + 2, box_rect.y + box_rect.height - 3), 2)

    header_rect = box_rect.inflate(-4, -4)
    header_rect.height = 30
    header_rect.x += 2
    header_rect.y += 2
    pygame.draw.rect(surface, UI_SECONDARY_BG, header_rect, 0, 8)

    draw_text(surface, pokemon.name, font_main, BLACK, box_rect.x + 15, box_rect.y + 10)
    draw_text(surface, f"Lv.{LEVEL}", font_main, BLACK, box_rect.x + 270, box_rect.y + 10)
    
    hp_bar_x = box_rect.x + 80
    hp_bar_y = box_rect.y + 50 if is_player_one else box_rect.y + 40
    hp_bar_width = 230
    
    draw_text(surface, "HP:", font_small, BLACK, box_rect.x + 15, box_rect.y + 47 if is_player_one else box_rect.y + 37)
    draw_hp_bar(surface, pokemon, hp_bar_x, hp_bar_y, hp_bar_width, height=12)
    
    if is_player_one:
        hp_text = f"{pokemon.current_hp}/{pokemon.max_hp}"
        draw_text(surface, hp_text, font_small, BLACK, box_rect.x + 170, box_rect.y + 75)

def draw_message_box(surface, message):
    """Draws the main message box."""
    msg_box_rect = pygame.Rect(0, SCREEN_HEIGHT - 130, SCREEN_WIDTH, 130)
    
    for y in range(msg_box_rect.y, msg_box_rect.bottom):
        alpha = int(255 * ((y - msg_box_rect.y) / msg_box_rect.height * 0.5 + 0.5))
        color = (MENU_ACCENT_BLUE[0], MENU_ACCENT_BLUE[1], MENU_ACCENT_BLUE[2], alpha)
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

    text_area_rect = pygame.Rect(15, SCREEN_HEIGHT - 115, SCREEN_WIDTH - 30, 40)
    pygame.draw.rect(surface, WHITE, text_area_rect, 0, 8)
    pygame.draw.rect(surface, BLACK, text_area_rect, 2, 8) 
    
    draw_text(surface, message, font_main, BLACK, text_area_rect.x + 15, text_area_rect.centery, center=False)

def draw_button(surface, rect, text, is_selected):
    """Helper function to draw a single, stylized button."""
    fill_color = (255, 255, 150) if is_selected else UI_PRIMARY_BG
    border_color = BLACK
    shadow_offset = 3
    
    if not is_selected:
        pygame.draw.rect(surface, UI_BORDER_DARK, (rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height), 0, 8)
    
    pygame.draw.rect(surface, fill_color, rect, 0, 8) 
    pygame.draw.rect(surface, border_color, rect, 2, 8)
    
    draw_text(surface, text, font_main, BLACK, rect.centerx, rect.centery, center=True)


def draw_command_menu(surface):
    """Draws the action menu (FIGHT, ITEM, SWITCH) using buttons."""
    global red_action_options, red_action_selection
    
    menu_x_start = SCREEN_WIDTH // 2 + 10
    menu_y_start = SCREEN_HEIGHT - 105
    button_width = (SCREEN_WIDTH // 2) - 40
    button_height = 40
    button_spacing = 10
    
    for i, option in enumerate(red_action_options):
        row = i % 2
        col = i // 2
        
        btn_x = menu_x_start + col * (button_width + button_spacing)
        btn_y = menu_y_start + row * (button_height + button_spacing)
        
        button_rect = pygame.Rect(btn_x, btn_y, button_width // 2 - button_spacing, button_height)
        draw_button(surface, button_rect, option, (i == red_action_selection))


def draw_fight_menu(surface):
    """Draws the move selection menu using buttons."""
    global red_move_selection
    
    menu_x_start = SCREEN_WIDTH // 2 + 10
    menu_y_start = SCREEN_HEIGHT - 105
    button_width = (SCREEN_WIDTH // 2) - 40
    button_height = 40
    button_spacing = 10
    
    moves = list(red_current.moves.keys())
    
    for i, move_name in enumerate(moves):
        row = i % 2
        col = i // 2
        
        btn_x = menu_x_start + col * (button_width + button_spacing)
        btn_y = menu_y_start + row * (button_height + button_spacing)
        
        button_rect = pygame.Rect(btn_x, btn_y, button_width // 2 - button_spacing, button_height)
        draw_button(surface, button_rect, move_name, (i == red_move_selection))


def draw_arena(surface):
    """Draws the background arena, platforms, and sprites with clouds."""
    global red_sprite, blue_sprite
    
    # 1. Main Sky Background (Gradient)
    for y in range(0, SCREEN_HEIGHT - 130):
        r = int(SKY_BLUE_LIGHT[0] + (SKY_BLUE_DARK[0] - SKY_BLUE_LIGHT[0]) * (y / (SCREEN_HEIGHT - 130)))
        g = int(SKY_BLUE_LIGHT[1] + (SKY_BLUE_DARK[1] - SKY_BLUE_LIGHT[1]) * (y / (SCREEN_HEIGHT - 130)))
        b = int(SKY_BLUE_LIGHT[2] + (SKY_BLUE_DARK[2] - SKY_BLUE_LIGHT[2]) * (y / (SCREEN_HEIGHT - 130)))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
    # 2. Clouds
    pygame.draw.ellipse(surface, WHITE, (50, 40, 150, 80), 0)
    pygame.draw.ellipse(surface, WHITE, (120, 30, 100, 60), 0)
    pygame.draw.ellipse(surface, WHITE, (600, 80, 180, 90), 0)
    pygame.draw.ellipse(surface, WHITE, (680, 70, 120, 70), 0)

    # 3. Platforms
    
    # Player Platform (Bottom-Left)
    player_platform_rect = pygame.Rect(30, 380, 320, 80)
    pygame.draw.ellipse(surface, PLAYER_PLATFORM_COLOR_LIGHT, player_platform_rect)
    pygame.draw.ellipse(surface, PLAYER_PLATFORM_COLOR_DARK, (player_platform_rect.x, player_platform_rect.y + 15, player_platform_rect.width, player_platform_rect.height - 15))
    pygame.draw.ellipse(surface, BLACK, player_platform_rect, 4) 
    
    # Opponent Platform (Top-Right)
    opp_platform_rect = pygame.Rect(450, 180, 320, 60)
    pygame.draw.ellipse(surface, OPPONENT_PLATFORM_COLOR_LIGHT, opp_platform_rect)
    pygame.draw.ellipse(surface, OPPONENT_PLATFORM_COLOR_DARK, (opp_platform_rect.x, opp_platform_rect.y + 10, opp_platform_rect.width, opp_platform_rect.height - 10))
    pygame.draw.ellipse(surface, BLACK, opp_platform_rect, 3) 

    # 4. Pokémon Sprites (Corrected Positions)
    
    # RED'S SPRITE (Player - Back, Left Side)
    if red_current and red_current.name in SPRITE_CACHE:
        # Pass False for flip_horizontally, as back sprites generally face forward (towards opponent)
        sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name], flip_horizontally=False)
        surface.blit(sprite, (player_platform_rect.x + player_platform_rect.width // 2 - sprite.get_width() // 2, player_platform_rect.y - sprite.get_height() + 40))
    
    # BLUE'S SPRITE (Opponent - Front, Right Side)
    if blue_current and blue_current.name in SPRITE_CACHE:
        # Pass True for flip_horizontally for opponent's front sprites to face left
        sprite = load_sprite_from_url(blue_current.name, SPRITES[blue_current.name], flip_horizontally=True)
        surface.blit(sprite, (opp_platform_rect.x + opp_platform_rect.width // 2 - sprite.get_width() // 2, opp_platform_rect.y - sprite.get_height() + 20))

# --- 6. GAME CONTROL FLOW ---

def handle_faint(fainted_pokemon):
    global red_current, blue_current, battle_state, message_queue, red_sprite, blue_sprite
    
    is_red = fainted_pokemon.is_player_one
    
    if not is_red: # Blue's Pokémon fainted (opponent)
        fainted_name = blue_current.name
        blue_team[:] = [p for p in blue_team if p.name != fainted_name]
        try:
            blue_current = blue_team[0]
            # Load new sprite, flipped for opponent
            blue_sprite = load_sprite_from_url(blue_current.name, SPRITES[blue_current.name], flip_horizontally=True)
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Blue sends out {blue_current.name}!")
        except IndexError:
            message_queue.append("Blue is defeated! Red wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    else: # Red's Pokémon fainted (player)
        fainted_name = red_current.name
        red_team[:] = [p for p in red_team if p.name != fainted_name]
        try:
            red_current = red_team[0]
            # Load new sprite, not flipped for player's back sprite
            red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name], flip_horizontally=False)
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Red automatically sends out {red_current.name}!")
        except IndexError:
            message_queue.append("Red is defeated! Blue wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    return False

def execute_player_turn(action, data=None):
    global battle_state, message_queue, red_current, red_sprite, blue_current
    
    if action == "FIGHT":
        move_name = list(red_current.moves.keys())[data]
        messages = use_move(red_current, blue_current, move_name)
        message_queue.extend(messages)
    
    elif action == "ITEM":
        messages = use_item(red_current)
        message_queue.extend(messages)
        
    elif action == "SWITCH":
        next_pokemon = next((p for p in red_team if p != red_current and not p.is_fainted()), None)
        
        if next_pokemon:
            old_name = red_current.name
            red_team.remove(next_pokemon)
            red_team.insert(0, next_pokemon)
            red_current = next_pokemon
            # Load new sprite, not flipped for player
            red_sprite = load_sprite_from_url(red_current.name, SPRITES[red_current.name], flip_horizontally=False)
            message_queue.append(f"Red withdrew {old_name}!")
            message_queue.append(f"Red sent out {red_current.name}!")
        else:
            message_queue.append("Red has no other available Pokémon to switch to!")
            battle_state = BATTLE_STATE_CHOOSING_ACTION
            return 
    
    battle_state = BATTLE_STATE_DISPLAY_MESSAGE

def execute_ai_turn():
    global battle_state, message_queue, blue_current, red_current
    
    if red_current.is_fainted():
        if handle_faint(red_current):
            return 
    
    if blue_current and not blue_current.is_fainted():
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
            
            if battle_state == BATTLE_STATE_CHOOSING_ACTION:
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

    if blue_current: draw_info_box(screen, blue_current, False)
    if red_current: draw_info_box(screen, red_current, True)
    
    current_message = message_queue[0] if message_queue else f"What will {red_current.name} do?"
    
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