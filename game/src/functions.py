import pygame
import os
from functools import wraps
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state, hud

# ========== Functions ==========
# ~~~~~~~~~~ Test for basic events ~~~~~~~~~~
def basic_events(self, event):
    # region ----|1|---- Quit
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    # endregion -|1|-

    # region ----|1|---- Video Resize
    elif event.type == pygame.VIDEORESIZE:
        if event.size != screen.display_size:
            if screen.fullscreen == False:
                print("*Video Resize*"
                        f"    Event Size:{event.size}," +
                        f"    Display Size:{screen.display_size}\n")
                screen.resize(event)
    # endregion -|1|-

    # region ----|1|---- Keydown
    elif event.type == pygame.KEYDOWN:
        print("*Keydown*")
        if event.key == pygame.K_F11:
            print("    F11\n")
            screen.toggle_fullscreen()

        elif event.key == pygame.K_ESCAPE:
            print("    Esc\n")
            if game_state.state != "MENU":
                print("-> Menu <-")
                hud.esc_menu()
    # endregion -|1|-

    return None

# ~~~~~~~~~~ Load Image ~~~~~~~~~~
def load_image(self, name: str):
    fullname = os.path.join("game", "assets", "images", f"{name}.png")
    image = pygame.image.load(fullname)
    return image

# ~~~~~~~~~~ Measure Function Time ~~~~~~~~~~
def timefn(fn):
    '''(Decorator): Measures function time of operation'''
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1} seconds")
        return result

    return measure_time
