import pygame
import time
from src.mainBox import MainBox

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_FONT = pygame.font.SysFont("comicsans", 30)
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
TYPING_SPEED = 50  # Caracteres por segundo

# ====== Código Principal ======
def new_game(game_state):
    running = True
    choice = ""
    clock = pygame.time.Clock()
    start_time = time.time()
    main_box = MainBox()

    starting_text = "Você acorda em um lugar estranho, você não se lembra de muita coisa, então não sabe se já esteve aqui antes..."
    while running:
        game_state.screen.window.fill(0)

        # ------ Definindo Variáveis ------
        if game_state.screen.fullscreen:
            scale = game_state.screen.fullscreen_scale
            window_width, window_height = game_state.screen.screen_width, game_state.screen.screen_height
        else:
            scale = game_state.screen.window_scale
            window_width, window_height = game_state.screen.window_width, game_state.screen.window_height
        mouse_pos = pygame.mouse.get_pos()
        size = (window_width,window_height)
        elapsed_time = (time.time() - start_time)

        # ------ Escalonando ------
        offset_x = (window_width - GAME_WIDTH * scale) // 2
        offset_y = (window_height - GAME_HEIGHT * scale) // 2
        mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale)

        #

        # ------ Base Surface Blit ------
        main_box.draw_text(BASE_SURFACE, starting_text)

        # ------ Window Blit ------
        scaled_surface = pygame.transform.scale(BASE_SURFACE, (int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale)))
        game_state.screen.window.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

        clock.tick(60)

        # ------ Detectando Eventos ------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Detecta eventos de redimensionamento
            elif event.type == pygame.VIDEORESIZE:
                if event.size != size:
                    print(f"Event Size:{event.size},\nWindow Size:{size}\n")
                    if game_state.screen.fullscreen == False:
                        game_state.screen.resize(event)
                        break
                    size = event.size

            # Detecta Click Esquerdo do Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
            # Verifica se F11 foi pressionado
            elif event.type == pygame.KEYDOWN:
                print("\nKEYDOWN")
                if event.key == pygame.K_F11:
                    print("\nF11")
                    game_state.screen.toggle_fullscreen()
                if event.key == pygame.K_RETURN or event.key == pygame.K_x:
                    print("\nIn")
                    main_box.skip_text = True


    return choice