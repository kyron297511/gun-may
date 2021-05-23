import settings

class KeyboardControl:
    def __init__(self, up, down, left, right):
        self.UP = up
        self.DOWN = down
        self.LEFT = left
        self.RIGHT = right

PLAYER_1_CONTROLS = KeyboardControl(
    settings.PLAYER_1_UP,
    settings.PLAYER_1_DOWN,
    settings.PLAYER_1_LEFT,
    settings.PLAYER_1_RIGHT
)

PLAYER_2_CONTROLS = KeyboardControl(
    settings.PLAYER_2_UP,
    settings.PLAYER_2_DOWN,
    settings.PLAYER_2_LEFT,
    settings.PLAYER_2_RIGHT
)