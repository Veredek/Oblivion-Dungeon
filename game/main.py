import pygame
pygame.init()
pygame.font.init()
from src.menu import menu
from src.new_game import new_game
import time
time.sleep(0.1)
from src.classes import Screen, GameState

# ====== Main Function ======
def main():
    screen = Screen()
    game_state = GameState(screen)
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state.state == "MENU":
            menu(game_state)

        elif game_state.state == "NEW GAME":
            new_game(game_state)

        elif game_state.state == "EXIT GAME":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

