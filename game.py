import pygame
import settings
import sprites
import spritesheet
import controls
import json


class Game:
    def __init__(self):
        """Initializes pygame."""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        """Starts a new Gun Meyham game."""
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.load_images()
        self.add_platforms()
        self.add_players()
        self.run()

    def add_platforms(self):
        """Creates and adds platforms to self.platforms and self.all_sprites."""
        for platform_attributes in settings.PLATFORM_LIST:
            coordinates, tile_count = platform_attributes
            platform = sprites.Platform(
                self.platform_image,
                coordinates,
                tile_count
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def parse_spritesheet_json(self, file_path) -> list[pygame.Rect]:
        """Returns a list of pygame.Rect objects representing each individaul frame of the sprite sheet."""
        with open(file_path) as f:
            data = json.load(f)
        frame_names = tuple(data["frames"].keys())

        rect_list = []
        for frame_name in frame_names:
            dimensions = data["frames"][frame_name]["frame"]
            x, y, w, h = dimensions["x"], dimensions["y"], dimensions["w"], dimensions["h"]
            rect_list.append(pygame.Rect(x, y, w, h))

        return rect_list

    def get_player_animations(self, color: str = "black") -> sprites.Animation:
        """
        Generates and returns a Animation object based on input color.

        Parameters:
        color (str): the color of the player model. Must match file directory name.
        """

        idle_frames = self.get_frames(color, "idle")
        run_frames = self.get_frames(color, "run")
        jump_frames = self.get_frames(color, "jump")
        animation = sprites.Animation(idle_frames, run_frames, jump_frames)
        return animation

    def get_frames(self, color: str, animation_name: str) -> list[pygame.Surface]:
        """
        Returns a list of pygame.Surface objects based on input color and animation name.

        Parameters:
        color (str): the color of the player model. Must match file directory name.
        animation_name (str): the name of the animation (eg. "run"). Must match file name.
        """

        image = pygame.image.load(
            "assets/player/{}/{}.png".format(color, animation_name))
        sheet = spritesheet.Spritesheet(image)
        rect_list = self.parse_spritesheet_json(
            "assets/player/{}.json".format(animation_name))
        frames = sheet.get_frames(rect_list)
        return frames

    def add_players(self):
        """Creates and adds the players to self.players and self.all_sprites."""

        player_1_animations = self.get_player_animations(
            settings.PLAYER_1_COLOR)
        player_2_animations = self.get_player_animations(
            settings.PLAYER_2_COLOR)

        self.player_1 = sprites.Player(
            controls.PLAYER_1_CONTROLS,
            settings.PLAYER_1_SPAWN_POINT,
            player_1_animations,
            settings.PLAYER_1_SPAWN_DIRECTION,
            self.muzzle_flash
        )

        self.player_2 = sprites.Player(
            controls.PLAYER_2_CONTROLS,
            settings.PLAYER_2_SPAWN_POINT,
            player_2_animations,
            settings.PLAYER_2_SPAWN_DIRECTION,
            self.muzzle_flash
        )

        self.players.add(self.player_1)
        self.all_sprites.add(self.player_1)
        self.players.add(self.player_2)
        self.all_sprites.add(self.player_2)

    def run(self):
        """Starts the game loop."""
        self.playing = True
        while self.playing:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        """Handles pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                for player in self.players:
                    if event.key == player.controls.SHOOT:
                        self.fire_bullet(player)
                
                '''
                if event.key == settings.PLAYER_1_SHOOT:
                    self.add_bullet(self.player_1)
                    self.add_recoil(self.player_1)
                elif event.key == settings.PLAYER_2_SHOOT:
                    self.add_bullet(self.player_2)
                    self.add_recoil(self.player_2)
                '''

    def fire_bullet(self, player):
        player.shooting = True
        self.add_bullet(player)
        self.add_recoil(player)

    def add_recoil(self, player):
        if player.direction == "left":
            player.vel.x += settings.GUN_RECOIL
        else:
            player.vel.x += -settings.GUN_RECOIL

    def load_images(self):
        self.bullet_image = pygame.image.load(
            "assets/bullet/bullet.png").convert()
        self.platform_image = pygame.image.load(
            "assets/platform/platform.png").convert()
        self.background = pygame.image.load(
            "assets/background/night.png").convert()
        self.muzzle_flash = pygame.image.load(
            "assets/misc/muzzle_flash.png").convert_alpha()

    def add_bullet(self, player):
        x_vel = settings.BULLET_SPEED + player.vel.x
        if player.direction == "left":
            x_vel = -settings.BULLET_SPEED + player.vel.x
        bullet = sprites.Bullet(player.pos, x_vel, self.bullet_image, player)

        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def update(self):
        self.all_sprites.update()
        self.handle_collisions()

    def handle_collisions(self):
        for player in self.players:
            platform_collisions = pygame.sprite.spritecollide(
                player, self.platforms, False, pygame.sprite.collide_mask)
            if platform_collisions:
                platform = platform_collisions[0]
                if player.falling:
                    player.vel.y = 0
                    player.standing = True
                    # offset due to sprite feet being above the bottom of the image
                    player.pos.y = platform.rect.top + settings.PLAYER_OFFSET
            else:
                player.standing = False

            bullet_collisions = pygame.sprite.spritecollide(
                player, self.bullets, True, pygame.sprite.collide_mask)

            if bullet_collisions:
                bullet = bullet_collisions[0]
                if bullet.author != player:
                    player.vel.x += bullet.vel.x * settings.KNOCKBACK_MULTIPLIER

    def render(self):
        """Renders a single frame to the display."""
        self.screen.blit(self.background, (0, 0))

        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def quit(self):
        """Close pygame."""
        pygame.quit()
