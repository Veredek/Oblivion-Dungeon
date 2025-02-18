import pygame
from screeninfo import get_monitors, Monitor

# ========== Tree ==========
    # --- Left Empty ---

# ========== Local Variables ==========
    # --- Left Empty ---

# ========== Functions ==========
def get_monitor_index():
    temp_window = pygame.display.set_mode((1,1), pygame.NOFRAME)
    monitors = get_monitors()
    for index, monitor in enumerate(monitors):
        # Verifica se a posição da janela está dentro dos limites do monitor
        if (monitor.x <= temp_window.get_width() < monitor.x + monitor.width and
            monitor.y <= temp_window.get_height() < monitor.y + monitor.height):
            pygame.display.quit()
            return index  # Retorna o índice do monitor

    # Se por acaso 
    pygame.display.quit()
    return 0

def get_monitor_scale(monitor_index : int):
    monitor = get_monitors()[monitor_index]
    temp_display = pygame.display.set_mode()
    scale =  monitor.width / temp_display.get_width()
    pygame.display.quit()
    print(f"scale:{scale}")
    return scale

def get_base_of_prop(monitor : Monitor):
    """
    se a tela for mais larga do que 16:9, terá barras pretas laterais,
    a altura (height) máxima da tela do display será a base para a resolução máxima.
    Vice-versa para telas mais estreitas que 16:9
    """

    screen_proportion = monitor.width / monitor.height

    if screen_proportion < (16/9):
        base_of_proportion = "width"

    elif screen_proportion >= (16/9):
        base_of_proportion = "height"

    return base_of_proportion

def get_maxresolution(monitor : Monitor, monitor_index : int, monitor_scale: float):
    #A proporção 16:9 está entre 1.7 e 1.8

    monitor = get_monitors()[monitor_index]

    # narrow screen
    if get_base_of_prop(monitor) == "width":         
        max_width = monitor.width / monitor_scale
        max_heigth = max_width / (16/9)

    # normal and wide screen
    elif get_base_of_prop(monitor) == "height":
        max_heigth = monitor.height / monitor_scale
        max_width = max_heigth * (16/9)

    max_resolution = (int(max_width), int(max_heigth))

    print(f"Game Max Resolution: {max_resolution}")
    return max_resolution


# ========== (config) ==========
class Config:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        # ----|1|---- Unmodifiable ----|1|----
        self.GAME_TITLE = "Oblivion Dungeon"

        self.SCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h) # Resolução com Escala DPI do Sistema

        self.BASE_HEIGHT = 1080 # Base to resolution scale
        self.TYPING_SPEED = 50  # Caracteres por segundo

        # ----|1|---- Modifiable ----|1|----
        self._monitor_index = get_monitor_index()
        self._monitor = get_monitors()[self._monitor_index]
        self.base_of_proportion = get_base_of_prop(self._monitor)
        self._monitor_scale = get_monitor_scale(self._monitor_index)

        self.screen_size = (int(self._monitor.width / self._monitor_scale),
                            int(self._monitor.height / self._monitor_scale))
        self.min_resolution = (int(854 / self._monitor_scale),
                               int(480 / self._monitor_scale))
        self.max_resolution = get_maxresolution(self._monitor, self._monitor_index, self._monitor_scale)

        self._game_width = self.max_resolution[0]
        self._game_height = self.max_resolution[1]

        self.display_update = False

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # ----|1|---- Width/Height ----|1|----

    # ----|2|---- Width ----|2|----
    @property
    def game_width(self):
        return self._game_width
    
    @game_width.setter
    def game_width(self, value):
        """
        Setter: auto updates game height
        """

        if value >= self.max_resolution[0]:    self._game_width = self.max_resolution[0]
        elif value > self.min_resolution[0]:    self._game_width = value
        elif value <= self.min_resolution[0]:    self._game_width = self.min_resolution[0]

        self._game_height = int(self._game_width / (16/9))

        self.display_update = True

    # ----|2|---- Height ----|2|----
    @property
    def game_height(self):
        return self._game_height

    @game_height.setter
    def game_height(self, value):
        """
        Setter: auto updates game width
        """
        if value >= self.max_resolution[1]:    self._game_height = self.max_resolution[1]
        elif value > self.min_resolution[1]:    self._game_height = value
        elif value <= self.min_resolution[1]:    self._game_height = self.min_resolution[1]

        self._game_width = int(self._game_height * (16/9))

        self.display_update = True

    # ----|1|---- Resolution ----|1|----
    @property
    def resolution(self):
        """
        (game_width, game_height)
        """
        return (self._game_width, self.game_height)
    
    @property
    def scale(self):
        """
        Scale visuals based on current resolution
        """
        scaled_height = self._game_height / self._monitor_scale
        return (scaled_height / self.BASE_HEIGHT)

    # ----|1|---- Font ----|1|----
    @property
    def title_font(self):
        return pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", round(self.scale * 65))
    
    @property
    def text_font(self):
        return pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", round(self.scale * 45))

    @property
    def gamename_font(self):
        return pygame.font.Font(r"game\assets\fonts\RoyalInitialen.ttf", round(self.scale * 140))

    @property
    def highlight_sign(self):
        return pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", round(self.scale * 50))

    # ----|1|---- Font Height ----|1|----
    @property
    def title_height(self):
        return self.title_font.size("Text Sample")[1]
    
    @property
    def text_height(self):
        return self.text_font.size("Text Sample")[1]
    
    # ----|1|---- Font Width ----|1|----
    @property
    def name_length(self):
        return self.title_font.size(12 * "#")[0]
    
    # ----|1|---- Padding ----|1|----
    @property
    def padding(self):
        return round(self.scale * 20)
    
    # ----|1|---- Size ----|1|----
    @property
    def highlight_sign_size(self):
        return self.highlight_sign.render("+", True, "Yellow").get_size()
    
    @property
    def main_box_size(self):
        return (0.9 * self.game_width,
                    self.text_height * 4 + 2 * self.padding)
    
    # ----|1|---- Center ----|1|----
    @property
    def enemy_center(self):
        center_x = self.game_width / 2
        center_y = self.game_height / 3
        return (center_x, center_y)

    # ----|1|---- Position ----|1|----
    @property
    def main_box_pos(self):
        x = (self.game_width - self.main_box_size[0]) / 2
        y = 0.7 * self.game_height
        return (x, y)

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    def monitor_change(self, new_index):
        """
        Updates config to new monitor
        """

        self._monitor_index = new_index
        self._monitor = get_monitors()[self._monitor_index]
        self.base_of_proportion = get_base_of_prop(self._monitor)
        self._monitor_scale = get_monitor_scale(self._monitor_index)

        self.screen_size = (int(self._monitor.width / self._monitor_scale),
                            int(self._monitor.height / self._monitor_scale))
        self.max_resolution = get_maxresolution(self._monitor, self._monitor_index, self._monitor_scale)

        return None

config = Config()