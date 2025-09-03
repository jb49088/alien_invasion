import sys
from random import randint
from time import sleep

import pygame

from button import Button
from dual_laser import DualLaser
from game_stats import GameStats
from settings import Settings
from ship import Ship
from star import Star
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
        self.stats = GameStats(self)
        pygame.display.set_caption("alien_invasion")
        self.ship = Ship(self)
        self.stars = pygame.sprite.Group()
        self.dual_lasers = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self._create_fleet()
        self._create_cluster()
        self.game_active = False
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._event_loop()

            if self.game_active:
                self.ship.update()
                self._update_dual_lasers()
                self._update_ufos()

            self._update_screen()
            self.clock.tick(self.settings.framerate)

    def _event_loop(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining lasers and UFO's
            self.dual_lasers.empty()
            self.ufos.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

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

        self._check_dual_lasers_ufo_collisions()

    def _check_dual_lasers_ufo_collisions(self):
        """Respond to laser-ufo collisions."""
        # Check for any lasers that have hit aliens.
        for laser in self.dual_lasers.copy():
            hit_ufos = []
            for ufo in self.ufos.copy():
                if laser.left_rect.colliderect(
                    ufo.rect
                ) or laser.right_rect.colliderect(ufo.rect):
                    hit_ufos.append(ufo)

            if hit_ufos:
                self.dual_lasers.remove(laser)
                for ufo in hit_ufos:
                    self.ufos.remove(ufo)

        if not self.ufos:
            # Destroy existing lasers and create new fleet.
            self.dual_lasers.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of UFO's."""
        # Create a UFO and keep doing so until there is no room
        # Spacing between UFO's is one UFO width and one UFO height
        ufo = UFO(self)
        ufo_width, ufo_height = ufo.rect.size

        current_x, current_y = ufo_width, ufo_height
        while current_y < (self.settings.screen_height - 5 * ufo_height):
            while current_x < (self.settings.screen_width - 2 * ufo_width):
                self._create_ufo(current_x, current_y)
                current_x += 2 * ufo_width

            # Finished a row: reset x value, and increment y value
            current_x = ufo_width
            current_y += 2 * ufo_height

    def _create_ufo(self, x_position, y_position):
        """Create a UFO and place it in the fleet."""
        new_ufo = UFO(self)
        new_ufo.x = x_position
        new_ufo.rect.x = x_position
        new_ufo.rect.y = y_position
        self.ufos.add(new_ufo)

    def _check_fleet_edges(self):
        """Respond appropriately if any UFO's have reached the edge."""
        for ufo in self.ufos.sprites():
            if ufo.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for ufo in self.ufos.sprites():
            ufo.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_ufos(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.ufos.update()

        # Look for ufo-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.ufos):  # type: ignore
            self._ship_hit()

        # Look for aliens hitthing the bottom of the screen
        self._check_ufos_bottom()

    def _check_ufos_bottom(self):
        """Check if any UFO's have reaches the bottom of the screen."""
        for ufo in self.ufos.sprites():
            if ufo.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _create_cluster(self):
        """Create the cluster of stars."""
        # Create stars in a grid pattern with 20-pixel spacing
        current_x, current_y = 0, 0
        while current_y < self.settings.screen_height:
            while current_x < self.settings.screen_width:
                self._create_star(current_x, current_y)
                current_x += 20

            # Finished a row: reset x value, and increment y value
            current_x = 0
            current_y += 20

    def _create_star(self, x_position, y_position):
        """Create a star with a random offset and place it in the cluster."""
        new_star = Star(self)

        random_x_offset = randint(-10, 10)
        random_y_offset = randint(-10, 10)

        new_star.rect.x = x_position + random_x_offset
        new_star.rect.y = y_position + random_y_offset
        self.stars.add(new_star)

    def _ship_hit(self):
        """Respond to the ship being hit by a UFO."""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens
            self.dual_lasers.empty()
            self.ufos.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for laser in self.dual_lasers.sprites():
            laser.draw_lasers()
        for star in self.stars.sprites():
            star.draw_star()
        self.ship.blitme()
        self.ufos.draw(self.screen)
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
