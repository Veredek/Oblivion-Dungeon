import pygame
import time
from src.Boxes import Boxes
from assets.dialogues.script import Script
from src.inventory import Inventory
from src.room import Room
# ====== Global Objects ======
from src.classes import screen, game_state
from src.entities import player

# ====== Global Variables ======
from src.variables import GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE

# ====== Definitions =======
from src.definitions import basic_events, blit_surface

# ====== Código Principal ======
def new_game():
    clock = pygame.time.Clock()
    start_time = time.time()
    boxes = Boxes()
    script = Script()
    inventory = Inventory()
    room = Room()
    game_state.ongame_state = "text"

    running = True
    while running:
        if game_state.state != "NEW GAME": break
        BASE_SURFACE.fill(0)

        # ------ Definindo Variáveis ------
        mouse_pos = screen.get_mouse()
        elapsed_time = (time.time() - start_time)

        # ------ Verify Script ------
        script_line = script.script()

        # ====== PROCESSING ======
        # ------ Room ------
        if game_state.ongame_state == "room":
            room.enemy_room()

        # ------ After Room ------
        elif script_line == "AFTER":
            if inventory.in_inventory:
                game_state.ongame_state = "inventory"
                inventory.inventory(player)
            else:
                game_state.ongame_state = "after"
                after_mouse_over = boxes.after_box(BASE_SURFACE)
                
        # ------ Text ------
        else:
            game_state.ongame_state = "text"
            boxes.draw_text(BASE_SURFACE,script)

        # ------ Window Blit ------
        if game_state.state == "NEW GAME" : blit_surface(BASE_SURFACE)

        clock.tick(60)

        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            basic_events(event)

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

        # ------ Exit ------
        if game_state.state != "NEW GAME": break

    return None