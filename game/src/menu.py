import pygame

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions
from src.entities import player

# ========== Local Variables ==========
class Local:
    def __init__(self):
        # region ----|1|---- Your Name Font
        self.your_name_font = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 75)
            # endregion
        # region ----|1|---- NameBox Position
        self.namebox_pos = ((config.BASE_WIDTH - config.name_length) / 2 - config.PADDING,
                            config.BASE_HEIGHT * (5/12) - config.PADDING)
            # endregion
        # region ----|1|---- NameBox Size
        self.namebox_size = (config.name_length + 2 * config.PADDING,
                             config.TITLE_HEIGHT + 2 * config.PADDING)
            # endregion
        # region ----|1|---- Game Title Rect
        surface = config.TITLE_FONT.render(config.GAME_TITLE, True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, config.BASE_HEIGHT / 5))
        self.gametitle_rect = rect
            # endregion
        # region ----|1|---- New Game Rect
        surface = config.TITLE_FONT.render("New Game", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, config.BASE_HEIGHT / 2.4))
        self.newgame_rect = rect
            # endregion
        # region ----|1|---- Load Rect
        surface = config.TITLE_FONT.render("Load", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, config.BASE_HEIGHT / 2.4 + 80))
        self.load_rect = rect
            # endregion        
        # region ----|1|---- Exit Rect
        surface = config.TITLE_FONT.render("Exit", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, config.BASE_HEIGHT / 2.4 + 160))
        self.exit_rect = rect
            # endregion
        # region ----|1|---- Your Name Rect
        surface = self.your_name_font.render("Your Name", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, int(config.BASE_HEIGHT * (4/12))))
        self.yourname_rect = rect
            # endregion
        # region ----|1|---- Enter Rect
        surface = config.TITLE_FONT.render("Enter", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, int(config.BASE_HEIGHT * (4/12)) + self.namebox_size[1] + 140))
        self.enter_rect = rect
            # endregion
        # region ----|1|---- Back Rect
        surface = config.TITLE_FONT.render("Back", True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, int(config.BASE_HEIGHT * (4/12)) + self.namebox_size[1] + 220))
        self.back_rect = rect
            # endregion
        # region ----|1|---- Name Rect
        surface = config.TEXT_FONT.render(player.name, True, "White")
        rect = surface.get_rect(center=(config.BASE_WIDTH / 2, self.namebox_pos[1] + self.namebox_size[1] / 2))
        self.name_rect = rect
            # endregion    

local = Local()

# ========== (menu) ==========
def menu():
    clock = pygame.time.Clock()
    
    running = True
    while running:
        if game_state.state != "MENU": break
        # ----|1|---- Clear Surfaces ----|1|----
        screen.clear_surfaces()

        # ----|1|---- Loop Variables ----|1|----
        mouse_pos = screen.mouse

        # ----|1|---- Menu Screen ----|1|----
        if game_state.ongame_state == "menu":

            # ----|2|---- Blit Text on Base Surface ----|2|----
            functions.text_on_base_surface(config.GAME_TITLE, config.GAMENAME_FONT,
                                           center=local.gametitle_rect.center)
            functions.text_on_base_surface("New Game", config.TITLE_FONT, h_button=True,
                                           center=local.newgame_rect.center)
            functions.text_on_base_surface("Load", config.TITLE_FONT, h_button=True,
                                           center=local.load_rect.center)
            functions.text_on_base_surface("Exit", config.TITLE_FONT, h_button=True,
                                           center=local.exit_rect.center)
            
        # ----|1|---- Your Name Screen ----|1|----
        elif game_state.ongame_state == "your name":
            # ----|2|---- Name Box Blit ----|2|----
            pygame.draw.rect(screen.base_surface, "White", (local.namebox_pos[0], local.namebox_pos[1], local.namebox_size[0], local.namebox_size[1]), 3, 10)

            # ----|2|---- Blit Text on Base Surface ----|2|----
            functions.text_on_base_surface("Your Name", local.your_name_font,
                                           center=local.yourname_rect.center)
            functions.text_on_base_surface("Enter", config.TITLE_FONT, h_button=True,
                                           center=local.enter_rect.center)
            functions.text_on_base_surface("Back", config.TITLE_FONT, h_button=True,
                                           center=local.back_rect.center)
            functions.text_on_base_surface(player.name, local.your_name_font,
                                           center=local.name_rect.center)

        # ----|1|---- Display Blit ----|1|----
        screen.blit_surface(screen.base_surface)

        # ----|1|---- Detecting Events ----|1|----
        for event in pygame.event.get():
            functions.basic_events(event)

            # ----|2|---- Mouse Button ----|2|----
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ----|3|---- Left Click ----|3|----
                if event.button == 1:
                    # ----|4|---- MENU ----|4|----
                    if game_state.ongame_state == "menu":
                        # New Game
                        if local.newgame_rect.collidepoint(mouse_pos):
                            game_state.ongame_state = "your name"
                        # Load Game
                        elif local.load_rect.collidepoint(mouse_pos):
                            game_state.ongame_state = "load"
                        # Exit Game
                        elif local.exit_rect.collidepoint(mouse_pos):
                            game_state.state = "EXIT GAME"

                    # ----|4|---- YOUR NAME ----|4|----
                    elif game_state.ongame_state == "your name":
                        # Enter
                        if local.enter_rect.collidepoint(mouse_pos) and player.name != "":
                            game_state.state = "NEW GAME"
                            print("-> New Game <-")
                        # Back
                        elif local.back_rect.collidepoint(mouse_pos):
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
                        print("-> New Game <-")
                    else:
                        char = event.unicode
                        name_len = config.TITLE_FONT.size(player.name)[0]
                        if name_len < config.name_length:
                            player.name += char

        # ----|1|---- Exit ----|1|----
        if game_state.state != "MENU": break
    
        # ----|1|---- Clock ----|1|----
        clock.tick(60)

    return None