User Request:

Can you add stars to the background and add a boss at the end of every level that floats

AI Task: Feature Implementation / Code Modification Protocol

Objective: Safely and effectively implement the feature or modification described in the User Request above. Prioritize understanding the goal, planning thoroughly, leveraging existing code, obtaining explicit user confirmation before action, and outlining verification steps. Adhere strictly to all core.md principles.

Phase 1: Understand Request & Validate Context (Mandatory First Steps)

Clarify Goal: Add a starfield background effect and implement a boss enemy that appears at the end of each level. The boss should have unique movement patterns and be more challenging than regular aliens.

Identify Target(s): 
- space_invaders.py (main game file)
- assets/ (for boss sprite and star images)

Verify Environment & Structure:
Current game features:
- Level system with progressive difficulty
- Player health and shield system
- Power-ups (shield, health, rapid fire, multi-shot)
- Score tracking
- Alien health system
- Progressive difficulty scaling

Phase 2: Analysis, Design & Planning (Mandatory Pre-computation)

Impact Assessment:
1. Game State:
   - Add starfield background rendering
   - Add boss spawning logic at level completion
   - Modify level completion conditions
   - Add boss health and attack patterns

2. Visual Elements:
   - Create starfield effect
   - Add boss sprite
   - Add boss health bar
   - Add boss attack patterns visualization

3. Gameplay Balance:
   - Adjust boss difficulty scaling with level
   - Balance boss health and damage
   - Ensure power-ups remain effective against bosses

Reusability Check:
- Leverage existing collision detection
- Reuse power-up system
- Adapt existing health system for boss

Consider Alternatives & Enhancements:
1. Starfield Implementation:
   - Option 1: Simple static stars
   - Option 2: Parallax scrolling stars
   - Option 3: Animated twinkling stars

2. Boss Design:
   - Option 1: Single large boss with multiple health segments
   - Option 2: Boss with multiple phases
   - Option 3: Boss with minion spawning

Phase 3: Propose Implementation Plan (User Confirmation Required)

Outline Execution Steps:
1. Add starfield background
2. Create boss class with unique movement patterns
3. Implement boss spawning at level completion
4. Add boss health and attack systems
5. Update UI for boss health display
6. Balance boss difficulty

Propose Code Changes:
1. Add Starfield:
```python
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)

class Boss:
    def __init__(self, level):
        self.health = 100 * level
        self.max_health = self.health
        self.x = WIDTH // 2
        self.y = 100
        self.speed = 2
        self.attack_pattern = 0
        self.attack_timer = 0
```

State Dependencies & Risks:
- Requires additional assets (boss sprite, star images)
- May need performance optimization for starfield
- Boss difficulty needs careful balancing

🚨 CRITICAL: Request Explicit Confirmation:
Should I proceed with implementing the starfield and boss system as outlined above?

Phase 4: Implementation (Requires User Confirmation from Phase 3)

Execute Confirmed Changes: Will implement after user confirmation.

Phase 5: Propose Verification (Mandatory After Successful Implementation)

Standard Checks:
1. Verify starfield performance
2. Test boss spawning at each level
3. Validate boss health scaling
4. Check collision detection with boss
5. Test power-up effectiveness against boss

Functional Verification Guidance:
1. Test starfield visual effect
2. Verify boss movement patterns
3. Check boss health scaling with level
4. Test boss attack patterns
5. Verify power-up interactions
6. Test level progression with boss defeat

Goal: Implement the user's request accurately, safely, and efficiently, incorporating best practices, proactive suggestions, and rigorous validation checkpoints, all while strictly following core.md protocols.