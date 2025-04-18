# Space Invaders Game

## Overview
Space Invaders is a classic arcade-style game where players control a spaceship to defeat waves of aliens and bosses. The game features power-ups, level progression, and enhanced gameplay mechanics.

Create using Cursor AI

## Recent Changes

### 1. Power-Up System
- Added various power-ups:
  - **Shield Power-up**: Absorbs damage with a temporary shield.
  - **Health Power-up**: Restores health points.
  - **Rapid Fire Power-up**: Increases firing rate.
  - **Multi-shot Power-up**: Allows shooting multiple bullets at once.

### 2. Level System
- Implemented a level system where the difficulty increases as players progress.
- Players can now start the game at a specified level using the command-line argument `--level`.

### 3. Boss Battles
- Introduced a boss enemy that appears every three levels.
- Boss battles now have two phases:
  - **Phase 1**: Standard attack patterns.
  - **Phase 2**: More aggressive attack patterns and increased speed.
- Added visual feedback for boss damage and invulnerability periods.

### 4. Level Completion Logic
- The level now only completes when both the boss is defeated and the required number of aliens are killed.

### 5. Command-Line Arguments
- Added support for starting the game at a specific level:
  - Usage: `python space_invaders.py --level <level_number>`
  - Default level is 1.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Add photo-quality graphics:
   - Place the following image files in the same directory as `space_invaders.py`:
     - `player.png`: Image for the player ship.
     - `alien.png`: Image for the alien enemies.
     - `bullet.png`: Image for the bullets.
     - `power_up.png`: Image for the power-ups.

## How to Play
1. Clone the repository.
2. Install the required dependencies.
3. Run the game using:
   ```bash
   python space_invaders.py
   ```
   or to start at a specific level:
   ```bash
   python space_invaders.py --level 3
   ```

## Game Features

- Realistic-looking aliens that shoot back.
- Modern power-ups (appear as blue squares).
- Simple collision detection between bullets and aliens.
- Photo-quality graphics for a more immersive experience.

## Future Improvements
- Consider adding more power-up types.
- Implement additional enemy types and behaviors.
- Enhance graphics and sound effects.

## License
This project is licensed under the MIT License.

Enjoy the game! 