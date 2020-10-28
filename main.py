import classes

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed = "X"
    rules = {
        "X": "F[S[-X]+SX]"
    }
    rulesTurtle = {
        "X": "F",
        "F": "F10",
        "-": "L45",
        "+": "R30~40",
        "S": "S",
        "[": "C",
        "]": "P"
    }
    tree = classes.LSystem(seed, rules)

    tree.next(3)

    turtle = classes.LSystem(tree.get_value(), rulesTurtle)
    turtle.next()

    artist = classes.Artist([0, 0], 0, [20, 20], 10, ['red'])
    artist.read_l_system(turtle.get_value())

    file = open("tree.txt", "w")
    print(turtle.get_value(), file=file)
    file.close()
