# ------ Class Skills ------
class Skill:
    def __init__(self, name, type, damage=0, condition=None):
        self.name = name
        self.type = type
        self.damage = damage
        self.condition = condition if condition else {}

    def activate(self, *player_entity, enemy_entity):
        if self.damage > 0:
            enemy_entity.stats["HP"] -= self.damage 
        if self.condition:
            for cond, value in self.condition.items():
                enemy_entity.gain_condition(cond, value)

    def __str__(self):
        return f"Skill {self.name}: Damage = {self.damage}, Condition = {self.condition}"


# ------ Skills List ------
def skill():
    name = "Skill"
    type = "Type"
    damage = 0
    condition = None

    return Skill(name, type, damage, condition)

def attack(entity):
    name = "Attack"
    type = "physical"
    damage = entity.stats.get("STR")

    return Skill(name, type, damage)