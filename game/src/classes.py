import pygame
pygame.init()
pygame.font.init()

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
MIN_WINDOW_WIDTH = 854
MIN_WINDOW_HEIGHT = 480
FPS = 60
GAME_TITLE = "OBLIVION DUNGEON"

# ====== Class Screen ======
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.maximized = False

        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        self.fullscreen_scale = min(self.screen_width / GAME_WIDTH, self.screen_height / GAME_HEIGHT)
        self.window_scale = 0.5
        self.scale = self.fullscreen_scale

        self.window_width = self.window_scale * GAME_WIDTH
        self.window_height = self.window_scale * GAME_HEIGHT

        self.size = (self.screen_width, self.screen_height)

        self.offset_x = (self.screen_width - GAME_WIDTH * self.scale) // 2
        self.offset_y = (self.screen_height - GAME_HEIGHT * self.scale) // 2

        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption(GAME_TITLE)

    def get_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)        
        return mouse_pos

    def toggle_fullscreen(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.fullscreen:
            self.fullscreen = False
            # ------ Atualizando Variáveis Internas
            self.scale = self.window_scale
            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2
            self.size = (self.window_width, self.window_height)
            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

            # ------ Set Mode ------
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        else:
            self.fullscreen = True
            # ------ Atualizando Variáveis Internas
            self.scale = self.fullscreen_scale
            self.offset_x = (self.screen_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.screen_height - GAME_HEIGHT * self.scale) // 2
            self.size = (self.screen_width, self.screen_height)
            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)

            # ------ Set Mode ------
            self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

        # ------ Atualizando Tela ------
        pygame.display.flip()
        print(f"(toggle) Fullscreen: {self.fullscreen}\n")

    def resize(self, event):
        event_width, event_height = event.size
        proportion = 1
        mouse_pos = pygame.mouse.get_pos()
        print(f"Maximized: {self.maximized}")

        # ------ Maximizando Tela ------
        if event_width == self.screen_width and not self.fullscreen:
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

            self.window_width = MIN_WINDOW_WIDTH
            self.window_height = MIN_WINDOW_HEIGHT
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
            if self.window_width < MIN_WINDOW_WIDTH or self.window_height < MIN_WINDOW_HEIGHT:
                self.window_width, self.window_height = MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT

            # Redefinindo Variáveis Internas
            self.size = (self.window_width, self.window_height)

            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.scale = self.window_scale

            self.offset_x = (self.window_width - GAME_WIDTH * self.scale) // 2
            self.offset_y = (self.window_height - GAME_HEIGHT * self.scale) // 2

            self.mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)                

            print("Normal resize")

        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.flip()
        print(f"New resolution: {self.window_width}x{self.window_height}")
        print(f"Maximized: {self.maximized}\n")

# ====== Class GameState ======
class GameState:
    def __init__(self, screen): 
        self.screen = screen
        self.state = "MENU"
        self.ongame_state = "menu"
        self.current_text = 0
        self.player_name = ""
        self.room = 0
