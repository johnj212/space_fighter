import pygame
import random
import sys
import os
import time
import math
import argparse  # Add argparse for command line arguments

# Initialize Pygame
pygame.init()

# Set up command line arguments
parser = argparse.ArgumentParser(description='Space Invaders Game')
parser.add_argument('--level', type=int, default=1, help='Starting level (default: 1)')
args = parser.parse_args()

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
boss_image = pygame.image.load('boss.png').convert_alpha()  # Add boss image

# Scale down the alien image
alien_image = pygame.transform.scale(alien_image, (30, 30))  # Reduced size
boss_image = pygame.transform.scale(boss_image, (100, 100))  # Scale boss image

# Starfield
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(100, 255)

# Create stars
stars = [Star() for _ in range(200)]

# Boss class
class Boss:
    def __init__(self, level):
        self.health = 100 * level
        self.max_health = self.health
        self.x = WIDTH // 2
        self.y = 100
        self.speed = 2 + (level - 1) * 0.5  # Scale speed with level
        self.attack_pattern = 0
        self.attack_timer = 0
        self.width, self.height = boss_image.get_size()
        self.movement_direction = 1
        self.movement_range = 300
        self.start_x = self.x
        self.hit_timer = 0  # For visual feedback when hit
        self.invulnerable = False  # For attack pattern transitions
        self.invulnerable_timer = 0
        self.phase = 1  # Boss battle phases
        self.phase_health_threshold = self.health * 0.5  # Phase change at 50% health

    def update(self):
        # Movement pattern
        self.x += self.speed * self.movement_direction
        if abs(self.x - self.start_x) > self.movement_range:
            self.movement_direction *= -1

        # Handle invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Attack pattern
        self.attack_timer += 1
        if self.attack_timer >= 60:  # Attack every second
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.attack_timer = 0
            # Become invulnerable briefly during pattern change
            self.invulnerable = True
            self.invulnerable_timer = 30

        # Phase transition
        if self.health <= self.phase_health_threshold and self.phase == 1:
            self.phase = 2
            self.speed *= 1.5  # Increase speed in phase 2
            self.invulnerable = True
            self.invulnerable_timer = 60  # Longer invulnerability during phase change

    def shoot(self):
        bullets = []
        if self.invulnerable:
            return bullets  # Don't shoot while invulnerable

        if self.phase == 1:
            if self.attack_pattern == 0:  # Single shot
                bullets.append([self.x + self.width // 2, self.y + self.height])
            elif self.attack_pattern == 1:  # Spread shot
                for angle in range(-30, 31, 15):
                    rad = math.radians(angle)
                    bullets.append([
                        self.x + self.width // 2 + math.sin(rad) * 20,
                        self.y + self.height + math.cos(rad) * 20
                    ])
            else:  # Circle shot
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    bullets.append([
                        self.x + self.width // 2 + math.sin(rad) * 20,
                        self.y + self.height // 2 + math.cos(rad) * 20
                    ])
        else:  # Phase 2 - more aggressive patterns
            if self.attack_pattern == 0:  # Double spread
                for angle in range(-45, 46, 15):
                    rad = math.radians(angle)
                    bullets.append([
                        self.x + self.width // 2 + math.sin(rad) * 20,
                        self.y + self.height + math.cos(rad) * 20
                    ])
            elif self.attack_pattern == 1:  # Double circle
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)
                    bullets.append([
                        self.x + self.width // 2 + math.sin(rad) * 20,
                        self.y + self.height // 2 + math.cos(rad) * 20
                    ])
            else:  # Triple shot
                for i in range(3):
                    bullets.append([
                        self.x + self.width // 2 + (i - 1) * 20,
                        self.y + self.height
                    ])
        return bullets

# Game state
class GameState:
    def __init__(self, start_level=1):
        self.level = start_level
        self.aliens_to_kill = 10 + (start_level - 1) * 5  # Adjust for starting level
        self.aliens_killed = 0
        self.level_complete = False
        self.game_over = False
        self.score = 0
        self.player_health = 100
        self.player_shield = 0
        self.rapid_fire = False
        self.multi_shot = False
        self.power_up_end_time = 0
        self.show_level_transition = False
        self.transition_timer = 0
        self.transition_duration = 2.0  # seconds
        self.boss_active = False
        self.boss = None

        # If starting at a higher level, spawn boss if needed
        if self.level % 3 == 0:
            self.boss_active = True
            self.boss = Boss(self.level)

    def advance_level(self):
        # Clear all game objects
        aliens.clear()
        alien_bullets.clear()
        bullets.clear()
        power_ups.clear()
        
        # Reset game state
        pygame.event.clear()  # Clear any pending events
        
        # Update level stats
        self.level += 1
        self.aliens_killed = 0
        self.aliens_to_kill = 10 + (self.level - 1) * 5
        self.level_complete = False
        
        # Restore some health between levels
        self.player_health = min(self.player_health + 20, 100)
        
        # Start transition animation
        self.show_level_transition = True
        self.transition_timer = time.time()

        # Spawn boss every 3 levels
        if self.level % 3 == 0:
            self.boss_active = True
            self.boss = Boss(self.level)

    def update_transition(self):
        if self.show_level_transition:
            if time.time() - self.transition_timer >= self.transition_duration:
                self.show_level_transition = False

    def get_alien_speed(self):
        return 2 + (self.level - 1) * 0.5  # Increase speed with level

    def get_alien_spawn_rate(self):
        return max(30, 60 - (self.level - 1) * 5)  # Decrease spawn delay with level

    def get_alien_health(self):
        return 1 + (self.level - 1)  # Increase health with level

# Initialize game state with starting level
game_state = GameState(args.level)

# Player
player_width, player_height = player_image.get_size()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

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

# Aliens
aliens = []
alien_width, alien_height = alien_image.get_size()

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
    global game_state
    
    power_up_duration = 10  # seconds
    game_state.power_up_end_time = time.time() + power_up_duration
    
    if power_up_type == 'shield':
        game_state.player_shield = 50
    elif power_up_type == 'health':
        game_state.player_health = min(game_state.player_health + 30, 100)
    elif power_up_type == 'rapid_fire':
        game_state.rapid_fire = True
    elif power_up_type == 'multi_shot':
        game_state.multi_shot = True

def check_power_up_expiry():
    global game_state
    
    if time.time() > game_state.power_up_end_time:
        game_state.rapid_fire = False
        game_state.multi_shot = False
        game_state.player_shield = 0

def create_bullet(x, y):
    return [x, y]

def create_alien():
    alien_x = random.randint(0, WIDTH - alien_width)
    return {
        'x': alien_x,
        'y': -alien_height,
        'health': game_state.get_alien_health()
    }

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_state.game_over:
        if game_state.level_complete and not game_state.show_level_transition:
            # Wait for space key to advance level
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_state.advance_level()
        elif not game_state.show_level_transition:
            # Normal gameplay
            # Update stars
            for star in stars:
                star.y += star.speed
                if star.y > HEIGHT:
                    star.y = 0
                    star.x = random.randint(0, WIDTH)

            # Update boss if active
            if game_state.boss_active and game_state.boss:
                game_state.boss.update()
                if random.randint(1, 30) == 1:  # Boss shooting frequency
                    new_bullets = game_state.boss.shoot()
                    alien_bullets.extend(new_bullets)

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
                if current_time - last_shot_time >= (shoot_delay / 2 if game_state.rapid_fire else shoot_delay):
                    if game_state.multi_shot:
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
            if random.randint(1, game_state.get_alien_spawn_rate()) == 1:
                aliens.append(create_alien())

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
                alien['y'] += game_state.get_alien_speed()
                if alien['y'] > HEIGHT:
                    aliens.remove(alien)
                # Alien shooting
                if random.randint(1, 100) == 1:
                    alien_bullets.append([alien['x'] + alien_width // 2, alien['y'] + alien_height])

            # Move power-ups
            for power_up in power_ups[:]:
                power_up['y'] += power_up_speed
                if power_up['y'] > HEIGHT:
                    power_ups.remove(power_up)

            # Collision detection - Player bullets hitting aliens
            for bullet in bullets[:]:
                # Check collision with boss first
                if game_state.boss_active and game_state.boss and not game_state.boss.invulnerable:
                    if (bullet[0] < game_state.boss.x + game_state.boss.width and
                        bullet[0] > game_state.boss.x and
                        bullet[1] < game_state.boss.y + game_state.boss.height and
                        bullet[1] > game_state.boss.y):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        # Apply damage with visual feedback
                        game_state.boss.health -= bullet_damage
                        game_state.boss.hit_timer = 5  # Flash boss when hit
                        if game_state.boss.health <= 0:
                            game_state.boss_active = False
                            game_state.score += 1000 * game_state.boss.phase  # More points for phase 2
                            # Spawn more power-ups on boss death
                            for _ in range(3 + game_state.boss.phase):  # More power-ups in phase 2
                                power_ups.append(create_power_up())
                            # Don't set level_complete here, wait for alien quota
                        continue  # Skip alien collision check for this bullet
                
                # Original alien collision detection
                for alien in aliens[:]:
                    if (bullet[0] < alien['x'] + alien_width and
                        bullet[0] > alien['x'] and
                        bullet[1] < alien['y'] + alien_height and
                        bullet[1] > alien['y']):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        alien['health'] -= bullet_damage
                        if alien['health'] <= 0:
                            if alien in aliens:
                                aliens.remove(alien)
                                game_state.aliens_killed += 1
                                game_state.score += 100
                                # Check for level completion only after alien kill
                                if (game_state.aliens_killed >= game_state.aliens_to_kill and 
                                    not game_state.boss_active):  # Boss must be defeated too
                                    game_state.level_complete = True
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
                    if game_state.player_shield > 0:
                        # Shield absorbs damage
                        absorbed = min(game_state.player_shield, damage)
                        game_state.player_shield -= absorbed
                        damage -= absorbed
                    game_state.player_health -= damage
                    if game_state.player_health <= 0:
                        game_state.game_over = True

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
    
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, (star.brightness, star.brightness, star.brightness),
                         (int(star.x), int(star.y)), star.size)
    
    # Draw level transition if active
    if game_state.show_level_transition:
        transition_text = game_font.render(f'LEVEL {game_state.level}', True, WHITE)
        screen.blit(transition_text, (WIDTH//2 - transition_text.get_width()//2, HEIGHT//2))
        game_state.update_transition()
    else:
        # Draw game objects
        if not game_state.game_over:
            # Draw shield effect if active
            if game_state.player_shield > 0:
                shield_rect = pygame.Rect(player_x - 5, player_y - 5,
                                        player_width + 10, player_height + 10)
                pygame.draw.rect(screen, BLUE, shield_rect, 2)
            screen.blit(player_image, (player_x, player_y))
        
        # Draw boss if active
        if game_state.boss_active and game_state.boss:
            # Flash boss when hit or invulnerable
            if game_state.boss.hit_timer > 0 or game_state.boss.invulnerable:
                screen.blit(boss_image, (game_state.boss.x, game_state.boss.y))
                color = RED if game_state.boss.hit_timer > 0 else YELLOW
                pygame.draw.rect(screen, color, (game_state.boss.x, game_state.boss.y,
                                             game_state.boss.width, game_state.boss.height), 2)
                if game_state.boss.hit_timer > 0:
                    game_state.boss.hit_timer -= 1
            else:
                screen.blit(boss_image, (game_state.boss.x, game_state.boss.y))
            
            # Draw boss health bar
            health_width = 100
            health_height = 10
            health_x = game_state.boss.x + (game_state.boss.width - health_width) // 2
            health_y = game_state.boss.y - 20
            pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
            pygame.draw.rect(screen, GREEN, (health_x, health_y,
                                           health_width * (game_state.boss.health / game_state.boss.max_health),
                                           health_height))
            
            # Draw phase indicator
            phase_text = small_font.render(f'Phase {game_state.boss.phase}', True, WHITE)
            screen.blit(phase_text, (health_x, health_y - 20))
        
        for alien in aliens:
            screen.blit(alien_image, (alien['x'], alien['y']))
        for bullet in bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))
        for bullet in alien_bullets:
            screen.blit(bullet_image, (bullet[0], bullet[1]))
        for power_up in power_ups:
            pygame.draw.rect(screen, power_up['color'],
                            (power_up['x'], power_up['y'], power_up_width, power_up_height))

        # Draw UI
        level_text = game_font.render(f'Level: {game_state.level}', True, WHITE)
        score_text = game_font.render(f'Score: {game_state.score}', True, WHITE)
        health_text = game_font.render(f'Health: {game_state.player_health}', True, WHITE)
        shield_text = game_font.render(f'Shield: {game_state.player_shield}', True, BLUE)
        aliens_text = game_font.render(f'Aliens: {game_state.aliens_killed}/{game_state.aliens_to_kill}', True, WHITE)
        
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(health_text, (10, 90))
        screen.blit(shield_text, (10, 130))
        screen.blit(aliens_text, (10, 170))

        # Draw active power-ups
        power_up_y = 210
        if game_state.rapid_fire:
            rapid_fire_text = small_font.render('Rapid Fire Active!', True, RED)
            screen.blit(rapid_fire_text, (10, power_up_y))
            power_up_y += 30
        if game_state.multi_shot:
            multi_shot_text = small_font.render('Multi-Shot Active!', True, YELLOW)
            screen.blit(multi_shot_text, (10, power_up_y))

        # Draw level complete screen
        if game_state.level_complete and not game_state.show_level_transition:
            level_complete_text = game_font.render('LEVEL COMPLETE!', True, GREEN)
            next_level_text = game_font.render('Press SPACE to continue', True, WHITE)
            screen.blit(level_complete_text, (WIDTH//2 - level_complete_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(next_level_text, (WIDTH//2 - next_level_text.get_width()//2, HEIGHT//2 + 50))

        # Draw game over screen
        if game_state.game_over:
            game_over_text = game_font.render('GAME OVER', True, RED)
            final_score_text = game_font.render(f'Final Score: {game_state.score}', True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 