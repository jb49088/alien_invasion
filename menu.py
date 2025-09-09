import pygame.font

from ship import Ship
from ufo import UFO


class Menu:
    """A class to display objects on the menu."""

    def __init__(self, ai_game):
        """Initialize menu attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.title = ai_game.settings.title

        self.text_color = (102, 255, 102)
        self.font = pygame.font.SysFont(None, 96)

        # Prepare the title image
        self._prep_title()

        # Prepare the ship image
        self._prep_ship()

        # Prepare the ufo image
        self._prep_ufo()

        # Prepare the dual lasers
        self._prep_dual_lasers()

    def _prep_title(self):
        """Turn the title into a rendered image."""
        title_str = self.title
        self.title_image = self.font.render(
            title_str, True, self.text_color, self.settings.bg_color
        )

        # Display the title
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.centery = self.settings.screen_height * (1 / 5)

    def _prep_ship(self):
        """Show a big ship facing left."""
        ship = Ship(self)

        # Scale the ship up for the menu
        scale_factor = 1.3
        self.ship_image = pygame.transform.scale(
            ship.image,
            (
                int(ship.rect.width * scale_factor),
                int(ship.rect.height * scale_factor),
            ),
        )

        # Rotate the ship
        rotation_angle = 90
        self.ship_image = pygame.transform.rotate(self.ship_image, rotation_angle)

        self.ship_rect = self.ship_image.get_rect()
        self.ship_rect.centerx = self.settings.screen_width * (2 / 3)
        self.ship_rect.centery = self.settings.screen_height * (1 / 3)

    def _prep_ufo(self):
        """Show a big ufo facing right."""
        ufo = UFO(self)

        scale_factor = 1.3
        self.ufo_image = pygame.transform.scale(
            ufo.image,
            (
                int(ufo.rect.width * scale_factor),
                int(ufo.rect.height * scale_factor),
            ),
        )
        rotation_angle = 90
        self.ufo_image = pygame.transform.rotate(self.ufo_image, rotation_angle)

        self.ufo_rect = self.ufo_image.get_rect()
        self.ufo_rect.centerx = self.settings.screen_width * (1 / 3)
        self.ufo_rect.centery = self.settings.screen_height * (1 / 3)

    def _prep_dual_lasers(self):
        """Show a big dual laser sideways."""
        x, y = self.settings.screen_width * 0.50, self.settings.screen_height * (1 / 3)
        width, height = 20, 2
        spacing = 7

        self.left_laser_rect = pygame.Rect(x, y - spacing, width, height)
        self.right_laser_rect = pygame.Rect(x, y + spacing, width, height)

    def draw_menu(self):
        """Draw the title, ship, UFO, and dual laser to the screen."""
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.ship_image, self.ship_rect)
        self.screen.blit(self.ufo_image, self.ufo_rect)

        pygame.draw.rect(
            self.screen, self.settings.dual_laser_color, self.left_laser_rect
        )
        pygame.draw.rect(
            self.screen, self.settings.dual_laser_color, self.right_laser_rect
        )
