import pygame
# ====== Definitions (Local) ======
def get_resolution():
    """
    A proporção 16:9 está entre 1.7 e 1.8
    """

    # Check if screen proportion is 16:9 or else
    screen_proportion = MONITOR_SIZE[0] / MONITOR_SIZE[1]

    # narrow screen
    if screen_proportion < (16/9): 
        # width as base to fit screen
        game_width = MONITOR_SIZE[0]
        game_heigth = game_width / (16/9)

    # normal and wide screen
    elif screen_proportion >= (16/9):
        # height as base to fit screen
        game_heigth = MONITOR_SIZE[1]
        game_width = game_heigth * (16/9)

    output_resolution = (game_width, game_heigth)
    return output_resolution

# ====== Global Variables ======
GAME_TITLE = "Oblivion Dungeon"

MONITOR_SIZE = (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
MIN_WINDOW_SIZE = (854,480)
RESOLUTION = get_resolution()
GAME_WIDTH = RESOLUTION[0]
GAME_HEIGHT = RESOLUTION[1]
RESOLUTION_SCALE = GAME_HEIGHT / 1080

BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
TRANSPARENT_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT), pygame.SRCALPHA)

TITLE_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", int(RESOLUTION_SCALE * 65))
TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", int(RESOLUTION_SCALE * 45))

TITLE_HEIGHT = TITLE_FONT.size("Text Sample")[1]
TEXT_HEIGHT = TEXT_FONT.size("Text Sample")[1]

HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", int(RESOLUTION_SCALE * 50))
HIGHLIGHT_SIGN_SIZE = HIGHLIGHT_SIGN.render("+", True, "Yellow").get_size()

TYPING_SPEED = 50  # Caracteres por segundo
PADDING = int(RESOLUTION_SCALE * 20)
 
MAIN_BOX_SIZE = (0.9 * GAME_WIDTH,
                 TEXT_HEIGHT * 4 + 2 * PADDING)
MAIN_BOX_POS = ((GAME_WIDTH - MAIN_BOX_SIZE[0]) // 2,
                0.7 * GAME_HEIGHT)

ENEMY_CENTER = (GAME_WIDTH / 2, GAME_HEIGHT / 3)