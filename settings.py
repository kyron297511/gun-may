from pygame.locals import *

# game settings
TITLE = "Gun Mayhem"
HEIGHT = 480
WIDTH = 720
FPS = 30

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# platform settings
PLATFORM_COLOR = GREEN
PLATFORM_LIST = [
    ((WIDTH / 2, HEIGHT - 100), (WIDTH - 200, 20)),
    ((150, HEIGHT - 200), (200, 20)),
    ((WIDTH - 150, HEIGHT - 200), (200, 20))
    ]

# player properties
PLAYER_ACC = 0.85
PLAYER_MAX_VEL = 4
PLAYER_FRICTION = -0.25
PLAYER_GRAVITY = 0.3
PLAYER_JUMP_HEIGHT = -8
PLAYER_ANIMATION_FPS = 10
PLAYER_OFFSET = 9

# player 1 properties
PLAYER_1_COLOR = "green"
PLAYER_1_SPAWN_POINT = (WIDTH - 100, 0)

# player 1 controls
PLAYER_1_UP = K_UP
PLAYER_1_DOWN = K_DOWN
PLAYER_1_LEFT = K_LEFT
PLAYER_1_RIGHT = K_RIGHT

# player 2 properties
PLAYER_2_COLOR = "red"
PLAYER_2_SPAWN_POINT = (100, 0)

# player 2 controls
PLAYER_2_UP = K_w
PLAYER_2_DOWN = K_s
PLAYER_2_LEFT = K_a
PLAYER_2_RIGHT = K_d


