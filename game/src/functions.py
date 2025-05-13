import pygame
import os

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state

# ========== (functions) ==========
class Functions:
    def __init__(self):  pass

    # ~~~~~~~~~~ Highlight Button ~~~~~~~~~~
    def highlight_button(self, mouse_pos : property, font : pygame.font.Font, text : str, text_rect : pygame.Rect):
        '''
        Blit a button on given surface
        '''

        surface = screen.base_surface

        if text_rect.collidepoint(mouse_pos):
            # ~~~~~~~~~~ Surfaces ~~~~~~~~~~
            text_surface = font.render(text, True, "Yellow")
            sign_surface = config.HIGHLIGHT_SIGN.render("+", True, "Yellow")

            # ~~~~~~~~~~ Sizes ~~~~~~~~~~
            text_size = text_surface.get_size()
            sign_size = sign_surface.get_size()

            spacer = 5

            highlighted_surface_size = (text_size[0] + 2 * sign_size[0] + 2*spacer,
                                        text_size[1])

            # ~~~~~~~~~~ Blit ~~~~~~~~~~
            highlighted_surface = pygame.Surface(highlighted_surface_size)
            highlighted_surface.blit(sign_surface, (0, (text_size[1] - sign_size[1]) // 2))
            highlighted_surface.blit(text_surface, (sign_size[0] + spacer, 0))
            highlighted_surface.blit(sign_surface, (sign_size[0] + text_size[0] + 2*spacer, (text_size[1] - sign_size[1]) // 2))

            surface.blit(highlighted_surface, (text_rect[0] - sign_size[0] - spacer, text_rect[1]))

        else:
            normal_surface = font.render(text, True, "White")
            surface.blit(normal_surface, text_rect)

    # ~~~~~~~~~~ Highlight Text ~~~~~~~~~~
    def highlight(self, surface : pygame.Surface, font : pygame.font, text : str, text_rect : pygame.Rect):
        """
        Cria um texto cinza que fica branco quando colide com o mouse
        """

        mouse_pos = screen.mouse

        if text_rect.collidepoint(mouse_pos):
            highlighted_surface = font.render(text, True, "White")
            surface.blit(highlighted_surface, text_rect)
        else:
            normal_surface = font.render(text, True, "Gray")
            surface.blit(normal_surface, text_rect)

    # ~~~~~~~~~~ Text with Outline ~~~~~~~~~~
    def glowing_text(self, text : str, font : pygame.font, text_color : str, outline_color : str, outline_width : int):
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

    # ~~~~~~~~~~ Esc Menu ~~~~~~~~~~
    def esc_menu(self):
        clock = pygame.time.Clock()

        inside = True
        while inside:
            screen.clear_surfaces()
            mouse_pos = screen.mouse

            # region ----|1|---- Font Surfaces
            continue_text = config.TITLE_FONT.render("Continue", True, "White")
            quit_text = config.TITLE_FONT.render("Quit", True, "White")
            # endregion -|1|-

            # region ----|1|---- Rectangles
            continue_text_rect = continue_text.get_rect(center=(config.game_width / 2, config.game_height / 2 - 80))
            quit_text_rect = quit_text.get_rect(center=(config.game_width / 2, config.game_height / 2 + 40))
            # endregion -|1|-

            # region ----|1|---- Blit Button on base_surface
            self.highlight_button(mouse_pos, config.TITLE_FONT, "Continue", continue_text_rect)
            self.highlight_button(mouse_pos, config.TITLE_FONT, "Quit", quit_text_rect)
            # endregion -|1|-

            # region ----|1|---- Display Blit
            screen.blit_surface(screen.base_surface)
            # endregion -|1|-

            # region ----|1|---- Event Handle

            for event in pygame.event.get():
                # region ----|2|---- Quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # endregion -|2|-

                # region ----|2|---- Videorisize
                elif event.type == pygame.VIDEORESIZE:
                    if event.size != screen.display_size:
                        if screen.fullscreen == False:
                            print("*Video Resize*"
                                    f"    Event Size:{event.size}," +
                                    f"    Display Size:{screen.display_size}\n")
                            screen.resize(event)
                # endregion -|2|-

                # region ----|2|---- Keydown
                elif event.type == pygame.KEYDOWN:
                    print("*Keydown*")
                    if event.key == pygame.K_F11:
                        print("    F11\n")
                        screen.toggle_fullscreen()

                    elif event.key == pygame.K_ESCAPE:
                        print("    Esc")
                        inside = False
                # endregion -|2|-

                # region ----|2|---- Mouse Button
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # region ----|3|---- Left Click
                    if event.button == 1:

                        # region ----|4|---- CONTINUE
                        if continue_text_rect.collidepoint(mouse_pos):
                            print("-> Continue <-\n")
                            inside = False
                        # endregion -|4|-

                        # region ----|4|---- QUIT
                        elif quit_text_rect.collidepoint(mouse_pos):
                            print("-> Quit <-\n")
                            game_state.state = "MENU"
                            game_state.ongame_state = "menu"
                            inside = False
                        # endregion -|4|-

                    # endregion -|3|-

                # endregion -|2|-

            # endregion -|1|-

            # Tick FPS
            clock.tick(60)

        return None

    # ~~~~~~~~~~ Test for basic events ~~~~~~~~~~
    def basic_events(self, event):
        # region ----|1|---- Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # endregion -|1|-

        # region ----|1|---- Video Resize
        elif event.type == pygame.VIDEORESIZE:
            if event.size != screen.display_size:
                if screen.fullscreen == False:
                    print("*Video Resize*"
                            f"    Event Size:{event.size}," +
                            f"    Display Size:{screen.display_size}\n")
                    screen.resize(event)
        # endregion -|1|-

        # region ----|1|---- Keydown
        elif event.type == pygame.KEYDOWN:
            print("*Keydown*")
            if event.key == pygame.K_F11:
                print("    F11\n")
                screen.toggle_fullscreen()

            elif event.key == pygame.K_ESCAPE:
                print("    Esc\n")
                if game_state.state != "MENU":
                    print("-> Menu <-")
                    self.esc_menu()
        # endregion -|1|-

        return None

    # ~~~~~~~~~~ Load Image ~~~~~~~~~~
    def load_image(self, name: str):
        fullname = os.path.join("game", "assets", "images", f"{name}.png")
        image = pygame.image.load(fullname)
        return image

    # ~~~~~~~~~~ Blit Text on Base Surface ~~~~~~~~~~
    def text_on_base_surface(self, text: str, font : pygame.font.Font, color : str = "white", topleft = False, center = False, h_button = False):
        text_surface = font.render(text, True, color)
        mouse_pos = screen.mouse

        if center:
            text_rect = text_surface.get_rect(center=center)
        elif topleft:
            text_rect = text_surface.get_rect(topleft=topleft)

        if h_button:
            self.highlight_button(mouse_pos, font, text, text_rect)
        else:
            screen.base_surface.blit(text_surface, text_rect)

# ====== Instaciation ======
functions = Functions()