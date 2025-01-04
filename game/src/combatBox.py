import pygame
from game.src.Boxes import draw_mainbox

def combatBox(WIN, FONT):
    WIN.fill()
    draw_mainbox(WIN)

    atkText = FONT.render("Attack", True, "White")
    skillText = FONT.render("Skills", True, "White")
    defendText = FONT.render("Defend", True, "White")
    runText = FONT.render("Run", True, "White")

    WIN.blit(atkText, ())

    pygame.display.update()

    
# ====== mainBox Sizes ======
mainBox_SIZE = (900, 200)
mainBox_START = (50,550)
mainBox_THICKNESS = 8

