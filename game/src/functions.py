import pygame
import math
import os

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state

# ========== Functions ==========
# ~~~~~~~~~~ Scale ~~~~~~~~~~
def s(value : int):
    updated_value = round(config.scale * value)
    return updated_value if updated_value > 0 else 1

# ========== (functions) ==========
class Functions:
    def __init__(self):
        pass

    # ~~~~~~~~~~ Highlight Button ~~~~~~~~~~
    def highlight_button(self, surface : pygame.Surface, font : pygame.font, text : str, text_rect : pygame.Rect):
        '''
        Blit a button on given surface
        '''

        mouse_pos = pygame.mouse.get_pos()
        
        if text_rect.collidepoint(mouse_pos):
            text_surface = font.render(text, True, "Yellow")
            sign_surface = config.highlight_sign.render("+", True, "Yellow")

            text_size = text_surface.get_size()
            sign_size = sign_surface.get_size()

            spacer = 5

            highlighted_surface_size = (text_size[0] + 2 * sign_size[0] + 2*spacer,
                                        text_size[1])
            
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

        mouse_pos = pygame.mouse.get_pos()

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
            mouse_pos = pygame.mouse.get_pos()

            # ----|1|---- Font Surfaces ----|1|----
            continue_text = config.title_font.render("Continue", True, "White")
            quit_text = config.title_font.render("Quit", True, "White")

            # ----|1|---- Rectangles ----|1|----
            continue_text_rect = continue_text.get_rect(center=(config.game_width / 2, config.game_height / 2 - 80))
            quit_text_rect = quit_text.get_rect(center=(config.game_width / 2, config.game_height / 2 + 40))

            # ----|1|---- Blit Button on base_surface ----|1|----
            self.highlight_button(screen.base_surface, config.title_font, "Continue", continue_text_rect)
            self.highlight_button(screen.base_surface, config.title_font, "Quit", quit_text_rect)

            # ----|1|---- Display Blit ----|1|----
            screen.blit_surface(screen.base_surface)

            # ----|1|---- Event Handle ----|1|----
            for event in pygame.event.get():
                # ----|2|---- Quit ----|2|----
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                # ----|2|---- Videorisize ----|2|----
                elif event.type == pygame.VIDEORESIZE:
                    if event.size != screen.display_size:
                        if screen.fullscreen == False:
                            print("*Video Resize*"
                                    f"    Event Size:{event.size}," +
                                    f"    Display Size:{screen.display_size}\n")
                            screen.resize(event)

                # ----|2|---- Keydown ----|2|----
                elif event.type == pygame.KEYDOWN:
                    print("*Keydown*")
                    if event.key == pygame.K_F11:
                        print("    F11\n")
                        screen.toggle_fullscreen()

                    elif event.key == pygame.K_ESCAPE:
                        print("    Esc")
                        inside = False

                # ----|2|---- Mouse Button ----|2|----
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # ----|3|---- Left Click ----|3|----
                    if event.button == 1:

                        # ----|4|---- CONTINUE ----|4|----
                        if continue_text_rect.collidepoint(mouse_pos):
                            print("-> Continue <-\n")
                            inside = False

                        # ----|4|---- QUIT ----|4|----
                        elif quit_text_rect.collidepoint(mouse_pos):
                            print("-> Quit <-\n")
                            game_state.state = "MENU"
                            game_state.ongame_state = "menu"                    
                            inside = False

            # ----|1|---- Tick FPS ----|1|----
            clock.tick(60)

        return None

    # ~~~~~~~~~~ Test for basic events ~~~~~~~~~~
    def basic_events(self, event):
        # ----|1|---- Quit ----|1|----
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ----|1|---- Video Resize ----|1|----
        elif event.type == pygame.VIDEORESIZE:
            if event.size != screen.display_size:
                if screen.fullscreen == False:
                    print("*Video Resize*"
                            f"    Event Size:{event.size}," +
                            f"    Display Size:{screen.display_size}\n")
                    screen.resize(event)

        # ----|1|---- Keydown ----|1|----
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

        return None

    # ~~~~~~~~~~ Load Image ~~~~~~~~~~
    def load_image(self, name: str):
        fullname = os.path.join("game", "assets", "images", f"{name}.png")
        image = pygame.image.load(fullname)
        return image

    # ~~~~~~~~~~ Blit Text on Base Surface ~~~~~~~~~~
    def text_on_base_surface(self, text: str, font : pygame.font.Font, color : str = "white", topleft = False, center = False, h_button = False):
        text_surface = font.render(text, True, color)

        if center:
            text_rect = text_surface.get_rect(center=center)
        elif topleft:
            text_rect = text_surface.get_rect(topleft=topleft)

        if h_button:
            self.highlight_button(screen.base_surface, font, text, text_rect)
        else:
            screen.base_surface.blit(text_surface, text_rect)

    # ~~~~~~~~~~ Calculate Physical Damage ~~~~~~~~~~
    def physical_dmg(self, caster, target, scale):
        caster_str = caster.stats["STR"]
        target_def = target.stats["DEF"]
        reduction = 5 * math.log10(target_def) + target_def / 10
        reduction = reduction / 100
        reduction = reduction if reduction > 0 else 0
        damage = scale * caster_str - target_def
        damage = round(damage - reduction * damage)

        return damage

# ====== Instaciation ======
functions = Functions()