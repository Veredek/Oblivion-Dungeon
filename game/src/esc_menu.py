import pygame

# ====== Global Variables ======
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
GAME_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)

# ====== Definitions ======
# ------ Highlight Button ------
def special_highlight(surface, font, text, text_rect,mouse_pos):
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

# ====== Esc Menu ======
class EscMenu():

    def __init__(self):
        self.inside = False
        self.continue_text = GAME_FONT.render("Continue", True, "White")
        self.continue_text_rect = self.continue_text.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 80))
        self.quit_text = GAME_FONT.render("Quit", True, "White")
        self.quit_text_rect = self.quit_text.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40))

    def esc(self, surface, mouse_pos):
        special_highlight(surface, GAME_FONT, "Continue", self.continue_text_rect, mouse_pos)
        special_highlight(surface, GAME_FONT, "Quit", self.quit_text_rect, mouse_pos)
        return 
    
    def mouse_over(self, mouse_pos):
        if self.continue_text_rect.collidepoint(mouse_pos):
            return "continue"
        elif self.quit_text_rect.collidepoint(mouse_pos):
            return "quit"
        
        return