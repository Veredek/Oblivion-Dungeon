import pygame
from src.equipaments import EQUIPAMENTS
from src.skills import SKILLS
from src.definitions import load_image
# ====== Global Objects ======
from src.classes import screen

# ====== Global Variables ======
from src.variables import GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE, TRANSPARENT_SURFACE ,ENEMY_CENTER

# ====== Definitions ======
  
# ------ Entity Class ------
class Entity:
    def __init__(self, name: str, stats: dict, skills: list, inventory: list, conditions: dict = None):
        self.name = name
        if name != "": self.img = load_image(self.name)
        self.stats = stats
        self.skills = skills
        self.inventory = inventory
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
        self.conditions = conditions if conditions is not None else {}

        self.flashing = False

        for item in inventory:
            if item in EQUIPAMENTS:
                equipament_function = EQUIPAMENTS.get(item)
                equipament = equipament_function()
                equipament.equip(self)

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

    def image(self):
        size = self.img.get_size()
        scale = (GAME_HEIGHT / 2) / size[1]
        resized_img = pygame.transform.scale_by(self.img, scale)
        return resized_img

    def blit(self):
        enemy_surface = self.image()
        enemy_surface_rect = enemy_surface.get_rect(center=ENEMY_CENTER)
        BASE_SURFACE.blit(enemy_surface, enemy_surface_rect)

    def gain_condition(self, condition_name, value):
        # Previne stun se o personagem for imune
        if condition_name == "stun" and "stun_immune" in self.conditions:
            return

        # Atualiza a condição existente ou adiciona uma nova
        if condition_name in self.conditions:
            self.conditions[condition_name] += value
        else:
            self.conditions[condition_name] = value

# ------ Entities def ------
def entity():
    name = "entity"

    stats = {
        "HP": 0,
        "MP": 0,
        "STR": 0,
        "DEX": 0,
        "WIS": 0,
        "DEF": 0,
        "MDEF": 0
    }

    skills = []

    inventory = []

    return Entity(name, stats, skills, inventory)    


# ====== Inicializing Player ======
def player__init__():
    name = ""

    stats = {
        "LEVEL" : 1,
        "EXP" : 0,
        "MAX_HP" : 100,
        "MAX_MP" : 100,
        "MAX_EXP" : 10,
        "HP": 100,
        "MP": 100,
        "STR": 10,
        "DEX": 10,
        "WIS": 10,
        "FORT": 10,
        "RES": 10,
        "DEF": 10,
        "MDEF": 10,
        "gold": 0,
        "attributes points": 0
    }

    skills = ["attack"]

    inventory = ["Broken Sword"]

    conditions = {"poisoned": 3}

    return Entity(name, stats, skills, inventory, conditions)

player = player__init__()

# ====== Enemies ======
def slime():
    name = "Slime"

    stats = {
        "HP": 50,
        "MP": 0,
        "STR": 5,
        "DEX": 3,
        "WIS": 1,
        "DEF": 2,
        "MDEF": 1
    }

    skills = []

    inventory = []

    return Entity(name, stats, skills, inventory)
