import sys
import pygame
from bullet import Bullet
from covid import Covid
from time import sleep


def check_keydown_events(event, ai_settings, screen, shooter, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        shooter.moving_right = True
    elif event.key == pygame.K_LEFT:
        shooter.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, shooter, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, shooter, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, shooter)
        bullets.add(new_bullet)

def check_keyup_events(event, shooter):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        shooter.moving_right = False
    elif event.key == pygame.K_LEFT:
        shooter.moving_left = False

def check_events(ai_settings, screen, stats, play_button, shooter, covids, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, shooter, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, shooter)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, shooter, covids, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, shooter, covids, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of covids and bullets
        covids.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, shooter, covids)
        shooter.center_shooter()

def update_bullets(ai_settings, screen, stats, sb, shooter, covids, bullets):
    """Update position of bullets and get rid of ols bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_covid_collisions(ai_settings, screen, stats, sb, shooter, covids, bullets)

def check_bullet_covid_collisions(ai_settings, screen, stats, sb, shooter, covids, bullets):
    """Respond to bullet-covid collisions."""
    # Remove any bullets and covids that have colided
    collisions = pygame.sprite.groupcollide(bullets, covids, True, True) # for making hi powered bullet change fist bool to false
    print(collisions)
    if collisions:
        for covids in collisions.values():
            stats.score += ai_settings.covid_points * len(covids)
            sb.prep_score()

    if len(covids) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, shooter, covids)


def update_screen(ai_settings, screen, stats, sb, shooter, covids, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind shooter and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    shooter.blitme()
    covids.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def get_number_rows(ai_settings, shooter_height, covid_height):
    """Determine the number of rows of covids that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3*covid_height) - shooter_height)
    number_rows = int(available_space_y / (2 * covid_height))
    return number_rows

def get_number_covids_x(ai_settings, covid_width):
    """Determine the number of covids that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * covid_width
    number_covids_x = int(available_space_x / (1.7 * covid_width))  # to add more covids you may change the numerator.
    return number_covids_x

def create_covid(ai_settings, screen, covids, covid_number, row_number):
    """Create a covid and place it in a row."""
    covid = Covid(ai_settings, screen)
    covid_width = covid.rect.width
    covid.x = covid_width + 2 * covid_width * covid_number
    covid.rect.x = covid.x  # added a 50 offset to each covid
    covid.rect.y = covid.rect.height + 2 * covid.rect.height * row_number
    covids.add(covid)

def create_fleet(ai_settings, screen, shooter, covids):
    """Create a full fleet of covids."""
    # Create a covid and find the number of covids in a row.
    covid = Covid(ai_settings, screen)
    number_covids_x = get_number_covids_x(ai_settings, covid.rect.width)
    number_rows = get_number_rows(ai_settings, shooter.rect.height, covid.rect.height)

    # Create the fleet of covids.
    for row_number in range(number_rows):
        for covid_number in range(number_covids_x):
            create_covid(ai_settings, screen, covids, covid_number, row_number)

def shooter_hit(ai_settings, stats, screen, shooter, covids, bullets):
    """Respond to shooter being hit by covid."""
    if stats.shooter_left > 0:
        # Decrement shooter_left.
        stats.shooter_left -= 1

        # Empty the list of covids and bullets.
        covids.empty()
        bullets.empty()

        # create a new fleet and center the shooter.
        create_fleet(ai_settings, screen, shooter, covids)
        shooter.center_shooter()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_covids_bottom(ai_settings, stats, screen, shooter, covids, bullets):
    """Check if any covids have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for covid in covids.sprites():
        if covid.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the shooter got hit.
            shooter_hit(ai_settings, stats, screen, shooter, covids, bullets)
            break

def update_covids(ai_settings, stats, screen, shooter, covids, bullets):
    """Check if the fleet is at an edge,
     and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, covids)
    covids.update()

    # Look for covid-shooter collisions
    if pygame.sprite.spritecollideany(shooter, covids):
        shooter_hit(ai_settings, stats, screen, shooter, covids, bullets)

    # Look for covid-shooter collisions.
    if pygame.sprite.spritecollideany(shooter, covids):
        print("YOU GOT HIT!")

    # Look for covids hitting the bottom of the screen.
    check_covids_bottom(ai_settings, stats, screen, shooter, covids, bullets)

def check_fleet_edges(ai_settings, covids):
    """Respond appropriately if any covids have reached an edge."""
    for covid in covids.sprites():
        if covid.check_edges():
            change_fleet_direction(ai_settings, covids)
            break

def change_fleet_direction(ai_settings, covids):
    """Drop the entire fleet and change the fleet's direction."""
    for covid in covids.sprites():
        covid.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

