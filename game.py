import pygame
import sys
import random

# --- 1. CONFIGURATION AND INITIAL SETUP ---
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulation (Polished)")

# --- COLORS AND STYLES (GBA/DS Aesthetic) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 215, 0)
RED = (200, 0, 0)
HP_BG = (170, 170, 170)
MENU_BLUE = (100, 100, 255) # Command box blue
MENU_GREY = (220, 220, 220) # Fight menu grey
PLATFORM_GREEN = (0, 150, 0) # Platform color

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
LEVEL = 50 # Common level for all Pokémon

# --- 2. GAME DATA: TYPE CHART AND MOVES (Simplified but complete) ---

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
# Fill in missing relationships with 1.0 (neutral)
for t in list(TYPE_CHART.keys()):
    for other_t in list(TYPE_CHART.keys()):
        if other_t not in TYPE_CHART[t]:
            TYPE_CHART[t][other_t] = 1.0


# --- 3. POKEMON AND DAMAGE LOGIC (Unchanged) ---

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

def calculate_damage(attacker, defender, move):
    """Calculates damage based on simplified Gen 2 formula, including multipliers."""
    power = move['power']
    move_type = move['type']
    
    # 1. Base Damage (Assuming level 50)
    base = int((((2 * LEVEL / 5 + 2) * power * attacker.attack / defender.defense) / 50) + 2)

    # 2. Critical Hit (1/16 chance)
    crit_chance = 1/16
    crit_multiplier = 1.5 if random.random() < crit_chance else 1.0
    
    # 3. Random Multiplier (0.85 to 1.0)
    random_mult = random.randint(85, 100) / 100.0

    # 4. STAB (Same Type Attack Bonus)
    stab_multiplier = 1.5 if attacker.type == move_type else 1.0

    # 5. Type Effectiveness
    type_mult = TYPE_CHART.get(move_type, {}).get(defender.type, 1.0)
    
    # Total Damage Calculation
    damage = int(base * crit_multiplier * random_mult * stab_multiplier * type_mult)
    if damage < 1:
        damage = 1

    return damage, crit_multiplier, type_mult

def use_move(attacker, defender, move_name):
    """Handles the move usage, damage application, and message generation."""
    move = attacker.moves.get(move_name)
    if not move:
        return [f"{attacker.name} failed to use {move_name}!"]

    damage, crit_mult, type_mult = calculate_damage(attacker, defender, move)
    defender.take_damage(damage)

    # Message sequence
    messages = [f"{attacker.name} used {move_name}!"]
    
    if crit_mult > 1.0:
        messages.append("A critical hit!")
    
    if type_mult >= 2.0:
        messages.append("It's Super Effective!")
    elif type_mult == 0.0:
        messages.append(f"It had no effect on {defender.name}!")
    elif type_mult < 1.0:
        messages.append("It's not very effective...")
        
    messages.append(f"{defender.name} took {damage} damage.")
    
    return messages

def use_item(pokemon):
    """Heals a Pokemon with a Potion."""
    global red_potions_left
    heal_amount = 60 
    
    current_hp = pokemon.current_hp
    max_hp = pokemon.max_hp
    
    if red_potions_left <= 0:
        return ["No Potions left!"]
        
    if current_hp == max_hp:
        return [f"{pokemon.name} is already at full health!"]

    red_potions_left -= 1
    
    new_hp = min(max_hp, current_hp + heal_amount)
    amount_healed = new_hp - current_hp
    pokemon.current_hp = new_hp
    
    messages = [
        f"Red used a Potion on {pokemon.name}!",
        f"{pokemon.name} recovered {amount_healed} HP."
    ]
    return messages

# --- 4. TEAM SETUP ---

# Red's Team (Gold/Silver Gen 2 Focus)
red_team_data = [
    # (Name, Type, Max HP, Attack, Defense, Moves, is_player_one)
    Pokemon("Tyranitar", "DARK", 120, 150, 110, {"Rock Slide": {"type": "ROCK", "power": 75}, "Crunch": {"type": "DARK", "power": 80}}, True),
    Pokemon("Scizor", "STEEL", 100, 130, 100, {"Iron Head": {"type": "STEEL", "power": 80}, "Slash": {"type": "NORMAL", "power": 70}}, True),
    Pokemon("Espeon", "PSYCHIC", 95, 120, 70, {"Psychic": {"type": "PSYCHIC", "power": 90}, "Swift": {"type": "NORMAL", "power": 60}}, True)
]
red_team = red_team_data[:] # Create a copy for battle

# Blue's Team (Red/Blue Gen 1 Focus)
blue_team_data = [
    # (Name, Type, Max HP, Attack, Defense, Moves, is_player_one)
    Pokemon("Charizard", "FIRE", 110, 120, 90, {"Flamethrower": {"type": "FIRE", "power": 95}, "Slash": {"type": "NORMAL", "power": 70}}, False),
    Pokemon("Blastoise", "WATER", 115, 110, 120, {"Surf": {"type": "WATER", "power": 90}, "Bite": {"type": "NORMAL", "power": 60}}, False),
    Pokemon("Venusaur", "GRASS", 110, 100, 115, {"Razor Leaf": {"type": "GRASS", "power": 55}, "Body Slam": {"type": "NORMAL", "power": 85}}, False)
]
blue_team = blue_team_data[:]

# Initial Battle State
red_current = red_team[0]
blue_current = blue_team[0]
turn = "RED"
message_queue.append(f"Battle Start! Blue sent out {blue_current.name}!")
message_queue.append(f"Red sent out {red_current.name}!")

# --- 5. ENHANCED DRAWING FUNCTIONS ---

def draw_text(surface, text, font, color, x, y, center=False):
    """Utility to draw text."""
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))

def draw_hp_bar(surface, pokemon, x, y, width=150, height=8):
    """Draws the HP bar within the info box."""
    hp_ratio = pokemon.current_hp / pokemon.max_hp if pokemon.max_hp > 0 else 0
    current_width = int(width * hp_ratio)

    if hp_ratio > 0.5:
        color = GREEN
    elif hp_ratio > 0.2:
        color = YELLOW
    else:
        color = RED

    # HP Bar background (black outline is enough)
    pygame.draw.rect(surface, HP_BG, (x, y, width, height))
    # HP Bar fill
    pygame.draw.rect(surface, color, (x, y, current_width, height))

def draw_info_box(surface, pokemon, is_player_one):
    """Draws the detailed name/HP box."""
    if is_player_one: # Red's Box (Bottom Left)
        box_rect = pygame.Rect(50, 350, 300, 100)
    else: # Blue's Box (Top Right)
        box_rect = pygame.Rect(450, 50, 300, 100)

    # Main Box BG
    pygame.draw.rect(surface, MENU_GREY, box_rect, 0, 10)
    # Box Outline (3D effect)
    pygame.draw.rect(surface, BLACK, box_rect, 2, 10)

    # Name and Level
    draw_text(surface, pokemon.name, font_main, BLACK, box_rect.x + 10, box_rect.y + 10)
    draw_text(surface, f"Lv.{LEVEL}", font_main, BLACK, box_rect.x + 230, box_rect.y + 10)

    # HP Bar Label ("HP")
    draw_text(surface, "HP", font_small, BLACK, box_rect.x + 10, box_rect.y + 40)

    # HP Bar and Text
    hp_bar_x = box_rect.x + 50
    hp_bar_y = box_rect.y + 42
    hp_bar_width = 200
    draw_hp_bar(surface, pokemon, hp_bar_x, hp_bar_y, hp_bar_width)
    
    # HP numbers (only for player's Pokemon, classic look)
    if is_player_one:
        hp_text = f"{pokemon.current_hp}/{pokemon.max_hp}"
        draw_text(surface, hp_text, font_small, BLACK, box_rect.x + 190, box_rect.y + 65)

def draw_message_box(surface, message):
    """Draws the main message box that takes up the bottom width."""
    msg_box_rect = pygame.Rect(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120)
    
    # Main box (Blue background for command/message area)
    pygame.draw.rect(surface, MENU_BLUE, msg_box_rect)
    pygame.draw.rect(surface, BLACK, msg_box_rect, 3) # Black Border

    # Text Area
    text_area_rect = pygame.Rect(10, SCREEN_HEIGHT - 110, SCREEN_WIDTH - 20, 50)
    pygame.draw.rect(surface, WHITE, text_area_rect)
    pygame.draw.rect(surface, BLACK, text_area_rect, 2)
    
    draw_text(surface, message, font_main, BLACK, text_area_rect.x + 10, text_area_rect.centery, center=False)

def draw_command_menu(surface):
    """Draws the action menu (FIGHT, ITEM, SWITCH) next to the message box."""
    global red_action_options, red_action_selection
    
    # Menu is drawn on the right half of the message box area
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 65
    menu_width, menu_height = SCREEN_WIDTH // 2, 65
    
    # Draw Menu Box
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    pygame.draw.rect(surface, MENU_GREY, menu_rect)
    pygame.draw.rect(surface, BLACK, menu_rect, 2)
    
    for i, option in enumerate(red_action_options):
        text_x = menu_x + 30 + (i % 2) * 200
        text_y = menu_y + 10 + (i // 2) * 30
        
        color = RED if i == red_action_selection else BLACK
        # Draw selection triangle
        if i == red_action_selection:
            triangle_points = [
                (text_x - 15, text_y + 8),
                (text_x - 5, text_y + 4),
                (text_x - 5, text_y + 12),
            ]
            pygame.draw.polygon(surface, color, triangle_points)
            
        draw_text(surface, option, font_main, color, text_x, text_y)

def draw_fight_menu(surface):
    """Draws the move selection menu."""
    global red_move_selection
    
    menu_x, menu_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 65
    menu_width, menu_height = SCREEN_WIDTH // 2, 65
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)

    # Draw Menu Box
    pygame.draw.rect(surface, MENU_GREY, menu_rect)
    pygame.draw.rect(surface, BLACK, menu_rect, 2)
    
    moves = list(red_current.moves.keys())
    
    for i, move_name in enumerate(moves):
        # Coordinates based on 2x2 grid
        text_x = menu_x + 30 + (i % 2) * 200
        text_y = menu_y + 10 + (i // 2) * 30
        
        color = RED if i == red_move_selection else BLACK
        
        # Draw selection triangle
        if i == red_move_selection:
            triangle_points = [
                (text_x - 15, text_y + 8),
                (text_x - 5, text_y + 4),
                (text_x - 5, text_y + 12),
            ]
            pygame.draw.polygon(surface, color, triangle_points)
            
        draw_text(surface, move_name, font_main, color, text_x, text_y)

def draw_arena(surface):
    """Draws the background arena and platforms."""
    # Main Sky/Background
    surface.fill((100, 150, 255)) # Light Blue Sky

    # Opponent Platform (Grass)
    opp_platform_rect = pygame.Rect(70, 200, 300, 50)
    pygame.draw.ellipse(surface, PLATFORM_GREEN, opp_platform_rect)
    pygame.draw.ellipse(surface, (0, 100, 0), opp_platform_rect, 5) # Dark border

    # Player Platform (Rock/Dirt)
    player_platform_rect = pygame.Rect(430, 400, 350, 50)
    pygame.draw.ellipse(surface, (150, 100, 50), player_platform_rect)
    pygame.draw.ellipse(surface, (100, 60, 20), player_platform_rect, 5) # Dark border

    # Pokémon Placeholders (Simulating Sprites)
    # Blue's Pokémon (Top-Left)
    blue_sprite_x, blue_sprite_y = 120, 120
    pygame.draw.rect(surface, MENU_GREY, (blue_sprite_x, blue_sprite_y, 100, 100), 0, 10)
    pygame.draw.rect(surface, BLACK, (blue_sprite_x, blue_sprite_y, 100, 100), 2, 10)
    draw_text(surface, blue_current.name, font_small, BLACK, blue_sprite_x + 50, blue_sprite_y + 50, center=True)
    

    # Red's Pokémon (Bottom-Right)
    red_sprite_x, red_sprite_y = 580, 280
    pygame.draw.rect(surface, MENU_GREY, (red_sprite_x, red_sprite_y, 100, 100), 0, 10)
    pygame.draw.rect(surface, BLACK, (red_sprite_x, red_sprite_y, 100, 100), 2, 10)
    draw_text(surface, red_current.name, font_small, BLACK, red_sprite_x + 50, red_sprite_y + 50, center=True)
    


def draw_inventory_and_status(surface):
    """Draws Red's inventory status next to the player's info box."""
    inventory_x, inventory_y = 50, 460
    
    # Draw simple button/box for Potion count
    box_rect = pygame.Rect(inventory_x, inventory_y, 150, 25)
    pygame.draw.rect(surface, (150, 200, 250), box_rect, 0, 5)
    pygame.draw.rect(surface, BLACK, box_rect, 1, 5)
    
    draw_text(surface, f"Potions: {red_potions_left}", font_small, BLACK, box_rect.centerx, box_rect.centery, center=True)


# --- 6. GAME CONTROL FLOW (Unchanged logic) ---

def handle_faint(fainted_pokemon):
    """Checks for fainting and handles switches or game end."""
    global red_current, blue_current, battle_state, message_queue
    
    if fainted_pokemon == blue_current:
        # Find the index of the fainted Pokémon in the original list to remove it
        for i, p in enumerate(blue_team):
            if p.name == blue_current.name:
                blue_team.pop(i)
                break
        
        try:
            blue_current = blue_team[0]
            message_queue.append(f"Blue sends out {blue_current.name}!")
        except IndexError:
            message_queue.append("Blue is defeated! Red wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    elif fainted_pokemon == red_current:
        message_queue.append(f"{red_current.name} fainted!")
        # Find and remove the fainted Pokémon from the red team list
        for i, p in enumerate(red_team):
            if p.name == red_current.name:
                red_team.pop(i)
                break
                
        try:
            red_current = red_team[0]
            message_queue.append(f"Red automatically sends out {red_current.name}!")
        except IndexError:
            message_queue.append("Red is defeated! Blue wins the simulation!")
            battle_state = BATTLE_STATE_END
            return True
            
    return False

def execute_player_turn(action, data=None):
    """Executes Red's chosen action and sets up Blue's counter-turn."""
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
            
            # Simple list manipulation to move the current to the back and the new to the front
            red_team.remove(next_pokemon)
            red_team.insert(0, next_pokemon)
            red_current = next_pokemon
            
            message_queue.append(f"Red withdrew {old_name}!")
            message_queue.append(f"Red sent out {red_current.name}!")
        else:
            message_queue.append("Red has no other available Pokémon to switch to!")
            # If switch failed, force re-selection of action
            battle_state = BATTLE_STATE_CHOOSING_ACTION
            return # Skip AI turn
    
    battle_state = BATTLE_STATE_DISPLAY_MESSAGE

def execute_ai_turn():
    """Executes Blue's turn (simple AI: always attacks with the first move)."""
    global battle_state, message_queue, blue_current, red_current
    
    # Check if Red fainted from the previous move (if any)
    if red_current.is_fainted():
        if handle_faint(red_current):
            return 
    
    # Blue attacks Red
    if blue_current and not blue_current.is_fainted():
        # Blue always chooses the first move for simplicity
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
            
            # Input handling depends on the current state
            if battle_state == BATTLE_STATE_CHOOSING_ACTION:
                if event.key == pygame.K_UP:
                    red_action_selection = max(0, red_action_selection - 2)
                elif event.key == pygame.K_DOWN:
                    red_action_selection = min(len(red_action_options) - 1, red_action_selection + 2)
                elif event.key == pygame.K_LEFT:
                    red_action_selection = max(0, red_action_selection - 1)
                elif event.key == pygame.K_RIGHT:
                    red_action_selection = min(len(red_action_options) - 1, red_action_selection + 1)
                elif event.key == pygame.K_RETURN:
                    chosen_action = red_action_options[red_action_selection]
                    
                    if chosen_action == "FIGHT":
                        battle_state = BATTLE_STATE_CHOOSING_MOVE
                        red_move_selection = 0 
                    elif chosen_action == "ITEM":
                        execute_player_turn("ITEM")
                        turn = "BLUE"
                    elif chosen_action == "SWITCH":
                        execute_player_turn("SWITCH")
                        turn = "BLUE"
                        
            elif battle_state == BATTLE_STATE_CHOOSING_MOVE:
                moves = list(red_current.moves.keys())
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    red_move_selection = max(0, red_move_selection - 1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    red_move_selection = min(len(moves) - 1, red_move_selection + 1)
                elif event.key == pygame.K_BACKSPACE:
                    battle_state = BATTLE_STATE_CHOOSING_ACTION # Go back to main menu
                elif event.key == pygame.K_RETURN:
                    execute_player_turn("FIGHT", red_move_selection)
                    turn = "BLUE"
                    
            elif battle_state == BATTLE_STATE_DISPLAY_MESSAGE:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Only advance if the current message timer has run out OR it's the very first message
                    if message_display_timer >= MESSAGE_DURATION or message_display_timer == 0:
                        message_queue.pop(0)
                        message_display_timer = 0
                
    # Update Logic
    if battle_state == BATTLE_STATE_DISPLAY_MESSAGE:
        # Auto-advance message after timer if no key is pressed
        if message_display_timer < MESSAGE_DURATION and message_queue:
            message_display_timer += 1
        
        # When messages are cleared, proceed to the next phase
        if not message_queue:
            if battle_state != BATTLE_STATE_END:
                # Check for faints again to ensure correct turn flow after a move
                if handle_faint(red_current) or handle_faint(blue_current):
                    # If fainting occurred, handle_faint will set the next state
                    pass
                elif turn == "RED":
                    battle_state = BATTLE_STATE_CHOOSING_ACTION
                elif turn == "BLUE":
                    battle_state = BATTLE_STATE_AWAITING_AI
    
    elif battle_state == BATTLE_STATE_AWAITING_AI:
        # Execute Blue's turn immediately
        execute_ai_turn()
        turn = "RED" # Switch back to Red after Blue's action
    
    # --- Drawing ---
    
    # 1. Draw Arena and Sprites
    draw_arena(screen)

    # 2. Draw Info Boxes
    if blue_current:
        draw_info_box(screen, blue_current, False)
    if red_current:
        draw_info_box(screen, red_current, True)
    
    # 3. Draw Menus / Message Box
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
        # Display the current message from the queue
        draw_message_box(screen, current_message)
    elif battle_state == BATTLE_STATE_END:
        # Display final message
        draw_message_box(screen, current_message)
        
    # Draw turn indicator if not displaying a message
    if battle_state in (BATTLE_STATE_CHOOSING_ACTION, BATTLE_STATE_CHOOSING_MOVE, BATTLE_STATE_AWAITING_AI):
         draw_text(screen, "Red's Turn" if turn == "RED" else "Blue's Turn", font_small, BLACK, SCREEN_WIDTH // 2, 20, center=True)

    pygame.display.flip()
    
    # Cap frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()