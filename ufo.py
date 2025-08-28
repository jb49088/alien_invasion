import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    """A class to represent a single UFO in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Load the UFO image and rect
        self.image = pygame.image.load("images/ufo.png")
        self.rect = self.image.get_rect()

        # Start each UFO near top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store x-position as float for smooth movement
        self.x = float(self.rect.x)
