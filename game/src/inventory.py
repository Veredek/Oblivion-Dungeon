import pygame

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions
from src.equipaments import EQUIPAMENTS
from src.Boxes import boxes

# ========== Functions ==========

# ========== (inventory) ==========
class Inventory:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        self.in_inventory = False
        self.EQUIPS_RECT_SIDE = 100
        # region ----|1|---- Font
        self.HPMPXP_FONT = pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", 35)

        self.PLUS_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 30)

        self.ATTRIBUTES_FONT = pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", 50)
            # endregion
        # region ----|1|---- Text
        self.BACK_TEXT = config.TITLE_FONT.render("Back", True, "white")

        self.PLUS_TEXT = self.PLUS_FONT.render(" + ", True, "white")
            # endregion
        # region ----|1|---- Height & Width
        self.ATTRIBUTES_TEXT_HEIGHT = self.ATTRIBUTES_FONT.render("sample", True, 0).get_height()
        self.ATTRIBUTES_TEXT_MAXWIDTH = self.ATTRIBUTES_FONT.render(" fort ", True, 0).get_width()
        self.VALUE_MAXWIDTH = self.ATTRIBUTES_FONT.render(" 000 ", True, 0).get_width()   
            # endregion
        # region ----|1|---- Size
        def ATTRIBUTES_SIZE(self):
            return (self.ATTRIBUTES_FONT.render(" fort  000 ", True, "white").get_width(), 5*self.ATTRIBUTES_TEXT_HEIGHT)

            # endregion
    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    
    # ----|1|---- Positions ----|1|----
    @property
    def POS_HELMET(self):
        return (boxes.equips_pos[0] + boxes.minorbox_size[0]/2 - self.EQUIPS_RECT_SIDE/2, boxes.equips_pos[1] + boxes.minorbox_TITLE_HEIGHT + config.PADDING)
    @property
    def POS_CHEST(self):
        return (self.POS_HELMET[0], self.POS_HELMET[1] + self.EQUIPS_RECT_SIDE + 30)
    @property
    def POS_LEG(self):
        return (self.POS_CHEST[0], self.POS_CHEST[1] + self.EQUIPS_RECT_SIDE + 30)
    @property
    def POS_BOOTS(self):
        return (self.POS_LEG[0], self.POS_LEG[1] + self.EQUIPS_RECT_SIDE + 30)
    @property
    def POS_RIGHTHAND(self):
        return (self.POS_CHEST[0] - self.EQUIPS_RECT_SIDE - 30, self.POS_CHEST[1])
    @property
    def POS_LEFTHAND(self):
        return (self.POS_CHEST[0] + self.EQUIPS_RECT_SIDE + 30, self.POS_CHEST[1])
    @property
    def POS_ITEM1(self):
        return (self.POS_LEG[0] - self.EQUIPS_RECT_SIDE - 30, self.POS_LEG[1])
    @property
    def POS_ITEM2(self):
        return (self.POS_LEG[0] + self.EQUIPS_RECT_SIDE + 30, self.POS_LEG[1])
    @property
    def ATTRIBUTES_POS(self):
        return (boxes.stats_pos[0] + (boxes.minorbox_size[0] - config.PADDING)/2 - (self.ATTRIBUTES_SIZE[0] + self.PLUS_TEXT.get_width() + 5),
                        boxes.minorbox_TITLE_HEIGHT + 2*config.PADDING + 3*self.HPMPXP_FONT.render("Sample", True, "white").get_height())
    @property
    def CONDITIONS_POS(self):
        return (boxes.stats_pos[0] + config.PADDING, self.ATTRIBUTES_POS[1] + self.ATTRIBUTES_SIZE[1] + config.PADDING)
    @property
    def STR_POS(self):
        return (self.ATTRIBUTES_POS)
    
    # ~~~~~~~~~~ Inventory ~~~~~~~~~~
    # ----|1|---- Rectangles ----|1|----
    @property
    def BACK_TEXT_RECT(self):
        return self.BACK_TEXT.get_rect(bottomright = (config.MAINBOX_POS[0] + config.MAINBOX_SIZE[0] - config.PADDING - config.HIGHLIGHT_SIGN_SIZE[0],
                                                      config.MAINBOX_POS[1] + config.MAINBOX_SIZE[1] - config.PADDING))
    
    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # ----|1|---- HPMPXP ----|1|----
    def bars(self, surface, player):
        for type in ["HP", "MP", "EXP"]:
            # ------ HP ------
            if type == "HP":
                hp_height = self.HPMPXP_FONT.render("HP", True, "White").get_size()[1]
                # ------ HP TEXT ------
                hp_text = self.HPMPXP_FONT.render("HP", True, "White")
                hp_text_rect = hp_text.get_rect(topleft=(boxes.stats_pos[0] + config.PADDING, boxes.minorbox_TITLE_HEIGHT + config.PADDING ))
                surface.blit(hp_text, hp_text_rect)

                # ------ HP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 - 4,
                                                    boxes.minorbox_TITLE_HEIGHT + config.PADDING + hp_height*1/2 - 4 - 4,
                                                    boxes.minorbox_size[0]*0.65 + 4 + 4 + 1,
                                                    10 + 4 + 4), 2)
                pygame.draw.line(surface, "Green", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175,
                                                    boxes.minorbox_TITLE_HEIGHT + config.PADDING + hp_height*1/2),(boxes.stats_pos[0] + boxes.minorbox_size[0]*0.825, boxes.minorbox_TITLE_HEIGHT + config.PADDING + hp_height*1/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minorbox_size[0]/2, boxes.minorbox_TITLE_HEIGHT + config.PADDING + hp_height/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

            # ------ MP ------
            if type == "MP":
                mp_height = self.HPMPXP_FONT.render("MP", True, "White").get_size()[1]
                # ------ MP TEXT ------
                mp_text = self.HPMPXP_FONT.render("MP", True, "White")
                mp_text_rect = mp_text.get_rect(topleft=(boxes.stats_pos[0] + config.PADDING, boxes.minorbox_TITLE_HEIGHT + config.PADDING + mp_height))
                surface.blit(mp_text, mp_text_rect)

                # ------ MP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 - 4, boxes.minorbox_TITLE_HEIGHT + config.PADDING + mp_height*3/2 - 4 - 4, boxes.minorbox_size[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
                pygame.draw.line(surface, "royalblue", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175, boxes.minorbox_TITLE_HEIGHT + config.PADDING + mp_height*3/2), (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.825, boxes.minorbox_TITLE_HEIGHT + config.PADDING + mp_height*3/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minorbox_size[0]/2, boxes.minorbox_TITLE_HEIGHT + config.PADDING + mp_height*3/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

            # ------ EXP ------
            if type == "EXP":
                exp_height = self.HPMPXP_FONT.render("EXP", True, "White").get_size()[1]
                exp_percent = player.stats["EXP"] / player.stats["MAX_EXP"]
                # ------ EXP TEXT ------
                exp_text = self.HPMPXP_FONT.render("EXP", True, "White")
                exp_text_rect = exp_text.get_rect(topleft=(boxes.stats_pos[0] + config.PADDING, boxes.minorbox_TITLE_HEIGHT + config.PADDING + 2*exp_height))
                surface.blit(exp_text, exp_text_rect)

                # ------ EXP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 - 4, boxes.minorbox_TITLE_HEIGHT + config.PADDING + exp_height*5/2 - 4 - 4, boxes.minorbox_size[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
                if exp_percent > 0:
                    pygame.draw.line(surface, "goldenrod", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175, boxes.minorbox_TITLE_HEIGHT + config.PADDING + exp_height*5/2), (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 + (boxes.minorbox_size[0]*0.65 * exp_percent), boxes.minorbox_TITLE_HEIGHT + config.PADDING + exp_height*5/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minorbox_size[0]/2, boxes.minorbox_TITLE_HEIGHT + config.PADDING + exp_height*5/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

    # ------ Attributes ------
    def attributes(self, surface, player):
        mouse_pos = screen.mouse

        pygame.draw.rect(surface, "white", (self.ATTRIBUTES_POS[0],
                                            self.ATTRIBUTES_POS[1],
                                            self.ATTRIBUTES_SIZE[0],
                                            self.ATTRIBUTES_SIZE[1]),
                                            2)
        
        # ATTRIBUTES BLIT
        attributes_list = ["STR", "DEX", "WIS", "FORT", "RES"]
        colors = ["red", "green", "royalblue", "sienna", "magenta"]
        for i in range(len(attributes_list)):
            # ATTRIBUTES TEXT
            attribute_text = self.ATTRIBUTES_FONT.render(f" {attributes_list[i]} ".lower(), True, colors[i])
            attribute_text_rect = attribute_text.get_rect(midtop=(self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_TEXT_MAXWIDTH/2,
                                                                  self.ATTRIBUTES_POS[1] + i*self.ATTRIBUTES_TEXT_HEIGHT))
            surface.blit(attribute_text, attribute_text_rect)

            # ATTRIBUTES VALUE
            attribute_value = self.ATTRIBUTES_FONT.render(f" {player.stats[attributes_list[i]]} ", True, "white")
            attribute_value_rect = attribute_value.get_rect(midtop=(self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_TEXT_MAXWIDTH + self.VALUE_MAXWIDTH/2, self.ATTRIBUTES_POS[1] + i*self.ATTRIBUTES_TEXT_HEIGHT))
            surface.blit(attribute_value, attribute_value_rect)

            # PLUS SIGN
            plus_rect = self.PLUS_TEXT.get_rect(midleft=(self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_SIZE[0] + 5, self.ATTRIBUTES_POS[1] + self.PLUS_TEXT.get_height() + i*self.ATTRIBUTES_TEXT_HEIGHT))
            pygame.draw.rect(surface, "white" if plus_rect.collidepoint(mouse_pos) else "darkgray", plus_rect, 2)
            functions.highlight(surface, self.PLUS_FONT, " + ", plus_rect)

            # INTERNAL LINES BLIT
            pygame.draw.line(surface, "white", (self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_TEXT_MAXWIDTH, self.ATTRIBUTES_POS[1]), (self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_TEXT_MAXWIDTH, self.ATTRIBUTES_POS[1] + self.ATTRIBUTES_SIZE[1] -1), 2)
            pygame.draw.line(surface, "white", (self.ATTRIBUTES_POS[0], self.ATTRIBUTES_POS[1] + i*self.ATTRIBUTES_TEXT_HEIGHT), (self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_SIZE[0] -1, self.ATTRIBUTES_POS[1] + i*self.ATTRIBUTES_TEXT_HEIGHT), 2)

        # POINTS BLIT
        points_text = self.ATTRIBUTES_FONT.render(f" points: {player.stats["attributes points"]} ", True, "white",)
        applyclear_text = self.ATTRIBUTES_FONT.render(" clear   apply ", True, "white")
        clear_text = self.ATTRIBUTES_FONT.render("clear", True, "white")
        apply_text = self.ATTRIBUTES_FONT.render("apply", True, "white")

        rect_size = (applyclear_text.get_width(), points_text.get_height() + applyclear_text.get_height())
        rect_pos = (self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_SIZE[0] + (self.PLUS_TEXT.get_width() + 5) + config.PADDING, self.ATTRIBUTES_POS[1] + (self.ATTRIBUTES_SIZE[1] - rect_size[1])/2)

        surface.blit(points_text, points_text.get_rect(midtop=(rect_pos[0] + rect_size[0]/2, rect_pos[1])))
        surface.blit(clear_text, clear_text.get_rect(midtop=(rect_pos[0] + (1/4)*rect_size[0], rect_pos[1] + points_text.get_height())))
        surface.blit(apply_text, apply_text.get_rect(midtop=(rect_pos[0] + (3/4)*rect_size[0], rect_pos[1] + points_text.get_height())))

        pygame.draw.rect(surface, "white", (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]), 2)
        pygame.draw.line(surface, "white", (rect_pos[0], rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0] -1, rect_pos[1] + points_text.get_height()), 2)
        pygame.draw.line(surface, "white", (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height() + applyclear_text.get_height() -1), 2)

    # ------ Conditions ------
    def conditions(self, surface, player):
        mouse_pos = screen.mouse

        conditions_text = config.TEXT_FONT.render("Conditions: ", True, "white")
        conditions_text_rect = conditions_text.get_rect(topleft=(self.CONDITIONS_POS[0], self.CONDITIONS_POS[1]))
        surface.blit(conditions_text, conditions_text_rect)

        conditions_rects = []
        for condition in player.conditions:
            condition_text = config.TEXT_FONT.render(condition, True, "white")
        return conditions_rects

    # ------ Equips ------
    def equips(self, surface, player):
        positions = [self.POS_HELMET,self.POS_CHEST,self.POS_LEG,self.POS_BOOTS,self.POS_RIGHTHAND,self.POS_LEFTHAND,self.POS_ITEM1,self.POS_ITEM2]
        for pos in positions:
            pygame.draw.rect(surface, "white", (pos[0], pos[1], self.EQUIPS_RECT_SIDE, self.EQUIPS_RECT_SIDE), 3, 5)
        
        #pygame.draw.line(surface, "white", (POS_RIGHTHAND[0] + self.EQUIPS_RECT_SIDE/2, POS_RIGHTHAND[1]), (self.POS_HELMET[0], self.POS_HELMET[1] + self.EQUIPS_RECT_SIDE/2), 3)

        #gold_text = config.TEXT_FONT.render()

        return None


    def inventory_mouse_over(self, mouse_pos):
        # ------ Rectangles ------
        inventory_rect = pygame.Rect(boxes.inventory_pos[0], boxes.inventory_pos[1], boxes.minor_box_size[0], boxes.minor_box_size[1])

        # ------ Checking Collidepoint ------
        if inventory_rect.collidepoint(mouse_pos):
            return "inventory"    

    # ~~~~~~~~~~ Inventory ~~~~~~~~~~
    def inventory(self, player):
        running = True
        while running:
            clock = pygame.time.Clock()
            # ------ Loop Variables ------
            mouse_pos = screen.mouse

            # ------ Screen ------
            screen.clear_surfaces()
            boxes.inventory_box(screen.base_surface)
            boxes.equips_box(screen.base_surface)
            boxes.stats_box(screen.base_surface)
            boxes.draw_mainbox()
            functions.highlight(screen.base_surface, config.TITLE_FONT, "Back", self.BACK_TEXT_RECT)

            # ------ Inventory Items List ------
            for item_pos in range(len(player.inventory)):
                item_text = config.TEXT_FONT.render(player.inventory[item_pos], True, 0)
                item_text_rect = item_text.get_rect(topleft=(config.MAINBOX_POS[0] + config.PADDING, boxes.minorbox_TITLE_HEIGHT + config.PADDING + (item_pos * config.TITLE_HEIGHT)))
                functions.highlight(screen.base_surface, config.TEXT_FONT, player.inventory[item_pos], item_text_rect)
            
            # ------ Stats ------
            self.bars(screen.base_surface, player)
            self.attributes(screen.base_surface, player)
            conditions_rects = self.conditions(screen.base_surface, player)
            self.equips(screen.base_surface, player)

            # ------ Window Blit ------
            if game_state.ongame_state == "inventory": screen.blit_surface(screen.base_surface)

            # ------ Detectando Eventos ------
            for event in pygame.event.get():
                # ------ Check Basic Events ------
                functions.basic_events(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                # ------ Quit Inventory ------
                    if self.BACK_TEXT_RECT.collidepoint(mouse_pos):
                        self.in_inventory = False
                        running = False
                
            # ------ Check if in Inventory Yet ------
            if game_state.ongame_state != "inventory":
                self.in_inventory = False
                running = False

            # ----|1|---- Clock ----|1|----
            clock.tick(60)

        return None

inventory = Inventory()