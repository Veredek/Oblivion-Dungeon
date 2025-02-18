import pygame

# ========== Tree ==========
from src.functions import functions

# ------ Class Skills ------
class Skill:
    def __init__(self, name, type, multicast = 1, scale = 1, condition=None):
        self.name = name
        self.type = type
        self.multicast = multicast
        self.scale = scale
        self.condition = condition if condition else {}

    def __str__(self):
        return f"Skill ({self.name}): Type = {self.type}, Multicast = {self.multicast}, Condition = {self.condition}"

    def activate(self, caster, target = None):
        # ------ Normal Physical Damage ------
        if self.type == "physical":
            damage = 0
            for cast in range(self.multicast):
                damage += functions.physical_dmg(caster, target, self.scale)
            target.stats["HP"] -= damage

# ------ Skills List ------
def skill():
    name = "Skill"
    type = "Type"
    multicast = 1
    scale = 1
    condition = None

    return Skill(name, type, multicast, scale, condition)

def attack():
    name = "attack"
    type = "physical"

    return Skill(name, type)

SKILLS = {
    "attack" : attack
}