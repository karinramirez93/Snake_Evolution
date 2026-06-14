import turtle
import random
from config import LEFT_LIMIT, RIGHT_LIMIT, TOP_LIMIT, BOTTOM_LIMIT, FRUIT_POOL

class Snake:
    """
    Manages the structural segments, directions, grid scales, and 
    collision vectors of the player-controlled snake.
    """
    def __init__(self, current_size):
        self.segments = []          # List to store turtle segment objects
        self.direction = "RIGHT"    # Initial movement heading vector
        self.current_size = current_size
        self.spawn_initial_body()

    def spawn_initial_body(self):
        """Creates the starting 3-segment snake aligned with the active size factor."""
        start_x = -self.current_size
        start_y = 0
        
        # Turtle shapes default to 20x20 pixels. Scale it relative to standard.
        stretch_factor = self.current_size / 20.0

        for i in range(3):
            segment = turtle.Turtle()
            segment.speed(0)
            segment.shape("square")
            
            # Use a tiny inner padding (-0.05) to visually split consecutive blocks cleanly
            segment.shapesize(stretch_wid=stretch_factor - 0.05, stretch_len=stretch_factor - 0.05)
            segment.color("#5E2D91")  # Clean regal purple palette
            segment.penup()
            segment.goto(start_x - (i * self.current_size), start_y)
            self.segments.append(segment)

    def move(self):
        """Shifts all trailing body segments to inherit positions forward recursively."""
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        # Displace the primary target head along the active direction vector
        if len(self.segments) > 0:
            head = self.segments[0]
            x = head.xcor()
            y = head.ycor()

            if self.direction == "UP":
                head.sety(y + self.current_size)
            elif self.direction == "DOWN":
                head.sety(y - self.current_size)
            elif self.direction == "LEFT":
                head.setx(x - self.current_size)
            elif self.direction == "RIGHT":
                head.setx(x + self.current_size)

    def add_segment(self):
        """Appends a new structural piece at the current position of the tail block."""
        stretch_factor = self.current_size / 20.0
        new_seg = turtle.Turtle()
        new_seg.speed(0)
        new_seg.shape("square")
        new_seg.shapesize(stretch_wid=stretch_factor - 0.05, stretch_len=stretch_factor - 0.05)
        new_seg.color("#7C3AED")  # Slightly brighter accent tone for growth
        new_seg.penup()
        
        tail = self.segments[-1]
        new_seg.goto(tail.xcor(), tail.ycor())
        self.segments.append(new_seg)

    def trim_tail(self):
        """Placeholder structural method used if manual truncation logic is required."""
        pass

    def check_self_collision(self):
        """Validates if the primary coordinate item overlaps any trailing body part."""
        if len(self.segments) <= 1:
            return False
            
        head = self.segments[0]
        # Skip the immediate neck segment to prevent false triggers during sharp turns
        for segment in self.segments[2:]:
            if head.distance(segment) < (self.current_size * 0.8):
                return True
        return False

    def check_wall_collision(self):
        """Validates if the primary coordinate item hits the external boundary definitions."""
        if len(self.segments) == 0:
            return False
            
        head = self.segments[0]
        x = head.xcor()
        y = head.ycor()
        margin = self.current_size / 2

        # Check if boundary limits are crossed taking segment margins into account
        if (x - margin < LEFT_LIMIT or x + margin > RIGHT_LIMIT or 
            y - margin < BOTTOM_LIMIT or y + margin > TOP_LIMIT):
            return True
        return False

    def hide_snake(self):
        """Hides render visibility flags for cleanly painting the overlay screens."""
        for segment in self.segments:
            segment.hideturtle()

    def clear_all(self):
        """Completely purges structural references and clean memory traces."""
        for segment in self.segments:
            segment.hideturtle()
            segment.clear()
        self.segments.clear()


class Food:
    """
    Manages the collectible targets, handling target point calculations,
    icon swaps, and clean mathematical grid-alignment.
    """
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.x = 0
        self.y = 0
        self.current_emoji = random.choice(FRUIT_POOL)

    def respawn(self, snake_segments, current_size):
        """Calculates a vacant mathematical grid row and column inside active boundaries."""
        self.pen.clear()
        
        # Determine total grid columns and rows based on current sizing parameters
        cols = int((RIGHT_LIMIT - LEFT_LIMIT) / current_size)
        rows = int((TOP_LIMIT - BOTTOM_LIMIT) / current_size)

        while True:
            rand_col = random.randint(0, cols - 1)
            rand_row = random.randint(0, rows - 1)

            # Map the clean cell coordinate precisely to center points
            fx = LEFT_LIMIT + (rand_col * current_size) + (current_size / 2)
            fy = BOTTOM_LIMIT + (rand_row * current_size) + (current_size / 2)

            # Prevent spawning directly underneath the snake's body
            valid = True
            for segment in snake_segments:
                if segment.distance(fx, fy) < (current_size * 0.7):
                    valid = False
                    break
            if valid:
                break

        self.x = fx
        self.y = fy
        self.current_emoji = random.choice(FRUIT_POOL)

        # Scale fonts smoothly based on current game grid proportions
        font_size = 24 if current_size >= 40 else (16 if current_size >= 20 else 11)
        y_offset = current_size * 0.35  # Shift text slightly down to vertically center emoji

        self.pen.goto(self.x, self.y - y_offset)
        self.pen.write(self.current_emoji, align="center", font=("Arial", font_size, "normal"))