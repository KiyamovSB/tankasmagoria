class Field:
    def __init__(self, pygame):
        self.pixel = 5
        self.small_x = 10 * self.pixel
        self.small_y = 10 * self.pixel
        self.big_x = 10 * self.small_x
        self.big_y = 10 * self.small_y
        self.tanks = []
        self.bullets = []

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (20, 20, 20)
        self.RED = (227,51,28)
        self.BlUE = (0,170,230)
        self.GREEN = (76,156,35)
        self.ORANGE = (255,165,0)
        self.PINK = (255, 192, 203)
        self.PURPLE = (170,27,221)

        self.sound_shot = pygame.mixer.Sound('sounds/shot.mp3')
        self.sound_explode = pygame.mixer.Sound('sounds/explode.mp3')
        self.sound_win = pygame.mixer.Sound('sounds/win.mp3')


