# ------ Class Equipament ------
class Equipament:
    VALID_PLACES = {"head", "body", "left hand", "right hand", "double hand", "legs", "feet", "accessory1", "accessory2"}

    def __init__(self, name, place, stats=None, skills=None, conditions=None):
        if place not in self.VALID_PLACES:
            raise ValueError(f"Invalid place '{place}'. Must be one of {self.VALID_PLACES}.")
        
        self.name = name
        self.place = place
        self.stats = stats if stats is not None else {
        "HP": 0,
        "MP": 0,
        "STR": 0,
        "DEX": 0,
        "WIS": 0,
        "DEF": 0,
        "MDEF": 0
    }
        self.skills = skills if skills is not None else []
        self.conditions = conditions if conditions is not None else []

    def equip(self, entity):
        # --- place ---
        entity.equipaments[self.place] = self.name

        # --- stats ---
        for stat in self.stats:
            entity.stats[stat] += self.stats.get(stat)

        # --- conditions ---
        for condition in self.conditions:
            entity.conditions.append(condition)

    def __str__(self):
        stats_str = ", ".join(f"{key}: {value}" for key, value in self.stats.items() if value != 0)
        skills_str = ", ".join(self.skills) if self.skills else "None"
        conditions_str = ", ".join(self.conditions) if self.conditions else "None"
        return (
            f"Name: {self.name}\n"
            f"Place: {self.place}\n"
            f"Stats: {stats_str if stats_str else 'No bonuses'}\n"
            f"Skills: {skills_str}\n"
            f"Conditions: {conditions_str}"
        )
    
# ------ Equipaments def ------
def equipament():
    name = "equipament"

    place = "place"

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

    conditions = []

    return Equipament(name, place, stats, skills, conditions)    


def broken_sword():
    name = "Broken Sword"

    place = "place"

    stats = {
        "HP": 0,
        "MP": 0,
        "STR": 1,
        "DEX": 0,
        "WIS": 0,
        "DEF": 0,
        "MDEF": 0
    }

    return Equipament(name, place, stats)

# ------ Equipaments List ------
    
EQUIPAMENTS = {
    "Broken Sword": broken_sword,
    }
