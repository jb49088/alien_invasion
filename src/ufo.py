import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    """A class to represent a single UFO in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the UFO image and rect
        self.image = pygame.image.load("images/ufo.png")
        self.rect = self.image.get_rect()

        # Start each UFO near top left
        self.rect.x, self.rect.y = self.rect.width, self.rect.height

        # Store x-position as float for smooth movement
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if UFO is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (
            self.rect.left <= screen_rect.left
        )

    def update(self):
        """Move the UFO right or left."""
        self.x += self.settings.ufo_speed * self.settings.fleet_direction
        self.rect.x = self.x
