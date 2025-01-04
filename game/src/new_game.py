import pygame
import time
from src.Boxes import Boxes
from assets.dialogues.script import Script
from src.entities import player__init__
from src.inventory import Inventory
from src.esc_menu import EscMenu
from src.definitions import basic_events

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_FONT = pygame.font.SysFont("comicsans", 30)
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)
TYPING_SPEED = 50  # Caracteres por segundo

# ====== Definitions =======

# ====== Código Principal ======
def new_game(game_state):
    clock = pygame.time.Clock()
    start_time = time.time()
    boxes = Boxes()
    script = Script()
    inventory = Inventory()
    esc_menu = EscMenu()
    player = player__init__(game_state.player_name)
    game_state.ongame_state = "text"

    running = True
    while running:
        BASE_SURFACE.fill(0)

        # ------ Definindo Variáveis ------
        screen = game_state.screen
        mouse_pos = screen.get_mouse()
        elapsed_time = (time.time() - start_time)

        # ------ Escalonando ------

        # ------ Verify Script ------
        script_line = script.script()

        # ====== PROCESSING ======
        # ------ Esc ------
        if esc_menu.inside:
            esc_menu.esc(BASE_SURFACE, mouse_pos)

        else:
            # ------ After ------
            if script_line == "AFTER":
                if inventory.in_inventory:
                    game_state.ongame_state = "inventory"
                    inventory.inventory(BASE_SURFACE, player, game_state)
                else:
                    game_state.ongame_state = "after"
                    after_mouse_over = boxes.after_box(BASE_SURFACE, mouse_pos)
                    
            # ------ Text ------
            else:
                game_state.ongame_state = "text"
                boxes.draw_text(BASE_SURFACE,script)

        # ------ Window Blit ------
        scaled_surface = pygame.transform.scale(BASE_SURFACE, (int(GAME_WIDTH * screen.scale), int(GAME_HEIGHT * screen.scale)))
        screen.window.blit(scaled_surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()

        clock.tick(60)

        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            basic_events(event, game_state)

            # Detecta Click Esquerdo do Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.ongame_state == "after":
                    if after_mouse_over == "inventory":
                        inventory.in_inventory = True
                    if after_mouse_over == "proceed":
                        game_state.ongame_state = "room"
            
            # ------ Keydown ------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Key: RETURN\n")
                    boxes.skip_text = True
                elif event.key == pygame.K_x:
                    print("Key: X\n")
                    if boxes.waiting:
                        script.state += 1
                        boxes.waiting = False
                        boxes.skip_text = False
                        boxes.time = time.time()
                    elif game_state.ongame_state == "text":
                        boxes.skip_text = True

        # ------ Check if in New Game Yet ------
        if game_state.state != "NEW GAME":
            running = False

    return None