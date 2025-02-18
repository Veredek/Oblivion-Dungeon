import pygame

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions, s
from src.entities import player

# ========== Local Variables ==========
class Local:
    def __init__(self):
        pass

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    @property
    def your_name_font(self):
        return pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", s(75))
    
    @property
    def namebox_pos(self):
        return ((config.game_width - config.name_length) / 2 - config.padding,
                config.game_height * (5/12) - config.padding)
    
    @property
    def namebox_size(self):
        return (config.name_length + 2 * config.padding,
                config.title_height + 2 * config.padding)
    
    @property
    def gametitle_rect(self):
        surface = config.title_font.render(config.GAME_TITLE, True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, config.game_height / 5))
        return rect
    
    @property
    def newgame_rect(self):
        surface = config.title_font.render("New Game", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, config.game_height / 2.4))
        return rect
    
    @property
    def load_rect(self):
        surface = config.title_font.render("Load", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, config.game_height / 2.4 + s(80)))
        return rect
    
    @property
    def exit_rect(self):
        surface = config.title_font.render("Exit", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, config.game_height / 2.4 + s(160)))
        return rect
    
    @property
    def yourname_rect(self):
        surface = self.your_name_font.render("Your Name", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, int(config.game_height * (4/12))))
        return rect
    
    @property
    def enter_rect(self):
        surface = config.title_font.render("Enter", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, int(config.game_height * (4/12)) + local.namebox_size[1] + s(140)))
        return rect
    
    @property
    def back_rect(self):
        surface = config.title_font.render("Back", True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, int(config.game_height * (4/12)) + local.namebox_size[1] + s(220)))
        return rect
    
    @property
    def name_rect(self):
        surface = config.text_font.render(player.name, True, "White")
        rect = surface.get_rect(center=(config.game_width / 2, local.namebox_pos[1] + local.namebox_size[1] / 2))
        return rect
    
local = Local()

# ========== Functions ==========

# ========== (menu) ==========
def menu():
    clock = pygame.time.Clock()
    
    running = True
    while running:
        if game_state.state != "MENU": break
        # ----|1|---- Clear Surfaces ----|1|----
        screen.clear_surfaces()

        # ----|1|---- Loop Variables ----|1|----
        mouse_pos = pygame.mouse.get_pos()

        # ----|1|---- Menu Screen ----|1|----
        if game_state.ongame_state == "menu":

            # ----|2|---- Blit Text on Base Surface ----|2|----
            functions.text_on_base_surface(config.GAME_TITLE, config.gamename_font,
                                           center=local.gametitle_rect.center)
            functions.text_on_base_surface("New Game", config.title_font, h_button=True,
                                           center=local.newgame_rect.center)
            functions.text_on_base_surface("Load", config.title_font, h_button=True,
                                           center=local.load_rect.center)
            functions.text_on_base_surface("Exit", config.title_font, h_button=True,
                                           center=local.exit_rect.center)
            
        # ----|1|---- Your Name Screen ----|1|----
        elif game_state.ongame_state == "your name":
            # ----|2|---- Name Box Blit ----|2|----
            pygame.draw.rect(screen.base_surface, "White", (local.namebox_pos[0], local.namebox_pos[1], local.namebox_size[0], local.namebox_size[1]), s(3), s(10))

            # ----|2|---- Blit Text on Base Surface ----|2|----
            functions.text_on_base_surface("Your Name", local.your_name_font,
                                           center=local.yourname_rect.center)
            functions.text_on_base_surface("Enter", config.title_font, h_button=True,
                                           center=local.enter_rect.center)
            functions.text_on_base_surface("Back", config.title_font, h_button=True,
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
                        if local.newgame_rect.collidepoint(mouse_pos):
                            game_state.ongame_state = "your name"

                        elif local.load_rect.collidepoint(mouse_pos):
                            game_state.ongame_state = "load"

                        elif local.exit_rect.collidepoint(mouse_pos):
                            game_state.state = "EXIT GAME"

                    # ----|4|---- YOUR NAME ----|4|----
                    elif game_state.ongame_state == "your name":
                        if local.enter_rect.collidepoint(mouse_pos) and player.name != "":
                            game_state.state = "NEW GAME"
                            print("-> New Game <-")

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
                        name_len = config.title_font.size(player.name)[0]
                        if name_len < config.name_length:
                            player.name += char

        # ----|1|---- Exit ----|1|----
        if game_state.state != "MENU": break
    
        # ----|1|---- Clock ----|1|----
        clock.tick(60)

    return None