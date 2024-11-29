import pygame

def menu(game_state):
    GameName_FONT = pygame.font.SysFont("Arial", 180)
    FONT = game_state.FONT
    WIN = game_state.WIN
    
    game_state.WIN.fill(0)
    window_width, window_height = pygame.display.get_window_size()
    center = window_width // 2

    # Textos e retângulos
    GameNameText = GameName_FONT.render("GAME NAME", True, "White")
    NewGameText = FONT.render("NEW GAME", True, "White")
    LoadText = FONT.render("LOAD", True, "White")
    ExitText = FONT.render("EXIT", True, "White")

    GameNameText_rect = GameNameText.get_rect(center=(center, 180))
    NewGameText_rect = NewGameText.get_rect(center=(center, 350))
    LoadText_rect = LoadText.get_rect(center=(center, 400))
    ExitText_rect = ExitText.get_rect(center=(center, 450))

    running = True
    choice = ""

    while running:
        WIN.fill(0)  # Redesenha o fundo
        mouse_pos = pygame.mouse.get_pos()  # Posição atual do mouse

        # Renderizar textos com destaque nos botões
        WIN.blit(GameNameText, GameNameText_rect)

        NewGameText_hover = FONT.render("NEW GAME", True, "Yellow" if NewGameText_rect.collidepoint(mouse_pos) else "White")
        LoadText_hover = FONT.render("LOAD", True, "Yellow" if LoadText_rect.collidepoint(mouse_pos) else "White")
        ExitText_hover = FONT.render("EXIT", True, "Yellow" if ExitText_rect.collidepoint(mouse_pos) else "White")

        WIN.blit(NewGameText_hover, NewGameText_rect)
        WIN.blit(LoadText_hover, LoadText_rect)
        WIN.blit(ExitText_hover, ExitText_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if NewGameText_rect.collidepoint(mouse_pos):
                    choice = "New Game"
                    running = False
                elif LoadText_rect.collidepoint(mouse_pos):
                    choice = "Load Game"
                    print("Load Game")
                    running = False
                elif ExitText_rect.collidepoint(mouse_pos):
                    choice = "Exit Game"
                    pygame.quit()
                    exit()
            
            # Verifica se F11 foi pressionado
            if event.type == pygame.KEYDOWN:
                print("KEYDOWN")
                if event.key == pygame.K_F11:
                    print("F11")
                    game_state.toggle_fullscreen()

    return choice
