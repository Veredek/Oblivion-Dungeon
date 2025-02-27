import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions

from src.Boxes import boxes
from src.entities import player
from src.inventory import inventory
from src.room import Room
from assets.dialogues.script import Script

# ========== Local Variables ==========

# ========== Functions ==========

# ====== (new_game) ======
def new_game():
    clock = pygame.time.Clock()
    start_time = time.time()
    script = Script()
    room = Room()
    game_state.ongame_state = "text"

    running = True
    while running:
        # ~~~~~~~~~~ Clear Surfaces ~~~~~~~~~~
        screen.clear_surfaces()

        # ------ Definindo Variáveis ------
        mouse_pos = screen.mouse
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
                after_mouse_over = boxes.after_box(screen.base_surface)
                
        # ------ Text ------
        else:
            game_state.ongame_state = "text"
            boxes.draw_text(script)

        # ------ Window Blit ------
        if game_state.state == "NEW GAME" : screen.blit_surface(screen.base_surface)


        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            functions.basic_events(event)

            # Detecta Click Esquerdo do Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.ongame_state == "after":
                    if after_mouse_over == "inventory":
                        inventory.in_inventory = True
                    if after_mouse_over == "proceed":
                        game_state.ongame_state = "room"
            
            # ------ Keydown ------
            elif event.type == pygame.KEYDOWN:
                print("*Keydown*")
                if event.key == pygame.K_RETURN:
                    print("    RETURN\n")
                    boxes.skip_text = True
                elif event.key == pygame.K_x:
                    print("    X\n")
                    if boxes.waiting:
                        script.state += 1
                        boxes.waiting = False
                        boxes.skip_text = False
                        boxes.time = time.time()
                    elif game_state.ongame_state == "text":
                        boxes.skip_text = True
                else:
                    print("\n")

        # ----|1|---- Exit ----|1|----
        if game_state.state != "NEW GAME": break

        # ----|1|---- Tick FPS ----|1|----
        clock.tick(60)

    return None