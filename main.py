import turtle
import time
from config import CANVAS_WIDTH, CANVAS_HEIGHT, LEFT_LIMIT, RIGHT_LIMIT, TOP_LIMIT, BOTTOM_LIMIT
from game_elements import Snake, Food
from interface import GameInterface

class GameManager:
    """
    Central loop coordinator regulating game states, ticks, asynchronous 
    key mappings, and adaptive level-speed updates.
    """
    def __init__(self):
        # Primary Turtle Application Screen initialization setups
        self.screen = turtle.Screen()
        self.screen.title("🐍 SNAKE GAME - EVOLUTIONARY SCALABILITY")
        self.screen.setup(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.screen.bgcolor("#E6EBF3") # Soft pastel light theme background
        self.screen.tracer(0)          # Turn off automated animations to manage ticks manually

        self.interface = GameInterface()
        self.snake = None
        self.food = None

        # Game Structural state controls: START, PLAYING, PAUSED, GAME_OVER
        self.game_state = "START"  
        self.high_score = 0
        self.level = 1
        self.points = 0
        self.fruits_eaten_this_level = 0
        self.fruits_needed_this_level = 2 
        
        # --- DYNAMIC REFRESH VELOCITY SCHEME ---
        self.base_delay = 0.20          # Starting sleep delay (Higher = Slower)
        self.current_delay = self.base_delay

        # Adaptive Grid block parameters (Transitions through: 40, 20, 10)
        self.current_snake_size = 20

        # Build initial canvas frames and configure keyboard events
        self.interface.draw_static_layout()
        self.setup_key_listeners()

    def setup_key_listeners(self):
        """Binds input hooks to directional state updates and system shortcuts."""
        self.screen.listen()
        # Alpha Keyboard Layout controls
        self.screen.onkeypress(lambda: self.change_direction("UP"), "w")
        self.screen.onkeypress(lambda: self.change_direction("DOWN"), "s")
        self.screen.onkeypress(lambda: self.change_direction("LEFT"), "a")
        self.screen.onkeypress(lambda: self.change_direction("RIGHT"), "d")
        
        # Positional Arrow Key alternatives
        self.screen.onkeypress(lambda: self.change_direction("UP"), "Up")
        self.screen.onkeypress(lambda: self.change_direction("DOWN"), "Down")
        self.screen.onkeypress(lambda: self.change_direction("LEFT"), "Left")
        self.screen.onkeypress(lambda: self.change_direction("RIGHT"), "Right")

        # Game UI State System Controls
        self.screen.onkeypress(self.handle_enter, "Return")
        self.screen.onkeypress(self.toggle_pause, "space")
        self.screen.onkeypress(self.quit_game, "Escape")

    def change_direction(self, target_dir):
        """Changes heading vectors while preventing a direct 180-degree self-collision."""
        if self.game_state != "PLAYING" or not self.snake:
            return
            
        current = self.snake.direction
        if target_dir == "UP" and current != "DOWN":
            self.snake.direction = "UP"
        elif target_dir == "DOWN" and current != "UP":
            self.snake.direction = "DOWN"
        elif target_dir == "LEFT" and current != "RIGHT":
            self.snake.direction = "LEFT"
        elif target_dir == "RIGHT" and current != "LEFT":
            self.snake.direction = "RIGHT"

    def handle_enter(self):
        """Processes Enter key triggers to progress through screens and state machines."""
        if self.game_state == "START":
            self.game_state = "PLAYING"
            self.interface.clear_menu_overlay()
            self.start_new_game()
        elif self.game_state == "GAME_OVER":
            self.game_state = "START"
            self.interface.clear_menu_overlay()
            self.show_start_menu()

    def toggle_pause(self):
        """Pauses or resumes the runtime game loop sequence."""
        if self.game_state == "PLAYING":
            self.game_state = "PAUSED"
            self.interface.draw_menu_overlay(
                "⏸️ GAME PAUSED", 
                "Controls:\nWASD or Arrow Keys to Move\n\nPress SPACE to Resume\nPress ESC to Quit Game"
            )
        elif self.game_state == "PAUSED":
            self.game_state = "PLAYING"
            self.interface.clear_menu_overlay()
            self.run_game_loop()

    def quit_game(self):
        """Immediately destroys window references to stop execution cleanly."""
        self.screen.bye()

    def show_start_menu(self):
        """Resets basic game states and shows the instructions screen."""
        self.level = 1
        self.points = 0
        self.current_snake_size = 20
        self.current_delay = self.base_delay # Restore initial speed settings
        self.interface.draw_static_layout()
        self.update_hud()
        self.interface.draw_menu_overlay(
            "🎮 READY PLAYER ONE", 
            "Controls:\nWASD or Arrow Keys to Move\nSPACE to Pause\n\nPress ENTER to Start the Game"
        )

    def start_new_game(self):
        """Instantiates game objects and triggers the core game loop."""
        self.fruits_eaten_this_level = 0
        self.fruits_needed_this_level = 2
        self.snake = Snake(self.current_snake_size)
        self.food = Food()
        
        self.food.respawn(self.snake.segments, self.current_snake_size)
        self.update_hud()
        self.run_game_loop()

    def run_game_loop(self):
        """Primary synchronous clock execution loop for handling game logic frames."""
        while self.game_state == "PLAYING":
            self.screen.update()
            self.snake.move()

            # Crash Evaluation checks
            if self.snake.check_wall_collision() or self.snake.check_self_collision():
                self.game_state = "GAME_OVER"
                break

            # Collision intersection check with target food items
            head = self.snake.segments[0]
            if head.distance(self.food.x, self.food.y) < (self.current_snake_size * 0.8):
                self.points += 10
                self.fruits_eaten_this_level += 1
                self.snake.add_segment()

                # Level Progress evaluation trigger
                if self.fruits_eaten_this_level >= self.fruits_needed_this_level:
                    self.level += 1
                    self.fruits_eaten_this_level = 0
                    self.fruits_needed_this_level += 1 
                    
                    # ----------------------------------------------------------
                    # MECHANIC: SPEED UP EVERY 2 LEVELS
                    # ----------------------------------------------------------
                    # Speed scales up on Level 3, 5, 7, etc. (Every 2 levels completed).
                    # Reducing delay by 15% means the loop ticks faster.
                    if self.level % 2 != 0:
                        self.current_delay = max(0.04, self.current_delay * 0.85)

                    # Dynamic Sizing Scale updates based on progression thresholds
                    if self.current_snake_size == 40:
                        self.current_snake_size = 20
                    elif self.current_snake_size == 20:
                        self.current_snake_size = 10
                        
                    # Re-adjust active structural sizes for existing snake parts
                    stretch_factor = self.current_snake_size / 20.0
                    for seg in self.snake.segments:
                        seg.shapesize(stretch_wid=stretch_factor - 0.05, stretch_len=stretch_factor - 0.05)

                self.update_hud()
                self.food.respawn(self.snake.segments, self.current_snake_size)
            else:
                self.snake.trim_tail()

            # Thread sleep delay regulating speed execution factors
            time.sleep(self.current_delay)

        # ======================================================================
        # GAME OVER CLEANUP PROCESSES
        # ======================================================================
        if self.points > self.high_score:
            self.high_score = self.points

        self.update_hud()
        if self.snake:
            self.snake.hide_snake()
        
        if self.game_state == "GAME_OVER":
            self.interface.draw_menu_overlay(
                "💥 GAME OVER", 
                f"Final Score: {self.points} Points\nLevel Reached: {self.level}\n\nPress ENTER to Return to Main Menu"
            )

        # Keep menu alive asynchronously during game over state
        while self.game_state == "GAME_OVER":
            self.screen.update()
            time.sleep(0.05)

        self.interface.clear_menu_overlay()
        
        # Clear out objects to prevent memory leaks on restart
        if self.snake:
            self.snake.clear_all()
        if self.food:
            self.food.pen.clear()

    def update_hud(self):
        """Passes current scores down to the view overlay layer."""
        self.interface.draw_hud_values(
            points=self.points,
            high_score=self.high_score,
            level=self.level,
            fruits_eaten=self.fruits_eaten_this_level,
            fruits_needed=self.fruits_needed_this_level
        )


# Global application execution entry checkpoint
if __name__ == "__main__":
    manager = GameManager()
    manager.show_start_menu()
    turtle.mainloop()