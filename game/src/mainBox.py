import pygame

def draw_mainbox(WIN, mainBox_START, mainBox_SIZE, mainBox_THICKNESS):
    mainBox = pygame.Rect(mainBox_START[0], mainBox_START[1], mainBox_SIZE[0], mainBox_SIZE[1])
    internal_mainBox = pygame.Rect(mainBox_START[0] + mainBox_THICKNESS, mainBox_START[1] + mainBox_THICKNESS, mainBox_SIZE[0] - 2 * mainBox_THICKNESS, mainBox_SIZE[1] - 2 * mainBox_THICKNESS)

    pygame.draw.rect(WIN, "white", mainBox)
    pygame.draw.rect(WIN, "black", internal_mainBox)

    pygame.display.update()