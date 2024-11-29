import pygame
import time
import random
pygame.init()
pygame.font.init()

# ====== mainBox Sizes ======
mainBox_SIZE = (900, 200)
mainBox_START = (50,550)
mainBox_THICKNESS = 8

# ====== GameState ======
class GameState:
    def __init__(self):
        self.Fullscreen = False
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH - 100, self.SCREEN_HEIGHT - 100), pygame.RESIZABLE)
        pygame.display.set_caption("Game Name")
        self.FONT = pygame.font.SysFont("comicsans", 30)
        
    def toggle_fullscreen(self):
        if self.Fullscreen:
            self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH - 100, self.SCREEN_HEIGHT - 100))
            self.Fullscreen = False
        else:
            self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
            self.Fullscreen = True
        pygame.display.flip()

game_state = GameState()

from src.menu import menu
#from src.mainBox import draw_mainbox
        
def main():
    #WIN.blit(BG, (0, 0))
    run = True

    #clock = pygame.time.Clock()

    #draw_mainbox(WIN, mainBox_START, mainBox_SIZE, mainBox_THICKNESS)

    choice = menu(game_state)

    if choice != "":
        pass

    while run:
        #clock.tick(60)
        print("ok")
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                run = False
                break

            # Posição do mouse e Highlight
            mouse_pos = pygame.mouse.get_pos()  # Posição atual do mouse

            # Verifica se F11 foi pressionado
            if event.type == pygame.KEYDOWN:
                print("KEYDOWN")
                if event.key == pygame.K_F11:
                    print("F11")
                    game_state.toggle_fullscreen()

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_UP]:

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

exit()