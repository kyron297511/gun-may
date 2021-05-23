import os
import pygame
import settings
import sprites
import spritesheet
import controls


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # start a new Game
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.add_platforms()
        self.add_players()
        self.run()

    def add_platforms(self):
        """Creates and adds platforms to self.platforms and self.all_sprites."""
        for platform_attributes in settings.PLATFORM_LIST:
            coordinates, dimensions = platform_attributes
            platform = sprites.Platform(
                coordinates, dimensions, settings.PLATFORM_COLOR)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def add_players(self):
        """Creates and adds the players to self.players and self.all_sprites."""
        file_path = "assets/player/green/Gunner_Green_Idle.png"
        image = pygame.image.load(file_path).convert_alpha()
        sheet = spritesheet.Spritesheet(image)
        player_1_idle = sheet.get_image(pygame.Rect(0,0,48,48))
        self.player_1 = sprites.Player(
            controls.PLAYER_1_CONTROLS,
            settings.PLAYER_1_SPAWN_POINT,
            sprites.Animation(player_1_idle)
        )
        self.player_2 = sprites.Player(
            controls.PLAYER_2_CONTROLS,
            settings.PLAYER_2_SPAWN_POINT,
            sprites.Animation(player_1_idle)
        )
        self.players.add(self.player_1)
        self.players.add(self.player_2)
        self.all_sprites.add(self.player_1)
        self.all_sprites.add(self.player_2)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                for player in self.players:
                    c = player.controls
                    if event.key == c.UP:
                        player.jump()

    def update(self):
        self.all_sprites.update()
        for player in self.players:
            hits = pygame.sprite.spritecollide(player, self.platforms, False)
            if hits:
                platform = hits[0]
                if player.falling:
                    player.standing = True
                    player.pos.y = platform.rect.top + 1  # keep in collision
                    player.vel.y = 0
            else:
                player.standing = False

    def render(self):
        self.screen.fill(settings.WHITE)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
