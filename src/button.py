import pygame.font


class Button:
    """A class to build buttons for the game."""

    def __init__(
        self,
        ai_game,
        msg,
        width,
        height,
        button_color,
        text_color,
        font_size,
        active=False,
        centerx=None,
        centery=None,
    ):
        """Initialize button atributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.msg = msg
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)

        # Build the buttons rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Set position
        self.rect.center = self.screen_rect.center
        if centerx is not None:
            self.rect.centerx = centerx
        if centery is not None:
            self.rect.centery = centery

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
