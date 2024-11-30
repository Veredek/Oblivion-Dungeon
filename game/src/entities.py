from src.equipaments import EQUIPAMENTS

# ------ Entity Class ------
class Entity:
    def __init__(self, name: str, stats: dict, skills: list, inventory: list, conditions: dict = None):
        self.name = name
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

        for item in inventory:
            if item in EQUIPAMENTS:
                equipament_function = EQUIPAMENTS.get(item)
                equipament = equipament_function()
                equipament.equip(self)

    def __str__(self):
        # Representação amigável para depuração
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


def player(player_name):
    name = player_name

    stats = {
        "HP": 100,
        "MP": 100,
        "STR": 10,
        "DEX": 10,
        "WIS": 10,
        "DEF": 10,
        "MDEF": 10
    }

    skills = []

    inventory = ["Broken Sword"]

    return Entity(name, stats, skills, inventory)


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
