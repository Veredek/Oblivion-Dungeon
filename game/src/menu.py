import pygame

# ====== Functions ======
from src.definitions import special_highlight, basic_events, blit_surface

# ====== Global Objects ======
from src.classes import screen, game_state
from src.entities import player

# ====== Global Variables ======
from src.variables import GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE
from src.variables import TITLE_FONT, TEXT_FONT, PADDING

GAME_NAME = "Oblivion Dungeon"
GAME_NAME_FONT = pygame.font.Font(r"game\assets\fonts\RoyalInitialen.ttf",140)
TEXT_HEIGHT = TITLE_FONT.size("Text Sample")[1]
NAME_LENGTH = TITLE_FONT.size(12 * "#")[0]

# ====== Menu ======
def menu():
    running = True
    while running:
        if game_state.state != "MENU": break
        # ------ Clear Base Surface ------
        BASE_SURFACE.fill(0)

        # ------ Loop Variables ------
        mouse_pos = screen.get_mouse()

        # ====== Menu Screen ======
        if game_state.ongame_state == "menu":
            # ------ Texts ------
            gamename_text = GAME_NAME_FONT.render(GAME_NAME, True, "White")
            newgame_text = TITLE_FONT.render("New Game", True, "White")
            loadgame_text = TITLE_FONT.render("Load", True, "White")
            exit_text = TITLE_FONT.render("Exit", True, "White")

            # ------ Rectangles ------
            gamename_text_rect = gamename_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 5))
            newgame_text_rect = newgame_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4))
            loadgame_text_rect = loadgame_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 80))
            exit_text_rect = exit_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 160))

            # ------ Base Surface Blit ------
            BASE_SURFACE.blit(gamename_text, gamename_text_rect)
            special_highlight(BASE_SURFACE, TITLE_FONT, "New Game", newgame_text_rect)
            special_highlight(BASE_SURFACE, TITLE_FONT, "Load", loadgame_text_rect)
            special_highlight(BASE_SURFACE, TITLE_FONT, "Exit", exit_text_rect)

        # ====== Your Name Screen ======
        elif game_state.ongame_state == "your name":
            # Name Box Blit
            x = (GAME_WIDTH - NAME_LENGTH) // 2 - PADDING
            y = int(GAME_HEIGHT * (5/12)) - PADDING
            width = NAME_LENGTH + 2 * PADDING
            height = TEXT_HEIGHT + 2 * PADDING
            pygame.draw.rect(BASE_SURFACE, "White", (x, y, width, height), 3, 10)

            # ------ Texts ------
            your_name_font = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 75)

            your_name_text = your_name_font.render("Your Name", True, "White")
            enter_text = TITLE_FONT.render("Enter", True, "White")
            back_text = TITLE_FONT.render("Back", True, "White")
            player_name_surface = TEXT_FONT.render(player.name, True, "White")

            # ------ Rectangles ------
            your_name_text_rect = your_name_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12))))
            enter_text_rect = enter_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12)) + height + 140))
            back_text_rect = back_text.get_rect(center=(GAME_WIDTH // 2, int(GAME_HEIGHT * (4/12)) + height + 220))
            player_name_rect = player_name_surface.get_rect(center=(x + width // 2, y + height // 2))

            # ------ Base Surface Blit ------
            BASE_SURFACE.blit(your_name_text, your_name_text_rect)
            special_highlight(BASE_SURFACE, TITLE_FONT, "Enter", enter_text_rect)
            special_highlight(BASE_SURFACE, TITLE_FONT, "Back", back_text_rect)
            BASE_SURFACE.blit(player_name_surface, player_name_rect)

        # ------ Window Blit ------
        blit_surface(BASE_SURFACE)

        # ------ Detecting Events ------
        for event in pygame.event.get():
            basic_events(event)

            # LEFT CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.ongame_state == "menu":
                    if newgame_text_rect.collidepoint(mouse_pos):
                        game_state.ongame_state = "your name"

                    elif loadgame_text_rect.collidepoint(mouse_pos):
                        game_state.ongame_state = "load"

                    elif exit_text_rect.collidepoint(mouse_pos):
                        game_state.state = "EXIT GAME"

                elif game_state.ongame_state == "your name":
                    if enter_text_rect.collidepoint(mouse_pos) and player.name != "":
                        game_state.state = "NEW GAME"

                    elif back_text_rect.collidepoint(mouse_pos):
                        player.name = ""
                        game_state.ongame_state = "menu"
            
            # KEYDOWN
            elif event.type == pygame.KEYDOWN:
                # Digitando Nome
                if game_state.ongame_state == "your name":
                    if event.key == pygame.K_BACKSPACE:
                        player.name = player.name[:-1]
                    elif event.key == pygame.K_RETURN and len(player.name) > 0:
                        game_state.state = "NEW GAME"
                    else:
                        char = event.unicode
                        name_len = TITLE_FONT.size(player.name)[0]
                        if name_len < NAME_LENGTH:
                            player.name += char

        # ------ Exit ------
        if game_state.state != "MENU": break

    return None