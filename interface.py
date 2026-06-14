import turtle
from config import CANVAS_WIDTH, CANVAS_HEIGHT, TITLE_BAR_Y_LIMIT, LEFT_LIMIT, RIGHT_LIMIT, TOP_LIMIT, BOTTOM_LIMIT

class GameInterface:
    """
    Renders UI cards, draws static backgrounds, updates scores on the HUD, 
    and opens modal dialog boxes.
    """
    def __init__(self):
        # Dedicated pen used exclusively for immutable frame boundaries and branding
        self.hud_pen = turtle.Turtle()
        self.hud_pen.hideturtle()
        self.hud_pen.penup()

        # Dynamic overlay pen for real-time scores, menus, and text metrics
        self.overlay_pen = turtle.Turtle()
        self.overlay_pen.hideturtle()
        self.overlay_pen.penup()

    def draw_static_layout(self):
        """Draws the primary white upper scoring card background and game boundaries."""
        self.hud_pen.clear()

        # Scoreboard Top Card Background Panel
        self.hud_pen.goto(-CANVAS_WIDTH // 2, TITLE_BAR_Y_LIMIT)
        self.hud_pen.color("#FFFFFF")
        self.hud_pen.begin_fill()
        for _ in range(2):
            self.hud_pen.forward(CANVAS_WIDTH)
            self.hud_pen.left(90)
            self.hud_pen.forward(CANVAS_HEIGHT - TITLE_BAR_Y_LIMIT)
            self.hud_pen.left(90)
        self.hud_pen.end_fill()

        # Game Branding Header Title text Component
        self.hud_pen.goto(0, CANVAS_HEIGHT // 2 - 50)
        self.hud_pen.color("#1E293B")
        self.hud_pen.write("🐍 SNAKE EVOLUTION", align="center", font=("Arial", 20, "bold"))

        # Main Playable Field Outer Boundary Line Frame
        self.hud_pen.goto(LEFT_LIMIT, TOP_LIMIT)
        self.hud_pen.color("#94A3B8")
        self.hud_pen.pendown()
        self.hud_pen.pensize(3)
        
        self.hud_pen.goto(RIGHT_LIMIT, TOP_LIMIT)
        self.hud_pen.goto(RIGHT_LIMIT, BOTTOM_LIMIT)
        self.hud_pen.goto(LEFT_LIMIT, BOTTOM_LIMIT)
        self.hud_pen.goto(LEFT_LIMIT, TOP_LIMIT)
        
        self.hud_pen.penup()
        self.hud_pen.pensize(1)

    def draw_hud_values(self, points, high_score, level, fruits_eaten, fruits_needed):
        """Erases old numeric parameters and overwrites fresh current scoreboard values."""
        self.overlay_pen.clear()
        self.overlay_pen.color("#475569")
        
        # Top Metrics Row: Current Points and Historical High Score
        self.overlay_pen.goto(-200, TITLE_BAR_Y_LIMIT + 40)
        self.overlay_pen.write(f"SCORE: {points}", align="left", font=("Arial", 12, "bold"))
        
        self.overlay_pen.goto(200, TITLE_BAR_Y_LIMIT + 40)
        self.overlay_pen.write(f"HI-SCORE: {high_score}", align="right", font=("Arial", 12, "bold"))
        
        # Bottom Metrics Row: Active Difficulty Level and Target Fruit Progression
        self.overlay_pen.goto(-200, TITLE_BAR_Y_LIMIT + 15)
        self.overlay_pen.write(f"LEVEL: {level}", align="left", font=("Arial", 12, "bold"))
        
        self.overlay_pen.goto(200, TITLE_BAR_Y_LIMIT + 15)
        self.overlay_pen.write(f"FRUITS: {fruits_eaten}/{fruits_needed}", align="right", font=("Arial", 12, "bold"))

    def draw_menu_overlay(self, title, message):
        """Generates a styled menu dialogue box in the center of the viewport screen."""
        self.overlay_pen.clear()
        
        # Decorative Drop Shadow Rectangular Layer
        self.overlay_pen.goto(-222, 152)
        self.overlay_pen.color("#64748B")
        self.overlay_pen.begin_fill()
        for _ in range(2):
            self.overlay_pen.forward(444)
            self.overlay_pen.right(90)
            self.overlay_pen.forward(304)
            self.overlay_pen.right(90)
        self.overlay_pen.end_fill()

        # Foreground White Menu Base Card Panel
        self.overlay_pen.goto(-220, 150)
        self.overlay_pen.color("#FFFFFF")
        self.overlay_pen.begin_fill()
        for _ in range(2):
            self.overlay_pen.forward(440)
            self.overlay_pen.right(90)
            self.overlay_pen.forward(300)
            self.overlay_pen.right(90)
        self.overlay_pen.end_fill()

        # Modal Header Title Placement (Dynamic Coloring matching state severity)
        self.overlay_pen.goto(0, 80)
        if "💥" in title or "GAME" in title:
            self.overlay_pen.color("#DC2626")  # Danger Red
        else:
            self.overlay_pen.color("#2563EB")  # System Blue
            
        self.overlay_pen.write(title, align="center", font=("Arial", 18, "bold"))

        # Explanatory Instructions body text block
        self.overlay_pen.goto(0, -40)
        self.overlay_pen.color("#334155")
        self.overlay_pen.write(message, align="center", font=("Arial", 12, "normal"))

    def clear_menu_overlay(self):
        """Clears all text and active menu screen overlay lines."""
        self.overlay_pen.clear()