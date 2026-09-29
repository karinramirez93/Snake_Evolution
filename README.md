# Snake Evolution

A Snake game developed in Python as the final project for an online introductory Python programming course offered by Stanford University.

The project applies fundamental programming concepts through a complete playable game built with Python's `turtle` module. The game includes movement controls, collision detection, scoring, levels, increasing difficulty, pause/resume behavior, and a graphical user interface.

## Project Background

Snake Evolution was created as the final project for an online introductory Python programming course offered by Stanford University while learning the fundamentals of Python.

The goal was to combine concepts covered in an introductory programming course into a larger program with multiple files and interacting classes. The project provided practice with program structure, object-oriented programming, conditionals, loops, functions, event handling, and game logic.

## Features

- Snake movement using WASD or the arrow keys.
- Protection against immediate 180-degree direction changes.
- Random fruit generation inside the playable area.
- Fruit placement that avoids the snake's current position.
- Snake growth after collecting fruit.
- Score and high-score tracking.
- Level progression.
- Increasing game speed as levels progress.
- Wall and self-collision detection.
- Pause and resume controls.
- Start and game-over screens.
- Heads-up display for score, high score, level, and fruit progress.

## Technologies

- Python
- Python Turtle Graphics
- Object-Oriented Programming

No external Python packages are required.

## Project Structure

```text
Snake_Evolution/
├── main.py
├── game_elements.py
├── interface.py
├── config.py
└── Snake picture.jpg
```

### `main.py`

Contains the `GameManager` class and the main game loop. It coordinates game states, keyboard controls, scoring, level progression, collision responses, and game restarts.

### `game_elements.py`

Contains the main game objects:

- `Snake` manages movement, body segments, growth, and collision detection.
- `Food` manages fruit selection and placement inside the game area.

### `interface.py`

Contains the `GameInterface` class, which draws the game layout, score display, menus, pause screen, and game-over screen.

### `config.py`

Stores shared configuration values such as window dimensions, playable boundaries, and the available fruit icons.

## Controls

| Key | Action |
| --- | --- |
| W / Up Arrow | Move up |
| S / Down Arrow | Move down |
| A / Left Arrow | Move left |
| D / Right Arrow | Move right |
| Space | Pause / Resume |
| Enter | Start game / Return to menu |
| Escape | Quit |

## Running the Game

Make sure Python is installed, then clone or download the repository and run:

```bash
python main.py
```

Depending on your system, the command may be:

```bash
python3 main.py
```

Because the project uses Python's standard `turtle` module, there is no separate package installation step.

## What I Practiced

This project gave me practical experience applying introductory Python concepts in a program larger than individual classroom exercises. In particular, I practiced:

- Breaking a program into multiple modules.
- Creating classes with separate responsibilities.
- Managing application state.
- Responding to keyboard events.
- Working with coordinates and collision detection.
- Updating a graphical interface based on program state.
- Building game rules from smaller programming concepts.

## Academic Project

This repository represents my final project from an online introductory Python course offered by Stanford University. It is preserved as part of my programming portfolio to demonstrate my foundational Python experience and progression as a developer.

## Author

**Mr. Karin Ramirez**  
Computer Science Student & Software Developer
