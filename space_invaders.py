import pygame
import random
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize font
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 20)

# Load images
# Note: Replace these paths with the actual paths to your image assets
player_image = pygame.image.load('player.png').convert_alpha()
alien_image = pygame.image.load('alien.png').convert_alpha()
bullet_image = pygame.image.load('bullet.png').convert_alpha()
power_up_image = pygame.image.load('power_up.png').convert_alpha()

# Scale down the alien image
alien_image = pygame.transform.scale(alien_image, (30, 30))  # Reduced size

# Player
player_width, player_height = player_image.get_size()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5
player_health = 100
player_score = 0
player_shield = 0
rapid_fire = False
multi_shot = False
power_up_end_time = 0

# Aliens
aliens = []
alien_width, alien_height = alien_image.get_size()
alien_speed = 2
alien_spawn_rate = 60  # frames

# Bullets
bullets = []
bullet_speed = 7
bullet_damage = 10
shoot_delay = 0.5  # seconds between shots
last_shot_time = 0

# Alien bullets
alien_bullets = []
alien_bullet_speed = 5
alien_bullet_damage = 10

# Power-ups
power_ups = []
power_up_width, power_up_height = power_up_image.get_size()
power_up_speed = 3
power_up_spawn_rate = 300  # frames

# Power-up types and their colors
POWER_UP_TYPES = {
    'shield': BLUE,      # Adds temporary shield
    'health': GREEN,     # Restores health
    'rapid_fire': RED,   # Increases fire rate
    'multi_shot': YELLOW # Shoots multiple bullets
}

# Game state
game_over = False

# Game loop
clock = pygame.time.Clock()
running = True

def create_power_up():
    power_up_type = random.choice(list(POWER_UP_TYPES.keys()))
    power_up_x = random.randint(0, WIDTH - power_up_width)
    return {
        'x': power_up_x,
        'y': -power_up_height,
        'type': power_up_type,
        'color': POWER_UP_TYPES[power_up_type]
    }

def apply_power_up(power_up_type):
    global player_health, player_shield, rapid_fire, multi_shot, power_up_end_time
    
    power_up_duration = 10  # seconds
    power_up_end_time = time.time() + power_up_duration
    
    if power_up_type == 'shield':
        player_shield = 50
    elif power_up_type == 'health':
        player_health = min(player_health + 30, 100)
    elif power_up_type == 'rapid_fire':
        rapid_fire = True
    elif power_up_type == 'multi_shot':
        multi_shot = True

def check_power_up_expiry():
    global rapid_fire, multi_shot, player_shield
    
    if time.time() > power_up_end_time:
        rapid_fire = False
        multi_shot = False
        player_shield = 0

def create_bullet(x, y):
    return [x, y]

while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed

        # Shooting
        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time >= (shoot_delay / 2 if rapid_fire else shoot_delay):
                if multi_shot:
                    # Create three bullets in a spread pattern
                    bullets.append(create_bullet(player_x + player_width // 2, player_y))
                    bullets.append(create_bullet(player_x + player_width // 2 - 20, player_y))
                    bullets.append(create_bullet(player_x + player_width // 2 + 20, player_y))
                else:
                    bullets.append(create_bullet(player_x + player_width // 2, player_y))
                last_shot_time = current_time

        # Check power-up expiry
        check_power_up_expiry()

        # Spawn aliens
        if random.randint(1, alien_spawn_rate) == 1:
            alien_x = random.randint(0, WIDTH - alien_width)
            aliens.append([alien_x, -alien_height])

        # Spawn power-ups
        if random.randint(1, power_up_spawn_rate) == 1:
            power_ups.append(create_power_up())

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Move alien bullets
        for bullet in alien_bullets[:]:
            bullet[1] += alien_bullet_speed
            if bullet[1] > HEIGHT:
                alien_bullets.remove(bullet)

        # Move aliens
        for alien in aliens[:]:
            alien[1] += alien_speed
            if alien[1] > HEIGHT:
                aliens.remove(alien)
            # Alien shooting
            if random.randint(1, 100) == 1:
                alien_bullets.append([alien[0] + alien_width // 2, alien[1] + alien_height])

        # Move power-ups
        for power_up in power_ups[:]:
            power_up['y'] += power_up_speed
            if power_up['y'] > HEIGHT:
                power_ups.remove(power_up)

        # Collision detection - Player bullets hitting aliens
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if (bullet[0] < alien[0] + alien_width and
                    bullet[0] > alien[0] and
                    bullet[1] < alien[1] + alien_height and
                    bullet[1] > alien[1]):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if alien in aliens:
                        aliens.remove(alien)
                        player_score += 100
                    break

        # Collision detection - Alien bullets hitting player
        for bullet in alien_bullets[:]:
            if (bullet[0] < player_x + player_width and
                bullet[0] > player_x and
                bullet[1] < player_y + player_height and
                bullet[1] > player_y):
                if bullet in alien_bullets:
                    alien_bullets.remove(bullet)
                damage = alien_bullet_damage
                if player_shield > 0:
                    # Shield absorbs damage
                    absorbed = min(player_shield, damage)
                    player_shield -= absorbed
                    damage -= absorbed
                player_health -= damage
                if player_health <= 0:
                    game_over = True

        # Collision detection - Player collecting power-ups
        for power_up in power_ups[:]:
            if (power_up['x'] < player_x + player_width and
                power_up['x'] + power_up_width > player_x and
                power_up['y'] < player_y + player_height and
                power_up['y'] + power_up_height > player_y):
                apply_power_up(power_up['type'])
                power_ups.remove(power_up)

    # Draw everything
    screen.fill(BLACK)
    
    # Draw game objects
    if not game_over:
        # Draw shield effect if active
        if player_shield > 0:
            shield_rect = pygame.Rect(player_x - 5, player_y - 5,
                                    player_width + 10, player_height + 10)
            pygame.draw.rect(screen, BLUE, shield_rect, 2)
        screen.blit(player_image, (player_x, player_y))
    
    for alien in aliens:
        screen.blit(alien_image, (alien[0], alien[1]))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for bullet in alien_bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for power_up in power_ups:
        pygame.draw.rect(screen, power_up['color'],
                        (power_up['x'], power_up['y'], power_up_width, power_up_height))

    # Draw UI
    score_text = game_font.render(f'Score: {player_score}', True, WHITE)
    health_text = game_font.render(f'Health: {player_health}', True, WHITE)
    shield_text = game_font.render(f'Shield: {player_shield}', True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(shield_text, (10, 90))

    # Draw active power-ups
    power_up_y = 130
    if rapid_fire:
        rapid_fire_text = small_font.render('Rapid Fire Active!', True, RED)
        screen.blit(rapid_fire_text, (10, power_up_y))
        power_up_y += 30
    if multi_shot:
        multi_shot_text = small_font.render('Multi-Shot Active!', True, YELLOW)
        screen.blit(multi_shot_text, (10, power_up_y))

    # Draw game over screen
    if game_over:
        game_over_text = game_font.render('GAME OVER', True, RED)
        final_score_text = game_font.render(f'Final Score: {player_score}', True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 