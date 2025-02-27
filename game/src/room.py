import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions
from src.Boxes import boxes
from src.skills import SKILLS
from src.entities import player, slime, Entity

# ====== Global Variables ======
attack_text_rect_center = (config.MAINBOX_POS[0] + (1/5)*config.MAINBOX_SIZE[0],
                            config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1])

# ========== Functions ==========
def flash_enemy(enemy : Entity):
    clock = pygame.time.Clock()
    image = enemy.image()
    flashed = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 0))
    flashed.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

    flashing = True
    timer = time.time()
    while flashing:
        # ----|1|---- Clear Surfaces ----|1|----
        screen.clear_surfaces()

        # ----|1|---- Elapsed Time ----|1|----
        elapsed = time.time() - timer

        # ----|1|---- Flash Frames ----|1|----
        if int(elapsed * 20) % 2 == 0:
            enemy_display = flashed
        else:
            enemy_display = image

        # ----|1|---- Window Blit ----|1|----
        boxes.draw_mainbox()

        enemy_display_rect = enemy_display.get_rect(center=config.ENEMY_CENTER)
        screen.base_surface.blit(enemy_display, enemy_display_rect)
        screen.blit_surface(screen.base_surface)

        # ----|1|---- Stop ----|1|----
        if elapsed > 0.5:
            flashing = False
    
        # ----|1|---- Tick FPS ----|1|----
        clock.tick(60)

# ========== (room) ==========
class Room:
    def __init__(self):
        self.attack_text_rect = config.TITLE_FONT.render("Attack", True, 0).get_rect(center=attack_text_rect_center)

    def enemy_room(self):
        clock = pygame.time.Clock()
        enemy = slime()
        my_turn = True

        running = True
        while running:
            if game_state.ongame_state != "room": break
            # ----|1|---- Clear Surfaces ----|1|----
            screen.clear_surfaces

            # ----|1|---- Loop Variables ----|1|----
            mouse_pos = screen.get_mouse()          

            # ----|1|---- Base Surface Blit ----|1|----
            enemy.blit()

            if my_turn:
                mouse_over = boxes.fight_box()

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
                            skill = SKILLS["attack"]()
                            skill.activate(player, enemy)
                            flash_enemy(enemy)
                            print(enemy.stats["HP"])
                    # ------ Escape ------

            # ----|1|---- Exit ----|1|----
            if game_state.ongame_state != "room": break

            # ----|1|---- Tick FPS ----|1|----
            clock.tick(60)

        return None