import sys
import os
import pygame
from pygame.sprite import Group
from settings import Settings
from shooter import Shooter
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

def run_game():
    # determine the pygame window position
    x = 100
    y = 45
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    # Initialize game and create a screen object.
    pygame.init()
    programIcon = pygame.image.load('images/covid_ic.png')
    pygame.display.set_icon(programIcon)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Corona Epidemic")
    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a shooter.
    shooter = Shooter(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group()
    covids = Group()

    # Create the fleet on covids.
    gf.create_fleet(ai_settings, screen, shooter, covids)


    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, shooter, covids, bullets)

        if stats.game_active:
            shooter.update()
            gf.update_bullets(ai_settings, screen, stats, sb, shooter, covids, bullets)
            gf.update_covids(ai_settings, stats, screen, shooter, covids, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, shooter, covids, bullets, play_button)

run_game()