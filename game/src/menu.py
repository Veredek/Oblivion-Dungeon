import pygame

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_TITLE = "DUNGEON"
GAME_NAME_FONT = pygame.font.Font(r"game\src\fonts\OldLondon.ttf",300)
GAME_FONT = pygame.font.SysFont("comicsans", 30)

def menu(game_state):
    running = True
    choice = ""
    while running:
        game_state.screen.window.fill(0)

        # ------ Definindo Variáveis ------
        base_surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        if game_state.screen.fullscreen:
            scale = game_state.screen.fullscreen_scale
            window_width, window_height = game_state.screen.screen_width, game_state.screen.screen_height
        else:
            scale = game_state.screen.window_scale
            window_width, window_height = game_state.screen.window_width, game_state.screen.window_height
        mouse_pos = pygame.mouse.get_pos()
        size = (window_width,window_height)

        # ------ Escalonando ------
        offset_x = (window_width - GAME_WIDTH * scale) // 2
        offset_y = (window_height - GAME_HEIGHT * scale) // 2
        mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale)

        # ------ Textos e retângulos ------
        GameNameText = GAME_NAME_FONT.render(GAME_TITLE, True, "White")
        NewGameText = GAME_FONT.render("NEW GAME", True, "White")
        LoadText = GAME_FONT.render("LOAD", True, "White")
        ExitText = GAME_FONT.render("EXIT", True, "White")

        GameNameText_rect = GameNameText.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 5))
        NewGameText_rect = NewGameText.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4))
        LoadText_rect = LoadText.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 60))
        ExitText_rect = ExitText.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2.4 + 120))

        # ------ Highlight Buttons ------
        NewGameText_hover = GAME_FONT.render("NEW GAME", True, "Yellow" if NewGameText_rect.collidepoint(mouse_pos) else "White")
        LoadText_hover = GAME_FONT.render("LOAD", True, "Yellow" if LoadText_rect.collidepoint(mouse_pos) else "White")
        ExitText_hover = GAME_FONT.render("EXIT", True, "Yellow" if ExitText_rect.collidepoint(mouse_pos) else "White")

        # ------ Base Surface Blit ------
        base_surface.blit(GameNameText, GameNameText_rect)
        base_surface.blit(NewGameText_hover, NewGameText_rect)
        base_surface.blit(LoadText_hover, LoadText_rect)
        base_surface.blit(ExitText_hover, ExitText_rect)

        # ------ Window Blit ------
        scaled_surface = pygame.transform.scale(base_surface, (int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale)))
        game_state.screen.window.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

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
                if NewGameText_rect.collidepoint(mouse_pos):
                    choice = "New Game"
                    print(f"{choice}\n")
                    running = False
                elif LoadText_rect.collidepoint(mouse_pos):
                    choice = "Load Game"
                    print(f"{choice}\n")
                    running = False
                elif ExitText_rect.collidepoint(mouse_pos):
                    choice = "Exit Game"
                    print(f"{choice}\n")
                    running = False
            
            # Verifica se F11 foi pressionado
            elif event.type == pygame.KEYDOWN:
                print("\nKEYDOWN")
                if event.key == pygame.K_F11:
                    print("\nF11")
                    game_state.screen.toggle_fullscreen()

    return choice
