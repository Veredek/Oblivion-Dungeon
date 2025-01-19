import pygame
pygame.init()
pygame.font.init()
from src.menu import menu
from src.new_game import new_game
import time
time.sleep(0.1)

# ====== Global Objects ======
from src.classes import screen, game_state

# ====== Main Function ======
def main():
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        if game_state.state == "MENU": menu()

        elif game_state.state == "NEW GAME": new_game()

        elif game_state.state == "EXIT GAME": break

    pygame.quit()

if __name__ == "__main__":
    main()

