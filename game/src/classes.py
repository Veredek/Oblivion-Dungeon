import pygame
import math
import random
import sqlite3
import time

# ========== Tree ==========
from src.config import config, db

# ========== (classes) ==========
# ~~~~~~~~~~ Screen ~~~~~~~~~~
class Screen:
    def __init__(self):
        # region ----|1|---- Display
        self.fullscreen = True
        self.maximized = False

        self.display_size = config.SCREEN_SIZE
        self.display = pygame.display.set_mode(self.display_size, pygame.FULLSCREEN)
        pygame.display.set_caption(config.GAME_TITLE)
        pygame.display.flip()
        # endregion -|1|-

        # region ----|1|---- Surfaces
        self.base_surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        self.second_surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        ### If another auxiliar surface is added, put it in extra_surfaces
        self.surfaces = [self.base_surface, self.second_surface]
        # endregion -|1|-

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # region ----|1|---- Offset x
    @property
    def offset_x(self):
        return int((self.display_size[0] - config.game_width) / 2)
    # endregion -|1|-

    # region ----|1|---- Offset y
    @property
    def offset_y(self):
        return int((self.display_size[1] - config.game_height) / 2)
    # endregion -|1|-

    # region ----|1|---- Display Width
    @property
    def width(self):
        return self.display_size[0]
    # endregion -|1|-

    # region ----|1|---- Display Height
    @property
    def height(self):
        return self.display_size[1]
    # endregion -|1|-

    # region ----|1|---- Mouse Position
    @property
    def mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = (mouse_pos[0]) / config.scale, (mouse_pos[1]) / config.scale

        return (mouse_x - self.offset_x, mouse_y - self.offset_y)
    # endregion -|1|-

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # region ----|1|---- Clear Surfaces
    def clear_surfaces(self):
        """
        Clears all surfaces
        """
        self.base_surface.fill((0,0,0,0))
        self.second_surface.fill((0,0,0,0))

    def clear_surface(self, surface: pygame.Surface):
        """
        Clears given surface
        """
        surface.fill((0,0,0,0))
    # endregion -|1|-

    # region ----|1|---- Update Display
    def update_display(self):
        if config.display_update:
            flag = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

            self.display = pygame.display.set_mode(self.display_size, flag)

            pygame.display.flip()

            config.display_update = False

            print(f"*Display Update*" +
                f"    Resolution: {config.resolution}" +
                f"    Display: {self.display_size}\n")
    # endregion -|1|-

    # region ----|1|---- Toggle Fullscreen
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        print("*Toggle Fullscreen*" +
              f"    Fullscreen: {self.fullscreen}\n")

        # ----|1|---- Config Update + Display Resize ----|1|----
        if self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width, config.game_height = config.MAX_RESOLUTION

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.SCREEN_SIZE

        elif not self.fullscreen:
            # ----|2|---- Config Update ----|2|----
            config.game_width = (config.min_resolution[0], "only")
            config.game_height = (config.min_resolution[1], "only")

            # ----|2|---- Display Resize ----|2|----
            self.display_size = config.min_resolution

        # ----|1|---- Display Update ----|1|----
        config.display_update = True
        self.update_display()
    # endregion -|1|-

    # region ----|1|---- Resize Display
    def resize(self, event : pygame.event):
        if self.display_size != event.size:
            event_width, event_height = event.size

            # Maximizing
            if event_width == config.SCREEN_SIZE[0]:
                self.maximized = True

                # Config Update + Display Resize
                config.game_height = event_height
                self.display_size = event.size

                print("*Maximizing*\n")

            # Unmaximizing
            elif self.maximized:
                self.maximized = False

                # Config Update + Display Resize
                config.game_width = (config.min_resolution[0], "only")
                config.game_height = (config.min_resolution[1], "only")
                self.display_size = config.min_resolution

                print("*Unmaximizing*\n")

            # Resizing
            else:
                # Config Update + Display Resize
                config.game_width = event_width
                self.display_size = config.resolution

                print("*Resizing*\n")

            # Display Update
            config.display_update = True
            self.update_display()
    # endregion -|1|-

    # region ----|1|---- Blit Surface On Display
    def blit_surface(self, surface: pygame.Surface):
        # Clear Display
        self.display.fill((0,0,0))

        # Scale Base Surface
        scaled_surface = pygame.transform.scale(surface, (config.game_width, config.game_height))

        # Blit Base Surface on Display
        self.display.blit(scaled_surface, (screen.offset_x, screen.offset_y))

        # Update Display
        pygame.display.flip()

    def blit_surfaces(self):
        # Clear Display
        self.display.fill((0,0,0))

        # Blit Each Surface
        for surface in self.surfaces:
            # Scale Surface
            scaled_surface = pygame.transform.scale(surface, (config.game_width, config.game_height))

            # Blit Surface on Display
            self.display.blit(scaled_surface, (screen.offset_x, screen.offset_y))

        # Update Display
        pygame.display.flip()

    # endregion -|1|-

screen = Screen()

# ~~~~~~~~~~ GameState ~~~~~~~~~~
class GameState:
    def __init__(self):
        self.state = "MENU" # ALL UPPERCASE
        self.ongame_state = "menu" # ALL LOWERCASE
        self.current_text = 0
        self.player_name = ""
        self.room = 0

game_state = GameState()

# ~~~~~~~~~~ HUD ~~~~~~~~~~
class Hud:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        self.time = time.time()
        self.skip_text = False
        self.waiting = False

        # region ----|1|---- MainBox
        self.main_x = config.MAINBOX_POS[0]
        self.main_y = config.MAINBOX_POS[1]

        self.main_w = config.MAINBOX_SIZE[0]
        self.main_h = config.MAINBOX_SIZE[1]
            # endregion

        # region ----|1|---- MinorBox
        self.minorbox_spacer = 0.5 * (config.game_height - self.main_y - self.main_h) # Spacer between minor boxes
        self.minorbox_TITLE_HEIGHT = self.minorbox_spacer + 1.5 * config.TITLE_HEIGHT + config.PADDING
        self.minorbox_w = (self.main_w - 2 * self.minorbox_spacer) // 3
        self.minorbox_h = config.game_height - self.main_h - 4 * self.minorbox_spacer
            # endregion

        # region ----|1|---- Position
        self.inventory_pos = (self.main_x,
                              self.minorbox_spacer)

        self.equips_pos = (self.main_x + self.minorbox_w + self.minorbox_spacer,
                           self.minorbox_spacer)

        self.stats_pos = (self.main_x + 2 * self.minorbox_w + 2 * self.minorbox_spacer,
                          self.minorbox_spacer)
            # endregion

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    def highlight(self, surface : pygame.Surface, font : pygame.font.Font, text : str, text_rect : pygame.Rect):
        """
        Creates a gray text that turns white on mouse collide
        """

        mouse_pos = screen.mouse

        if text_rect.collidepoint(mouse_pos):
            highlighted_surface = font.render(text, True, "White")
            surface.blit(highlighted_surface, text_rect)
        else:
            normal_surface = font.render(text, True, "Gray")
            surface.blit(normal_surface, text_rect)

    def highlight_button(self, mouse_pos : property, font : pygame.font.Font, text : str, text_rect : pygame.Rect):
        '''
        Blit a button on given surface
        '''

        surface = screen.base_surface

        if text_rect.collidepoint(mouse_pos):
            # ~~~~~~~~~~ Surfaces ~~~~~~~~~~
            text_surface = font.render(text, True, "Yellow")
            sign_surface = config.HIGHLIGHT_SIGN.render("+", True, "Yellow")

            # ~~~~~~~~~~ Sizes ~~~~~~~~~~
            text_size = text_surface.get_size()
            sign_size = sign_surface.get_size()

            spacer = 5

            highlighted_surface_size = (text_size[0] + 2 * sign_size[0] + 2*spacer,
                                        text_size[1])

            # ~~~~~~~~~~ Blit ~~~~~~~~~~
            highlighted_surface = pygame.Surface(highlighted_surface_size)
            highlighted_surface.blit(sign_surface, (0, (text_size[1] - sign_size[1]) // 2))
            highlighted_surface.blit(text_surface, (sign_size[0] + spacer, 0))
            highlighted_surface.blit(sign_surface, (sign_size[0] + text_size[0] + 2*spacer, (text_size[1] - sign_size[1]) // 2))

            surface.blit(highlighted_surface, (text_rect[0] - sign_size[0] - spacer, text_rect[1]))

        else:
            normal_surface = font.render(text, True, "White")
            surface.blit(normal_surface, text_rect)

    def glowing_text(self, text : str, font : pygame.font.Font, text_color : str, outline_color : str, outline_width : int):
        # Renderizar o texto com a cor do contorno
        outline_surface = font.render(text, True, outline_color)

        # Criar uma superfície maior para acomodar o contorno
        w, h = outline_surface.get_size()
        surface = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)

        # Desenhar o contorno ao redor do texto
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx**2 + dy**2 <= outline_width**2:  # Forma circular
                    surface.blit(outline_surface, (dx + outline_width, dy + outline_width))

        # Renderizar o texto principal
        text_surface = font.render(text, True, text_color)
        surface.blit(text_surface, (outline_width, outline_width))

        return surface

    def text_on_base_surface(self, text: str, font : pygame.font.Font, color : str = "white", topleft = False, center = False, h_button = False):
        text_surface = font.render(text, True, color)
        mouse_pos = screen.mouse

        if center:
            text_rect = text_surface.get_rect(center=center)
        elif topleft:
            text_rect = text_surface.get_rect(topleft=topleft)

        # if highlight button
        if h_button:
            self.highlight_button(mouse_pos, font, text, text_rect)
        else:
            screen.base_surface.blit(text_surface, text_rect)

    def draw_mainbox(self):
        pygame.draw.rect(screen.base_surface, (0, 0, 0), (self.main_x, self.main_y, self.main_w, self.main_h))
        pygame.draw.rect(screen.base_surface, "White", (self.main_x, self.main_y, self.main_w, self.main_h), 3, 10)

    def type_text(self, full_text, speed):
        if self.skip_text:
            return full_text
        else:
            elapsed_time = time.time() - self.time
            chars_to_show = int(elapsed_time * speed)
            return full_text[:chars_to_show]

    def draw_text(self, script, surface=screen.base_surface, speed=config.TYPING_SPEED):
        text = script.script()
        font = config.TEXT_FONT
        current_text = self.type_text(text,speed)
        if current_text == text:
            self.waiting = True
        words = current_text.split(" ")
        lines = []
        current_line = ""

        # Ajusta o texto
        for word in words:
            if font.size(current_line + word)[0] > (self.main_w - config.PADDING):
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
            surface.blit(text_surface, (self.main_x + config.PADDING, self.main_y + config.PADDING + i * config.TEXT_HEIGHT))

    def after_box(self, mouse_pos):
        # ------ Local Variables ------
        font = config.TITLE_FONT

        # ------ Clear Box ------
        self.draw_mainbox()

        # ------ Texts ------
        proceed_text = font.render("Proceed", True, "White")
        inventory_text = font.render("Inventory", True, "White")

        # ------ Rectangles ------
        proceed_text_rect = proceed_text.get_rect(center=(config.BASE_WIDTH * (1/3),
                                                          self.main_y + self.main_h // 2))

        inventory_text_rect = inventory_text.get_rect(center=(config.BASE_WIDTH * (2/3),
                                                              self.main_y + self.main_h // 2))

        # ------ Base Surface Blit ------
        self.highlight_button(mouse_pos, font, "Proceed", proceed_text_rect)
        self.highlight_button(mouse_pos, font, "Inventory", inventory_text_rect)

        # ------ Click ------
        if inventory_text_rect.collidepoint(mouse_pos): return "inventory"
        elif proceed_text_rect.collidepoint(mouse_pos): return "proceed"

    def inventory_box(self, surface):
        pygame.draw.rect(surface, "White", (self.inventory_pos[0], self.inventory_pos[1], self.minorbox_w, self.minorbox_h), 3, 10)

        inventory_text = config.TITLE_FONT.render("Inventory", True, "White")
        inventory_text_rect = inventory_text.get_rect(center=(self.inventory_pos[0] + self.minorbox_w // 2, self.inventory_pos[1] + config.TITLE_FONT.size("Text Sample")[1]))
        surface.blit(inventory_text, inventory_text_rect)
        pygame.draw.line(surface, "White", (self.inventory_pos[0], self.minorbox_TITLE_HEIGHT), (self.inventory_pos[0] + self.minorbox_w - 3, self.minorbox_TITLE_HEIGHT), 3)

    def equips_box(self, surface):
        pygame.draw.rect(surface, "White", (self.equips_pos[0], self.equips_pos[1], self.minorbox_w, self.minorbox_h), 3, 10)
        equips_text = config.TITLE_FONT.render("Equips", True, "White")
        equips_text_rect = equips_text.get_rect(center=(self.equips_pos[0] + self.minorbox_w // 2, self.equips_pos[1] + config.TEXT_HEIGHT))
        surface.blit(equips_text, equips_text_rect)
        pygame.draw.line(surface, "White", (self.equips_pos[0], self.equips_pos[1] + 1.5 * config.TITLE_HEIGHT + config.PADDING), (self.equips_pos[0] + self.minorbox_w - 3, self.equips_pos[1] + 1.5 * config.TITLE_HEIGHT + config.PADDING), 3)

    def stats_box(self, surface):
        pygame.draw.rect(surface, "White", (self.stats_pos[0], self.stats_pos[1], self.minorbox_w, self.minorbox_h), 3, 10)
        stats_text = config.TITLE_FONT.render("Stats", True, "White")
        stats_text_rect = stats_text.get_rect(center=(self.stats_pos[0] + self.minorbox_w // 2, self.stats_pos[1] + config.TEXT_HEIGHT))
        surface.blit(stats_text, stats_text_rect)
        pygame.draw.line(surface, "White", (self.stats_pos[0], self.stats_pos[1] + 1.5 * config.TITLE_HEIGHT + config.PADDING), (self.stats_pos[0] + self.minorbox_w - 3, self.stats_pos[1] + 1.5 * config.TITLE_HEIGHT + config.PADDING), 3)

    def fight_box(self, mouse_pos):
        # ------ Local Variables ------
        font = config.TITLE_FONT

        # ------ Clear Box ------
        self.draw_mainbox()

        # ------ Texts ------
        attack_text = font.render("Attack", True, 0)
        skill_text = font.render("Skills", True, 0)
        defend_text = font.render("Defend", True, 0)
        escape_text = font.render("Escape", True, 0)

        # ------ Rectangles ------
        attack_text_rect = attack_text.get_rect(center=(config.MAINBOX_POS[0] + (1/5)*config.MAINBOX_SIZE[0], config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1]))
        skill_text_rect = skill_text.get_rect(center=(config.MAINBOX_POS[0] + (2/5)*config.MAINBOX_SIZE[0], config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1]))
        defend_text_rect = defend_text.get_rect(center=(config.MAINBOX_POS[0] + (3/5)*config.MAINBOX_SIZE[0], config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1]))
        escape_text_rect = escape_text.get_rect(center=(config.MAINBOX_POS[0] + (4/5)*config.MAINBOX_SIZE[0], config.MAINBOX_POS[1] + (1/2)*config.MAINBOX_SIZE[1]))

        # ------ Base Surface Blit ------
        self.highlight_button(mouse_pos, font, "Attack", attack_text_rect)
        self.highlight_button(mouse_pos, font, "Skills", skill_text_rect)
        self.highlight_button(mouse_pos, font, "Defend", defend_text_rect)
        self.highlight_button(mouse_pos, font, "Escape", escape_text_rect)

        # ------ Mouse Over ------
        if attack_text_rect.collidepoint(mouse_pos): return "attack"
        elif skill_text_rect.collidepoint(mouse_pos): return "skill"
        elif defend_text_rect.collidepoint(mouse_pos): return "defend"
        elif escape_text_rect.collidepoint(mouse_pos): return "escape"

    def esc_menu(self):
        clock = pygame.time.Clock()

        inside = True
        while inside:
            screen.clear_surfaces()
            mouse_pos = screen.mouse

            # region ----|1|---- Font Surfaces
            continue_text = config.TITLE_FONT.render("Continue", True, "White")
            quit_text = config.TITLE_FONT.render("Quit", True, "White")
            # endregion -|1|-

            # region ----|1|---- Rectangles
            continue_text_rect = continue_text.get_rect(center=(config.game_width / 2, config.game_height / 2 - 80))
            quit_text_rect = quit_text.get_rect(center=(config.game_width / 2, config.game_height / 2 + 40))
            # endregion -|1|-

            # region ----|1|---- Blit Button on base_surface
            self.highlight_button(mouse_pos, config.TITLE_FONT, "Continue", continue_text_rect)
            self.highlight_button(mouse_pos, config.TITLE_FONT, "Quit", quit_text_rect)
            # endregion -|1|-

            # region ----|1|---- Display Blit
            screen.blit_surface(screen.base_surface)
            # endregion -|1|-

            # region ----|1|---- Event Handle

            for event in pygame.event.get():
                # region ----|2|---- Quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # endregion -|2|-

                # region ----|2|---- Videorisize
                elif event.type == pygame.VIDEORESIZE:
                    if event.size != screen.display_size:
                        if screen.fullscreen == False:
                            print("*Video Resize*"
                                    f"    Event Size:{event.size}," +
                                    f"    Display Size:{screen.display_size}\n")
                            screen.resize(event)
                # endregion -|2|-

                # region ----|2|---- Keydown
                elif event.type == pygame.KEYDOWN:
                    print("*Keydown*")
                    if event.key == pygame.K_F11:
                        print("    F11\n")
                        screen.toggle_fullscreen()

                    elif event.key == pygame.K_ESCAPE:
                        print("    Esc")
                        inside = False
                # endregion -|2|-

                # region ----|2|---- Mouse Button
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # region ----|3|---- Left Click
                    if event.button == 1:

                        # region ----|4|---- CONTINUE
                        if continue_text_rect.collidepoint(mouse_pos):
                            print("-> Continue <-\n")
                            inside = False
                        # endregion -|4|-

                        # region ----|4|---- QUIT
                        elif quit_text_rect.collidepoint(mouse_pos):
                            print("-> Quit <-\n")
                            game_state.state = "MENU"
                            game_state.ongame_state = "menu"
                            inside = False
                        # endregion -|4|-

                    # endregion -|3|-

                # endregion -|2|-

            # endregion -|1|-

            # Tick FPS
            clock.tick(60)

        return None

hud = Hud()

# ~~~~~~~~~~ Entities ~~~~~~~~~~
class Entity:
    # ~~~~~~~~~~ Class Config ~~~~~~~~~~
    _config = False
    def __new__(cls, *args, **kwargs):
        if not cls._config:
            cls.self_config()
            cls._config = True
        return super().__new__(cls)

    @classmethod
    def self_config(cls):

        # region ----|1|---- Attributes
        for attribute in config.ENTITY_ATTRIBUTES:

            getter = lambda self, attr=attribute:  max(0, self._attributes.get(attr))

            setter = lambda self, value, attr=attribute:  self._attributes.__setitem__(attr, value)

            setattr(cls, attribute, property(getter, setter))
        # endregion -|1|-

        # region ----|1|---- Not Elemental Stats
        for stat in [stat for stat in config.ENTITY_STATS if 'res' not in stat.lower() and 'pow' not in stat.lower()]:

            # SyntaxError handle
            if stat == 'def':  stat = 'Def'

            getter = lambda self, s=stat:  max(0, (self._stat_from_attributes(s) + self._stats.get(s)))

            setter = lambda self, value, s=stat:  self._stats.__setitem__(s, value)

            setattr(cls, stat, property(getter,setter))
        # endregion -|1|-

        # region ----|1|---- Elemental Stats
        for stat in [stat for stat in config.ENTITY_STATS if 'res' in stat.lower() or 'pow' in stat.lower()]:

            getter = lambda self, s=stat:  math.clamp((self._stat_from_attributes(s) + self._stats.get(s)), -999, 999)

            setter = lambda self, value, s=stat:  self._stats.__setitem__(s, value)

            setattr(cls, stat, property(getter,setter))
        # endregion -|1|-

    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self, name: str):
        from src.functions import load_image

        assert name in config.ENTITIES_NAMES, "Not a valid entity name"

        self.flashing = False

        # region ----|1|---- Id
        db.execute("SELECT id FROM Entities WHERE name=?", (name,))
        self.id = db.cursor.fetchone()[0]
        # endregion -|1|-

        # region ----|1|---- Name
        if name == "player":
            self.name = ""
            self.player_bool = True
        else:
            self.name = name
            self.player_bool = False
        # endregion -|1|-

        # region ----|1|---- Image
        if not self.player_bool:
            self.img = load_image(self.name)
        # endregion -|1|-

        # region ----|1|---- Attributes

        # region ----|2|---- Proper
        db.execute("SELECT * FROM entity_attributes WHERE entity_id=?",(self.id,))
        ATTRIBUTES = [desc[0] for desc in db.cursor.description][1:] # exclude id
        values = db.cursor.fetchone()[1:] # exclude id
        self._attributes = dict(zip(ATTRIBUTES, values))
        # endregion -|2|-

        # region ----|2|---- Current
        attributes = [ATTRIBUTE.lower() for ATTRIBUTE in ATTRIBUTES]
        for attribute,value in zip(attributes,values):    self._attributes[attribute] = value
        # endregion -|2|-

        self.attributes_points = 0
        # endregion -|1|-

        # region ----|1|---- Stats
        ### Lower case (e.g. "hp") means current value, Upper case (e.g. "HP") means proper value ###

        # region ----|2|---- Proper
        db.execute("SELECT * FROM entity_base_stats WHERE entity_id=?",(self.id,))
        STATS = [desc[0] for desc in db.cursor.description][1:] # exclude id
        values = db.cursor.fetchone()[1:] # exclude id
        self._stats = dict(zip(STATS, values))
        # endregion -|2|-

        # region ----|2|---- Current
        stats = [STAT.lower() for STAT in STATS]
        stats = ['Def' if stat == 'def' else stat for stat in stats]
        for stat,value in zip(stats,values):    self._stats[stat] = value
        # endregion -|2|-

        # endregion -|1|-

        # region ----|1|---- Skills
        self.skills = []
        db.execute("SELECT skill_id FROM entity_skills WHERE entity_id=?",(self.id,))
        skills_ids = db.cursor.fetchall()[0]
        for skill_id in skills_ids:
            db.execute("SELECT name FROM skills WHERE id=?",(skill_id,))
            skill_name = db.cursor.fetchone()[0]
            self.skills.append(skill_name)
        # endregion -|1|-

        # region ----|1|---- Inventory
        self.inventory = []
        # db.execute("SELECT")
        # endregion -|1|-

        # region ----|1|---- Equipaments
        self.equipaments = {
            "head": None,
            "body": None,
            "left hand": None,
            "right hand": None,
            "double hand": None,
            "legs": None,
            "feet": None,
            "accessory1": None,
            "accessory2": None
        }
        # endregion -|1|-

        # region ----|1|---- Conditions
        self.conditions = {}
        # endregion -|1|-

        self._hp = self.MAX_HP
        self._mp = self.MAX_MP

        # ~~~~~~~~~~ Exp ~~~~~~~~~~
        if self.player_bool:    self.total_exp = int(0)

    # ~~~~~~~~~~ String ~~~~~~~~~~
    def __str__(self):
        # Representação para depuração
        stats_str = "\n".join(f"{key}: {value}" for key, value in self.stats.items())
        conditions_str = ", ".join(f"{key}: {value}" for key, value in self.conditions.items())
        equipaments_str = ", ".join(f"{key} ({value})" for key, value in self.equipaments.items())
        inventory_str = ", ".join(self.inventory) if self.inventory else "None"
        return (
            f"Name: {self.name}\n"
            f"Stats:\n{stats_str}\n"
            f"Conditions: {conditions_str if self.conditions else 'None'}\n"
            f"Skills: {', '.join(self.skills) if self.skills else 'None'}\n"
            f"Equipaments: {equipaments_str}\n"
            f"Inventory: {inventory_str if self.inventory else 'None'}"
        )

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # region ----|1|---- EXP & Level
    @property
    def level(self):
        level = math.sqrt(self.total_exp/10)
        return int(level) # auto round down

    @property
    def exp(self):
        level_exp_required = 10*(self.level**2)
        return self.total_exp - level_exp_required

    @property
    def exp_to_up(self):
        level_up = self.level + 1
        level_up_exp_required = 10*(level_up**2)
        return level_up_exp_required - self.total_exp

    @property
    def next_level_exp(self):
        return self.exp + self.exp_to_up

    # endregion -|1|-

    # region ----|1|---- hp/mp
    @property
    def hp(self):  return self._hp

    @hp.setter
    def hp(self, value):  self._hp = min(value, self.max_hp)

    @property
    def mp(self):  return self._hp

    @mp.setter
    def mp(self, value):  self._hm = min(value, self.max_mp)
    # endregion -|1|-

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    def _value_of_stat(self, stat: str):
        value = self._stat_from_attributes(stat) + self._stats[stat]
        if value > 0:  return value
        else:          return 0

    def _stat_from_attributes(self, stat: str):

        formulas = {
            'max_hp':      lambda: 2 * self.fort,
            'MAX_HP':      lambda: 2 * self.FORT,

            'hp_regen':    lambda: int(0.1 * self.str),
            'HP_REGEN':    lambda: int(0.1 * self.STR),

            'max_mp':          lambda: 1 * self.wis,
            'MAX_MP':          lambda: 1 * self.WIS,

            'mp_regen':    lambda: int(0.1 * self.wis),
            'MP_REGEN':    lambda: int(0.1 * self.WIS),

            'Def':         lambda: 1 * self.fort,
            'DEF':         lambda: 1 * self.FORT,

            'mdef':        lambda: 1 * self.res,
            'MDEF':        lambda: 1 * self.RES,

            # multiplier
            'crit_chance': lambda: 0.005 * self.dex,
            'CRIT_CHANCE': lambda: 0.005 * self.DEX,

            # multiplier
            'crit_dmg':    lambda: 0.025 * self.str,
            'CRIT_DMG':    lambda: 0.025 * self.STR,

            # multiplier
            'accuracy':    lambda: 0.02 * self.dex,
            'ACCURACY':    lambda: 0.02 * self.DEX,

            # multiplier
            'avoid':       lambda: 0.005 * self.dex,
            'AVOID':       lambda: 0.005 * self.DEX,

            # multiplier
            'resist':      lambda: 0.005 * self.res,
            'RESIST':      lambda: 0.005 * self.RES,
        }

        return formulas[stat]()

    def dmg_reduction(self, type: str):
        '''Returns a value between 0 and 100'''
        if   type == 'physical':  return 100 - 100 * (100/(self.Def + 100))
        elif type == 'magical':   return 100 - 100 * (100/(self.mdef + 100))
        else:                     return 0

    def image(self):
        size = self.img.get_size()
        scale = (config.game_height / 2) / size[1]
        resized_img = pygame.transform.scale_by(self.img, scale)
        return resized_img

    def blit(self):
        enemy_surface = self.image()
        enemy_surface_rect = enemy_surface.get_rect(center=config.ENEMY_CENTER)
        screen.base_surface.blit(enemy_surface, enemy_surface_rect)

    def gain_condition(self, condition_name, value):
        # Previne stun se o personagem for imune
        if condition_name == "stun" and "stun_immune" in self.conditions:
            return

        # Atualiza a condição existente ou adiciona uma nova
        if condition_name in self.conditions:
            self.conditions[condition_name] += value
        else:
            self.conditions[condition_name] = value

player = Entity("player")

# ~~~~~~~~~~ Skills ~~~~~~~~~~
class Skill:
    # ---------- Init ----------
    def __init__(self, name: str):
        assert name in config.skills_tuple

        self.name = name

        # region ----|1|---- Id
        db.execute("SELECT id FROM skills WHERE name=?",(self.name,))
        self.id = db.cursor.fetchone()[0]
        # endregion -|1|-

        # region ----|1|---- Text
        db.execute("SELECT text FROM skills WHERE name=?",(self.name,))
        self.text = db.cursor.fetchone()[0]
        # endregion -|1|-

    # ---------- Str ----------
    def __str__(self):
        return f"[id:{self.id}] Skill ({self.name}):\n" + f"{self.text}"

    # ---------- Blit Damage on Enemy ----------
    def blit_damage(self, enemy: Entity, damage: int, elapsed: float = 5):

        dmg_font = config.PIXEL_FONT
        clock    = pygame.time.Clock()
        timer    = time.time()
        flashing = True

        # region ----|1|---- Making a White copy of the Enemy Image
        enemy_image = enemy.image()
        enemy_flashed = enemy_image.copy()
        overlay = pygame.Surface(enemy_image.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 0))
        enemy_flashed.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        # endregion -|1|-

        # region ----|1|---- Damage Surface
        if damage > 0:  damage_surface = dmg_font.render(f"{damage}", True, 'red')
        if damage == 0: damage_surface = dmg_font.render(f"{damage}", True, 'white')
        if damage < 0:  damage_surface = dmg_font.render(f"{damage}", True, 'green')
        # endregion -|1|-

        # region ----|1|---- Enemy Rectangle
        enemy_display_rect = enemy_image.get_rect(center=config.ENEMY_CENTER)
        # endregion -|1|-

        while flashing:
            # Clear Surfaces
            screen.clear_surfaces()

            # Elapsed Time
            elapsed = time.time() - timer

            # region ----|1|---- Flash Frames
            if int(elapsed * 20) % 2 == 0:
                enemy_display = enemy_flashed
            else:
                enemy_display = enemy_image
            # endregion -|1|-

            # region ----|1|---- Damage Rectangle
            damage_rect = damage_surface.get_rect(center=(config.BASE_WIDTH/2,
                                                          config.BASE_HEIGHT/5 - elapsed*100))
            # endregion -|1|-

            # region ----|1|---- Window Blit
            hud.draw_mainbox()

            screen.base_surface.blit(enemy_display, enemy_display_rect)
            screen.second_surface.blit(damage_surface, damage_rect)

            screen.blit_surfaces()
            # endregion -|1|-

            # region ----|1|---- Stop
            if elapsed > config.flashing_time:
                flashing = False
            # endregion -|1|-

            # Tick FPS
            clock.tick(60)

        return None

    # ---------- Miss Animation ----------
    def miss(self, target: Entity):
        # region ----|1|---- Constants
        miss_font = config.PIXEL_FONT
        clock     = pygame.time.Clock()
        timer     = time.time()
        anim_time = 1 # time of animation
        missing   = True

        miss_surface   = miss_font.render('miss', True, 'white')
        miss_rect      = miss_surface.get_rect(center=config.ENEMY_CENTER)
        target_surface = target.image()
        target_rect    = target_surface.get_rect(center=config.ENEMY_CENTER)
        # endregion -|1|-

        while missing:
            # Clear Surfaces
            screen.clear_surfaces()

            # Elapsed Time
            elapsed = time.time() - timer

            # Load HUD
            hud.draw_mainbox()

            # region ----|1|---- Window Blit
            screen.base_surface.blit(target_surface, target_rect)
            screen.second_surface.blit(miss_surface, miss_rect)

            screen.blit_surfaces()
            # endregion -|1|-

            # region ----|1|---- Stop
            if elapsed > anim_time:
                missing = False
            # endregion -|1|-

            # Tick FPS
            clock.tick(60)

        return None

    # ---------- Avoid Animation ----------
    def avoid(self, target: Entity):
        from src.functions import clamp

        # region ----|1|---- Constants
        avoid_font = config.PIXEL_FONT
        clock      = pygame.time.Clock()
        timer      = time.time()
        anim_time  = 1 # time of animation
        avoiding   = True
        direction  = random.choice(['left', 'right'])

        avoid_surface  = avoid_font.render('avoid', True, 'white')
        avoid_rect     = avoid_surface.get_rect(center=config.ENEMY_CENTER)
        target_surface = target.image()
        target_rect    = target_surface.get_rect(center=config.ENEMY_CENTER)
        # endregion -|1|-

        # region ----|1|---- Movement Variables
        max_distance = 200 # in pixels
        acceleration = clamp(1 + target.avoid, 1, 2)
        distance     = lambda elapsed: clamp((acceleration * max_distance * math.sin(math.pi * elapsed / anim_time)), 0, max_distance)
        # endregion -|1|-

        if   direction == 'left':   enemy_center_x = lambda elapsed: config.ENEMY_CENTER[0] - distance(elapsed)
        elif direction == 'right':  enemy_center_x = lambda elapsed: config.ENEMY_CENTER[0] + distance(elapsed)

        while avoiding:
            # Clear Surfaces
            screen.clear_surfaces()

            # Elapsed Time
            elapsed = time.time() - timer

            # Enemy Move
            if target != player:
                target_rect = target_surface.get_rect(center=(enemy_center_x(elapsed),
                                                              config.ENEMY_CENTER[1]))

            # Load HUD
            hud.draw_mainbox()

            # region ----|1|---- Window Blit
            screen.base_surface.blit(target_surface, target_rect)
            screen.second_surface.blit(avoid_surface, avoid_rect)

            screen.blit_surfaces()
            # endregion -|1|-

            # region ----|1|---- Stop
            if elapsed > anim_time:
                avoiding = False
            # endregion -|1|-

            # Tick FPS
            clock.tick(60)

        return None

    # ---------- Activate Skill ----------
    def activate(self, caster: Entity, target: Entity):
        import random

        print(f"\n--- Skill({self.name}): caster({caster.name}) -> target({target.name}) ---")

        # region ----|1|---- Instances
        db.execute("SELECT sequencer FROM skill_instances WHERE skill_id=?", (self.id,))
        instances = len(db.cursor.fetchall())
        # endregion -|1|-

        for instance in range(instances):

            # ~~~~~~~~~~ Instance Values ~~~~~~~~~~

            # region ----|1|---- Type
            ''' Skill Damage Type'''

            db.execute("SELECT type_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            type_id = db.cursor.fetchone()[0]

            db.execute("SELECT type FROM skill_types WHERE id=?", (type_id,))
            skill_type = db.cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Element
            db.execute("SELECT element_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            element_id = db.cursor.fetchone()[0]

            db.execute("SELECT element FROM elements WHERE id=?", (element_id,))
            try:    element = db.cursor.fetchone()[0]
            except: element = None
            # endregion -|1|-

            # region ----|1|---- Source
            db.execute("SELECT source_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            source_id = db.cursor.fetchone()[0]

            db.execute("SELECT source FROM skill_source WHERE id=?", (source_id,))
            source = db.cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Check if it's damage, heal or condition
            ### 1: damage, 0: heal, None: condition ###

            db.execute("SELECT is_damage FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            is_damage = db.cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Base Value
            if is_damage != None:
                db.execute("SELECT base_value FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                base_value = db.cursor.fetchone()[0]

            # endregion -|1|-

            # region ----|1|---- Scale
            if is_damage != None:
                db.execute("SELECT scale FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                scale = db.cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Condition
            if is_damage == None:
                db.execute("SELECT condition_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                condition_id = db.cursor.fetchone()[0]

                db.execute("SELECT name FROM conditions WHERE id=?", (condition_id,))
                condition = str(db.cursor.fetchone()[0])
            # endregion -|1|-

            # region ----|1|---- Condition Stacks
            if is_damage == None:
                db.execute("SELECT condition_stacks FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                con_stacks = db.cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Accuracy
            db.execute("SELECT accuracy FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            skill_accuracy = db.cursor.fetchone()[0]
            # endregion -|1|-

            # ~~~~~~~~~~ Apply ~~~~~~~~~~
            print(f"instance: {instance + 1}/{instances}")
            # region ----|1|---- Hit/Miss/Avoid Check

            # region ----|2|---- Hit/Miss
            if skill_accuracy == None:
                print(f"skill accuracy: (auto hit)")

            else:
                hit_percent = int((skill_accuracy * caster.accuracy) * 100)
                hit = random.randint(1,100)

                print(f"skill accuracy: {skill_accuracy}, caster accuracy: {caster.accuracy}")
                print(f"hit chance: {hit_percent}%,", end=" ")

                if hit > hit_percent:
                    print("(miss!)")
                    self.miss(target)
                    continue
            # endregion -|2|-

            # region ----|2|---- Avoid
            if target != caster:

                avoid_stat_percent = int(100*target.avoid)
                avoid_chance_percent = min(int(100*(avoid_stat_percent/hit_percent)), 100)
                hit = random.randint(1, 100)

                print(f"avoid chance: {avoid_chance_percent}%", end=" ")

                if hit < avoid_chance_percent:
                    print("(avoid!)")
                    self.avoid(target)
                    continue
                else:  print("(hit!)")
            # endregion -|2|-

            # endregion -|1|-

            # region ----|1|---- Value Calculation
            if is_damage != None: # can be 0 (heal)

                # region ----|2|---- Scale/Reduction
                value = base_value

                # Source Scale
                if source:                   value += scale * getattr(caster, source)

                # Element Scale
                if element:                  value *= 1 + getattr(caster, (element + '_pow'))/100

                # Type Reduction
                if skill_type:               value *= 1 - target.dmg_reduction(skill_type)/100

                # Element Reduction
                if element:                  value *= 1 - getattr(target, (element + '_res'))/100

                # endregion -|2|-

                # region ----|2|---- Value Random Gap
                min_value = int(0.9*value)
                max_value = int(1.1*value)
                value = random.randint(min_value,max_value)
                # endregion -|2|-

                # region ----|2|---- Damage Infliction
                if is_damage == 1 :
                    print(f"damage: {value}, target hp: {target.hp}/{target.max_hp}", end=" -> ")
                    target.hp -= value
                    print(f"{target.hp}/{target.max_hp}")
                elif is_damage == 0 :
                    print(f"heal: {value}, target hp: {target.hp}/{target.max_hp}", end=" -> ")
                    target.hp += value
                    print(f"{target.hp}/{target.max_hp}")
                # endregion -|2|-

                # region ----|2|---- Damage Blit on Surface
                if target != player:  self.blit_damage(target, value)
                # endregion -|2|-

            # endregion -|1|-

            # region ----|1|---- Condition Handle
            # endregion -|1|-

# ~~~~~~~~~~ Conditions ~~~~~~~~~~
class Condition:

    # ~~~~~~~~~~ Class Config ~~~~~~~~~~
    _config = False
    def __new__(cls, *args, **kwargs):
        if not cls._config:
            cls.self_config()
            cls._config = True
        return super().__new__(cls)

    @classmethod
    def self_config(cls):

        # region ----|1|---- Tuple of all valid Conditions
        db.execute("SELECT name FROM conditions")
        cls.CONDITIONS = tuple([con[0] for con in db.cursor.fetchall()])

        cls.UNSTACKABLE = ['stun',
                            'sleep']
        # endregion -|1|-

    def apply(self, condition: str, target: Entity, stacks: int = None):

        # ---------- Unstackable ----------
        if condition in self.UNSTACKABLE:
            if target.conditions[condition] == 0:    target.conditions[condition] = 1

        # ---------- Stackable ----------
        else:
            target.conditions[condition] += stacks

    def start_turn(self, entity: Entity):
        # region ----|1|---- Bleed
        if entity.conditions['bleed'] != 0:
            damage = int((entity.conditions['bleed'] / 100) * entity.stats['HP'])
            entity.stats['hp'] -= damage
            entity.conditions['bleed'] -= 1
        # endregion -|1|-

        # region ----|1|---- Poison
        if entity.conditions['poison'] != 0:
            damage = entity.conditions['poison']
            entity.stats['hp']
        # endregion -|1|-

        # region ----|1|---- Burn
        if entity.conditions['burn'] != 0:
            damage = entity.conditions['burn']
        # endregion -|1|-
