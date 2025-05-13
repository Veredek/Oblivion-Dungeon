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
        self.second_surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        ### If another auxiliar surface is added, put it in extra_surfaces
        self.surfaces = [self.base_surface, self.second_surface]

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

# ~~~~~~~~~~ Entities ~~~~~~~~~~
class Entity:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self, name: str):
        from src.functions import functions
        conn = sqlite3.connect("game\src\database\database.sqlite")
        cursor = conn.cursor()

        assert name in config.entities_tuple, "Not a valid entity name"

        self.flashing = False

        # region ----|1|---- Id
        cursor.execute("SELECT id FROM Entities WHERE name=?", (name,))
        self.id = cursor.fetchone()[0]
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
            self.img = functions.load_image(self.name)
        # endregion -|1|-

        # region ----|1|---- Attributes

        # region ----|2|---- Proper
        cursor.execute("SELECT * FROM entity_attributes WHERE id=?",(self.id,))
        ATTRIBUTES = [desc[0] for desc in cursor.description][1:] # exclude id
        values = cursor.fetchone()[1:] # exclude id
        self.ATTRIBUTES = dict(zip(ATTRIBUTES, values))
        # endregion -|2|-

        # region ----|2|---- Current
        self.attributes = dict()
        attributes = [ATTRIBUTE.lower() for ATTRIBUTE in ATTRIBUTES]
        for attribute,value in zip(attributes,values):    self.attributes[attribute] = value
        # endregion -|2|-

        self.attributes_points = 0
        # endregion -|1|-

        # region ----|1|---- Stats
        ### Lower case (e.g. "hp") means current value, Upper case (e.g. "HP") means proper value ###

        # region ----|2|---- Proper
        cursor.execute("SELECT * FROM entity_base_stats WHERE id=?",(self.id,))
        STATS = [desc[0] for desc in cursor.description][1:] # exclude id
        values = cursor.fetchone()[1:] # exclude id
        self.STATS = dict(zip(STATS, values))
        # endregion -|2|-

        # region ----|2|---- Current
        self.stats = dict()

        ''' This can be negative, and in that case, the stat property will return 0.
            Status effects will affect here (modified when applied, and unmodified when expired).'''

        stats = [STAT.lower() for STAT in STATS]
        for stat,value in zip(stats,values):    self.stats[stat] = value
        # endregion -|2|-

        # endregion -|1|-

        # region ----|1|---- Skills
        self.skills = []
        cursor.execute("SELECT skill_id FROM entity_skills WHERE entity_id=?",(self.id,))
        skills_ids = cursor.fetchall()[0]
        for skill_id in skills_ids:
            cursor.execute("SELECT name FROM skills WHERE id=?",(skill_id,))
            skill_name = cursor.fetchone()
            print(skill_name)
            self.skills.append(skill_name)
        # endregion -|1|-

        # region ----|1|---- Inventory
        self.inventory = []
        # cursor.execute("SELECT")
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

        # ~~~~~~~~~~ Exp ~~~~~~~~~~
        if self.player_bool:    self.total_exp = int(0)

        cursor.close()

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

    # region ----|1|---- Stats
    @property
    def stat(self, name: str):
        ''' Use lowercase.
            Returns the final current value of the stat.'''

        attribute_stat = self._stats_from_attributes(name)[name]
        return attribute_stat + self.stats[name]

    # endregion -|1|-

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    def _stats_from_attributes(self, attribute: str):
        ''' Use lowercase'''
        assert attribute in ['str', 'dex', 'wis', 'fort', 'res'], "Not a valid attribute"

        stats = dict()

        if attribute == 'str':
            stats['hp_regen'] =    int(0.1 * self.attributes['str'])
            stats['crit_dmg'] =    0.025 * self.attributes['str']
        elif attribute == 'dex':
            stats['accuracy'] =    0.02 * self.attributes['dex']
            stats['avoid'] =       0.005 * self.attributes['dex']
            stats['crit_chance'] = 0.005 * self.attributes['dex']
        elif attribute == 'wis':
            stats['mp_regen'] =    int(0.1 * self.attributes['wis'])
            stats['mp'] =          1 * self.attributes['wis']
        elif attribute == 'fort':
            stats['hp'] =          2 * self.attributes['fort']
            stats['def'] =         1 * self.attributes['fort']
        elif attribute == 'res':
            stats['resist'] =      0.005 * self.attributes['fort']
            stats['mdef'] =        1 * self.attributes['res']

        return stats

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
        # endregion -|1|-

        # region ----|1|---- Text
        cursor.execute("SELECT text FROM skills WHERE name=?",(self.name,))
        self.text = cursor.fetchone()[0]
        # endregion -|1|-

        cursor.close()

    # ---------- Str ----------
    def __str__(self):
        return f"[id:{self.id}] Skill ({self.name}):\n" + f"{self.text}"

    # ---------- Blit Damage on Enemy ----------
    def blit_damage(self, damage: int, elapsed: float):
        font = config.PIXEL_FONT
        surface = screen.second_surface

        damage_surface = font.render(f"{damage}", True, (255,0,0,0))
        damage_rect = damage_surface.get_rect(center=(config.BASE_WIDTH/2,
                                                        config.BASE_HEIGHT/5 - elapsed*100
        ))

        surface.blit(damage_surface, damage_rect)
        return None

    # ---------- Hurt Animation ----------
    def flash_enemy(self, enemy : Entity, damage: int):
        from src.boxes import boxes

        clock = pygame.time.Clock()

        # region ----|1|---- Making a White copy of the Enemy Image
        image = enemy.image()
        flashed = image.copy()
        overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 0))
        flashed.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        # endregion -|1|-

        flashing = True
        timer = time.time()
        while flashing:
            # Clear Surfaces
            screen.clear_surfaces()

            # Elapsed Time
            elapsed = time.time() - timer

            # region ----|1|---- Flash Frames
            if int(elapsed * 20) % 2 == 0:
                enemy_display = flashed
            else:
                enemy_display = image
            # endregion -|1|-

            # region ----|1|---- Window Blit
            boxes.draw_mainbox()

            enemy_display_rect = enemy_display.get_rect(center=config.ENEMY_CENTER)
            screen.base_surface.blit(enemy_display, enemy_display_rect)
            self.blit_damage(damage, elapsed)
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
    def miss(self):
        return None

    # ---------- Avoid Animation ----------
    def avoid(self):
        return None

    # ---------- Damage Reduction ----------
    def dmg_reduction(stat_value: int):
        reduction = 100 - 100 * (100/(stat_value + 100))
        return reduction

    # ---------- Activate Skill ----------
    def activate(self, caster: Entity, target: Entity):
        import random

        conn = sqlite3.connect("game\src\database\database.sqlite")
        cursor = conn.cursor()

        # region ----|1|---- Instances
        cursor.execute("SELECT sequencer FROM skill_instances WHERE skill_id=?", (self.id,))
        instances = len(cursor.fetchall())
        # endregion -|1|-

        for instance in range(instances):

            # region ----|1|---- Type
            ''' Skill Damage Type'''

            cursor.execute("SELECT type_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            type_id = cursor.fetchone()[0]

            cursor.execute("SELECT type FROM skill_types WHERE id=?", (type_id,))
            skill_type = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Element
            cursor.execute("SELECT element_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            element_id = cursor.fetchone()[0]

            cursor.execute("SELECT element FROM elements WHERE id=?", (element_id,))
            element = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Source
            cursor.execute("SELECT source_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            source_id = cursor.fetchone()[0]

            cursor.execute("SELECT source FROM skill_source WHERE id=?", (source_id,))
            source = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Check if it's damage, heal or condition
            ### 1: damage, 0: heal, None: condition ###

            cursor.execute("SELECT is_damage FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            is_damage = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Base Value
            if is_damage != None:
                cursor.execute("SELECT base_value FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                base_value = cursor.fetchone()[0]

            # endregion -|1|-

            # region ----|1|---- Scale
            if is_damage != None:
                cursor.execute("SELECT scale FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                scale = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Condition
            if is_damage == None:
                cursor.execute("SELECT condition_id FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                condition_id = cursor.fetchone()[0]

                cursor.execute("SELECT name FROM conditions WHERE id=?", (condition_id,))
                condition = str(cursor.fetchone()[0])
            # endregion -|1|-

            # region ----|1|---- Condition Stacks
            if is_damage == None:
                cursor.execute("SELECT condition_stacks FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
                con_stacks = cursor.fetchone()[0]
            # endregion -|1|-

            # region ----|1|---- Accuracy
            cursor.execute("SELECT accuracy FROM skill_instances WHERE sequencer=? AND skill_id=?", (instance, self.id))
            skill_accuracy = cursor.fetchone()[0]
            # endregion -|1|-

            # ~~~~~~~~~~ Apply ~~~~~~~~~~
            # region ----|1|---- Hit/Miss/Avoid Check

            # region ----|2|---- Hit/Miss
            if skill_accuracy != None:
                hit_percent = int((skill_accuracy * caster.stat('accuracy')) * 100)
                hit = random.randint(1,100)

                if hit > hit_percent:
                    self.miss()
                    continue
                else:  pass
            # endregion -|2|-

            # region ----|2|---- Avoid
            if target != caster:

                avoid_percent = int(target.stats["avoid"] * 100)
                chance_percent = hit_percent - avoid_percent
                hit = random.randint(1,hit_percent)

                if hit > chance_percent:
                    self.avoid()
                    continue
                else:  pass
            # endregion -|2|-

            # endregion -|1|-

            # region ----|1|---- Value Calculation
            if is_damage != None:

                # region ----|2|---- Source Scale
                value = base_value + (scale * source)
                # endregion -|2|-

                # region ----|2|---- Element Scale
                if element != None:
                    element_pow = element + '_pow'
                    caster_element_pow = caster.stats[element_pow]
                    value = (100+caster_element_pow)*value
                # endregion -|2|-

                # region ----|2|---- Skill Type Reduction
                if skill_type == 'physical':
                    target_def = target.stat('def')
                    reduction = self.dmg_reduction(target_def)

                if skill_type == 'magical':
                    target_mdef = target.stat('mdef')
                    reduction = self.dmg_reduction(target_mdef)

                value = (100-reduction)*value
                # endregion -|2|-

                # region ----|2|---- Value Element Reduction
                if element != None:
                    element_res = element + '_res'
                    target_element_res = target.stats[element_res]
                    value = (100-target_element_res)*value
                # endregion -|2|-

                # region ----|2|---- Value Random Gap
                min_value = int(0.9*value)
                max_value = int(1.1*value)
                value = random.randint(min_value,max_value)
                # endregion -|2|-

            # endregion -|1|-

            # region ----|1|---- Condition Handle
            # endregion -|1|-

        cursor.close()