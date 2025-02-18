import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions, s

# ====== Global Variables ======

# ========== Functions ==========

# ========== (boxes) ==========
class Boxes:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        self.time = time.time()
        self.skip_text = False
        self.waiting = False

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    @property
    def main_x(self):
        return config.main_box_pos[0]
    
    @property
    def main_y(self):
        return config.main_box_pos[1]

    @property
    def main_w(self):
        return config.main_box_size[0]
    
    @property
    def main_h(self):
        return config.main_box_size[1]
    
    @property
    def minorbox_spacer(self): # Spacer between minor boxes
        spacer = 0.5 * (config.game_height - self.main_y - self.main_h)
        return spacer
    
    @property
    def minorbox_size(self):
        w = (self.main_w - 2 * self.minorbox_spacer) // 3
        h = config.game_height - config.main_box_size[1] - 4 * self.minorbox_spacer
        return (w, h)
    
    @property
    def minorbox_title_height(self):
        return self.minorbox_spacer + 1.5 * config.title_height + config.padding
    
    #----|1|---- Position ----|1|----
    @property
    def inventory_pos(self):
        x = self.main_x
        y = self.minorbox_spacer
        return (x, y)
    
    @property
    def equips_pos(self):
        x = self.main_x + self.minorbox_size[0] + self.minorbox_spacer
        y = self.minorbox_spacer
        return (x, y)
    
    @property
    def stats_pos(self):
        x = self.main_x + 2 * self.minorbox_size[0] + 2 * self.minorbox_spacer
        y = self.minorbox_spacer
        return (x, y)
    
    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    def draw_mainbox(self):
        pygame.draw.rect(screen.base_surface, (0, 0, 0), (self.main_x, self.main_y, self.main_w, self.main_h))
        pygame.draw.rect(screen.base_surface, "White", (self.main_x, self.main_y, self.main_w, self.main_h), s(3), s(10))

    # ----|1|---- Text Part to Show ----|1|----
    def type_text(self, full_text, speed):
        if self.skip_text:
            return full_text
        else:
            elapsed_time = time.time() - self.time
            chars_to_show = int(elapsed_time * speed)
            return full_text[:chars_to_show]

    # ----|1|---- Draw Text ----|1|----
    def draw_text(self, script, surface=screen.base_surface, speed=config.TYPING_SPEED):
        text = script.script()
        font = config.text_font
        current_text = self.type_text(text,speed)
        if current_text == text:
            self.waiting = True
        words = current_text.split(" ")
        lines = []
        current_line = ""

        # Ajusta o texto
        for word in words:
            if font.size(current_line + word)[0] > (self.main_w - config.padding):
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line += word + " "
        if current_line:
            lines.append(current_line)

        # Clear Box
        self.draw_mainbox()

        # Renderiza o texto linha por linha
        for i, line in enumerate(lines):
            text_surface = font.render(line.strip(), True, "White")
            surface.blit(text_surface, (self.main_x + config.padding, self.main_y + config.padding + i * config.text_height))

    # ------ After Box ------
    def after_box(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        # ------ Local Variables ------
        font = config.title_font

        # ------ Clear Box ------
        self.draw_mainbox()

        # ------ Texts ------
        proceed_text = font.render("Proceed", True, "White")
        inventory_text = font.render("Inventory", True, "White")

        # ------ Rectangles ------
        proceed_text_rect = proceed_text.get_rect(center=(int(config.game_width * (1/3)), self.main_y + self.main_h // 2))
        inventory_text_rect = inventory_text.get_rect(center=(int(config.game_width * (2/3)), self.main_y + self.main_h // 2))

        # ------ Base Surface Blit ------
        functions.highlight_button(surface, font, "Proceed", proceed_text_rect)
        functions.highlight_button(surface, font, "Inventory", inventory_text_rect)

        # ------ Click ------
        if inventory_text_rect.collidepoint(mouse_pos): return "inventory"
        elif proceed_text_rect.collidepoint(mouse_pos): return "proceed"

    def inventory_box(self, surface):
        pygame.draw.rect(surface, "White", (self.inventory_pos[0], self.inventory_pos[1], self.minorbox_size[0], self.minorbox_size[1]), 3, 10)
        inventory_text = config.title_font.render("Inventory", True, "White")
        inventory_text_rect = inventory_text.get_rect(center=(self.inventory_pos[0] + self.minorbox_size[0] // 2, self.inventory_pos[1] + config.title_font.size("Text Sample")[1]))
        surface.blit(inventory_text, inventory_text_rect)
        pygame.draw.line(surface, "White", (self.inventory_pos[0], self.minorbox_title_height), (self.inventory_pos[0] + self.minorbox_size[0] - 3, self.minorbox_title_height), 3)

    def equips_box(self, surface):
        pygame.draw.rect(surface, "White", (self.equips_pos[0], self.equips_pos[1], self.minorbox_size[0], self.minorbox_size[1]), 3, 10)
        equips_text = config.title_font.render("Equips", True, "White")
        equips_text_rect = equips_text.get_rect(center=(self.equips_pos[0] + self.minorbox_size[0] // 2, self.equips_pos[1] + config.text_height))
        surface.blit(equips_text, equips_text_rect)
        pygame.draw.line(surface, "White", (self.equips_pos[0], self.equips_pos[1] + 1.5 * config.title_height + config.padding), (self.equips_pos[0] + self.minorbox_size[0] - 3, self.equips_pos[1] + 1.5 * config.title_height + config.padding), 3)

    def stats_box(self, surface):
        pygame.draw.rect(surface, "White", (self.stats_pos[0], self.stats_pos[1], self.minorbox_size[0], self.minorbox_size[1]), 3, 10)
        stats_text = config.title_font.render("Stats", True, "White")
        stats_text_rect = stats_text.get_rect(center=(self.stats_pos[0] + self.minorbox_size[0] // 2, self.stats_pos[1] + config.text_height))
        surface.blit(stats_text, stats_text_rect)
        pygame.draw.line(surface, "White", (self.stats_pos[0], self.stats_pos[1] + 1.5 * config.title_height + config.padding), (self.stats_pos[0] + self.minorbox_size[0] - 3, self.stats_pos[1] + 1.5 * config.title_height + config.padding), 3)

    def fight_box(self):
        # ------ Local Variables ------
        font = config.title_font
        mouse_pos = screen.get_mouse()

        # ------ Clear Box ------
        self.draw_mainbox()

        # ------ Texts ------
        attack_text = font.render("Attack", True, 0)
        skill_text = font.render("Skills", True, 0)
        defend_text = font.render("Defend", True, 0)
        escape_text = font.render("Escape", True, 0)

        # ------ Rectangles ------
        attack_text_rect = attack_text.get_rect(center=(config.main_box_pos[0] + (1/5)*config.main_box_size[0], config.main_box_pos[1] + (1/2)*config.main_box_size[1]))
        skill_text_rect = skill_text.get_rect(center=(config.main_box_pos[0] + (2/5)*config.main_box_size[0], config.main_box_pos[1] + (1/2)*config.main_box_size[1]))
        defend_text_rect = defend_text.get_rect(center=(config.main_box_pos[0] + (3/5)*config.main_box_size[0], config.main_box_pos[1] + (1/2)*config.main_box_size[1]))
        escape_text_rect = escape_text.get_rect(center=(config.main_box_pos[0] + (4/5)*config.main_box_size[0], config.main_box_pos[1] + (1/2)*config.main_box_size[1]))

        # ------ Base Surface Blit ------
        functions.highlight_button(screen.base_surface, font, "Attack", attack_text_rect)
        functions.highlight_button(screen.base_surface, font, "Skills", skill_text_rect)
        functions.highlight_button(screen.base_surface, font, "Defend", defend_text_rect)
        functions.highlight_button(screen.base_surface, font, "Escape", escape_text_rect)

        # ------ Mouse Over ------
        if attack_text_rect.collidepoint(mouse_pos): return "attack"
        elif skill_text_rect.collidepoint(mouse_pos): return "skill"
        elif defend_text_rect.collidepoint(mouse_pos): return "defend"
        elif escape_text_rect.collidepoint(mouse_pos): return "escape"
        
# ========== Init ==========
boxes = Boxes()