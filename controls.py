from settings import *

class KeyboardControl:
    def __init__(self, up, down, left, right):
        self.UP = up
        self.DOWN = down
        self.LEFT = left
        self.RIGHT = right

PLAYER_1_CONTROLS = KeyboardControl(
    PLAYER_1_UP,
    PLAYER_1_DOWN,
    PLAYER_1_LEFT,
    PLAYER_1_RIGHT
)

PLAYER_2_CONTROLS = KeyboardControl(
    PLAYER_2_UP,
    PLAYER_2_DOWN,
    PLAYER_2_LEFT,
    PLAYER_2_RIGHT
)