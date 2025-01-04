import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Configurações
color = (255, 255, 255)  # Branco
rect_width = 400
rect_height = 200
radius = 20  # Raio do arredondamento
x, y = 200, 150  # Posição do retângulo

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fundo preto

    # Desenha o retângulo principal (com altura reduzida para evitar sobreposição nos cantos superiores)
    pygame.draw.rect(screen, color, (x, y + radius, rect_width, rect_height - radius))

    # Desenha os cantos superiores arredondados
    pygame.draw.circle(screen, color, (x + radius, y + radius), radius)  # Canto superior esquerdo
    pygame.draw.circle(screen, color, (x + rect_width - radius, y + radius), radius)  # Canto superior direito

    # Desenha retângulos "extras" para conectar as bordas arredondadas
    pygame.draw.rect(screen, color, (x + radius, y, rect_width - 2 * radius, radius))  # Parte superior

    pygame.display.flip()

pygame.quit()
