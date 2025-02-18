import pygame
pygame.init()
pygame.font.init()
import time
time.sleep(0.1)

# ========= Tree =========
from src.config import config
from src.classes import screen, game_state
from src.menu import menu
from src.new_game import new_game

# ========== Local Variables ==========
    # --- Left Empty ---

# ========= (main) =========
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

