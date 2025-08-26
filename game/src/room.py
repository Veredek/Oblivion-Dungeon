import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state, hud, player, Entity, Skill
from src.functions import basic_events

# ====== Global Variables ======
attack_text_rect_center = (config.MAINBOX_POS[0] + (1/5)*config.MAINBOX_SIZE[0],
                            config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1])

# ========== Functions ==========

# ========== (room) ==========
class Room:
    def __init__(self):
        self.attack_text_rect = config.TITLE_FONT.render("Attack", True, 0).get_rect(center=attack_text_rect_center)
        self.dmg_timer = False

    def enemy_room(self):
        clock = pygame.time.Clock()
        enemy = Entity("slime")
        my_turn = True

        running = True
        while running:
            if game_state.ongame_state != "room": break
            # ----|1|---- Clear Surfaces ----|1|----
            screen.clear_surface(screen.base_surface)

            # ----|1|---- Loop Variables ----|1|----
            mouse_pos = screen.mouse

            # region ----|2|---- Damage fade
            if self.dmg_timer:
                fade_time = 1.5
                if self.dmg_timer:  elapsed_time = time.time() - self.dmg_timer
                else:               elapsed_time = False

                if elapsed_time > fade_time:
                    screen.clear_surface(screen.second_surface)
                    screen.second_surface.set_alpha(255)
                    self.dmg_timer = False
                else:
                    screen.second_surface.set_alpha(255 - (255/fade_time)*elapsed_time)
                    # screen.blit_surface(screen.second_surface)
            # endregion

            # ----|1|---- Base Surface Blit ----|1|----
            enemy.blit()

            if my_turn:
                mouse_over = hud.fight_box(mouse_pos)

            # ----|1|---- Display Blit ----|1|----
            if game_state.ongame_state == "room": screen.blit_surfaces()

            # ----|1|---- Event Handle ----|1|----
            for event in pygame.event.get():
                basic_events(event)

                # ----|2|---- Mouse ----|2|----
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # ----|3|---- Left Click ----|3|----
                    if event.button == 1:
                        if mouse_over == "attack":
                            skill = Skill("attack")
                            skill.activate(player, enemy)
                            self.dmg_timer = time.time()
                    # ------ Escape ------

            # ----|1|---- Exit ----|1|----
            if game_state.ongame_state != "room": break

            # ----|1|---- Tick FPS ----|1|----
            clock.tick(60)

        return None