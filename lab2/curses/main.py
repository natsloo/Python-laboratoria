import curses

# "stałe"
PANEL_HEIGHT = 10

# funkcje
def draw_separator(stdscr, rows, cols):
    y = rows - (PANEL_HEIGHT + 1)
    #stdscr.hline(y, 0, '-', cols)
    stdscr.addstr(y, 0, '-' * cols)
    stdscr.refresh()

def show_title_screen(stdscr, rows, cols):
    contents = ["Map maker", "version 1.0", "", "Naciśnij dowolny klawisz aby kontynuować"]     #definicja listy
    offset_y = (rows - len(contents)) // 2      # len zwraca długość dowolnego kontenera
    for i, line in enumerate(contents):         # enumerate(contents) to funkcja, która podczas iteracji zwraca pary (numer_indeksu, element)
        y = offset_y + i                        # zatem pętla przypisuje przy każdej iteracji i = indeks, line = treść linii
        x = (cols - len(line)) // 2             # dzielenie całkowite //
        stdscr.addstr(y, x, line)
    stdscr.refresh()
    stdscr.getch()

def draw_map(stdscr, rows, cols, structures):
    # for structure in structures:
    #     y, x = structure
    #     stdscr.addstr(y,x,'*')
    #     # stdscr.addstr(structure[0], structures[1], '*')

    # global - zmienna, której używamy wewnątrz funkcji, ma być traktowana jako zmienna globalna, istniejąca również na zewnątrz funkcji
    global barracks

    # for i, line in enumerate(barracks[1]):
    #     stdscr.addstr(i, 0, line)

    for y, x in structures:
        #stdscr.addstr(y, x, '*')
        draw_structure(stdscr, x, y, barracks, centered = True, labeled = True, highlighted = True)

def draw_structure(stdscr, x, y, structure, centered = False, labeled = False, highlighted = False):    # argumenty domyślne
    name, art = structure
    offset_y = y - len(art)
    offset_x = x - len(art[0])// 2 if centered else x
    for i, line in enumerate(art):
        stdscr.addstr(offset_y + i, offset_x, line, curses.color_pair(1 if highlighted else 0))         # operator trójargumentowy
    if labeled:
        stdscr.addstr(offset_y + len(art) + 1, offset_x, name, curses.color_pair(1 if highlighted else 0))

def add_structure(structures, y,x, rows):
    max_y = rows - (PANEL_HEIGHT + 1)
    if y < max_y:
        structures.append((y,x))

def load_structure_from_file(path):
    # alternatywnie:
    #fd = open(path)
    #fd.close()

    # with - zarządzanie zasobami - po zakończeniu tego bloku plik zostanie automatycznie zamknięty, nawet jeśli nastąpi jakiś błąd
    # open(path) - otwiera plik wskazany ścieżką i zwraca obiekt pliku do manipulowania jego zawartością
    # as fd - obiekt pliku zwrócony funkcją open jest podpisany pod zmienną fd

    with open(path) as fd:
        content = fd.read()
        lines = content.splitlines()
        #print(lines)
        name, image = lines[0], lines[1:]
        return name, image      # zwracamy krotkę

barracks = load_structure_from_file('structures/barracks.txt')

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    height, width = stdscr.getmaxyx()
    stdscr.clear()
    #stdscr.addstr(5, 10, f"* {height}x{width} *")
    show_title_screen(stdscr, height, width)
    stdscr.clear()
    structures = []
    while True:
        draw_map(stdscr, height, width, structures)
        draw_separator(stdscr, height, width)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_CLICKED:
                add_structure(structures, y,x, height)

    #stdscr.refresh()



if __name__ == '__main__':
    curses.wrapper(main)