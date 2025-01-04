import pygame
pygame.init()
pygame.font.init()

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_TITLE = "Oblivion Dungeon"
GAME_NAME_FONT = pygame.font.Font(r"game\assets\fonts\RoyalInitialen.ttf",140)
GAME_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 45)
HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)
TEXT_HEIGHT = GAME_FONT.size("Text Sample")[1]
NAME_LENGTH = GAME_FONT.size(12 * "#")[0]
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
PADDING = 20

# ====== Definitions ======
# ------ Highlight Button ------
def special_highlight(surface, font, text, text_rect,mouse_pos):
    if text_rect.collidepoint(mouse_pos):
        text_surface = font.render(text, True, "Yellow")
        sign_surface = HIGHLIGHT_SIGN.render("+", True, "Yellow")
        text_size = text_surface.get_size()
        sign_size = sign_surface.get_size()
        highlight_surface = pygame.Surface((text_size[0] + 2 * sign_size[0] + 10, text_size[1] if text_size[1] > sign_size[1] else sign_size[1]))
        highlight_surface.blit(sign_surface, (0, (text_size[1] - sign_size[1]) // 2))
        highlight_surface.blit(text_surface, (sign_size[0] + 5, 0))
        highlight_surface.blit(sign_surface, (sign_size[0] + text_size[0] + 10, (text_size[1] - sign_size[1]) // 2))
        surface.blit(highlight_surface, (text_rect[0] - sign_size[0] - 5, text_rect[1]))
    else:
        normal_surface = font.render(text, True, "White")
        surface.blit(normal_surface, text_rect)

# ------ Text with Outline ------
def glowing_text(text, font, text_color, outline_color, outline_width):
    # Renderizar o texto com a cor do contorno
    outline_surface = font.render(text, True, outline_color)

    # Criar uma superfície maior para acomodar o contorno
    w, h = outline_surface.get_size()
    surface = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)

    # Desenhar o contorno ao redor do texto
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx**2 + dy**2 <= outline_width**2:  # Forma circular
                surface.blit(outline_surface, (dx + outline_width, dy + outline_width))

    # Renderizar o texto principal
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (outline_width, outline_width))

    return surface

def basic_events(event, game_state):
    screen = game_state.screen
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    # Detecta eventos de redimensionamento
    elif event.type == pygame.VIDEORESIZE:
        if event.size != screen.size:
            print(f"Event Size:{event.size},\nWindow Size:{screen.size}\n")
            if screen.fullscreen == False:
                screen.resize(event)

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F11:
            print("F11\n")
            screen.toggle_fullscreen()

    return None