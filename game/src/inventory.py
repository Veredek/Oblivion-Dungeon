import pygame
from src.equipaments import EQUIPAMENTS
from src.Boxes import Boxes
from src.Boxes import INVENTORY_POS, MINOR_BOX_SIZE, MAIN_BOX_POS, MAIN_BOX_SIZE, MINOR_BOX_TITLE_HEIGHT, MINOR_BOX_DISTANCE, STATS_POS, EQUIPS_POS
from src.definitions import special_highlight, glowing_text, basic_events, highlight, blit_surface

# ====== Global Objects ======
from src.classes import screen, game_state

# ====== Global Variables ======
from src.variables import GAME_WIDTH, GAME_HEIGHT, BASE_SURFACE
from src.variables import TITLE_FONT, TEXT_FONT, PADDING
from src.variables import HIGHLIGHT_SIGN, HIGHLIGHT_SIGN_SIZE

GAMETEXT_HEIGHT = TITLE_FONT.size("Text Sample")[1]
HPMPXP_FONT = pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", 35)

PLUS_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 30)
PLUS_TEXT = PLUS_FONT.render(" + ", True, "white",)

ATTRIBUTES_FONT = pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", 50)
ATTRIBUTES_TEXT_HEIGHT = ATTRIBUTES_FONT.render("sample", True, "white").get_size()[1]
ATTRIBUTES_TEXT_MAXWIDTH = ATTRIBUTES_FONT.render(" fort ", True, 0).get_width()
ATTRIBUTES_SIZE = (ATTRIBUTES_FONT.render(" fort  000 ", True, "white").get_width(), 5*ATTRIBUTES_TEXT_HEIGHT)
ATTRIBUTES_POS = (STATS_POS[0] + (MINOR_BOX_SIZE[0] - PADDING)/2 - (ATTRIBUTES_SIZE[0] + PLUS_TEXT.get_width() + 5), MINOR_BOX_TITLE_HEIGHT + 2*PADDING + 3*HPMPXP_FONT.render("Sample", True, "white").get_height())
CONDITIONS_POS = (STATS_POS[0] + PADDING, ATTRIBUTES_POS[1] + ATTRIBUTES_SIZE[1] + PADDING)
VALUE_MAXWIDTH = ATTRIBUTES_FONT.render(" 000 ", True, 0).get_width()
STR_POS = (ATTRIBUTES_POS)

EQUIPS_RECT_SIDE = 100
POS_HELMET = (EQUIPS_POS[0] + MINOR_BOX_SIZE[0]/2 - EQUIPS_RECT_SIDE/2, EQUIPS_POS[1] + MINOR_BOX_TITLE_HEIGHT + PADDING)
POS_CHEST = (POS_HELMET[0], POS_HELMET[1] + EQUIPS_RECT_SIDE + 30)
POS_LEG = (POS_CHEST[0], POS_CHEST[1] + EQUIPS_RECT_SIDE + 30)
POS_BOOTS = (POS_LEG[0], POS_LEG[1] + EQUIPS_RECT_SIDE + 30)
POS_RIGHTHAND = (POS_CHEST[0] - EQUIPS_RECT_SIDE - 30, POS_CHEST[1])
POS_LEFTHAND = (POS_CHEST[0] + EQUIPS_RECT_SIDE + 30, POS_CHEST[1])
POS_ITEM1 = (POS_LEG[0] - EQUIPS_RECT_SIDE - 30, POS_LEG[1])
POS_ITEM2 = (POS_LEG[0] + EQUIPS_RECT_SIDE + 30, POS_LEG[1])

# ====== Definitions ======
# ------ HPMPXP ------
def bars(surface, player):
    for type in ["HP", "MP", "EXP"]:
        # ------ HP ------
        if type == "HP":
            hp_height = HPMPXP_FONT.render("HP", True, "White").get_size()[1]
            # ------ HP TEXT ------
            hp_text = HPMPXP_FONT.render("HP", True, "White")
            hp_text_rect = hp_text.get_rect(topleft=(STATS_POS[0] + PADDING, MINOR_BOX_TITLE_HEIGHT + PADDING ))
            surface.blit(hp_text, hp_text_rect)

            # ------ HP BAR ------
            pygame.draw.rect(surface, "White", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175 - 4, MINOR_BOX_TITLE_HEIGHT + PADDING + hp_height*1/2 - 4 - 4, MINOR_BOX_SIZE[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
            pygame.draw.line(surface, "Green", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175, MINOR_BOX_TITLE_HEIGHT + PADDING + hp_height*1/2), (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.825, MINOR_BOX_TITLE_HEIGHT + PADDING + hp_height*1/2), 10)

            numbers_text = HPMPXP_FONT.render(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", True, "White")
            numbers_text_rect= numbers_text.get_rect(center=(STATS_POS[0] + MINOR_BOX_SIZE[0]/2, MINOR_BOX_TITLE_HEIGHT + PADDING + hp_height/2 - 4))
            surface.blit(glowing_text(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

        # ------ MP ------
        if type == "MP":
            mp_height = HPMPXP_FONT.render("MP", True, "White").get_size()[1]
            # ------ MP TEXT ------
            mp_text = HPMPXP_FONT.render("MP", True, "White")
            mp_text_rect = mp_text.get_rect(topleft=(STATS_POS[0] + PADDING, MINOR_BOX_TITLE_HEIGHT + PADDING + mp_height))
            surface.blit(mp_text, mp_text_rect)

            # ------ MP BAR ------
            pygame.draw.rect(surface, "White", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175 - 4, MINOR_BOX_TITLE_HEIGHT + PADDING + mp_height*3/2 - 4 - 4, MINOR_BOX_SIZE[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
            pygame.draw.line(surface, "royalblue", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175, MINOR_BOX_TITLE_HEIGHT + PADDING + mp_height*3/2), (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.825, MINOR_BOX_TITLE_HEIGHT + PADDING + mp_height*3/2), 10)

            numbers_text = HPMPXP_FONT.render(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", True, "White")
            numbers_text_rect= numbers_text.get_rect(center=(STATS_POS[0] + MINOR_BOX_SIZE[0]/2, MINOR_BOX_TITLE_HEIGHT + PADDING + mp_height*3/2 - 4))
            surface.blit(glowing_text(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

        # ------ EXP ------
        if type == "EXP":
            exp_height = HPMPXP_FONT.render("EXP", True, "White").get_size()[1]
            exp_percent = player.stats["EXP"] / player.stats["MAX_EXP"]
            # ------ EXP TEXT ------
            exp_text = HPMPXP_FONT.render("EXP", True, "White")
            exp_text_rect = exp_text.get_rect(topleft=(STATS_POS[0] + PADDING, MINOR_BOX_TITLE_HEIGHT + PADDING + 2*exp_height))
            surface.blit(exp_text, exp_text_rect)

            # ------ EXP BAR ------
            pygame.draw.rect(surface, "White", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175 - 4, MINOR_BOX_TITLE_HEIGHT + PADDING + exp_height*5/2 - 4 - 4, MINOR_BOX_SIZE[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
            if exp_percent > 0:
                pygame.draw.line(surface, "goldenrod", (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175, MINOR_BOX_TITLE_HEIGHT + PADDING + exp_height*5/2), (STATS_POS[0] + MINOR_BOX_SIZE[0]*0.175 + (MINOR_BOX_SIZE[0]*0.65 * exp_percent), MINOR_BOX_TITLE_HEIGHT + PADDING + exp_height*5/2), 10)

            numbers_text = HPMPXP_FONT.render(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", True, "White")
            numbers_text_rect= numbers_text.get_rect(center=(STATS_POS[0] + MINOR_BOX_SIZE[0]/2, MINOR_BOX_TITLE_HEIGHT + PADDING + exp_height*5/2 - 4))
            surface.blit(glowing_text(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

# ------ Attributes ------
def attributes(surface, player):
    mouse_pos = screen.get_mouse()

    pygame.draw.rect(surface, "white", (ATTRIBUTES_POS[0],
                                           ATTRIBUTES_POS[1],
                                           ATTRIBUTES_SIZE[0],
                                           ATTRIBUTES_SIZE[1]),
                                           2)
    
    # ATTRIBUTES BLIT
    attributes_list = ["STR", "DEX", "WIS", "FORT", "RES"]
    colors = ["red", "green", "royalblue", "sienna", "magenta"]
    for i in range(len(attributes_list)):
        # ATTRIBUTES TEXT
        attribute_text = ATTRIBUTES_FONT.render(f" {attributes_list[i]} ".lower(), True, colors[i])
        attribute_text_rect = attribute_text.get_rect(midtop=(ATTRIBUTES_POS[0] + ATTRIBUTES_TEXT_MAXWIDTH/2, ATTRIBUTES_POS[1] + i*ATTRIBUTES_TEXT_HEIGHT))
        surface.blit(attribute_text, attribute_text_rect)

        # ATTRIBUTES VALUE
        attribute_value = ATTRIBUTES_FONT.render(f" {player.stats[attributes_list[i]]} ", True, "white")
        attribute_value_rect = attribute_value.get_rect(midtop=(ATTRIBUTES_POS[0] + ATTRIBUTES_TEXT_MAXWIDTH + VALUE_MAXWIDTH/2, ATTRIBUTES_POS[1] + i*ATTRIBUTES_TEXT_HEIGHT))
        surface.blit(attribute_value, attribute_value_rect)

        # PLUS SIGN
        plus_rect = PLUS_TEXT.get_rect(midleft=(ATTRIBUTES_POS[0] + ATTRIBUTES_SIZE[0] + 5, ATTRIBUTES_POS[1] + PLUS_TEXT.get_height() + i*ATTRIBUTES_TEXT_HEIGHT))
        pygame.draw.rect(surface, "white" if plus_rect.collidepoint(mouse_pos) else "darkgray", plus_rect, 2)
        highlight(surface, PLUS_FONT, " + ", plus_rect)

        # INTERNAL LINES BLIT
        pygame.draw.line(surface, "white", (ATTRIBUTES_POS[0] + ATTRIBUTES_TEXT_MAXWIDTH, ATTRIBUTES_POS[1]), (ATTRIBUTES_POS[0] + ATTRIBUTES_TEXT_MAXWIDTH, ATTRIBUTES_POS[1] + ATTRIBUTES_SIZE[1] -1), 2)
        pygame.draw.line(surface, "white", (ATTRIBUTES_POS[0], ATTRIBUTES_POS[1] + i*ATTRIBUTES_TEXT_HEIGHT), (ATTRIBUTES_POS[0] + ATTRIBUTES_SIZE[0] -1, ATTRIBUTES_POS[1] + i*ATTRIBUTES_TEXT_HEIGHT), 2)

    # POINTS BLIT
    points_text = ATTRIBUTES_FONT.render(f" points: {player.stats["attributes points"]} ", True, "white",)
    applyclear_text = ATTRIBUTES_FONT.render(" clear   apply ", True, "white")
    clear_text = ATTRIBUTES_FONT.render("clear", True, "white")
    apply_text = ATTRIBUTES_FONT.render("apply", True, "white")

    rect_size = (applyclear_text.get_width(), points_text.get_height() + applyclear_text.get_height())
    rect_pos = (ATTRIBUTES_POS[0] + ATTRIBUTES_SIZE[0] + (PLUS_TEXT.get_width() + 5) + PADDING, ATTRIBUTES_POS[1] + (ATTRIBUTES_SIZE[1] - rect_size[1])/2)

    surface.blit(points_text, points_text.get_rect(midtop=(rect_pos[0] + rect_size[0]/2, rect_pos[1])))
    surface.blit(clear_text, clear_text.get_rect(midtop=(rect_pos[0] + (1/4)*rect_size[0], rect_pos[1] + points_text.get_height())))
    surface.blit(apply_text, apply_text.get_rect(midtop=(rect_pos[0] + (3/4)*rect_size[0], rect_pos[1] + points_text.get_height())))

    pygame.draw.rect(surface, "white", (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]), 2)
    pygame.draw.line(surface, "white", (rect_pos[0], rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0] -1, rect_pos[1] + points_text.get_height()), 2)
    pygame.draw.line(surface, "white", (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height() + applyclear_text.get_height() -1), 2)

# ------ Conditions ------
def conditions(surface, player):
    mouse_pos = screen.get_mouse()

    conditions_text = TEXT_FONT.render("Conditions: ", True, "white")
    conditions_text_rect = conditions_text.get_rect(topleft=(CONDITIONS_POS[0], CONDITIONS_POS[1]))
    surface.blit(conditions_text, conditions_text_rect)

    conditions_rects = []
    for condition in player.conditions:
        condition_text = TEXT_FONT.render(condition, True, "white")
    return conditions_rects

# ------ Equips ------
def equips(surface, player):
    positions = [POS_HELMET,POS_CHEST,POS_LEG,POS_BOOTS,POS_RIGHTHAND,POS_LEFTHAND,POS_ITEM1,POS_ITEM2]
    for pos in positions:
        pygame.draw.rect(surface, "white", (pos[0], pos[1], EQUIPS_RECT_SIDE, EQUIPS_RECT_SIDE), 3, 5)
    
    #pygame.draw.line(surface, "white", (POS_RIGHTHAND[0] + EQUIPS_RECT_SIDE/2, POS_RIGHTHAND[1]), (POS_HELMET[0], POS_HELMET[1] + EQUIPS_RECT_SIDE/2), 3)

    #gold_text = TEXT_FONT.render()

    return None

# ====== Class Inventory ======
class Inventory:
    def __init__(self):
        self.in_inventory = False
        self.back_text = TITLE_FONT.render("Back", True, "white")
        self.back_text_rect = self.back_text.get_rect(bottomright = (MAIN_BOX_POS[0] + MAIN_BOX_SIZE[0] - PADDING - HIGHLIGHT_SIGN_SIZE[0], MAIN_BOX_POS[1] + MAIN_BOX_SIZE[1] - PADDING))

    def inventory(self, player):
        boxes = Boxes()
        running = True
        while running:
            # ------ Loop Variables ------
            mouse_pos = screen.get_mouse()

            # ------ Screen ------
            BASE_SURFACE.fill(0)
            boxes.inventory_box(BASE_SURFACE)
            boxes.equips_box(BASE_SURFACE)
            boxes.stats_box(BASE_SURFACE)
            boxes.draw_mainbox()
            special_highlight(BASE_SURFACE, TITLE_FONT, "Back", self.back_text_rect)

            # ------ Inventory Items List ------
            for item_pos in range(len(player.inventory)):
                item_text = TEXT_FONT.render(player.inventory[item_pos], True, 0)
                item_text_rect = item_text.get_rect(topleft=(MAIN_BOX_POS[0] + PADDING, MINOR_BOX_TITLE_HEIGHT + PADDING + (item_pos * GAMETEXT_HEIGHT)))
                highlight(BASE_SURFACE, TEXT_FONT, player.inventory[item_pos], item_text_rect)
            
            # ------ Stats ------
            bars(BASE_SURFACE, player)
            attributes(BASE_SURFACE, player)
            conditions_rects = conditions(BASE_SURFACE, player)
            equips(BASE_SURFACE, player)

            # ------ Window Blit ------
            if game_state.ongame_state == "inventory": blit_surface(BASE_SURFACE)

            # ------ Detectando Eventos ------
            for event in pygame.event.get():
                # ------ Check Basic Events ------
                basic_events(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                # ------ Quit Inventory ------
                    if self.back_text_rect.collidepoint(mouse_pos):
                        self.in_inventory = False
                        running = False
                
            # ------ Check if in Inventory Yet ------
            if game_state.ongame_state != "inventory":
                self.in_inventory = False
                running = False

        return None

    def inventory_mouse_over(self, mouse_pos):
        # ------ Rectangles ------
        inventory_rect = pygame.Rect(INVENTORY_POS[0], INVENTORY_POS[1], MINOR_BOX_SIZE[0], MINOR_BOX_SIZE[1])

        # ------ Checking Collidepoint ------
        if inventory_rect.collidepoint(mouse_pos):
            return "inventory"
