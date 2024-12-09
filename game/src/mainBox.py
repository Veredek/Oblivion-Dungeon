import pygame
import time

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_FONT = pygame.font.SysFont("comicsans", 30)
TEXT_HEIGHT = GAME_FONT.size("Text Sample")[1]
BASE_SURFACE = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
TYPING_SPEED = 50  # Caracteres por segundo
PADDING = 20

# ====== Class Main Box ======
class MainBox:
    def __init__(self):
        self.start_time = time.time()
        self.width = 0.9 * GAME_WIDTH
        self.height = TEXT_HEIGHT * 5 + 2 * PADDING
        self.x = (GAME_WIDTH - self.width) // 2
        self.y = 0.7 * GAME_HEIGHT
        self.skip_text = False

    def draw_box(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "White", (self.x, self.y, self.width, self.height), 3)

    # ------ Função para simular a digitação do texto ------
    def type_text(self, full_text, speed):
        elapsed_time = time.time() - self.start_time
        chars_to_show = int(elapsed_time * speed)
        return full_text[:chars_to_show]

    # ------ Draw Text ------
    def draw_text(self, surface, text, speed=TYPING_SPEED):
        font = GAME_FONT
        if self.skip_text:
            speed = 999999
            self.skip_text = False
        current_text = self.type_text(text,speed)
        words = current_text.split(" ")
        lines = []
        current_line = ""

        # Ajusta o texto
        for word in words:
            if font.size(current_line + word)[0] > (self.width - PADDING):
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line += word + " "
        if current_line:
            lines.append(current_line)

        # Clear Box
        self.draw_box(surface)

        # Renderiza o texto linha por linha
        for i, line in enumerate(lines):
            text_surface = font.render(line.strip(), True, "White")
            surface.blit(text_surface, (self.x + PADDING, self.y + PADDING + i * TEXT_HEIGHT))
