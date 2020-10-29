import classes

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed = "X"
    rules = {
        "X": "F-[[X]+X]+F[+FX]-X",
        "F": "FF"
    }
    rulesTurtle = {
        "F": "F",
        "X": "",
        "-": "L25",
        "+": "R25",
        "[": "C",
        "]": "P"
    }
    tree = classes.LSystem(seed, rules)

    tree.next(8)

    turtle = classes.LSystem(tree.get_value(), rulesTurtle)
    turtle.next()

    artist = classes.Artist([720, 2800], 180, [1600, 2400], "#9BC2CF", 4, ['#416c41'])
    artist.read_l_system(turtle.get_value())
    artist.save_canvas("test")
