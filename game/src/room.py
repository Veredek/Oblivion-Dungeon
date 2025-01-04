import pygame
from src.Boxes import Boxes
from src.definitions import basic_events

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
GAME_FONT = pygame.font.SysFont("comicsans", 30)
HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)
TYPING_SPEED = 50  # Caracteres por segundo

# ====== Definitions ======

# ====== Main Function ======
def enemy_room(game_state):
    screen = game_state.screen
    boxes = Boxes()
    running = True
    while running:
        # ------ Loop Variables ------
        mouse_pos = screen.get_mouse()          

        # ------ Screen ------
        BASE_SURFACE.fill(0)
        boxes.draw_mainbox(BASE_SURFACE)

        # ------ Window Blit ------
        scaled_surface = pygame.transform.scale(BASE_SURFACE, (int(GAME_WIDTH * screen.scale), int(GAME_HEIGHT * screen.scale)))
        screen.window.blit(scaled_surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()             

        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            basic_events(event, game_state)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # ------ Escape ------

    return None