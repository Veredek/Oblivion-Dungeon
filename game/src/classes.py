import pygame

# ========== Tree ==========
from src.config import config

# ========== (classes) ==========
# ~~~~~~~~~~ Screen ~~~~~~~~~~
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.maximized = False

        self.display_size = config.SCREEN_SIZE
        self.display = pygame.display.set_mode(self.display_size, pygame.FULLSCREEN)
        pygame.display.set_caption(config.GAME_TITLE)
        pygame.display.flip()

        self.base_surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)        

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # region ----|1|---- Offset x
    @property
    def offset_x(self):
        return int((self.display_size[0] - config.game_width) / 2)
        # endregion
    # region ----|1|---- Offset y
    @property
    def offset_y(self):
        return int((self.display_size[1] - config.game_height) / 2)    
        # endregion
    # region ----|1|---- Display Width
    @property
    def width(self):
        return self.display_size[0]
        # endregion
    # region ----|1|---- Display Height
    @property
    def height(self):
        return self.display_size[1]
        # endregion
    # region ----|1|---- Mouse Position
    @property
    def mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = (mouse_pos[0]) / config.scale, (mouse_pos[1]) / config.scale

        return (mouse_x - self.offset_x, mouse_y - self.offset_y)
        # endregion
    
    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # region ----|1|---- Clear Surfaces
    def clear_surfaces(self):
        """
        Clears base_surface and alpha surface
        """
        self.base_surface.fill((0,0,0))
        # endregion
    # region ----|1|---- Update Display
    def update_display(self):
        if config.display_update:
            flag = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

            self.display = pygame.display.set_mode(self.display_size, flag)
            
            pygame.display.flip()
            
            config.display_update = False

            print(f"*Display Update*" + 
                f"    Resolution: {config.resolution}" +
                f"    Display: {self.display_size}\n")
        # endregion
    # region ----|1|---- Toggle Fullscreen
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        print("*Toggle Fullscreen*" +
              f"    Fullscreen: {self.fullscreen}\n")

        # ----|1|---- Config Update + Display Resize ----|1|----
        if self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width, config.game_height = config.MAX_RESOLUTION

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.SCREEN_SIZE          

        elif not self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width = (config.min_resolution[0], "only")
            config.game_height = (config.min_resolution[1], "only")

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.min_resolution
            
        # ----|1|---- Display Update ----|1|----
        config.display_update = True
        self.update_display()
        # endregion
    # region ----|1|---- Resize Display
    def resize(self, event : pygame.event):
        if self.display_size != event.size:
            event_width, event_height = event.size

            # ----|1|---- Maximizing ----|1|----
            if event_width == config.SCREEN_SIZE[0]:
                self.maximized = True

                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_height = event_height
                self.display_size = event.size

                print("*Maximizing*\n")

            # ----|1|---- Unmaximizing ----|1|----
            elif self.maximized:
                self.maximized = False
                
                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_width = (config.min_resolution[0], "only")
                config.game_height = (config.min_resolution[1], "only")
                self.display_size = config.min_resolution

                print("*Unmaximizing*\n")

            # ----|1|---- Resizing ----|1|----
            else:
                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_width = event_width
                self.display_size = config.resolution

                print("*Resizing*\n")

            # ----|1|---- Display Update ----|1|----
            config.display_update = True
            self.update_display()
        # endregion
    # region ----|1|---- Blit Surface On Display
    def blit_surface(self, surface: pygame.Surface):
        scaled_surface = pygame.transform.scale(surface, (config.game_width, config.game_height))
        self.display.blit(scaled_surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()
        # endregion

screen = Screen()

# ~~~~~~~~~~ GameState ~~~~~~~~~~
class GameState:
    def __init__(self): 
        self.state = "MENU" # ALL UPPERCASE
        self.ongame_state = "menu" # ALL LOWERCASE
        self.current_text = 0
        self.player_name = ""
        self.room = 0

game_state = GameState()