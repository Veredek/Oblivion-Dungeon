import pygame
import time

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080

GAME_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
GAME_FONT_HEIGHT = GAME_FONT.size("Text Sample")[1]
TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 45)
TEXT_HEIGHT = TEXT_FONT.size("Text Sample")[1]

TYPING_SPEED = 50  # Caracteres por segundo
PADDING = 20
HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)

MAIN_BOX_SIZE = (0.9 * GAME_WIDTH, TEXT_HEIGHT * 4 + 2 * PADDING)
MAIN_BOX_POS = ((GAME_WIDTH - MAIN_BOX_SIZE[0]) // 2, 0.7 * GAME_HEIGHT)

MINOR_BOX_DISTANCE = 0.5 * (GAME_HEIGHT - MAIN_BOX_POS[1] - MAIN_BOX_SIZE[1])
MINOR_BOX_SIZE = ((MAIN_BOX_SIZE[0] - 2 * MINOR_BOX_DISTANCE) // 3, GAME_HEIGHT - MAIN_BOX_SIZE[1] - 4 * MINOR_BOX_DISTANCE)
MINOR_BOX_TITLE_HEIGHT = MINOR_BOX_DISTANCE + 1.5 * GAME_FONT_HEIGHT + PADDING

INVENTORY_POS = (MAIN_BOX_POS[0], MINOR_BOX_DISTANCE)
EQUIPS_POS = (MAIN_BOX_POS[0] + MINOR_BOX_SIZE[0] + MINOR_BOX_DISTANCE, MINOR_BOX_DISTANCE)
STATS_POS = (MAIN_BOX_POS[0] + 2 * MINOR_BOX_SIZE[0] + 2 * MINOR_BOX_DISTANCE, MINOR_BOX_DISTANCE)

# ====== Definitions ======
# ------ Highlight Button ------
def highlight(surface, font, text, text_rect,mouse_pos):
    if text_rect.collidepoint(mouse_pos):
        text_surface = font.render(text, True, "Yellow")
        sign_surface = HIGHLIGHT_SIGN.render("+", True, "Yellow")
        text_size = text_surface.get_size()
        sign_size = sign_surface.get_size()
        highlight_surface = pygame.Surface((text_size[0] + 2 * sign_size[0] + 10, text_size[1] if text_size[1] > sign_size[1] else sign_size[1]))
        highlight_surface.blit(sign_surface, (0, (text_size[1] - sign_size[1]) // 2))
        highlight_surface.blit(text_surface, (sign_size[0] + 5, 0))
        highlight_surface.blit(sign_surface, (sign_size[0] + text_size[0] + 10, (text_size[1] - sign_size[1]) // 2))
        surface.blit(highlight_surface, (text_rect[0] - sign_size[0] - 5, text_rect[1]))
    else:
        normal_surface = font.render(text, True, "White")
        surface.blit(normal_surface, text_rect)

# ====== Class Main Box ======
class Boxes:
    def __init__(self, pos = (MAIN_BOX_POS[0], MAIN_BOX_POS[1]), size = (MAIN_BOX_SIZE[0], MAIN_BOX_SIZE[1])):
        self.time = time.time()
        self.width = size[0]
        self.height = size[1]
        self.x = pos[0]
        self.y = pos[1]
        self.skip_text = False
        self.waiting = False

    def draw_mainbox(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "White", (self.x, self.y, self.width, self.height), 3, 10)

    # ------ Função para simular a digitação do texto ------
    def type_text(self, full_text, speed):
        if self.skip_text:
            return full_text
        else:
            elapsed_time = time.time() - self.time
            chars_to_show = int(elapsed_time * speed)
            return full_text[:chars_to_show]

    # ------ Draw Text ------
    def draw_text(self, surface, script, speed=TYPING_SPEED):
        text = script.script()
        font = TEXT_FONT
        current_text = self.type_text(text,speed)
        if current_text == text:
            self.waiting = True
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
        self.draw_mainbox(surface)

        # Renderiza o texto linha por linha
        for i, line in enumerate(lines):
            text_surface = font.render(line.strip(), True, "White")
            surface.blit(text_surface, (self.x + PADDING, self.y + PADDING + i * TEXT_HEIGHT))

    # ------ After Box ------
    def after_box(self, surface, mouse_pos, speed=TYPING_SPEED):
        # Clear Box
        self.draw_mainbox(surface)
        font = GAME_FONT

        # ------ Texts ------
        proceed_text = font.render("Proceed", True, "White")
        inventory_text = font.render("Inventory", True, "White")

        # ------ Rectangles ------
        proceed_text_rect = proceed_text.get_rect(center=(int(GAME_WIDTH * (1/3)), self.y + self.height // 2))
        inventory_text_rect = inventory_text.get_rect(center=(int(GAME_WIDTH * (2/3)), self.y + self.height // 2))

        # ------ Base Surface Blit ------
        highlight(surface, font, "Proceed", proceed_text_rect, mouse_pos)
        highlight(surface, font, "Inventory", inventory_text_rect, mouse_pos)

        # ------ Inventory Click ------
        if inventory_text_rect.collidepoint(mouse_pos):
            return "inventory"

    def inventory_box(self, surface):
        pygame.draw.rect(surface, "White", (INVENTORY_POS[0], INVENTORY_POS[1], MINOR_BOX_SIZE[0], MINOR_BOX_SIZE[1]), 3, 10)
        inventory_text = GAME_FONT.render("Inventory", True, "White")
        inventory_text_rect = inventory_text.get_rect(center=(INVENTORY_POS[0] + MINOR_BOX_SIZE[0] // 2, INVENTORY_POS[1] + GAME_FONT.size("Text Sample")[1]))
        surface.blit(inventory_text, inventory_text_rect)
        pygame.draw.line(surface, "White", (INVENTORY_POS[0], MINOR_BOX_TITLE_HEIGHT), (INVENTORY_POS[0] + MINOR_BOX_SIZE[0] - 3, MINOR_BOX_TITLE_HEIGHT), 3)

    def equips_box(self, surface):
        pygame.draw.rect(surface, "White", (EQUIPS_POS[0], EQUIPS_POS[1], MINOR_BOX_SIZE[0], MINOR_BOX_SIZE[1]), 3, 10)
        equips_text = GAME_FONT.render("Equips", True, "White")
        equips_text_rect = equips_text.get_rect(center=(EQUIPS_POS[0] + MINOR_BOX_SIZE[0] // 2, EQUIPS_POS[1] + GAME_FONT.size("Text Sample")[1]))
        surface.blit(equips_text, equips_text_rect)
        pygame.draw.line(surface, "White", (EQUIPS_POS[0], EQUIPS_POS[1] + 1.5 * GAME_FONT_HEIGHT + PADDING), (EQUIPS_POS[0] + MINOR_BOX_SIZE[0] - 3, EQUIPS_POS[1] + 1.5 * GAME_FONT_HEIGHT + PADDING), 3)

    def stats_box(self, surface):
        pygame.draw.rect(surface, "White", (STATS_POS[0], STATS_POS[1], MINOR_BOX_SIZE[0], MINOR_BOX_SIZE[1]), 3, 10)
        stats_text = GAME_FONT.render("Stats", True, "White")
        stats_text_rect = stats_text.get_rect(center=(STATS_POS[0] + MINOR_BOX_SIZE[0] // 2, STATS_POS[1] + GAME_FONT.size("Text Sample")[1]))
        surface.blit(stats_text, stats_text_rect)
        pygame.draw.line(surface, "White", (STATS_POS[0], STATS_POS[1] + 1.5 * GAME_FONT_HEIGHT + PADDING), (STATS_POS[0] + MINOR_BOX_SIZE[0] - 3, STATS_POS[1] + 1.5 * GAME_FONT_HEIGHT + PADDING), 3)

