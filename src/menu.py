import pygame.font

from button import Button
from ship import Ship
from ufo import UFO


class Menu:
    """A class to display objects on the menu."""

    def __init__(self, ai_game):
        """Initialize menu attributes."""
        self.ai_game = ai_game  # Store reference to main game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.title = ai_game.settings.title
        self.text_color = (102, 255, 102)
        self.font = pygame.font.SysFont(None, 96)

        self._prep_ui_elements()

    def _prep_ui_elements(self):
        # Prepare the title image
        self._prep_title()
        # Prepare the ship image
        self._prep_ship()
        # Prepare the ufo image
        self._prep_ufo()
        # Prepare the dual lasers
        self._prep_dual_lasers()
        # Create buttons
        self._create_buttons()

    def _create_buttons(self):
        """Create play button and difficulty buttons."""
        # Create play button
        self.play_button = Button(
            self.ai_game,
            msg="Play",
            width=200,
            height=50,
            button_color=(102, 255, 102),
            text_color=(0, 0, 0),
            font_size=48,
        )

        # Create difficulty buttons
        difficulty_data = [
            ("Easy", (102, 255, 102)),
            ("Medium", (255, 165, 0)),
            ("Hard", (255, 0, 0)),
        ]

        start_y = 450
        spacing = 50

        self.difficulty_buttons = []

        for i, (label, color) in enumerate(difficulty_data):
            button = Button(
                self.ai_game,
                msg=label,
                width=200,
                height=30,
                button_color=color,
                text_color=(0, 0, 0),
                font_size=30,
                centery=start_y + i * spacing,
            )
            self.difficulty_buttons.append(button)

    def check_play_button(self, mouse_pos):
        """Check if play button was clicked."""
        return self.play_button.rect.collidepoint(mouse_pos)

    def check_difficulty_buttons(self, mouse_pos):
        """Check if a difficulty button was clicked and return the difficulty."""
        for button in self.difficulty_buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.msg == "Easy":
                    return 1.1
                elif button.msg == "Medium":
                    return 1.2
                elif button.msg == "Hard":
                    return 1.3
        return None

    def _draw_difficulty_indicator(self, button):
        """Draw indicator for selected difficulty."""
        check_rect = pygame.Rect(button.rect.right - 15, button.rect.top + 5, 10, 10)
        pygame.draw.rect(self.screen, (0, 0, 0), check_rect)

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
        ship = Ship(self.ai_game)
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
        ufo = UFO(self.ai_game)
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
        """Draw the title, ship, UFO, dual laser, and buttons to the screen."""
        # Draw menu elements
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.ship_image, self.ship_rect)
        self.screen.blit(self.ufo_image, self.ufo_rect)
        pygame.draw.rect(
            self.screen, self.settings.ship_laser_color, self.left_laser_rect
        )
        pygame.draw.rect(
            self.screen, self.settings.ship_laser_color, self.right_laser_rect
        )

        # Draw buttons
        self.play_button.draw_button()

        # Draw difficulty buttons with indicators
        speed_mapping = {"Easy": 1.1, "Medium": 1.2, "Hard": 1.3}
        for button in self.difficulty_buttons:
            button.draw_button()
            if speed_mapping.get(button.msg) == self.settings.speedup_scale:
                self._draw_difficulty_indicator(button)
