import pygame
import time

# ========== Tree ==========
from src.config import config
from src.classes import screen
from src.functions import functions
from src.Boxes import boxes
from src.classes import Entity

# ========== Functions ==========
# ~~~~~~~~~~ Blit Damage on Enemy ~~~~~~~~~~
def blit_damage(damage: int, elapsed: float):
    font = config.TEXT_FONT
    surface = screen.base_surface

    damage_surface = font.render(f"{damage}", True, "red")
    damage_rect = damage_surface.get_rect(center=(config.BASE_WIDTH,
                                                    config.BASE_HEIGHT/3 - elapsed*10
    ))

    surface.blit(damage_surface, damage_rect)
    return None

# ~~~~~~~~~~ Damage animation ~~~~~~~~~~
def flash_enemy(enemy : Entity, damage: int):

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
        blit_damage(damage, elapsed)
        screen.blit_surface(screen.base_surface)

        # ----|1|---- Stop ----|1|----
        if elapsed > 0.5:
            flashing = False
    
        # ----|1|---- Tick FPS ----|1|----
        clock.tick(60)

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
            damage = 0 # init

            for cast in range(self.multicast):
                damage += functions.physical_dmg(caster, target, self.scale)
            target.stats["HP"] -= damage
            flash_enemy(target, damage)

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