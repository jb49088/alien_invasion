# TODO: implement smooth movement for the laser

import pygame
from pygame.sprite import Sprite


class UFOLaser(Sprite):
    """A class to manage lasers fired from UFO's."""

    def __init__(self, ai_game, ufo):
        """Create a laser."""
        super().__init__()
        self.screen = ai_game.screen
        self.ufo = ufo
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.color = self.settings.ufo_laser_color

        # Create the laser rect
        self.laser_rect = pygame.Rect(
            0, 0, self.settings.laser_width, self.settings.laser_height
        )
        self.laser_rect.midtop = self.ufo.rect.midbottom

        self.y = float(self.laser_rect.y)

    def update(self):
        """Move the lasers down the screen."""
        # Update y-position
        self.y += self.settings.ufo_laser_speed

        self.laser_rect.y = int(self.y)

    def draw_lasers(self):
        """Draw the laser to the screen."""
        pygame.draw.rect(self.screen, self.color, self.laser_rect)
