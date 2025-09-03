import turtle

def koch_edge(t, length, depth, inward=True):
    if depth == 0:
        t.forward(length)
        return

    length /= 3.0
    sgn = -1 if inward else 1   

    koch_edge(t, length, depth - 1, inward)
    t.left(60 * sgn)
    koch_edge(t, length, depth - 1, inward)
    t.right(120 * sgn)
    koch_edge(t, length, depth - 1, inward)
    t.left(60 * sgn)
    koch_edge(t, length, depth - 1, inward)


def draw_fractal_polygon(sides, side_len, depth, inward=True):
    scr = turtle.Screen()
    scr.title("Inward-indented fractal polygon")
    scr.tracer(0, 0) 

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(1)

    exterior_angle = 360.0 / sides

   
    t.penup()
    t.goto(-side_len * 0.6, side_len * 0.6) 
    t.pendown()

    for _ in range(sides):
        koch_edge(t, side_len, depth, inward=inward)
        t.right(exterior_angle)

    scr.update()
    turtle.done()


sides = int(input("Enter the number of sides: "))
side_len = float(input("Enter the side length (pixels): "))
depth = int(input("Enter the recursion depth: "))

if sides < 3:
    print("Number of sides must be at least 3. Using 3.")
    sides = 3

draw_fractal_polygon(sides, side_len, depth, inward=True)
