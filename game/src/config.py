import pygame
from screeninfo import get_monitors, Monitor

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

    MAX_RESOLUTION = (int(max_width), int(max_heigth))

    print(f"Game Max Resolution: {MAX_RESOLUTION}")
    return MAX_RESOLUTION

# ========== (config) ==========
class Config:
    # ~~~~~~~~~~ Init ~~~~~~~~~~
    def __init__(self):
        # region ----|1|---- Game Title
        self.GAME_TITLE = "Oblivion Dungeon"
            # endregion
        # region ----|1|---- Monitor
        self._monitor_index = get_monitor_index()
        self._monitor = get_monitors()[self._monitor_index]
        self.base_of_proportion = get_base_of_prop(self._monitor)
        self._monitor_scale = get_monitor_scale(self._monitor_index)
            # endregion        
        # region ----|1|---- Screen
        self.BASE_WIDTH = 1920
        self.BASE_HEIGHT = 1080 
        self.SCREEN_SIZE = (self._monitor.width, self._monitor.height)
        self.MAX_RESOLUTION = get_maxresolution(self._monitor, self._monitor_index, self._monitor_scale)
        self.min_resolution = (int(854 / self._monitor_scale),
                               int(480 / self._monitor_scale))
            # endregion
        # region ----|1|---- Padding
        self.PADDING = 20
            #endregion
        # region ----|1|---- Typing Speed
        self.TYPING_SPEED = 50  # Caracteres por segundo   
            # endregion
        # region ----|1|---- Font
        self.TITLE_FONT = pygame.font.Font(r"game\assets\fonts\Iglesia.ttf", 65)
        
        self.TEXT_FONT = pygame.font.Font(r"game\assets\fonts\Mirage final.ttf", 45)

        self.GAMENAME_FONT = pygame.font.Font(r"game\assets\fonts\RoyalInitialen.ttf", 140)

        self.HIGHLIGHT_SIGN = pygame.font.Font(r"game\assets\fonts\BLKCHCRY.TTF", 50)
            # endregion
        # region ----|1|---- Font Height
        self.TITLE_HEIGHT = self.TITLE_FONT.size("Text Sample")[1]

        self.TEXT_HEIGHT = self.TEXT_FONT.size("Text Sample")[1]
            # endregion
        # region ----|1|---- Font Width
        self.name_length = self.TITLE_FONT.size(12 * "#")[0]
            # endregion
        # region ----|1|---- MainBox
        self.MAINBOX_SIZE = (0.9 * self.BASE_WIDTH,
                              self.TEXT_HEIGHT * 4 + 2 * self.PADDING)
        self.MAINBOX_POS = ((self.BASE_WIDTH - self.MAINBOX_SIZE[0]) / 2,
                             0.7 * self.BASE_HEIGHT)     
            # endregion
        # region ----|1|---- Size
        self.HIGHLIGHT_SIGN_SIZE = self.HIGHLIGHT_SIGN.render("+", True, "Yellow").get_size()
            # endregion
        # region ----|1|---- Center
        self.ENEMY_CENTER = (self.BASE_WIDTH / 2,
                             self.BASE_HEIGHT / 3)
            # endregion
        # region ----|1|---- Game Width/Height
        self._game_width = self.MAX_RESOLUTION[0]
        self._game_height = self.MAX_RESOLUTION[1]
            # endregion
        # region ----|1|---- Display Update
        self.display_update = False
            # endregion

    # ~~~~~~~~~~ Properties ~~~~~~~~~~
    # region ----|1|---- Width/Height

    # region ----|2|---- Width
    @property
    def game_width(self):
        return self._game_width
    
    @game_width.setter
    def game_width(self, value):
        """
        Auto updates game height, to not do so, use (value, "only")
        """

        flag = False # init flag
        if isinstance(value, tuple): # if value is tuple
            flag = value[1]
            value = value[0]

        if value >= self.MAX_RESOLUTION[0]:    self._game_width = self.MAX_RESOLUTION[0]
        elif value > self.min_resolution[0]:    self._game_width = value
        elif value <= self.min_resolution[0]:    self._game_width = self.min_resolution[0]

        if flag != "only":
            self._game_height = int(self._game_width / (16/9))

        self.display_update = True
        # endregion

    # region ----|2|---- Height
    @property
    def game_height(self):
        return self._game_height

    @game_height.setter
    def game_height(self, value):
        """
        Auto updates game width, to not do so, use (value, "only")
        """
        
        flag = False # init flag
        if isinstance(value, tuple): # if value is tuple
            flag = value[1]
            value = value[0]

        if value >= self.MAX_RESOLUTION[1]:    self._game_height = self.MAX_RESOLUTION[1]
        elif value > self.min_resolution[1]:    self._game_height = value
        elif value <= self.min_resolution[1]:    self._game_height = self.min_resolution[1]

        if flag != "only":
            self._game_width = int(self._game_height * (16/9))

        self.display_update = True
        # endregion

    # endregion

    # region ----|1|---- Resolution
    @property
    def resolution(self):
        """
        (game_width, game_height)
        """
        return (self._game_width, self.game_height)
        # endregion
    
    # region ----|1|---- Scale
    @property
    def scale(self):
        """
        Scale visuals based on current resolution
        """
        
        return min(self._game_width / self.BASE_WIDTH, self._game_height / self.BASE_HEIGHT)
        # endregion

    # ~~~~~~~~~~ Functions ~~~~~~~~~~
    # region ----|1|---- Monitor Change
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
        self.MAX_RESOLUTION = get_maxresolution(self._monitor, self._monitor_index, self._monitor_scale)

        return None
        # endregion

config = Config()