from game_state import GameState
from team import Team
import turtle
import time

# I generated most of this code with chatGPT but also edited it considerably
# to get it to work as intendend

# Constants
field_width = 533  # Approximation for 53 1/3 yards
field_length = 1100  # 120 yards
scale = 3  # Scaling factor for better visualization

# Scaled dimensions
field_width_scaled = field_width // scale
field_length_scaled = field_length // scale
yard_line_spacing = 10 // scale  # 10 yards
end_zone_length = 100 // scale
# Function to draw a single line
def draw_line(t, x1, y1, x2, y2):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)

# Function to draw hash marks
def draw_hash_marks(t, x_start, x_end, y_positions, yard_line_spacing):
    for x in range(x_start, x_end, 5 * yard_line_spacing):  # Hash marks every 5 yards
        for y in y_positions:
            draw_line(t, x - 2, y, x + 2, y)  # Small horizontal lines

# Function to add yard line numbers
def add_yard_numbers(t, field_length_scaled, field_width_scaled, yard_line_spacing):
    t.penup()
    t.color("white")
    t.hideturtle()
    font = ("Arial", 10, "bold")
    for i in range(-40, 50, 10):  # Numbering every 10 yards
        x = i * yard_line_spacing
        # Add numbers at the bottom of the field
        t.goto(x, -field_width_scaled / 2 - 15)
        t.write(50 - abs(i), align="center", font=font)
        # Add numbers at the top of the field
        t.goto(x, field_width_scaled / 2 + 5)
        t.write(50 - abs(i), align="center", font=font)
def draw_field():
    # Initialize the turtle
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.title("Gridiron Football Field")
    screen.bgcolor("green")  # Set the background to green
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()


    # Draw the field outline
    t.color("white")
    t.pensize(3)
    draw_line(t, -field_length_scaled / 2, -field_width_scaled / 2,
            -field_length_scaled / 2, field_width_scaled / 2)
    draw_line(t, field_length_scaled / 2, -field_width_scaled / 2,
            field_length_scaled / 2, field_width_scaled / 2)
    draw_line(t, -field_length_scaled / 2, field_width_scaled / 2,
            field_length_scaled / 2, field_width_scaled / 2)
    draw_line(t, -field_length_scaled / 2, -field_width_scaled / 2,
            field_length_scaled / 2, -field_width_scaled / 2)

    # Draw the yard lines
    t.color("white")
    for i in range(-50, 51, 5):  # 5-yard intervals
        x = i * yard_line_spacing
        draw_line(t, x, -field_width_scaled / 2, x, field_width_scaled / 2)

    # Draw the end zones
    t.color("blue")
    t.fillcolor("lightblue")
    for x in [-field_length_scaled / 2, field_length_scaled / 2 - end_zone_length]:
        t.penup()
        t.goto(x, -field_width_scaled / 2)
        t.pendown()
        t.begin_fill()
        t.goto(x + end_zone_length, -field_width_scaled / 2)
        t.goto(x + end_zone_length, field_width_scaled / 2)
        t.goto(x, field_width_scaled / 2)
        t.goto(x, -field_width_scaled / 2)
        t.end_fill()

    # Draw hash marks
    hash_mark_positions = [-field_width_scaled * (0.5 - 0.4421875), field_width_scaled * (0.5 - 0.4421875)]
    draw_hash_marks(t, (-field_length_scaled // 2) + 33, (field_length_scaled // 2) - 33, hash_mark_positions, yard_line_spacing)

    # Add yard line numbers
    add_yard_numbers(t, field_length_scaled, field_width_scaled, yard_line_spacing)
    return t, screen



def draw_game_state(game_state, t):
    line_of_scrimmage = (game_state.yard_line - 50) * yard_line_spacing
    first_down_line = line_of_scrimmage + game_state.distance * yard_line_spacing
    if game_state.team_with_posession == game_state.away_team:
        first_down_line = line_of_scrimmage + game_state.distance * yard_line_spacing
    t.color("black")
    draw_line(t, line_of_scrimmage, -field_width_scaled / 2, line_of_scrimmage, field_width_scaled / 2)
    t.color("yellow")
    draw_line(t, first_down_line, -field_width_scaled / 2, first_down_line, field_width_scaled / 2)
    font = ("Arial", 20, "bold")
    t.color("white")
    description = str(game_state).split("\n")
    t.penup()
    t.goto(0, field_width_scaled)
    t.write(description[0], align="center", font=font)
    t.penup()
    t.goto(0, -field_width_scaled)
    t.write(description[1], align="center", font=font)
    t.penup()
    t.goto(0, -1.5 * field_width_scaled)
    t.write(description[2], align="center", font=font)

def erase_game_state(game_state, t):
    NUM_TURTLE_COMMANDS = 17
    for i in range(NUM_TURTLE_COMMANDS):
        t.undo()

if __name__ == '__main__':
    gs = GameState(Team("Minnesota", "MIN", "Vikings"), Team("Green Bay", "GB", "Packers"))
    t, screen = draw_field()
    draw_game_state(gs, t)
    time.sleep(1)
    erase_game_state(gs, t)

    # Finalize
    screen.mainloop()