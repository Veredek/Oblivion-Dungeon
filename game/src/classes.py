import pygame
pygame.init()
pygame.font.init()

# ====== Global Variables ======
from src.variables import GAME_TITLE
from src.variables import GAME_WIDTH, GAME_HEIGHT, MIN_WINDOW_SIZE, MONITOR_SIZE, RESOLUTION_SCALE
from src.variables import BASE_SURFACE, TRANSPARENT_SURFACE

# ====== Definitions ======

# ====== Class Screen ======
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.maximized = False

        self.fullscreen_height = MONITOR_SIZE[1]

        self.fullscreen_scale = min(MONITOR_SIZE[0] / GAME_WIDTH, self.fullscreen_height / GAME_HEIGHT)
        self.window_scale = 0.5
        self.scale = self.fullscreen_scale

        self.window_width = self.window_scale * GAME_WIDTH
        self.window_height = self.window_scale * GAME_HEIGHT

        self.size = (MONITOR_SIZE[0], self.fullscreen_height)

        self.offset_x = (MONITOR_SIZE[0] - GAME_WIDTH * self.scale) // 2
        self.offset_y = (self.fullscreen_height - GAME_HEIGHT * self.scale) // 2

        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

        self.screen = pygame.display.set_mode((MONITOR_SIZE[0], self.fullscreen_height), pygame.FULLSCREEN)
        pygame.display.set_caption(GAME_TITLE)

    def get_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale,
                     (mouse_pos[1] - self.offset_y) / self.scale)        
        return mouse_pos
    
    def resize_surfaces(self):
        global GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE, TRANSPARENT_SURFACE, RESOLUTION_SCALE

        GAME_WIDTH, GAME_HEIGHT = self.scale * GAME_WIDTH, self.scale * GAME_HEIGHT
        RESOLUTION_SCALE = GAME_HEIGHT / 1080

        BASE_SURFACE = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        TRANSPARENT_SURFACE = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        if self.fullscreen:
            self.screen = pygame.display.set_mode((MONITOR_SIZE[0], self.fullscreen_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        print(f"Game resized: ({GAME_WIDTH},{GAME_HEIGHT})")

        return None

    def toggle_fullscreen(self):
        global GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE, RESOLUTION_SCALE
        mouse_pos = pygame.mouse.get_pos()

        if self.fullscreen:

            self.fullscreen = False
            # ------ Atualizando Variáveis Internas 
            self.scale = self.window_scale 
            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2
            self.size = (self.window_width, self.window_height)
            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

            # ------ Resize Surfaces ------
            self.resize_surfaces()

        else:
            self.fullscreen = True
            # ------ Atualizando Variáveis Internas
            self.scale = self.fullscreen_scale
            self.offset_x = (MONITOR_SIZE[0] - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.fullscreen_height - GAME_HEIGHT * self.scale) // 2
            self.size = (MONITOR_SIZE[0], self.fullscreen_height)
            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

            # ------ Resize Surfaces ------
            self.resize_surfaces()

        # ------ Atualizando Tela ------
        pygame.display.flip()
        print(f"(toggle) Fullscreen: {self.fullscreen}\n")

    def resize(self, event):
        event_width, event_height = event.size
        proportion = 1
        mouse_pos = pygame.mouse.get_pos()
        print(f"Maximized: {self.maximized}")

        # ------ Maximizando Tela ------
        if event_width == MONITOR_SIZE[0] and not self.fullscreen:
            self.maximized = True

            self.window_width = event_width
            self.window_height = event_height
            self.size = (self.window_width, self.window_height)

            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.scale = self.window_scale

            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2

            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)
            
            print("Maximizando")

        # ------ Desmaximizando Tela ------
        elif self.maximized:
            self.maximized = False

            self.window_width = MIN_WINDOW_SIZE[0]
            self.window_height = MIN_WINDOW_SIZE[1]
            self.size = (self.window_width, self.window_height)

            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.scale = self.window_scale

            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2

            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)
            
            print("Desmaximizando")

        # ------ Tela Não Maximizada ------
        else:
            if event_width < self.window_width or event_height < self.window_height:
                proportion = min(event_width / self.window_width, event_height / self.window_height)
            elif event_width > self.window_width or event_height > self.window_height:
                proportion = max(event_width / self.window_width, event_height / self.window_height)

            self.window_width = int(proportion * self.window_width)
            self.window_height = int(proportion * self.window_height)

            # Checando tamanho mínimo de Tela
            if self.window_width < MIN_WINDOW_SIZE[0] or self.window_height < MIN_WINDOW_SIZE[1]:
                self.window_width, self.window_height = MIN_WINDOW_SIZE[0], MIN_WINDOW_SIZE[1]

            # Redefinindo Variáveis Internas
            self.size = (self.window_width, self.window_height)

            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.scale = self.window_scale

            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2

            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)                

            print("Normal resize")

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.flip()
        print(f"New resolution: {self.window_width}x{self.window_height}")
        print(f"Maximized: {self.maximized}\n")

screen = Screen()

# ====== Class GameState ======
class GameState:
    def __init__(self, screen): 
        self.screen = screen
        self.state = "MENU"
        self.ongame_state = "menu"
        self.current_text = 0
        self.player_name = ""
        self.room = 0

game_state = GameState(screen)