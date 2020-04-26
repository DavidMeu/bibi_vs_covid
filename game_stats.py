class GameStats():
    """Track statistics for covid Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start Corona Pandemic in an active state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.shooter_left = self.ai_settings.shooter_limit
        self.score = 0