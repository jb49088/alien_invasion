import sys

import pygame

from dual_laser import DualLaser
from settings import Settings
from ship import Ship
from ufo import UFO


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("alien_invasion")
        self.ship = Ship(self)
        self.dual_lasers = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_dual_lasers()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_dual_lasers()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_dual_lasers(self):
        """Create a new dual laser and add it to the dual lasers group."""
        if len(self.dual_lasers) < self.settings.dual_laser_limit:
            new_dual_laser = DualLaser(self)
            self.dual_lasers.add(new_dual_laser)

    def _update_dual_lasers(self):
        """Update the position of dual lasers and get rid of old dual lasers."""
        # Update dual laser positions
        self.dual_lasers.update()

        # Remove lasers that have moved offscreen
        for laser in self.dual_lasers.copy():
            if laser.left_rect.bottom <= 0 or laser.right_rect.bottom <= 0:
                self.dual_lasers.remove(laser)

    def _create_fleet(self):
        """Create the fleet of UFO's."""
        # Create a UFO and keep doing so until there is no room.
        # Spacing between UFO's is one UFO width.
        ufo = UFO(self)
        ufo_width = ufo.rect.width

        current_x = ufo_width
        while current_x < (self.settings.screen_width - 2 * ufo_width):
            new_ufo = UFO(self)
            new_ufo.x = current_x
            new_ufo.rect.x = current_x
            self.ufos.add(new_ufo)
            current_x += 2 * ufo_width

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for laser in self.dual_lasers.sprites():
            laser.draw_lasers()
        self.ship.blitme()
        self.ufos.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
