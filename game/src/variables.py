import pygame
# ====== Definitions (Local) ======
def get_resolution():
    """
    A proporção 16:9 está entre 1.7 e 1.8
    """

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    output_resolution = (0,0)

    # Check if screen proportion is 16:9 or else
    screen_proportion = screen_width / screen_height

    # narrow screen
    if screen_proportion < (16/9): 
        # width as base to fit screen
        for resolution in RESOLUTIONS:
            if screen_width >= resolution[0]:
                output_resolution = resolution
            else:
                break

    # normal and wide screen
    elif screen_proportion >= (16/9):
        # height as base to fit screen
        for resolution in RESOLUTIONS:
            if screen_height >= resolution[1]:
                output_resolution = resolution
            else:
                break

    return output_resolution

# ====== Global Variables ======
RESOLUTIONS = [(854,480), # WVGA
               (960,540), # qHD
               (1280, 720), # HD
               (1366,768), # HD
               (1600, 900), # HD+
               (1920, 1080), # FULL HD 
               (2560, 1440), # QHD
               (3840, 2160)] # 4k
GAME_RESOLUTION = get_resolution()
GAME_WIDTH = GAME_RESOLUTION[0]
GAME_HEIGHT = GAME_RESOLUTION[1]
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