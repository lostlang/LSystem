import classes
import time
import numpy

seed = "X"
rules = {
    "X": "F-[[X]+X]+F[+FX]-X",
    "F": "FF"
}
rulesTurtle = {
    "F": "F0-1",
    "X": "",
    "-": "L25",
    "+": "R25",
    "[": "C",
    "]": "P"
}

def bench(seed=seed,
          rules=rules,
          rulesTurtle=rulesTurtle,
          count=10):
    all_time = 0
    min_time: int

    for i in range(count):
        start_time = time.time()

        tree = classes.LSystem(seed, rules)
        tree.next(8)

        turtle = classes.LSystem(tree.get_value(), rulesTurtle)
        turtle.next()

        artist = classes.ArtistNumpy([720, 2800], 90, [1600, 2400],
                                      "#9BC2CF", 8, ['#416c41'])
        artist.read_l_system(turtle.get_value())

        artist.draw()

        artist.save_canvas("testNP")

        end_time = time.time()

        time_bench = end_time - start_time

        all_time += end_time - start_time

        try:
            min_time = min(min_time, time_bench)
        except:
            min_time = time_bench

    return min_time, all_time / count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("log.txt", 'a') as log:
        print(bench(), file=log)
