class Settings:
    """A class to store all settings for alien_invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 900
        self.screen_height = 750
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5

        # Laser settings
        self.dual_laser_speed = 2.0
        self.dual_laser_width = 2
        self.dual_laser_height = 15
        self.dual_laser_color = (102, 255, 102)
        self.dual_laser_limit = 3
