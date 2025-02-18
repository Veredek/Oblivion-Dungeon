import pygame

# ========== Tree ==========
from src.config import config
from src.classes import screen, game_state
from src.functions import functions, s
from src.equipaments import EQUIPAMENTS
from src.boxes import boxes

# ========== Functions ==========

# ========== (inventory) ==========
class Inventory:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        self.in_inventory = False
        self.EQUIPS_RECT_SIDE = 100

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # ----|1|---- Font ----|1|----
    @property
    def HPMPXP_FONT(self):
        return pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", s(35))
    @property
    def PLUS_FONT(self):
        return pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", s(30))
    @property
    def ATTRIBUTES_FONT(self):
        return pygame.font.Font(r"game\assets\fonts\FancyCardText.ttf", s(50))
    
    # ----|1|---- Text ----|1|----
    @property
    def BACK_TEXT(self):
        return config.title_font.render("Back", True, "white")
    @property
    def PLUS_TEXT(self):
        return self.PLUS_FONT.render(" + ", True, "white",)
    
    # ----|1|---- Height & Width ----|1|----
    @property
    def ATTRIBUTES_TEXT_HEIGHT(self):
        return self.ATTRIBUTES_FONT.render("sample", True, 0).get_size()[1]
    @property
    def ATTRIBUTES_TEXT_MAXWIDTH(self):
        return self.ATTRIBUTES_FONT.render(" fort ", True, 0).get_width()
    @property
    def VALUE_MAXWIDTH(self):
        return self.ATTRIBUTES_FONT.render(" 000 ", True, 0).get_width()    
    
    # ----|1|---- Size ----|1|----
    @property
    def ATTRIBUTES_SIZE(self):
        return (self.ATTRIBUTES_FONT.render(" fort  000 ", True, "white").get_width(), 5*self.ATTRIBUTES_TEXT_HEIGHT)
    
    # ----|1|---- Positions ----|1|----
    @property
    def POS_HELMET(self):
        return (boxes.equips_pos[0] + boxes.minor_box_size[0]/2 - self.EQUIPS_RECT_SIDE/2, boxes.equips_pos[1] + boxes.minor_box_title_height + config.padding)
    @property
    def POS_CHEST(self):
        return (self.POS_HELMET[0], self.POS_HELMET[1] + self.EQUIPS_RECT_SIDE + s(30))
    @property
    def POS_LEG(self):
        return (self.POS_CHEST[0], self.POS_CHEST[1] + self.EQUIPS_RECT_SIDE + s(30))
    @property
    def POS_BOOTS(self):
        return (self.POS_LEG[0], self.POS_LEG[1] + self.EQUIPS_RECT_SIDE + s(30))
    @property
    def POS_RIGHTHAND(self):
        return (self.POS_CHEST[0] - self.EQUIPS_RECT_SIDE - s(30), self.POS_CHEST[1])
    @property
    def POS_LEFTHAND(self):
        return (self.POS_CHEST[0] + self.EQUIPS_RECT_SIDE + s(30), self.POS_CHEST[1])
    @property
    def POS_ITEM1(self):
        return (self.POS_LEG[0] - self.EQUIPS_RECT_SIDE - s(30), self.POS_LEG[1])
    @property
    def POS_ITEM2(self):
        return (self.POS_LEG[0] + self.EQUIPS_RECT_SIDE + s(30), self.POS_LEG[1])
    @property
    def ATTRIBUTES_POS(self):
        return (boxes.stats_pos[0] + (boxes.minor_box_size[0] - config.padding)/2 - (self.ATTRIBUTES_SIZE[0] + self.PLUS_TEXT.get_width() + 5),
                        boxes.minor_box_title_height + 2*config.padding + 3*self.HPMPXP_FONT.render("Sample", True, "white").get_height())
    @property
    def CONDITIONS_POS(self):
        return (boxes.stats_pos[0] + config.padding, self.ATTRIBUTES_POS[1] + self.ATTRIBUTES_SIZE[1] + config.padding)
    @property
    def STR_POS(self):
        return (self.ATTRIBUTES_POS)
    
    # ~~~~~~~~~~ Inventory ~~~~~~~~~~
    # ----|1|---- Rectangles ----|1|----
    @property
    def BACK_TEXT_RECT(self):
        return self.BACK_TEXT.get_rect(bottomright = (config.main_box_pos[0] + config.main_box_size[0] - config.padding - config.highlight_sign_size[0],
                                                      config.main_box_pos[1] + config.main_box_size[1] - config.padding))
    
    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # ----|1|---- HPMPXP ----|1|----
    def bars(self, surface, player):
        for type in ["HP", "MP", "EXP"]:
            # ------ HP ------
            if type == "HP":
                hp_height = self.HPMPXP_FONT.render("HP", True, "White").get_size()[1]
                # ------ HP TEXT ------
                hp_text = self.HPMPXP_FONT.render("HP", True, "White")
                hp_text_rect = hp_text.get_rect(topleft=(boxes.stats_pos[0] + config.padding, boxes.minorbox_title_height + config.padding ))
                surface.blit(hp_text, hp_text_rect)

                # ------ HP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 - 4,
                                                    boxes.minorbox_title_height + config.padding + hp_height*1/2 - 4 - 4,
                                                    boxes.minorbox_size[0]*0.65 + 4 + 4 + 1,
                                                    10 + 4 + 4), 2)
                pygame.draw.line(surface, "Green", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175,
                                                    boxes.minorbox_title_height + config.padding + hp_height*1/2),(boxes.stats_pos[0] + boxes.minorbox_size[0]*0.825, boxes.minorbox_title_height + config.padding + hp_height*1/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minorbox_size[0]/2, boxes.minorbox_title_height + config.padding + hp_height/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["HP"]}/{player.stats["MAX_HP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

            # ------ MP ------
            if type == "MP":
                mp_height = self.self.HPMPXP_FONT.render("MP", True, "White").get_size()[1]
                # ------ MP TEXT ------
                mp_text = self.HPMPXP_FONT.render("MP", True, "White")
                mp_text_rect = mp_text.get_rect(topleft=(boxes.stats_pos[0] + config.padding, boxes.minor_box_title_height + config.padding + mp_height))
                surface.blit(mp_text, mp_text_rect)

                # ------ MP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minor_box_size[0]*0.175 - 4, boxes.minor_box_title_height + config.padding + mp_height*3/2 - 4 - 4, boxes.minor_box_size[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
                pygame.draw.line(surface, "royalblue", (boxes.stats_pos[0] + boxes.minor_box_size[0]*0.175, boxes.minor_box_title_height + config.padding + mp_height*3/2), (boxes.stats_pos[0] + boxes.minor_box_size[0]*0.825, boxes.minor_box_title_height + config.padding + mp_height*3/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minor_box_size[0]/2, boxes.minor_box_title_height + config.padding + mp_height*3/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["MP"]}/{player.stats["MAX_MP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

            # ------ EXP ------
            if type == "EXP":
                exp_height = self.HPMPXP_FONT.render("EXP", True, "White").get_size()[1]
                exp_percent = player.stats["EXP"] / player.stats["MAX_EXP"]
                # ------ EXP TEXT ------
                exp_text = self.HPMPXP_FONT.render("EXP", True, "White")
                exp_text_rect = exp_text.get_rect(topleft=(boxes.stats_pos[0] + config.padding, boxes.minorbox_title_height + config.padding + 2*exp_height))
                surface.blit(exp_text, exp_text_rect)

                # ------ EXP BAR ------
                pygame.draw.rect(surface, "White", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 - 4, boxes.minorbox_title_height + config.padding + exp_height*5/2 - 4 - 4, boxes.minorbox_size[0]*0.65 + 4 + 4 + 1,  10 + 4 + 4), 2)
                if exp_percent > 0:
                    pygame.draw.line(surface, "goldenrod", (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175, boxes.minorbox_title_height + config.padding + exp_height*5/2), (boxes.stats_pos[0] + boxes.minorbox_size[0]*0.175 + (boxes.minorbox_size[0]*0.65 * exp_percent), boxes.minorbox_title_height + config.padding + exp_height*5/2), 10)

                numbers_text = self.HPMPXP_FONT.render(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", True, "White")
                numbers_text_rect= numbers_text.get_rect(center=(boxes.stats_pos[0] + boxes.minorbox_size[0]/2, boxes.minorbox_title_height + config.padding + exp_height*5/2 - 4))
                surface.blit(functions.glowing_text(f"{player.stats["EXP"]}/{player.stats["MAX_EXP"]}", self.HPMPXP_FONT, "White", "Black", 2), numbers_text_rect)

    # ------ Attributes ------
    def attributes(self, surface, player):
        mouse_pos = screen.get_mouse()

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
        rect_pos = (self.ATTRIBUTES_POS[0] + self.ATTRIBUTES_SIZE[0] + (self.PLUS_TEXT.get_width() + 5) + config.padding, self.ATTRIBUTES_POS[1] + (self.ATTRIBUTES_SIZE[1] - rect_size[1])/2)

        surface.blit(points_text, points_text.get_rect(midtop=(rect_pos[0] + rect_size[0]/2, rect_pos[1])))
        surface.blit(clear_text, clear_text.get_rect(midtop=(rect_pos[0] + (1/4)*rect_size[0], rect_pos[1] + points_text.get_height())))
        surface.blit(apply_text, apply_text.get_rect(midtop=(rect_pos[0] + (3/4)*rect_size[0], rect_pos[1] + points_text.get_height())))

        pygame.draw.rect(surface, "white", (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]), 2)
        pygame.draw.line(surface, "white", (rect_pos[0], rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0] -1, rect_pos[1] + points_text.get_height()), 2)
        pygame.draw.line(surface, "white", (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height()), (rect_pos[0] + rect_size[0]/2, rect_pos[1] + points_text.get_height() + applyclear_text.get_height() -1), 2)

    # ------ Conditions ------
    def conditions(self, surface, player):
        mouse_pos = screen.get_mouse()

        conditions_text = config.text_font.render("Conditions: ", True, "white")
        conditions_text_rect = conditions_text.get_rect(topleft=(self.CONDITIONS_POS[0], self.CONDITIONS_POS[1]))
        surface.blit(conditions_text, conditions_text_rect)

        conditions_rects = []
        for condition in player.conditions:
            condition_text = config.text_font.render(condition, True, "white")
        return conditions_rects

    # ------ Equips ------
    def equips(self, surface, player):
        positions = [self.POS_HELMET,self.POS_CHEST,self.POS_LEG,self.POS_BOOTS,self.POS_RIGHTHAND,self.POS_LEFTHAND,self.POS_ITEM1,self.POS_ITEM2]
        for pos in positions:
            pygame.draw.rect(surface, "white", (pos[0], pos[1], self.EQUIPS_RECT_SIDE, self.EQUIPS_RECT_SIDE), 3, 5)
        
        #pygame.draw.line(surface, "white", (POS_RIGHTHAND[0] + self.EQUIPS_RECT_SIDE/2, POS_RIGHTHAND[1]), (self.POS_HELMET[0], self.POS_HELMET[1] + self.EQUIPS_RECT_SIDE/2), 3)

        #gold_text = config.text_font.render()

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
            # ------ Loop Variables ------
            mouse_pos = pygame.mouse.get_pos()

            # ------ Screen ------
            screen.base_surface.fill(0)
            boxes.inventory_box(screen.base_surface)
            boxes.equips_box(screen.base_surface)
            boxes.stats_box(screen.base_surface)
            boxes.draw_mainbox()
            functions.highlight(screen.base_surface, config.title_font, "Back", self.BACK_TEXT_RECT)

            # ------ Inventory Items List ------
            for item_pos in range(len(player.inventory)):
                item_text = config.text_font.render(player.inventory[item_pos], True, 0)
                item_text_rect = item_text.get_rect(topleft=(config.main_box_pos[0] + config.padding, boxes.minorbox_title_height + config.padding + (item_pos * config.title_height)))
                functions.highlight(screen.base_surface, config.text_font, player.inventory[item_pos], item_text_rect)
            
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

        return None

inventory = Inventory()