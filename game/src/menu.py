import pygame
from src.definitions import special_highlight, basic_events

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_TITLE = "Oblivion Dungeon"
GAME_NAME_FONT = pygame.font.Font(r"game\assets\fonts\RoyalInitialen.ttf",140)
GAME_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 45)
TEXT_HEIGHT = GAME_FONT.size("Text Sample")[1]
NAME_LENGTH = GAME_FONT.size(12 * "#")[0]
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
PADDING = 20

# ====== Menu ======
def menu(game_state):
    running = True
    game_state.player_name = ""
    while running:
        # ------ Clear Base Surface ------
        BASE_SURFACE.fill(0)

        # ------ Definindo Variáveis ------
        screen = game_state.screen
        mouse_pos = screen.get_mouse()

        # ====== Menu Screen ======
        if game_state.ongame_state == "MENU":
            # ------ Texts ------
            gamename_text = GAME_NAME_FONT.render(GAME_TITLE, True, "White")
            newgame_text = GAME_FONT.render("New Game", True, "White")
            loadgame_text = GAME_FONT.render("Load", True, "White")
            exit_text = GAME_FONT.render("Exit", True, "White")

            # ------ Rectangles ------
            gamename_text_rect = gamename_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 5))
            newgame_text_rect = newgame_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4))
            loadgame_text_rect = loadgame_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 80))
            exit_text_rect = exit_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 160))

            # ------ Base Surface Blit ------
            BASE_SURFACE.blit(gamename_text, gamename_text_rect)
            special_highlight(BASE_SURFACE, GAME_FONT, "New Game", newgame_text_rect, mouse_pos)
            special_highlight(BASE_SURFACE, GAME_FONT, "Load", loadgame_text_rect, mouse_pos)
            special_highlight(BASE_SURFACE, GAME_FONT, "Exit", exit_text_rect, mouse_pos)

        # ====== Your Name Screen ======
        elif game_state.ongame_state == "YOUR NAME":
            # Name Box Blit
            x = (GAME_WIDTH - NAME_LENGTH) // 2 - PADDING
            y = int(GAME_HEIGHT * (5/12)) - PADDING
            width = NAME_LENGTH + 2 * PADDING
            height = TEXT_HEIGHT + 2 * PADDING
            pygame.draw.rect(BASE_SURFACE, "White", (x, y, width, height), 3, 10)

            # ------ Texts ------
            your_name_font = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 75)

            your_name_text = your_name_font.render("Your Name", True, "White")
            enter_text = GAME_FONT.render("Enter", True, "White")
            back_text = GAME_FONT.render("Back", True, "White")
            player_name = TEXT_FONT.render(game_state.player_name, True, "White")

            # ------ Rectangles ------
            your_name_text_rect = your_name_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12))))
            enter_text_rect = enter_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12)) + height + 140))
            back_text_rect = back_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12)) + height + 220))
            player_name_rect = player_name.get_rect(center=(x + width // 2, y + height // 2))

            # ------ Base Surface Blit ------
            BASE_SURFACE.blit(your_name_text, your_name_text_rect)
            special_highlight(BASE_SURFACE, GAME_FONT, "Enter", enter_text_rect, mouse_pos)
            special_highlight(BASE_SURFACE, GAME_FONT, "Back", back_text_rect, mouse_pos)
            BASE_SURFACE.blit(player_name, player_name_rect)

        # ------ Window Blit ------
        scaled_surface = pygame.transform.scale(BASE_SURFACE, (int(GAME_WIDTH * screen.scale), int(GAME_HEIGHT * screen.scale)))
        screen.window.blit(scaled_surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()

        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            basic_events(event, game_state)

            # LEFT CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.ongame_state == "MENU":
                    if newgame_text_rect.collidepoint(mouse_pos):
                        game_state.ongame_state = "YOUR NAME"
                    elif loadgame_text_rect.collidepoint(mouse_pos):
                        game_state.ongame_state = "LOAD"
                        running = False
                    elif exit_text_rect.collidepoint(mouse_pos):
                        game_state.state = "Exit Game"
                        running = False
                elif game_state.ongame_state == "YOUR NAME":
                    if enter_text_rect.collidepoint(mouse_pos) and game_state.player_name != "":
                        game_state.state = "New Game"
                        running = False
                    if back_text_rect.collidepoint(mouse_pos):
                        game_state.ongame_state = "MENU"
            
            # KEYDOWN
            elif event.type == pygame.KEYDOWN:
                # Digitando Nome
                if game_state.ongame_state == "YOUR NAME":
                    if event.key == pygame.K_BACKSPACE:
                        game_state.player_name = game_state.player_name[:-1]
                    elif event.key == pygame.K_RETURN and len(game_state.player_name) > 0:
                        running = False
                    else:
                        char = event.unicode
                        name_len = GAME_FONT.size(game_state.player_name)[0]
                        if name_len < NAME_LENGTH:
                            game_state.player_name += char

    return None