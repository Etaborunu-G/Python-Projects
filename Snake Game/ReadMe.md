# Snake Game (Pygame)

A simple Snake game built using Python and the Pygame library. Control the snake, eat apples to grow longer, earn points, and avoid crashing into yourself. The snake wraps around the screen instead of hitting walls.

---

## Features
- Classic snake movement
- Snake grows when eating apples
- Score tracking (+10 per apple)
- Game timer display
- Self-collision detection (Game Over)
- Screen wrap-around mechanics

---

## Controls
- Arrow Keys: Move the snake
- ESC: Quit the game
- Y: Play again after Game Over
- N: Exit after Game Over

---

## Requirements
- Python 3.x
- Pygame

Install Pygame using:
pip install pygame

---

## How to Run
1. Save the code in a file called:
   snake_game.py

2. Run the game using:
   python snake_game.py

---

## Gameplay Rules
- Eat the orange apple to grow the snake
- Each apple increases the score by 10
- If the snake collides with its own body, the game ends
- Moving past the screen edge wraps the snake to the opposite side

---

## Project Structure
This project is implemented in a single Python file and includes:

- Apple class for food handling
- Segment and Snake classes for movement and growth
- Collision detection and boundary handling
- Score and game time rendering
- Main game loop inside the main() function

---

## Notes
- Apple respawning uses random and trigonometric calculations
- Snake speed is controlled using SPEED and FPS constants
- No wall collision; only self-collision ends the game

---

## License
This project is intended for educational and personal use.
