import pygame as pg
from settings import *
from controls import *

# aliases
Vector = pg.math.Vector2
Sprite = pg.sprite.Sprite


class Player(Sprite):
    """A class for players. KeyboardControls object required to be passed through. Optionally pass through tuple: spawn_point (x, y) (default is the center of the screen), and tuple: color (R, G, B) (default is WHITE)."""
    def __init__(self, controls: KeyboardControl, spawn_point: tuple = (WIDTH / 2, HEIGHT / 2), color = WHITE) -> None:
        super().__init__()
        self.image = pg.Surface((20, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.pos = Vector(spawn_point)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        
        self.rect.midbottom = self.pos
        
        self.falling = True
        self.standing = False
        
        self.controls = controls
        
        self.spawn_point = spawn_point

    def update(self):
        self.acc = Vector(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[self.controls.LEFT]:
            self.acc.x = -PLAYER_ACC
        elif keys[self.controls.RIGHT]:
            self.acc.x = PLAYER_ACC
        
        '''
        if self.vel.magnitude() > 0:
            # apply friction
            # unit vector = (1/|v|) * v       
            self.acc += PLAYER_FRIC * (1 / self.vel.magnitude()) * self.vel
        '''

        # model horizontal friction as proportional to velocity (similar to fluid resistance)
        # this will result in a logarithmic shape of velocity/time graph
        # maximum speed can thus be limited in a smooth way

        # F_net = ma, m = 1 unit -> a = F_applied + F_friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # update position
        # Δd = v_1Δt + (1/2)aΔt^2, Δt = 1 tick -> Δd = v_1 + 0.5a
        self.pos += self.vel + 0.5 * self.acc

        # update new velocity
        # v_2 = v_1 + aΔt, Δt = 1 tick -> v_2 = v_1 + a
        self.vel += self.acc

        # update location of sprite
        self.rect.midbottom = self.pos

        self.falling = self.vel.y > 0
    
    def jump(self):
        if self.standing:
            self.vel.y = PLAYER_JUMP_HEIGHT

    def respawn(self):
        self.pos = self.spawn_point


class Platform(Sprite):
    """Class for platforms. Pass through tuple: coordinates (x, y) and tuple dimensions (width, height). Optioanlly pass through tuple: color (R, G, B). Platform will be generated with (x, y) as self.rect.center."""
    def __init__(self, coordinates: tuple, dimensions: tuple, color = GREEN) -> None:
        super().__init__()
        self.image = pg.Surface(dimensions)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = coordinates


class Bullet(Sprite):
    def __init__(self, velocity, coordinates):
        super().__init__()
        self.image = pg.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coordinates
