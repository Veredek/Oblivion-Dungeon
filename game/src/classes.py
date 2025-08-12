import pygame
import math
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
            from src.functions import functions as f

            getter = lambda self, s=stat:  f.clamp((self._stat_from_attributes(s) + self._stats.get(s)), -999, 999)

            setter = lambda self, value, s=stat:  self._stats.__setitem__(s, value)

            setattr(cls, stat, property(getter,setter))
        # endregion -|1|-

    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self, name: str):
        from src.functions import functions

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
            self.img = functions.load_image(self.name)
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
            if skill_accuracy != None:
                hit_percent = int((skill_accuracy * caster.accuracy) * 100)
                hit = random.randint(1,100)

                print(f"skill accuracy: {skill_accuracy}, caster accuracy: {caster.accuracy}")
                print(f"hit chance: {hit_percent}%,", end=" ")

                if hit > hit_percent:
                    print("(miss!)")
                    self.miss()
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
                    self.avoid()
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
        # endregion -|1|-

    def __init__(self):
        db.execute("SELECT name FROM conditions")
        self.CONDITIONS = [condition[0] for condition in db.cursor.fetchall()]

        self.UNSTACKABLE = ['stun',
                            'sleep']


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
