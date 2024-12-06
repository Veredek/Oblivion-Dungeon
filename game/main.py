import pygame
pygame.init()
pygame.font.init()
from src.menu import menu
from src.new_game import new_game

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_TITLE = "DUNGEON"
GAME_FONT = pygame.font.SysFont("comicsans", 30)
FPS = 60
MIN_WINDOW_WIDTH = 854
MIN_WINDOW_HEIGHT = 480

# ====== Class Screen ======
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.fullscreen_scale = min(self.screen_width / GAME_WIDTH, self.screen_height / GAME_HEIGHT)
        self.window_scale = 0.5
        self.window_width = self.window_scale * GAME_WIDTH
        self.window_height = self.window_scale * GAME_HEIGHT
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.maximized = False
        pygame.display.set_caption(GAME_TITLE)

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
            self.fullscreen = True
        pygame.display.flip()

    def resize(self, event):
        event_width, event_height = event.size
        proportion = 1

        # ------ Maximizando Tela ------
        if event_width == self.screen_width:
            self.window_width = event_width
            self.window_height = event_height
            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.maximized = True

        # ------ Desmaximizando Tela ------
        elif self.maximized:
            self.window_width = event_width
            self.window_height = event_height
            self.window_scale = min(self.window_width / GAME_WIDTH, self.window_height / GAME_HEIGHT)
            self.maximized = False

        # ------ Tela Não Maximizada ------
        else:
            if event_width < self.window_width or event_height < self.window_height:
                proportion = min(event_width / self.window_width, event_height / self.window_height)
            elif event_width > self.window_width or event_height > self.window_height:
                proportion = max(event_width / self.window_width, event_height / self.window_height)

            self.window_width = int(proportion * self.window_width)
            self.window_height = int(proportion * self.window_height)

            if self.window_width < MIN_WINDOW_WIDTH or self.window_height < MIN_WINDOW_HEIGHT:
                self.window_width, self.window_height = MIN_WINDOW_WIDTH,MIN_WINDOW_HEIGHT

            self.window_scale = self.window_width / GAME_WIDTH

        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.flip()
        print(f"New resolution: {self.window_width}x{self.window_height}\n")

# ====== Class GameState ======
class GameState:
    def __init__(self, screen): 
        self.screen = screen
        self.state = "menu"

# ====== Main Function ======
def main():
    screen = Screen()
    game_state = GameState(screen)
    running = True

    while running:

        if game_state.state == "menu":
            game_state.state = menu(game_state)

        elif game_state.state == "New Game":
            game_state.state = new_game(game_state)

        elif game_state.state == "Exit Game":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

