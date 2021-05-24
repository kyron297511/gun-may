import pygame
import settings
import controls
import itertools

# aliases
Vector = pygame.math.Vector2
Sprite = pygame.sprite.Sprite


class Animation():
    """A class for player animations."""

    def __init__(self, idle: tuple[pygame.Surface], run: tuple[pygame.Surface], jump: tuple[pygame.Surface]):
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

        self.spawn_direction = direction
        self.direction = direction

        self.spawn_point = spawn_point
        self.controls = controls
        self.falling = True
        self.standing = False

        self.animation_tick = itertools.cycle(
            range(settings.FPS//settings.PLAYER_ANIMATION_FPS))

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

        if self.pos.y > settings.VOID_HEIGHT:
            self.respawn()

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

        # fixes perpetual running
        if abs(self.vel.x) < 0.4:
            self.vel.x = 0

    def apply_friction(self):
        # model friction as proportional to player speed
        # this limits max speed
        self.acc.x += self.vel.x * settings.PLAYER_FRICTION

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
        self.direction = self.spawn_direction
        self.vel.x, self.vel.y = 0, 0


class Platform(Sprite):
    """A class for platforms."""

    def __init__(self, image: pygame.Surface, coordinates: tuple, tile_count: int) -> None:
        """
        Initializes the Platform object.

        Parameters:
        image (pygame.Surface): a surface representing one tile.
        coordinates (tuple): (x, y) representing the center of the platform.
        tile_count (int): number of tiles the platform contains.
        """
        super().__init__()
        self.count = tile_count

        h = image.get_height()
        w = image.get_width()

        self.create_surface(h, w)
        self.blit_tiles(image, w)

        self.set_rect(coordinates)
        self.mask = pygame.mask.from_surface(self.image)

    def create_surface(self, h: int, w: int):
        width = w * self.count
        self.image = pygame.Surface((width, h))
        self.image.fill((255, 0, 0))

    def blit_tiles(self, image: pygame.Surface, w: int):
        x = 0
        for i in range(self.count):
            self.image.blit(image, (x, 0))
            x += w

    def set_rect(self, coordinates: tuple):
        self.rect = self.image.get_rect()
        self.rect.center = coordinates


class Bullet(Sprite):
    """A class for bullets."""
    def __init__(self, player_pos: tuple, x_vel: int, image: pygame.Surface, author: object) -> None:
        """
        Initializes the Bullet object.

        Parameters:
        player_pos (tuple): the position of the player when the bullet was fired.
        x_vel (int): the velocity of the bullet.
        image (pygame.Surface): the image of the bullet.
        author (object): the player who fired the bullet.
        """
        super().__init__()
        self.author = author

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

        self.set_vectors(player_pos, x_vel)
        self.set_rect()

    def set_vectors(self, player_pos: tuple, x_vel: int) -> None:
        player_x, player_y = player_pos
        x_offset, y_offset = self.get_offset(x_vel)

        self.pos = Vector(player_x + x_offset, player_y + y_offset)
        self.vel = Vector(x_vel, 0)

    def get_offset(self, x_vel: int) -> tuple:
        x_offset = settings.BULLET_OFFSET_X
        y_offset = settings.BULLET_OFFSET_Y
        # check if player was moving
        if abs(x_vel) > settings.BULLET_SPEED:
            # add additonal offset due to change in height
            y_offset += settings.ADDITIONAL_BULLET_OFFSET
        if x_vel < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            x_offset *= -1  # flip x-offset
        return (x_offset, y_offset)

    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def update(self):
        self.pos.x += self.vel.x
        self.rect.center = self.pos

        # check if outside of screen
        if not (0 <= self.pos.x <= settings.WIDTH):
            self.kill()  # delete from all groups
