import json
import sys
from pathlib import Path
from random import choice, randint
from time import sleep

import pygame

from game_stats import GameStats
from hud import HUD
from menu import Menu
from settings import Settings
from ship import Ship
from ship_lasers import ShipLasers
from star import Star
from ufo import UFO
from ufo_laser import UFOLaser


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
        pygame.display.set_caption(self.settings.title)
        self.high_score_file = Path("data/high_score.json")
        self.stats = GameStats(self)
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.ship = Ship(self)
        self.ship_lasers = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_lasers = pygame.sprite.Group()
        self.ufo_fire_counter = 0
        self.stars = pygame.sprite.Group()
        self._create_fleet()
        self._create_cluster()
        self.game_active = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._event_loop()

            if self.game_active:
                self.ship.update()
                self._update_ship_lasers()
                self._update_ufo_lasers()
                self._update_ufos()
                self._handle_ufo_fire_counter()

            self._update_screen()
            self.clock.tick(self.settings.framerate)

    def _event_loop(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._write_high_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_p and not self.game_active:
            self._start_game()
        elif event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_ship_lasers()
        elif event.key == pygame.K_q:
            self._write_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_buttons(self, mouse_pos):
        """Check for button clicks and handle them."""
        if not self.game_active:
            # Check play button
            if self.menu.check_play_button(mouse_pos):
                self._start_game()

            # Check difficulty buttons
            difficulty_speed = self.menu.check_difficulty_buttons(mouse_pos)
            if difficulty_speed:
                self.settings.speedup_scale = difficulty_speed

    def _write_high_score(self):
        self.high_score_file.write_text(json.dumps(self.stats.high_score))

    def _start_game(self):
        self.game_active = True

        # Reset the game settings
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics
        self.stats.reset_stats()

        # Reset the scoreboard
        self.hud.prep_score()

        # Reset the level
        self.hud.prep_level()

        # Reset the ship lives
        self.hud.prep_ships()

        # Get rid of any remaining lasers and UFO's
        self.ship_lasers.empty()
        self.ufos.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _handle_ufo_fire_counter(self):
        self.ufo_fire_counter += 1
        if self.ufo_fire_counter >= self.settings.ufo_fire_interval:
            self._fire_ufo_laser()
            self.ufo_fire_counter = 0

    def _fire_ufo_laser(self):
        """Create new UFO laser and add it to the UFO lasers group."""
        chosen_ufo = choice(self._get_bottom_most_ufos())

        new_ufo_laser = UFOLaser(self, chosen_ufo)
        self.ufo_lasers.add(new_ufo_laser)

    def _update_ufo_lasers(self):
        """Update the position of UFO lasers and get id of old lasers."""
        self.ufo_lasers.update()

        # Remove lasers that have moved offscreen
        for laser in self.ufo_lasers.copy():
            if laser.laser_rect.top >= self.settings.screen_height:
                self.ufo_lasers.remove(laser)

        self._check_ufo_laser_ship_collisions()

    def _check_ufo_laser_ship_collisions(self):
        for laser in self.ufo_lasers:
            if laser.laser_rect.colliderect(self.ship.rect):
                self._ship_hit()

    def _fire_ship_lasers(self):
        """Create new ship lasers and add them to the ship lasers group."""
        if len(self.ship_lasers) < self.settings.ship_laser_limit:
            new_dual_laser = ShipLasers(self)
            self.ship_lasers.add(new_dual_laser)

    def _update_ship_lasers(self):
        """Update the position of ship lasers and get rid of old lasers."""
        # Update dual laser positions
        self.ship_lasers.update()

        # Remove lasers that have moved offscreen
        for laser in self.ship_lasers.copy():
            if laser.left_rect.bottom <= 0 or laser.right_rect.bottom <= 0:
                self.ship_lasers.remove(laser)

        self._check_ship_laser_ufo_collisions()

    def _check_ship_laser_ufo_collisions(self):
        """Respond to laser-ufo collisions."""
        # Check for any lasers that have hit aliens.
        for laser in self.ship_lasers.copy():
            hit_ufos = []
            for ufo in self.ufos.copy():
                if laser.left_rect.colliderect(
                    ufo.rect
                ) or laser.right_rect.colliderect(ufo.rect):
                    hit_ufos.append(ufo)

            if hit_ufos:
                self.ship_lasers.remove(laser)
                for ufo in hit_ufos:
                    self.ufos.remove(ufo)
                    self.stats.score += self.settings.ufo_points
                self.hud.prep_score()
                self.hud.check_high_score()

        if not self.ufos:
            self._start_new_level()

    def _start_new_level(self):
        # Destroy existing lasers and create new fleet.
        self.ship_lasers.empty()
        self.ufo_lasers.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.hud.prep_level()

    def _create_fleet(self):
        """Create the fleet of UFO's."""
        # Create a UFO and keep doing so until there is no room
        # Spacing between UFO's is one UFO width and one UFO height
        ufo = UFO(self)
        ufo_width, ufo_height = ufo.rect.size

        current_x, current_y = ufo_width, ufo_height * 2
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

    def _get_bottom_most_ufos(self):
        """Return a list of the bottom-most UFO's in each column."""
        bottom_ufos = {}
        for ufo in self.ufos:
            column = ufo.rect.x
            # If this column is empty or this UFO is lower, replace it
            if column not in bottom_ufos or ufo.rect.y > bottom_ufos[column].rect.y:
                bottom_ufos[column] = ufo

        # Return only the UFO's one per column
        return list(bottom_ufos.values())

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

        # Look for aliens hitting the bottom of the screen
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
            self.hud.prep_ships()

            # Get rid of any remaining laser and UFO's
            self.ship_lasers.empty()
            self.ufo_lasers.empty()
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

        # Draw stars
        for star in self.stars.sprites():
            star.draw_star()

        if self.game_active:
            # Draw lasers, UFO's, ship and the HUD
            self.hud.draw_hud()
            self.ship.blitme()
            for laser in self.ship_lasers.sprites():
                laser.draw_lasers()
            self.ufos.draw(self.screen)
            for laser in self.ufo_lasers.sprites():
                laser.draw_lasers()
        else:
            # Menu handles drawing all buttons and menu elements
            self.menu.draw_menu()

        pygame.display.flip()


if __name__ == "__main__":
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
