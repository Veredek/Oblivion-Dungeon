import pygame
import time

pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((1900, 1000))
clock = pygame.time.Clock()

# Carregar imagem do inimigo com fundo transparente
enemy_image = pygame.image.load("C:\\Users\\Hugo\\.vscode\\game\\assets\\images\\Slime.png").convert_alpha()

# Função para criar o efeito de "piscar"
def flash_enemy(image, flash_color=(255, 255, 255), alpha=0):
    # Cria uma cópia da imagem original
    flashed = image.copy()
    # Cria uma superfície branca semi-transparente
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill((*flash_color, alpha))
    # Sobrepõe a superfície branca na imagem
    flashed.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return flashed

# Loop principal
running = True
flashing = False
flash_timer = 0
enemy_pos = (300, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simula o início de uma animação de dano
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Pressione espaço para começar o flash
        flashing = True
        flash_timer = time.time()

    # Lógica para intercalar entre imagem normal e "branca"
    if flashing:
        elapsed = time.time() - flash_timer
        if int(elapsed * 100) % 2 == 0:  # Pisca alternando a cada 0.1s
            enemy_display = flash_enemy(enemy_image)
        else:
            enemy_display = enemy_image

        # Parar o piscar após 1 segundo
        if elapsed > 1:
            flashing = False
    else:
        enemy_display = enemy_image

    # Renderização
    screen.fill((0, 0, 0))
    screen.blit(enemy_display, enemy_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
