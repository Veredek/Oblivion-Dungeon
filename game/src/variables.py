import pygame
# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080

BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
TRANSPARENT_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT), pygame.SRCALPHA)

TITLE_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 45)

TITLE_HEIGHT = TITLE_FONT.size("Text Sample")[1]
TEXT_HEIGHT = TEXT_FONT.size("Text Sample")[1]

HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)
HIGHLIGHT_SIGN_SIZE = HIGHLIGHT_SIGN.render("+", True, "Yellow").get_size()

TYPING_SPEED = 50  # Caracteres por segundo
PADDING = 20

MAIN_BOX_SIZE = (0.9 * GAME_WIDTH,
                 TEXT_HEIGHT * 4 + 2 * PADDING)
MAIN_BOX_POS = ((GAME_WIDTH - MAIN_BOX_SIZE[0]) // 2,
                0.7 * GAME_HEIGHT)

ENEMY_CENTER = (GAME_WIDTH / 2, GAME_HEIGHT / 3)