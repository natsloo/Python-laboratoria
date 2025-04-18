import curses
from random import randint
from time import time

def create_drops(min, max):
    y = 0
    x = randint(min, max)
    v = randint(1,3)
    drop = [x, y, v]
    return drop

def update_drops(drops, height):
    start = time()
    while True:
        counter = 0
        end = time()
        if (end - start) > 2:
            break
        for drop in drops:

            if drop[1] == height:
                drops.pop(counter)
            if drop[2] == 1:
                drop[1] += 1
            elif drop[2] == 2:
                drop[1] += 2
            else:
                drop[1] += 3
            counter += 1

def draw_drops(stdscr, drops, height):
    update_drops(drops, height)
    c = None
    for drop in drops:
        if drop[2] == 1:
            c = "."
        elif drop[2] == 2:
            c = "'"
        else:
            c = "|"
        stdscr.addstr(drop[1], drop[0], c)
    stdscr.retresh()


def main(stdscr):
    curses.curs_set(0)
    drops = []
    height, width = stdscr.getmaxyx() # height - liczba wierszy, width - kolumn
    krople = randint(1,10)
    while (True):
        for i in range(krople):
            d = create_drops(0,width)
            drops.append(d)
        update_drops(drops, height)
        draw_drops(stdscr, drops)


if __name__ == "__main__":
    curses.wrapper(main)