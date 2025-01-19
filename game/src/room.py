import pygame
import time

from src.Boxes import boxes
from src.skills import SKILLS

# ====== Global Objects ======
from src.classes import screen, game_state
from src.entities import player
from src.entities import slime

# ====== Global Variables ======
from src.variables import GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE, TRANSPARENT_SURFACE
from src.variables import TITLE_FONT, TEXT_FONT
from src.variables import MAIN_BOX_POS, MAIN_BOX_SIZE
from src.variables import ENEMY_CENTER

# ====== Definitions ======
from src.definitions import basic_events, blit_surface

def flash_enemy(enemy):
    clock = pygame.time.Clock()
    image = enemy.image()
    flashed = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 0))
    flashed.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

    flashing = True
    timer = time.time()
    while flashing:
        elapsed = time.time() - timer

        # ------ Flash Frames ------
        if int(elapsed * 20) % 2 == 0:
            enemy_display = flashed
        else:
            enemy_display = image

        # ------ Window Blit ------
        BASE_SURFACE.fill(0)
        boxes.draw_mainbox()

        enemy_display_rect = enemy_display.get_rect(center=ENEMY_CENTER)
        BASE_SURFACE.blit(enemy_display, enemy_display_rect)
        blit_surface(BASE_SURFACE)

        # ------ Stop ------
        if elapsed > 0.5:
            flashing = False
    
        # ------ FPS ------
        clock.tick(60)

# ====== Class Enemy Room ======
class Room:
    def __init__(self):
        self.attack_text_rect = TITLE_FONT.render("Attack", True, 0).get_rect(center=(MAIN_BOX_POS[0] + (1/5)*MAIN_BOX_SIZE[0], MAIN_BOX_POS[1] + (1/2)*MAIN_BOX_SIZE[1]))


    def enemy_room(self):
        clock = pygame.time.Clock()
        enemy = slime()
        my_turn = True

        running = True
        while running:
            if game_state.ongame_state != "room": break
            # ------ Loop Variables ------
            mouse_pos = screen.get_mouse()          

            # ------ Screen ------
            BASE_SURFACE.fill(0)
            enemy.blit()

            if my_turn:
                mouse_over = boxes.fight_box()

            # ------ Window Blit ------
            if game_state.ongame_state == "room": blit_surface(BASE_SURFACE)

            # ------ Detectando Eventos ------
            for event in pygame.event.get():
                basic_events(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_over == "attack":
                        skill = SKILLS["attack"]()
                        skill.activate(player, enemy)
                        flash_enemy(enemy)
                        print(enemy.stats["HP"])
                    # ------ Escape ------

            # ------ FPS ------
            clock.tick(60)

            # ------ Exit ------
            if game_state.ongame_state != "room": break

        return None