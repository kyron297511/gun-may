import pygame
import settings
import controls

# aliases
Vector = pygame.math.Vector2
Sprite = pygame.sprite.Sprite


class Player(Sprite):
    """A class for players."""

    def __init__(self, controls: controls.KeyboardControl, spawn_point: tuple, color: tuple) -> None:
        """
        Initializes the Player object.

        Parameters:
        controls (KeyboardControl): player keyboard control settings.
        spawn_point (tuple): coordinates (x, y) where player will be created.
        color (tuple): values (R, G, B) that represent the player's color.
        """
        super().__init__()
        self.set_image(color)
        self.set_vectors(spawn_point)
        self.set_rect()

        self.spawn_point = spawn_point
        self.controls = controls
        self.falling = True
        self.standing = False

    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def set_vectors(self, spawn_point):
        self.pos = Vector(spawn_point)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    def set_image(self, color):
        self.image = pygame.Surface((20, 40))
        self.image.fill(color)

    def update(self):
        self.update_acc()
        self.apply_friction()
        self.update_velocity()
        self.update_position()

    def update_position(self):
        # update position
        # Δd = v_2Δt - (1/2)aΔt^2, Δt = 1 tick -> Δd = v_2 - 0.5a
        self.pos += self.vel - 0.5 * self.acc
        # update location of sprite
        self.rect.midbottom = self.pos
        self.falling = self.vel.y > 0

    def update_velocity(self):
        # update new velocity
        # v_2 = v_1 + aΔt, Δt = 1 tick -> v_2 = v_1 + a
        self.vel += self.acc
        if abs(self.vel.x) > settings.PLAYER_MAX_VEL:
            if self.vel.x < 0:
                self.vel.x = -settings.PLAYER_MAX_VEL
            else:
                self.vel.x = settings.PLAYER_MAX_VEL

    def apply_friction(self):
        if self.vel.x != 0:
            # check direcition of velocity
            if self.vel.x < 0:
                self.acc.x -= settings.PLAYER_FRICTION
            else:
                self.acc.x += settings.PLAYER_FRICTION
        '''
        # model horizontal friction as proportional to velocity (similar to fluid resistance)
        # this will result in a logarithmic shape of velocity/time graph
        # maximum speed can thus be limited in a smooth way
        # F_net = ma, m = 1 unit -> a = F_applied + F_friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        '''

    def update_acc(self):
        self.acc = Vector(0, settings.PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[self.controls.LEFT]:
            self.acc.x = -settings.PLAYER_ACC
        elif keys[self.controls.RIGHT]:
            self.acc.x = settings.PLAYER_ACC

    def jump(self):
        if self.standing:
            self.vel.y = settings.PLAYER_JUMP_HEIGHT

    def respawn(self):
        self.pos = self.spawn_point


class Platform(Sprite):
    """A class for platforms."""

    def __init__(self, coordinates: tuple, dimensions: tuple, color=settings.GREEN) -> None:
        """
        Initializes the Platform object.

        Parameters:
        coordinates (tuple): coordinates (x, y) representing the center of the platform.
        dimensions (tuple): values (width, height). 
        Optional: color (tuple): values (R, G, B).
        """
        super().__init__()
        self.set_image(dimensions, color)
        self.set_rect(coordinates)

    def set_rect(self, coordinates):
        self.rect = self.image.get_rect()
        self.rect.center = coordinates

    def set_image(self, dimensions, color):
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)


class Bullet(Sprite):
    def __init__(self, velocity, coordinates):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coordinates
