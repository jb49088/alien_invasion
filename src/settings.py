class Settings:
    """A class to store all settings for alien_invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Title
        self.title = "Alien Invasion"

        # Frame rate
        self.framerate = 60

        # Screen settings
        self.screen_width = 901
        self.screen_height = 761
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Laser settings
        self.laser_width = 2
        self.laser_height = 15

        self.ship_laser_color = (102, 255, 102)
        self.ship_laser_limit = 3

        self.ufo_laser_color = (255, 0, 0)

        # UFO settings
        self.fleet_drop_speed = 10
        self.ufo_fire_interval = 120

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
        self.ship_laser_speed = 5.0

        self.ufo_laser_speed = 3.0

        # UFO settings
        self.ufo_speed = 2.0
        self.fleet_direction = 1  # 1 = right, -1 = left

        # Scoring settings
        self.ufo_points = 50

    def increase_speed(self):
        """Increase speed settings and UFO point values."""
        self.ship_speed *= self.speedup_scale
        self.ship_laser_speed *= self.speedup_scale
        self.ufo_speed *= self.speedup_scale

        self.ufo_points = int(self.ufo_points * self.score_scale)
