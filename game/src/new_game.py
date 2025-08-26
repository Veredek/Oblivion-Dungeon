import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state, player, hud
from src.functions import basic_events

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
                after_mouse_over = hud.after_box(mouse_pos)

        # ------ Text ------
        else:
            game_state.ongame_state = "text"
            hud.draw_text(script)

        # ~~~~~~~~~~ Window Blit ~~~~~~~~~~
        if game_state.state == "NEW GAME" : screen.blit_surface(screen.base_surface)


        # region ----|1|---- Event Handle
        for event in pygame.event.get():
            basic_events(event)

            # region ----|2|---- MOUSEBUTTOMDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:

                # region ----|3|---- Left Click
                if event.button == 1:
                    if game_state.ongame_state == "after":
                        if after_mouse_over == "inventory":
                            inventory.in_inventory = True
                        if after_mouse_over == "proceed":
                            game_state.ongame_state = "room"
                    # endregion

                # endregion

            # ------ Keydown ------
            elif event.type == pygame.KEYDOWN:
                print("*Keydown*")
                if event.key == pygame.K_RETURN:
                    print("    RETURN\n")
                    hud.skip_text = True
                elif event.key == pygame.K_x:
                    print("    X\n")
                    if hud.waiting:
                        script.state += 1
                        hud.waiting = False
                        hud.skip_text = False
                        hud.time = time.time()
                    elif game_state.ongame_state == "text":
                        hud.skip_text = True
                else:
                    print("\n")
            # endregion

        # ----|1|---- Exit ----|1|----
        if game_state.state != "NEW GAME": break

        # ----|1|---- Tick FPS ----|1|----
        clock.tick(60)

    return None