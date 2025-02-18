import pygame

# ========== Tree ==========
from src.config import config

# ========== Local Variables ==========
    # --- Left Empty ---   

# ========== Functions ==========
    # --- Left Empty ---

# ========== (classes) ==========
# ~~~~~~~~~~ Screen ~~~~~~~~~~
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.maximized = False

        self.display_size = config.screen_size
        self.display = pygame.display.set_mode(self.display_size, pygame.FULLSCREEN)
        pygame.display.set_caption(config.GAME_TITLE)
        pygame.display.flip()

        self.base_surface = pygame.Surface(config.resolution)
        self.alpha_surface = pygame.Surface((config.resolution), pygame.SRCALPHA)        

    # ----|1|---- Properties ----|1|----
    @property
    def offset_x(self):
        return int((self.display_size[0] - config.game_width) / 2)
    
    @property
    def offset_y(self):
        return int((self.display_size[1] - config.game_height) / 2)    

    # ----|1|---- Functions ----|1|----
    def clear_surfaces(self):
        """
        Clears base_surface and alpha surface
        """
        self.base_surface.fill((0,0,0))
        self.alpha_surface.fill((0,0,0,0))

    def update_display(self):
        if config.display_update:
            flag = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

            self.display = pygame.display.set_mode(self.display_size, flag)
            self.base_surface = pygame.Surface(config.resolution)
            self.alpha_surface = pygame.Surface(config.resolution, pygame.SRCALPHA)
            
            pygame.display.flip()
            
            config.display_update = False

            print(f"*Display Update*" + 
                f"    Resolution: {config.resolution}" +
                f"    Display: {self.display_size}\n")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        print("*Toggle Fullscreen*" +
              f"    Fullscreen: {self.fullscreen}\n")

        # ----|1|---- Config Update + Display Resize ----|1|----
        if self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width, config.game_height = config.max_resolution

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.screen_size          

        elif not self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width, config.game_height = config.min_resolution

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.min_resolution
            
        # ----|1|---- Display Update ----|1|----
        config.display_update = True
        self.update_display()

    def resize(self, event : pygame.event):
        if self.display_size != event.size:
            event_width, event_height = event.size

            # ----|1|---- Maximizing ----|1|----
            if event_width == config.screen_size[0]:
                self.maximized = True

                # ----|2|---- Config Update + Display Resize ----|2|----
                if config.base_of_proportion == "width":
                    config.game_width = event_width
                elif config.base_of_proportion == "height":
                    config.game_height = event_height
                self.display_size = event.size

                print("*Maximizing*\n")

            # ----|1|---- Unmaximizing ----|1|----
            elif self.maximized:
                self.maximized = False
                
                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_width, config.game_height = config.min_resolution
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

    def blit_surface(self, surface: pygame.Surface):
        self.display.blit(surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()    

screen = Screen()

# ~~~~~~~~~~ GameState ~~~~~~~~~~
class GameState:
    def __init__(self): 
        self.state = "MENU"
        '''
        All Uppercase
        '''
        self.ongame_state = "menu"
        '''
        All Lowercase
        '''
        self.current_text = 0
        self.player_name = ""
        self.room = 0

game_state = GameState()