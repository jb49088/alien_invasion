import pygame
from pygame.sprite import Sprite


class DualLaser(Sprite):
    """A class to manage dual lasers fired simultaneously from the ship."""

    def __init__(self, ai_game):
        """Create dual laser objects at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.dual_laser_color

        # Create left laser rect
        self.left_rect = pygame.Rect(
            0, 0, self.settings.dual_laser_width, self.settings.dual_laser_height
        )
        self.left_rect.midtop = (
            ai_game.ship.rect.midtop[0] - 5,  # 5 pixels left of ship's midtop
            ai_game.ship.rect.midtop[1],
        )

        # Create right laser rect
        self.right_rect = pygame.Rect(
            0, 0, self.settings.dual_laser_width, self.settings.dual_laser_height
        )
        self.right_rect.midtop = (
            ai_game.ship.rect.midtop[0] + 5,  # 5 pixels right of ship's midtop
            ai_game.ship.rect.midtop[1],
        )

        # Store shared y-position as float for smooth movement
        self.y = float(ai_game.ship.rect.midtop[1])

    def update(self):
        """Move the laser up the screen."""
        # Update y-position
        self.y -= self.settings.dual_laser_speed

        # Sync rect with y-position
        self.left_rect.y = int(self.y)
        self.right_rect.y = int(self.y)

    def draw_lasers(self):
        """Draw both lasers to the screen."""
        pygame.draw.rect(self.screen, self.color, self.left_rect)
        pygame.draw.rect(self.screen, self.color, self.right_rect)
