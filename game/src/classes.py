import pygame
import math
import sqlite3
import time

# ========== Tree ==========
from src.config import config

# ========== (classes) ==========
# ~~~~~~~~~~ Screen ~~~~~~~~~~
class Screen:
    def __init__(self):
        self.fullscreen = True
        self.maximized = False

        self.display_size = config.SCREEN_SIZE
        self.display = pygame.display.set_mode(self.display_size, pygame.FULLSCREEN)
        pygame.display.set_caption(config.GAME_TITLE)
        pygame.display.flip()

        self.base_surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)        

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # region ----|1|---- Offset x
    @property
    def offset_x(self):
        return int((self.display_size[0] - config.game_width) / 2)
        # endregion
    # region ----|1|---- Offset y
    @property
    def offset_y(self):
        return int((self.display_size[1] - config.game_height) / 2)    
        # endregion
    # region ----|1|---- Display Width
    @property
    def width(self):
        return self.display_size[0]
        # endregion
    # region ----|1|---- Display Height
    @property
    def height(self):
        return self.display_size[1]
        # endregion
    # region ----|1|---- Mouse Position
    @property
    def mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = (mouse_pos[0]) / config.scale, (mouse_pos[1]) / config.scale

        return (mouse_x - self.offset_x, mouse_y - self.offset_y)
        # endregion
    
    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # region ----|1|---- Clear Surfaces
    def clear_surfaces(self):
        """
        Clears base_surface and alpha surface
        """
        self.base_surface.fill((0,0,0))
        # endregion
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
        # endregion
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
        # endregion
    # region ----|1|---- Resize Display
    def resize(self, event : pygame.event):
        if self.display_size != event.size:
            event_width, event_height = event.size

            # ----|1|---- Maximizing ----|1|----
            if event_width == config.SCREEN_SIZE[0]:
                self.maximized = True

                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_height = event_height
                self.display_size = event.size

                print("*Maximizing*\n")

            # ----|1|---- Unmaximizing ----|1|----
            elif self.maximized:
                self.maximized = False
                
                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_width = (config.min_resolution[0], "only")
                config.game_height = (config.min_resolution[1], "only")
                self.display_size = config.min_resolution

                print("*Unmaximizing*\n")

            # ----|1|---- Resizing ----|1|----
            else:
                # ----|2|---- Config Update + Display Resize ----|2|----
                config.game_width = event_width
                self.display_size = config.resolution

                print("*Resizing*\n")

            # ----|1|---- Display Update ----|1|----
            config.display_update = True
            self.update_display()
        # endregion
    # region ----|1|---- Blit Surface On Display
    def blit_surface(self, surface: pygame.Surface):
        scaled_surface = pygame.transform.scale(surface, (config.game_width, config.game_height))
        self.display.blit(scaled_surface, (screen.offset_x, screen.offset_y))
        pygame.display.flip()
        # endregion

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

# ~~~~~~~~~~ Entities ~~~~~~~~~~
class Entity:
    
    def __init__(self, name: str):
        from src.functions import functions
        conn = sqlite3.connect("game\src\database\database.sqlite")
        cursor = conn.cursor()

        assert name in config.entities_tuple, "Not a valid entity name"

        self.flashing = False

        # region ----|1|---- Id
        cursor.execute("SELECT id FROM Entities WHERE name=?", (name,))
        self.id = cursor.fetchone()[0]
            # endregion

        # region ----|1|---- Name
        if name == "player":
            self.name = ""
            self.player_bool = True
        else:
            self.name = name
            self.player_bool = False
            # endregion

        # region ----|1|---- Image
        if not self.player_bool:
            self.img = functions.load_image(self.name)
            # endregion

        # region ----|1|---- Attributes

        # region ----|2|---- Proper
        cursor.execute("SELECT * FROM entity_attributes WHERE id=?",(self.id,))
        ATTRIBUTES = [desc[0] for desc in cursor.description][1:] # exclude id
        values = cursor.fetchone()[1:] # exclude id
        self.attributes = dict(zip(ATTRIBUTES, values))
            # endregion

        # region ----|2|---- Current
        attributes = [ATTRIBUTE.lower() for ATTRIBUTE in ATTRIBUTES]
        for attribute,value in zip(attributes,values):    self.attributes[attribute] = value
            # endregion

        self.attributes_points = 0
        # endregion

        # region ----|1|---- Stats
        ''' Lower case (e.g. "hp") means current value, Upper case (e.g. "HP") means proper value '''

        # region ----|2|---- Proper
        cursor.execute("SELECT * FROM entity_base_stats WHERE id=?",(self.id,))
        STATS = [desc[0] for desc in cursor.description][1:] # exclude id
        values = cursor.fetchone()[1:] # exclude id
        self.stats = dict(zip(STATS, values))
            # endregion

        # region ----|2|---- Current
        stats = [STAT.lower() for STAT in STATS]
        for stat,value in zip(stats,values):    self.stats[stat] = value
            # endregion

        # endregion

        # region ----|1|---- Skills
        self.skills = []
        cursor.execute("SELECT skill_id FROM entity_skills WHERE entity_id=?",(self.id,))
        skills_ids = cursor.fetchall()[0]
        for skill_id in skills_ids:
            cursor.execute("SELECT name FROM skills WHERE id=?",(skill_id,))
            skill_name = cursor.fetchone()
            print(skill_name)
            self.skills.append(skill_name)
            # endregion

        # region ----|1|---- Inventory
        self.inventory = []
        # cursor.execute("SELECT")
            # endregion

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
            # endregion
        
        # region ----|1|---- Conditions
        self.conditions = []
            # endregion

        # ~~~~~~~~~~ Exp ~~~~~~~~~~
        if self.player_bool:    self.total_exp = int(0)

        cursor.close()

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

        conn = sqlite3.connect("game\src\database\database.sqlite")
        cursor = conn.cursor()

        self.name = name

        # region ----|1|---- Id
        cursor.execute("SELECT id FROM skills WHERE name=?",(self.name,))
        self.id = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Text
        cursor.execute("SELECT text FROM skills WHERE name=?",(self.name,))
        self.text = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Damage Type
        cursor.execute("SELECT type_id FROM skills WHERE name=?",(self.name,))
        type_id = cursor.fetchone()[0]
        cursor.execute("SELECT type FROM skill_types WHERE id=?",(type_id,))
        self.type = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Damage Source
        cursor.execute("SELECT dmg_source_id FROM skills WHERE name=?",(self.name,))
        src_id = cursor.fetchone()[0]
        cursor.execute("SELECT source FROM dmg_source WHERE id=?",(src_id,))
        self.dmg_source = cursor.fetchone()[0]
        # endregion 

        # region ----|1|---- Multicast
        cursor.execute("SELECT multicast FROM skills WHERE name=?",(self.name,))
        self.multicast = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Scale
        cursor.execute("SELECT scale FROM skills WHERE name=?",(self.name,))
        self.scale = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Accuracy
        cursor.execute("SELECT accuracy FROM skills WHERE name=?",(self.name,))
        self.accuracy = cursor.fetchone()[0]
        # endregion

        # region ----|1|---- Conditions
        cursor.execute("SELECT * FROM skill_conditions WHERE skill_id=?",(self.id,))
        try:
            ### If there is conditions
            HEADERS = [desc[0] for desc in cursor.description][2:] # exclude ids
            values = cursor.fetchone()[2:] # exclude ids
            self.conditions = dict(zip(HEADERS, values))
        except TypeError:
            ### if there is no conditions
            self.conditions = None
        # endregion

        cursor.close()

    # ---------- Str ----------
    def __str__(self):
        return f'''[id:{self.id}] Skill ({self.name}): Type = {self.type},
                                                       Source = {self.dmg_source},
                                                       Multicast = {self.multicast},
                                                       Scale = {self.scale},
                                                       Accuracy = {self.accuracy}
                                                       Conditions = {self.conditions}'''

    # ---------- Blit Damage on Enemy ----------
    def blit_damage(self, damage: int, elapsed: float):
        font = config.TEXT_FONT
        surface = screen.base_surface

        damage_surface = font.render(f"{damage}", True, "red")
        damage_rect = damage_surface.get_rect(center=(config.BASE_WIDTH,
                                                        config.BASE_HEIGHT/3 - elapsed*10
        ))

        surface.blit(damage_surface, damage_rect)
        return None

    # ---------- Hurt Animation ----------
    def flash_enemy(self, enemy : Entity, damage: int):
        from src.boxes import boxes

        clock = pygame.time.Clock()
        image = enemy.image()
        flashed = image.copy()
        overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 0))
        flashed.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

        flashing = True
        timer = time.time()
        while flashing:
            # ----|1|---- Clear Surfaces ----|1|----
            screen.clear_surfaces()

            # ----|1|---- Elapsed Time ----|1|----
            elapsed = time.time() - timer

            # ----|1|---- Flash Frames ----|1|----
            if int(elapsed * 20) % 2 == 0:
                enemy_display = flashed
            else:
                enemy_display = image

            # ----|1|---- Window Blit ----|1|----
            boxes.draw_mainbox()

            enemy_display_rect = enemy_display.get_rect(center=config.ENEMY_CENTER)
            screen.base_surface.blit(enemy_display, enemy_display_rect)
            self.blit_damage(damage, elapsed)
            screen.blit_surface(screen.base_surface)

            # ----|1|---- Stop ----|1|----
            if elapsed > 0.5:
                flashing = False
        
            # ----|1|---- Tick FPS ----|1|----
            clock.tick(60)

    # ---------- Activate Skill ----------
    def activate(self, caster, target = None):
        from src.functions import functions
        # ------ Normal Physical Damage ------
        if self.type == "physical":
            damage = 0 # init

            for cast in range(self.multicast):
                damage += functions.physical_dmg(caster, target, self.scale)
            target.stats["HP"] -= damage
            self.flash_enemy(target, damage)
