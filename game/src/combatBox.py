import pygame
from src.mainBox import draw_mainbox

def combatBox(WIN, FONT):
    WIN.fill()
    draw_mainbox(WIN)

    atkText = FONT.render("Attack", True, "White")
    skillText = FONT.render("Skills", True, "White")
    defendText = FONT.render("Defend", True, "White")
    runText = FONT.render("Run", True, "White")

    WIN.blit(atkText, ())

    pygame.display.update()
