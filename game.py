import pygame as pg
from settings import *
from sprites import *
from controls import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new Game
        self.players = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

        self.add_platforms()
        self.add_players()
        self.run()

    def add_platforms(self):
        """Creates and adds platforms to self.platforms and self.all_sprites."""
        for p in PLATFORM_LIST:
            self.platforms.add(Platform(*p, PLATFORM_COLOR))
            self.all_sprites.add(Platform(*p, PLATFORM_COLOR))

    def add_players(self):
        """Creates and adds the players to self.players and self.all_sprites."""
        self.player_1 = Player(
            PLAYER_1_CONTROLS,
            PLAYER_1_SPAWN_POINT,
            PLAYER_1_COLOR
            )
        self.player_2 = Player(
            PLAYER_2_CONTROLS,
            PLAYER_2_SPAWN_POINT,
            PLAYER_2_COLOR
            )
        self.players.add(self.player_1)
        self.players.add(self.player_2)
        self.all_sprites.add(self.player_1)
        self.all_sprites.add(self.player_2)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                for player in self.players:
                    c = player.controls
                    if event.key == c.UP:
                        player.jump()

    def update(self):
        self.all_sprites.update()
        for player in self.players:
            hits = pg.sprite.spritecollide(player, self.platforms, False)
            if hits:
                platform = hits[0]
                if player.falling:
                    player.standing = True
                    player.pos.y = platform.rect.top + 1  # keep in collision
                    player.vel.y = 0
            else:
                player.standing = False

    def render(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def quit(self):
        pg.quit()

