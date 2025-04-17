import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)

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

# Aliens
aliens = []
alien_width, alien_height = alien_image.get_size()
alien_speed = 2
alien_spawn_rate = 60  # frames

# Bullets
bullets = []
bullet_speed = 7

# Alien bullets
alien_bullets = []
alien_bullet_speed = 5

# Power-ups
power_ups = []
power_up_width, power_up_height = power_up_image.get_size()
power_up_speed = 3
power_up_spawn_rate = 300  # frames

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        bullets.append([player_x + player_width // 2, player_y])

    # Spawn aliens
    if random.randint(1, alien_spawn_rate) == 1:
        alien_x = random.randint(0, WIDTH - alien_width)
        aliens.append([alien_x, -alien_height])

    # Spawn power-ups
    if random.randint(1, power_up_spawn_rate) == 1:
        power_up_x = random.randint(0, WIDTH - power_up_width)
        power_ups.append([power_up_x, -power_up_height])

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
        if random.randint(1, 100) == 1:  # Adjust shooting frequency
            alien_bullets.append([alien[0] + alien_width // 2, alien[1] + alien_height])

    # Move power-ups
    for power_up in power_ups[:]:
        power_up[1] += power_up_speed
        if power_up[1] > HEIGHT:
            power_ups.remove(power_up)

    # Collision detection
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if (bullet[0] < alien[0] + alien_width and
                bullet[0] > alien[0] and
                bullet[1] < alien[1] + alien_height and
                bullet[1] > alien[1]):
                bullets.remove(bullet)
                aliens.remove(alien)
                break

    # Draw everything
    screen.fill(BLACK)
    screen.blit(player_image, (player_x, player_y))
    for alien in aliens:
        screen.blit(alien_image, (alien[0], alien[1]))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for bullet in alien_bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for power_up in power_ups:
        screen.blit(power_up_image, (power_up[0], power_up[1]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 