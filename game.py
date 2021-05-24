import os
import sys
import pygame
import settings
import sprites
import spritesheet
import controls
import json


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
                coordinates,
                dimensions,
                settings.PLATFORM_COLOR)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def parse_json(self, file_path) -> "list[pygame.Rect]":
        with open(file_path) as f:
            data = json.load(f)
        frame_names = tuple(data["frames"].keys())

        rect_list = []
        for frame_name in frame_names:
            dimensions = data["frames"][frame_name]["frame"]
            x, y, w, h = dimensions["x"], dimensions["y"], dimensions["w"], dimensions["h"]
            rect_list.append(pygame.Rect(x, y, w, h))

        return rect_list

    def get_player_animations(self, color: str) -> sprites.Animation:
        idle_frames = self.get_frames(color, "idle")
        run_frames = self.get_frames(color, "run")
        jump_frames = self.get_frames(color, "jump")
        animation = sprites.Animation(idle_frames, run_frames, jump_frames)
        return animation

    def get_frames(self, color: str, animation_name: str) -> "list[pygame.Surface]":
        image = pygame.image.load(
            "assets/player/{}/{}.png".format(color, animation_name))
        sheet = spritesheet.Spritesheet(image)
        rect_list = self.parse_json(
            "assets/player/{}.json".format(animation_name))
        frames = sheet.get_images(rect_list)
        return frames

    def add_players(self):
        """Creates and adds the players to self.players and self.all_sprites."""

        player_1_animations = self.get_player_animations("green")
        player_2_animations = self.get_player_animations("red")

        self.player_1 = sprites.Player(
            controls.PLAYER_1_CONTROLS,
            settings.PLAYER_1_SPAWN_POINT,
            player_1_animations
        )
        self.player_2 = sprites.Player(
            controls.PLAYER_2_CONTROLS,
            settings.PLAYER_2_SPAWN_POINT,
            player_2_animations
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
            # elif event.type == pygame.KEYDOWN:
            #     for player in self.players:
            #         if event.key == player.controls.UP:
            #             player.jump()

    def update(self):
        self.all_sprites.update()
        for player in self.players:
            hits = pygame.sprite.spritecollide(
                player, self.platforms, False, pygame.sprite.collide_rect)
            if hits:
                platform = hits[0]
                if player.falling and player.pos.y <= platform.rect.top + 10:
                    player.vel.y = 0
                    player.standing = True
                    # offset due to sprite feet being 9 px from the bottom of the image
                    player.pos.y = platform.rect.top + 9
                    
                    
            else:
                player.standing = False

    def render(self):
        self.screen.fill(settings.BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
