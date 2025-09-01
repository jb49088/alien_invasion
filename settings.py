class Settings:
    """A class to store all settings for alien_invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Frame rate
        self.framerate = 60

        # Screen settings
        self.screen_width = 900
        self.screen_height = 760
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5

        # Laser settings
        self.dual_laser_speed = 2.0
        self.dual_laser_width = 2
        self.dual_laser_height = 15
        self.dual_laser_color = (102, 255, 102)
        self.dual_laser_limit = 3

        # UFO settings
        self.ufo_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 = right, -1 = left

        # Star settings
        self.star_width = 1
        self.star_height = 1
        self.star_color = (255, 255, 255)
