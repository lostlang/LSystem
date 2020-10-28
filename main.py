import classes

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed = "X"
    rules = {
        "X": "F[S[-X]+SX]"
    }
    rulesTurtle = {
        "X": "F",
        "F": "F",
        "-": "L45",
        "+": "R30",
        "S": "S",
        "[": "C",
        "]": "P"
    }
    tree = classes.LSystem(seed, rules)

    tree.next(14)

    turtle = classes.LSystem(tree.get_value(), rulesTurtle)
    turtle.next()

    file = open("tree.txt", "w")
    print(turtle.get_value(), file=file)
    file.close()
