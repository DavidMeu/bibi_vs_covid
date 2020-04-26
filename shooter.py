import pygame

class Shooter():

    def __init__(self, ai_settings, screen):
        """Initializing the shooter and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the shooter image and get its rect.
        self.image = pygame.image.load('images/bibi.bmp').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new shooter at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the shooter's center.
        self.center = float(self.rect.centerx)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the shooter's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.shooter_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.shooter_speed_factor
        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the shooter at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_shooter(self):
        """Center the shooter on the screen."""
        self.center = self.screen_rect.centerx