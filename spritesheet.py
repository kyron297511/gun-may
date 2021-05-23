import pygame

class Spritesheet:
    """A class for sprite sheets."""
    def __init__(self, surface: pygame.Surface):
        """
        Initializes the sprite sheet object.

        Parameters:
        surface (pygame.Surface) = surface containing the sprite sheet.
        """
        self.sheet = surface

    def get_image(self, rect: pygame.Rect, colorkey = (0,0,0)) -> pygame.Surface:
        """Returns a single pygame.Surface object from pygame.Rect input."""
        image = pygame.Surface(rect.size)
        image.set_colorkey(colorkey)
        image.blit(self.sheet, (0, 0), rect)
        return image

    def get_images(self, rects: tuple[pygame.Rect]) -> tuple[pygame.Surface]:
        """Returns a tuple of pygame.Surface objects from a input tuple of pygame.Rect."""
        return (self.get_image(rect) for rect in rects)
