import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and rect
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        # Position ship at bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        # Store x-position as float for smooth movement
        self.x = float(self.rect.x)

        # Initialize movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update x-position
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # Sync rect with self.x
        self.rect.x = int(self.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
