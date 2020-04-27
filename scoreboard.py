import pygame.ftfont
from pygame.sprite import Group
from shooter import Shooter

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_shooters()

    def prep_score(self):
        """Turn the acore into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("Current score " + score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.screen_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("Record " + high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render("Level " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_shooters(self):
        """Show how many shooters are left."""
        self.shooters = Group()
        self.lives_image = self.font.render("Lives left", True, self.text_color,
                                            self.ai_settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.x = 0
        self.lives_rect.y = 20

        for shooter_number in range(self.stats.shooters_left):
            shooter = Shooter(self.ai_settings, self.screen)
            shooter.rect.x = 100 + shooter_number * shooter.rect.width
            shooter.rect.y = 0
            self.shooters.add(shooter)

    def show_score(self):
        """Draw scores and shooters to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)

        # Draw shooters.
        self.shooters.draw(self.screen)