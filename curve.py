# HIT137 - Assignment 2 (Q3)
# Simple recursive polygon with inward dents on each edge (turtle)


import turtle

def koch_inward(t, length, depth):
    """
    One edge of the pattern.
    If depth == 0: just draw the line.
    Otherwise: split into 3 and make the middle third into an inward triangle.
    """
    if depth == 0:
        t.forward(length)
        return

    third = length / 3.0
    # For counter-clockwise polygon, use these turns so the dent points inward.
    koch_inward(t, third, depth - 1)
    t.right(60)
    koch_inward(t, third, depth - 1)
    t.left(120)
    koch_inward(t, third, depth - 1)
    t.right(60)
    koch_inward(t, third, depth - 1)

def draw_polygon(sides, side_len, depth):
    # basic guards so it doesn't crash on weird inputs
    if sides < 3:
        sides = 3
    if side_len < 1:
        side_len = 1
    if depth < 0:
        depth = 0

    screen = turtle.Screen()
    screen.title("Fractal Polygon (inward dents)")
    screen.setup(1000, 800)
    # speed up drawing (no animation)
    screen.tracer(0, 0)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(1)

    angle = 360 / sides

    # start somewhere reasonable so most sizes fit on screen
    t.penup()
    t.goto(-side_len, -side_len / 2)
    t.setheading(0)   # face right
    t.pendown()

    # draw the polygon counter-clockwise so "inward" means inside the shape
    for _ in range(sides):
        koch_inward(t, side_len, depth)
        t.left(angle)

    screen.update()
    turtle.done()

if __name__ == "__main__":
    print("Fractal polygon with inward triangle dents on each edge.")
    try:
        s = int(input("Enter number of sides (>=3): "))
    except ValueError:
        s = 4
        print("Invalid input for sides. Using 4.")
    try:
        L = int(input("Enter side length in pixels (>0): "))
    except ValueError:
        L = 300
        print("Invalid input for side length. Using 300.")
    try:
        d = int(input("Enter recursion depth (>=0): "))
    except ValueError:
        d = 2
        print("Invalid input for depth. Using 2.")

    # note: deeper depth explodes segment count (4^depth per edge). Keep it small.
    draw_polygon(s, L, d)
