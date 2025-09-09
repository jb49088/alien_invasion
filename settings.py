class Settings:
    """A class to store all settings for alien_invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Frame rate
        self.framerate = 60

        # Screen settings
        self.screen_width = 901
        self.screen_height = 761
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Laser settings
        self.dual_laser_width = 2
        self.dual_laser_height = 15
        self.dual_laser_color = (102, 255, 102)
        self.dual_laser_limit = 3

        # UFO settings
        self.fleet_drop_speed = 10

        # Star settings
        self.star_width = 1
        self.star_height = 1
        self.star_color = (255, 255, 255)

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the ufo point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        # Ship settings
        self.ship_speed = 3.0

        # Laser settings
        self.dual_laser_speed = 5.0

        # UFO settings
        self.ufo_speed = 2.0
        self.fleet_direction = 1  # 1 = right, -1 = left

        # Scoring settings
        self.ufo_points = 50

    def increase_speed(self):
        """Increase speed settings and UFO point values."""
        self.ship_speed *= self.speedup_scale
        self.dual_laser_speed *= self.speedup_scale
        self.ufo_speed *= self.speedup_scale

        self.ufo_points = int(self.ufo_points * self.score_scale)
