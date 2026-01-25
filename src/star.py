import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a single star in the cluster."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.color = self.settings.star_color

        # Create star rect using settings
        self.rect = pygame.Rect(
            0, 0, self.settings.star_width, self.settings.star_height
        )

        # Start each star near top left
        self.rect.x, self.rect.y = self.rect.width, self.rect.height

    def draw_star(self):
        """Draw the star to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
