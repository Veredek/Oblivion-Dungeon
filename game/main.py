import pygame
pygame.init()
pygame.font.init()
from src.menu import menu
from src.new_game import new_game
import time
time.sleep(0.1)
from src.classes import Screen, GameState

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
MIN_WINDOW_WIDTH = 854
MIN_WINDOW_HEIGHT = 480
FPS = 60
GAME_TITLE = "OBLIVION DUNGEON"

# ====== Main Function ======
def main():
    screen = Screen()
    game_state = GameState(screen)
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state.state == "Menu":
            menu(game_state)

        elif game_state.state == "New Game":
            new_game(game_state)

        elif game_state.state == "Exit Game":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

