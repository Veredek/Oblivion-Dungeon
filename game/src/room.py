import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state, player, Entity, Skill
from src.functions import functions
from src.Boxes import boxes

# ====== Global Variables ======
attack_text_rect_center = (config.MAINBOX_POS[0] + (1/5)*config.MAINBOX_SIZE[0],
                            config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1])

# ========== Functions ==========

# ========== (room) ==========
class Room:
    def __init__(self):
        self.attack_text_rect = config.TITLE_FONT.render("Attack", True, 0).get_rect(center=attack_text_rect_center)

    def enemy_room(self):
        clock = pygame.time.Clock()
        enemy = Entity("slime")
        my_turn = True

        running = True
        while running:
            if game_state.ongame_state != "room": break
            # ----|1|---- Clear Surfaces ----|1|----
            screen.clear_surfaces

            # ----|1|---- Loop Variables ----|1|----
            mouse_pos = screen.mouse         

            # ----|1|---- Base Surface Blit ----|1|----
            enemy.blit()

            if my_turn:
                mouse_over = boxes.fight_box(mouse_pos)

            # ----|1|---- Display Blit ----|1|----
            if game_state.ongame_state == "room": screen.blit_surface(screen.base_surface)

            # ----|1|---- Event Handle ----|1|----
            for event in pygame.event.get():
                functions.basic_events(event)

                # ----|2|---- Mouse ----|2|----
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # ----|3|---- Left Click ----|3|----
                    if event.button == 1:
                        if mouse_over == "attack":
                            skill = Skill("attack")
                            skill.activate(player, enemy)
                            print(enemy.stats["HP"])
                    # ------ Escape ------

            # ----|1|---- Exit ----|1|----
            if game_state.ongame_state != "room": break

            # ----|1|---- Tick FPS ----|1|----
            clock.tick(60)

        return None