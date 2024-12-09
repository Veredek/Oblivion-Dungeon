while running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen.resize(event)

    # Exemplo de desenho do conteúdo centralizado
    screen.window.fill((0, 0, 0))  # Limpa a tela com fundo preto
    content_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    content_surface.fill((255, 0, 0))  # Exemplo de um conteúdo (fundo vermelho)

    # Aplica a escala
    scaled_surface = pygame.transform.scale(content_surface, (screen.window_width, screen.window_height))
    screen.window.blit(scaled_surface, (screen.offset_x, screen.offset_y))

    pygame.display.flip()
