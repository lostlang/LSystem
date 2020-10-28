import turtle

import random

file = open("tree.txt")
k = file.read()
i = 0


turtle.up()
turtle.right(90)
turtle.forward(370)
turtle.left(90)
turtle.down()

b_step = 150
step = b_step
turtle_stack = []

turtle.left(90)
turtle.color("#90EE90")
turtle.tracer(False)


while True:
    try:
        action = k[i]
        value_action = ""
    except IndexError:
        break
    if action in ["R", "L"]:
        i += 1
        try:
            while k[i] not in ["R", "L", "C", "P", "F", "S"]:
                value_action += k[i]
                i += 1
        except IndexError:
            pass
    else:
        i += 1

    if action == "S":
        step = step * 0.8
    elif action == "F":
        turtle.forward(step)
    elif action == "R":
        turtle.right(random.randint(0, int(value_action)))
    elif action == "L":
        turtle.left(random.randint(0, int(value_action)))
    elif action == "C":
        turtle_stack.append([
            turtle.xcor(),
            turtle.ycor(),
            turtle.heading(),
            step
        ])
    elif action == "P":
        turtle.up()
        turtle.setx(turtle_stack[-1][0])
        turtle.sety(turtle_stack[-1][1])
        turtle.setheading(turtle_stack[-1][2])
        turtle.down()
        step = turtle_stack[-1][3]
        turtle_stack.pop()

turtle.tracer(True)
turtle.done()

