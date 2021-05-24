import pygame
import settings
import controls
import itertools

# aliases
Vector = pygame.math.Vector2
Sprite = pygame.sprite.Sprite


class Animation():
    def __init__(self, idle: "tuple[pygame.Surface]", run: "tuple[pygame.Surface]", jump: "tuple[pygame.Surface]"):
        self.idle = itertools.cycle(idle)
        self.run = itertools.cycle(run)
        self.jump = jump


class Player(Sprite):
    """A class for players."""

    def __init__(self, controls: controls.KeyboardControl, spawn_point: tuple, animation: Animation, direction="right") -> None:
        """
        Initializes the Player object.

        Parameters:
        controls (KeyboardControl): player keyboard control settings.
        spawn_point (tuple): coordinates (x, y) where player will be created.
        animations (Animation): contains images that represent the player's visual appearance.
        """
        super().__init__()
        self.animation = animation
        self.set_image()
        self.set_vectors(spawn_point)
        self.set_rect()
        self.set_mask()

        self.direction = direction

        self.spawn_point = spawn_point
        self.controls = controls
        self.falling = True
        self.standing = False

        self.animation_tick = itertools.cycle(range(settings.FPS//settings.PLAYER_ANIMATION_FPS))

    def set_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def set_vectors(self, spawn_point):
        self.pos = Vector(spawn_point)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    def set_image(self):
        self.image = next(self.animation.idle)

    def update(self):
        self.handle_keys()
        self.apply_friction()
        self.update_velocity()
        self.update_position()
        self.update_image()
        self.set_mask()

    def update_image(self):
        if not self.standing:
            if self.falling:
                self.image = self.animation.jump[0]
            else:
                self.image = self.animation.jump[1]
            self.flip_if_necessary()
        else:
            if next(self.animation_tick) == 0:
                if self.vel.x == 0:
                    self.image = next(self.animation.idle)
                else:
                    self.image = next(self.animation.run)
                self.flip_if_necessary()

    def flip_if_necessary(self):
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)


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
        # glitch fix
        if abs(self.vel.x) < 0.3:
            self.vel.x = 0

        if self.vel.x != 0:
            # check direcition of velocity
            if self.vel.x < 0:
                self.acc.x -= settings.PLAYER_FRICTION
            else:
                self.acc.x += settings.PLAYER_FRICTION

    def handle_keys(self):
        self.acc = Vector(0, settings.PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[self.controls.UP] and self.standing:
            self.vel.y = settings.PLAYER_JUMP_HEIGHT
            self.standing = False
        if keys[self.controls.LEFT]:
            self.acc.x = -settings.PLAYER_ACC
            self.direction = "left"
        elif keys[self.controls.RIGHT]:
            self.acc.x = settings.PLAYER_ACC
            self.direction = "right"

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
        self.mask = pygame.mask.from_surface(self.image)

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
