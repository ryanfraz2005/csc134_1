import pygame
import sys
import random

# --- 1. CONFIGURATION AND INITIAL SETUP ---
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulation (Polished GFX)")

# --- COLORS AND STYLES (GBA/DS Aesthetic) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MENU_BLUE = (100, 100, 255) # Command box blue
MENU_GREY = (220, 220, 220) # Fight menu grey
SKY_BLUE = (135, 206, 235) # Light Sky
GRASS_GREEN = (0, 150, 0) # Platform 1 color
DIRT_BROWN = (150, 100, 50) # Platform 2 color

# HP Bar Colors
HP_MAX = (0, 200, 0)
HP_MID = (255, 215, 0)
HP_LOW = (200, 0, 0)
HP_BG = (170, 170, 170)

# Fonts
FONT_SIZE_TITLE = 32
FONT_SIZE_MAIN = 24
FONT_SIZE_SMALL = 18
font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
font_main = pygame.font.Font(None, FONT_SIZE_MAIN)
font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 30

# State Management (Unchanged logic)
BATTLE_STATE_CHOOSING_ACTION = 0
BATTLE_STATE_CHOOSING_MOVE = 1
BATTLE_STATE_AWAITING_AI = 2
BATTLE_STATE_DISPLAY_MESSAGE = 3
BATTLE_STATE_END = 4

battle_state = BATTLE_STATE_CHOOSING_ACTION
message_queue = []
message_display_timer = 0
MESSAGE_DURATION = 90 # 3 seconds at 30 FPS

# Player inventory and selection
red_potions_left = 3
red_action_options = ["FIGHT", "ITEM", "SWITCH"]
red_move_selection = 0
red_action_selection = 0
LEVEL = 50 

# --- 2. GAME DATA: TYPE CHART AND MOVES (Unchanged) ---

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
        if other_t not in TYPE_CHART[t]:
            TYPE_CHART[t][other_t] = 1.0


# --- 3. POKEMON AND DAMAGE LOGIC (Unchanged) ---

class Pokemon:
    # (Simplified class structure remains the same)
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

def calculate_damage(attacker, defender, move):
    # (Damage calculation logic remains the same)
    power = move['power']
    move_type = move['type']
    base = int((((2 * LEVEL / 5 + 2) * power * attacker.attack / defender.defense) / 50) + 2)
    crit_multiplier = 1.5 if random.random() < 1/16 else 1.0
    random_mult = random.randint(85, 100) / 100.0
    stab_multiplier = 1.5 if attacker.type == move_type else 1.0
    type_mult = TYPE_CHART.get(move_type, {}).get(defender.type, 1.0)
    
    damage = int(base * crit_multiplier * random_mult * stab_multiplier * type_mult)
    if damage < 1:
        damage = 1
    return damage, crit_multiplier, type_mult

def use_move(attacker, defender, move_name):
    # (Move execution and message generation logic remains the same)
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
    # (Item usage logic remains the same)
    global red_potions_left
    heal_amount = 60 
    
    current_hp = pokemon.current_hp
    max_hp = pokemon.max_hp
    
    if red_potions_left <= 0:
        return ["No Potions left!"]
        
    if current_hp == max_hp:
        return [f"{pokemon.name} is already at full health!"]

    red_potions_left -= 1
    
    amount_healed = min(max_hp - current_hp, heal_amount)
    pokemon.current_hp += amount_healed
    
    messages = [
        f"Red used a Potion on {pokemon.name}!",
        f"{pokemon.name} recovered {amount_healed} HP."
    ]
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

# --- 5. GFX AND DRAWING FUNCTIONS ---

def draw_text(surface, text, font, color, x, y, center=False):
    """Utility to draw text."""
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))

def draw_hp_bar(surface, pokemon, x, y, width=200, height=8):
    """Draws the HP bar within the info box with color changes."""
    hp_ratio = pokemon.current_hp / pokemon.max_hp if pokemon.max_hp > 0 else 0
    current_width = int(width * hp_ratio)

    if hp_ratio > 0.5:
        color = HP_MAX
    elif hp_ratio > 0.2:
        color = HP_MID
    else:
        color = HP_LOW

    # Draw the black outline
    pygame.draw.rect(surface, BLACK, (x - 2, y - 2, width + 4, height + 4))
    # Draw the background grey
    pygame.draw.rect(surface, HP_BG, (x, y, width, height))
    # Draw the colored fill
    pygame.draw.rect(surface, color, (x, y, current_width, height))

def draw_info_box(surface, pokemon, is_player_one):
    """Draws the detailed name/HP box with 3D effect."""
    
    if is_player_one: # Red's Box (Bottom Left)
        box_rect = pygame.Rect(50, 350, 300, 100)
    else: # Blue's Box (Top Right)
        box_rect = pygame.Rect(450, 50, 300, 100)

    # 3D Top-Left Light Edge
    pygame.draw.line(surface, WHITE, (box_rect.x, box_rect.y + 1), (box_rect.x + box_rect.width, box_rect.y + 1), 3)
    pygame.draw.line(surface, WHITE, (box_rect.x + 1, box_rect.y), (box_rect.x + 1, box_rect.y + box_rect.height), 3)

    # Main Box BG
    pygame.draw.rect(surface, MENU_GREY, box_rect, 0, 8)
    # Box Outline (3D effect)
    pygame.draw.rect(surface, BLACK, box_rect, 3, 8)
    
    # Name, Level, and HP bar details
    draw_text(surface, pokemon.name, font_main, BLACK, box_rect.x + 10, box_rect.y + 10)
    draw_text(surface, f"Lv.{LEVEL}", font_main, BLACK, box_rect.x + 230, box_rect.y + 10)

    draw_text(surface, "HP:", font_small, BLACK, box_rect.x + 10, box_rect.y + 40)

    hp_bar_x = box_rect.x + 50
    hp_bar_y = box_rect.y + 42
    hp_bar_width = 230
    draw_hp_bar(surface, pokemon, hp_bar_x, hp_bar_y, hp_bar_width, height=12)
    
    if is_player_one:
        hp_text = f"{pokemon.current_hp}/{pokemon.max_hp}"
        draw_text(surface, hp_text, font_small, BLACK, box_rect.x + 180, box_rect.y + 68)

def draw_message_box(surface, message):
    """Draws the main message box with a professional border."""
    msg_box_rect = pygame.Rect(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120)
    
    # Bottom area background
    pygame.draw.rect(surface, MENU_BLUE, msg_box_rect)
    
    # Text Area Box - This is where the message appears
    text_area_rect = pygame.Rect(10, SCREEN_HEIGHT - 110, SCREEN_WIDTH - 20, 50)
    pygame.draw.rect(surface, WHITE, text_area_rect, 0, 5)
    
    # GBA style border
    pygame.draw.rect(surface, BLACK, text_area_rect, 3, 5) 
    
    draw_text(surface, message, font_main, BLACK, text_area_rect.x + 15, text_area_rect.centery, center=False)

def draw_command_menu(surface):
    """Draws the action menu (FIGHT, ITEM, SWITCH) with button style."""
    global red_action_options, red_action_selection
    
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 65
    menu_width, menu_height = SCREEN_WIDTH // 2, 65
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

    # Draw Button Panel Background
    pygame.draw.rect(surface, (180, 180, 180), menu_rect)
    pygame.draw.rect(surface, BLACK, menu_rect, 2)
    
    for i, option in enumerate(red_action_options):
        # Coordinates for 2x2 layout
        row = i // 2
        col = i % 2
        
        button_x = menu_x + 5 + col * (menu_width // 2)
        button_y = menu_y + 5 + row * (menu_height // 2 - 5)
        button_width = menu_width // 2 - 10
        button_height = menu_height // 2 - 10
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        is_selected = (i == red_action_selection)
        
        # Button Fill and 3D Effect
        fill_color = (200, 200, 255) if is_selected else MENU_GREY
        shadow_color = BLACK if is_selected else (100, 100, 100)
        
        pygame.draw.rect(surface, shadow_color, (button_x + 2, button_y + 2, button_width, button_height), 0, 5) # Shadow
        pygame.draw.rect(surface, fill_color, button_rect, 0, 5) # Main button
        pygame.draw.rect(surface, BLACK, button_rect, 1, 5) # Border
        
        text_color = BLACK
        draw_text(surface, option, font_main, text_color, button_rect.centerx, button_rect.centery, center=True)

def draw_fight_menu(surface):
    """Draws the move selection menu with button style."""
    global red_move_selection
    
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 65
    menu_width, menu_height = SCREEN_WIDTH // 2, 65
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

    pygame.draw.rect(surface, (180, 180, 180), menu_rect)
    pygame.draw.rect(surface, BLACK, menu_rect, 2)
    
    moves = list(red_current.moves.keys())
    
    for i, move_name in enumerate(moves):
        # Coordinates for 2x2 layout
        row = i // 2
        col = i % 2
        
        button_x = menu_x + 5 + col * (menu_width // 2)
        button_y = menu_y + 5 + row * (menu_height // 2 - 5)
        button_width = menu_width // 2 - 10
        button_height = menu_height // 2 - 10
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        is_selected = (i == red_move_selection)
        
        # Button Fill and 3D Effect
        fill_color = (255, 255, 200) if is_selected else MENU_GREY
        shadow_color = BLACK if is_selected else (100, 100, 100)
        
        pygame.draw.rect(surface, shadow_color, (button_x + 2, button_y + 2, button_width, button_height), 0, 5)
        pygame.draw.rect(surface, fill_color, button_rect, 0, 5)
        pygame.draw.rect(surface, BLACK, button_rect, 1, 5)
        
        draw_text(surface, move_name, font_main, BLACK, button_rect.centerx, button_rect.centery, center=True)


def draw_arena(surface):
    """Draws the background arena and platforms with gradients."""
    
    # 1. Main Sky/Background (Simple Gradient)
    for y in range(0, SCREEN_HEIGHT - 120):
        # Fade from light blue (top) to slightly darker blue (bottom)
        r = int(135 + (200 - 135) * (y / (SCREEN_HEIGHT - 120)))
        g = int(206 + (200 - 206) * (y / (SCREEN_HEIGHT - 120)))
        b = int(235 + (180 - 235) * (y / (SCREEN_HEIGHT - 120)))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
    # 2. Opponent Platform (Grass-like, Top Left)
    opp_platform_rect = pygame.Rect(70, 200, 300, 50)
    pygame.draw.ellipse(surface, GRASS_GREEN, opp_platform_rect)
    pygame.draw.ellipse(surface, (0, 100, 0), opp_platform_rect, 4) # Dark border
    
    # 3. Player Platform (Dirt/Rock-like, Bottom Right)
    player_platform_rect = pygame.Rect(430, 400, 350, 50)
    pygame.draw.ellipse(surface, DIRT_BROWN, player_platform_rect)
    pygame.draw.ellipse(surface, (100, 60, 20), player_platform_rect, 4) # Dark border

    # 4. Pokémon Sprite Display Areas (Where your PNGs would go)
    
    # BLUE'S SPRITE (Opponent - Top-Left)
    blue_sprite_x, blue_sprite_y = 120, 100
    sprite_size = 150
    # Placeholder for loaded image
    pygame.draw.rect(surface, BLACK, (blue_sprite_x - 5, blue_sprite_y - 5, sprite_size + 10, sprite_size + 10), 0, 15) # Shadow/Outline
    pygame.draw.rect(surface, (255, 200, 200), (blue_sprite_x, blue_sprite_y, sprite_size, sprite_size), 0, 15) # Main Area
    draw_text(surface, blue_current.name, font_main, BLACK, blue_sprite_x + 75, blue_sprite_y + 75, center=True)
    draw_text(surface, "PLACEHOLDER", font_small, BLACK, blue_sprite_x + 75, blue_sprite_y + 105, center=True)
    # Visual placeholder for Charizard 

    # RED'S SPRITE (Player - Bottom-Right)
    red_sprite_x, red_sprite_y = 500, 230
    sprite_size = 180
    # Placeholder for loaded image (larger since it's the back sprite)
    pygame.draw.rect(surface, BLACK, (red_sprite_x - 5, red_sprite_y - 5, sprite_size + 10, sprite_size + 10), 0, 15)
    pygame.draw.rect(surface, (200, 200, 255), (red_sprite_x, red_sprite_y, sprite_size, sprite_size), 0, 15)
    draw_text(surface, red_current.name, font_main, BLACK, red_sprite_x + 90, red_sprite_y + 90, center=True)
    draw_text(surface, "PLACEHOLDER (BACK VIEW)", font_small, BLACK, red_sprite_x + 90, red_sprite_y + 120, center=True)
    # Visual placeholder for Tyranitar 

# --- IMAGE LOADING COMMENTARY ---
# To load actual images, uncomment and use the following function:
"""
def load_pokemon_images():
    try:
        # Load your opponent sprite (e.g., Charizard.png)
        global OPPONENT_SPRITE 
        OPPONENT_SPRITE = pygame.image.load('assets/charizard.png').convert_alpha()
        OPPONENT_SPRITE = pygame.transform.scale(OPPONENT_SPRITE, (150, 150))
        
        # Load your player back sprite (e.g., Tyranitar_back.png)
        global PLAYER_SPRITE
        PLAYER_SPRITE = pygame.image.load('assets/tyranitar_back.png').convert_alpha()
        PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE, (180, 180))
        
        # You would then replace the 'draw_rect' placeholders in draw_arena 
        # with 'surface.blit(PLAYER_SPRITE, (red_sprite_x, red_sprite_y))'
        
    except pygame.error as e:
        print(f"Error loading images. Ensure you have 'assets/charizard.png' and 'assets/tyranitar_back.png' in place. Error: {e}")

# Call load_pokemon_images() at the start of the main loop.
"""
# --- END IMAGE LOADING COMMENTARY ---

def draw_inventory_and_status(surface):
    """Draws Red's inventory status."""
    inventory_x, inventory_y = 50, 460
    
    box_rect = pygame.Rect(inventory_x, inventory_y, 150, 25)
    pygame.draw.rect(surface, (150, 200, 250), box_rect, 0, 5)
    pygame.draw.rect(surface, BLACK, box_rect, 2, 5)
    
    draw_text(surface, f"Potions: {red_potions_left}", font_small, BLACK, box_rect.centerx, box_rect.centery, center=True)


# --- 6. GAME CONTROL FLOW (Unchanged logic) ---

def handle_faint(fainted_pokemon):
    # (Faint and switch logic remains the same)
    global red_current, blue_current, battle_state, message_queue
    
    if fainted_pokemon == blue_current:
        fainted_name = blue_current.name
        # Remove fainted from list
        blue_team[:] = [p for p in blue_team if p.name != fainted_name]
        
        try:
            blue_current = blue_team[0]
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Blue sends out {blue_current.name}!")
        except IndexError:
            message_queue.append("Blue is defeated! Red wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    elif fainted_pokemon == red_current:
        fainted_name = red_current.name
        # Remove fainted from list
        red_team[:] = [p for p in red_team if p.name != fainted_name]
                
        try:
            red_current = red_team[0]
            message_queue.append(f"{fainted_name} fainted!")
            message_queue.append(f"Red automatically sends out {red_current.name}!")
        except IndexError:
            message_queue.append("Red is defeated! Blue wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    return False

def execute_player_turn(action, data=None):
    # (Turn execution logic remains the same)
    global battle_state, message_queue, red_current
    
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
            
            # Move the new Pokémon to the front of the battle list
            red_team.remove(next_pokemon)
            red_team.insert(0, next_pokemon)
            red_current = next_pokemon
            
            message_queue.append(f"Red withdrew {old_name}!")
            message_queue.append(f"Red sent out {red_current.name}!")
        else:
            message_queue.append("Red has no other available Pokémon to switch to!")
            battle_state = BATTLE_STATE_CHOOSING_ACTION
            return 
    
    battle_state = BATTLE_STATE_DISPLAY_MESSAGE

def execute_ai_turn():
    # (AI execution logic remains the same)
    global battle_state, message_queue, blue_current, red_current
    
    if red_current.is_fainted():
        if handle_faint(red_current):
            return 
    
    if blue_current and not blue_current.is_fainted():
        # AI always chooses the first move
        move_name = list(blue_current.moves.keys())[0]
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
        draw_inventory_and_status(screen)
    elif battle_state == BATTLE_STATE_CHOOSING_MOVE:
        draw_message_box(screen, "Choose a move.")
        draw_fight_menu(screen)
        draw_inventory_and_status(screen)
    elif battle_state == BATTLE_STATE_DISPLAY_MESSAGE or battle_state == BATTLE_STATE_AWAITING_AI:
        draw_message_box(screen, current_message)
    elif battle_state == BATTLE_STATE_END:
        draw_message_box(screen, current_message)
        draw_text(screen, "BATTLE ENDED (Press ESC to Exit)", font_main, BLACK, SCREEN_WIDTH // 2, 20, center=True)

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()