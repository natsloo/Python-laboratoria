import curses
import os
import pickle
import sys

# "stałe"
#PANEL_HEIGHT = 10

# funkcje
# def draw_separator(stdscr, rows, cols):
#     y = rows - (PANEL_HEIGHT + 1)
#     #stdscr.hline(y, 0, '-', cols)
#     stdscr.addstr(y, 0, '-' * cols)
#     stdscr.refresh()

def show_title_screen(stdscr, rows, cols):
    contents = ["Map maker", "version 1.0", "", "Naciśnij dowolny klawisz aby kontynuować"]     #definicja listy
    offset_y = (rows - len(contents)) // 2      # len zwraca długość dowolnego kontenera
    for i, line in enumerate(contents):         # enumerate(contents) to funkcja, która podczas iteracji zwraca pary (numer_indeksu, element)
        y = offset_y + i                        # zatem pętla przypisuje przy każdej iteracji i = indeks, line = treść linii
        x = (cols - len(line)) // 2             # dzielenie całkowite //
        stdscr.addstr(y, x, line)
    stdscr.refresh()
    stdscr.getch()

def draw_map(stdscr, rows, cols, structures, available_structures, active_structure):
    stdscr.clear()
    stdscr.addstr(rows-1, 0, list(available_structures.keys())[active_structure]) # w prawym dolnym rogu wypisuje nazwę aktualnie wybranej struktury
    for y, x, name in structures:
        structure = available_structures[name]
        draw_structure(stdscr,x,y,structure,centered=True)


    # for structure in structures:
    #     y, x = structure
    #     stdscr.addstr(y,x,'*')
    #     # stdscr.addstr(structure[0], structures[1], '*')

    # global - zmienna, której używamy wewnątrz funkcji, ma być traktowana jako zmienna globalna, istniejąca również na zewnątrz funkcji
    #global barracks

    # for i, line in enumerate(barracks[1]):
    #     stdscr.addstr(i, 0, line)

    #for y, x in structures:
        #stdscr.addstr(y, x, '*')
        #draw_structure(stdscr, x, y, barracks, centered = True)

def draw_structure(stdscr, x, y, structure, centered = False, labeled = False, highlighted = False):    # argumenty domyślne
    name, art = structure
    offset_y = y - len(art)
    offset_x = x - len(art[0])// 2 if centered else x
    for i, line in enumerate(art):
        stdscr.addstr(offset_y + i, offset_x, line, curses.color_pair(1 if highlighted else 0))         # operator trójargumentowy
    if labeled:
        stdscr.addstr(offset_y + len(art) + 1, offset_x, name, curses.color_pair(1 if highlighted else 0))

def add_structure(structures, y,x, available_structures, active_structure):
    name = list(available_structures.keys())[active_structure]
    structures.append((y, x, name))

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



def load_structures_from_directory():
    path = "structures"
    dir_list = os.listdir(path) # funkcja zwraca listę nazw plików i katalogów znajdujących się w podanej ścieżce
    #print(dir_list)
    result = {}

    for file_name in dir_list:
        filepath = os.path.join(path, file_name)
        structure = load_structure_from_file(filepath)
        result[structure[0]] = structure
    return result

#barracks = load_structure_from_file('structures/barracks.txt')

def save_map(structures): # zapis mapy do pliku binarnego za pomocą modułu pickle
    file = open("map.bin", "wb")  # moduł pickle zajmuje się serializacją obiektów,
    pickle.dump(structures, file) # a funkcja dump zapisuje wynik tej operacji do pliku
    file.close()

def load_map(path):
    file = open(path, "rb")
    structures = pickle.load(file)
    file.close()
    return structures

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
    available_structures = load_structures_from_directory()
    active_structure = 0

    if len(sys.argv) == 2:
        structures = load_map(sys.argv[1])

    while True:
        draw_map(stdscr, height, width, structures, available_structures, active_structure)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse() # jeśli został kliknięty lewy przycisk myszy =
            if bstate & curses.BUTTON1_CLICKED:    # dodaj w tym miejscu obecnie wybraną (aktywną) strukturę
                add_structure(structures, y, x, available_structures, active_structure)
        elif key == ord("q"): # funkcja ord() zwraca kod Unicode dla znaku będącego argumentem
            return            # q - quit
        elif key == ord("s"):
            save_map(structures) # s - save
        elif key in range(ord("1"), ord("4")+1): # przełączanie między wybranymi strukturami: wartości 1-4
            active_structure = key - ord("1")    # indeks aktywnej struktury obliczany jako key - kodUnicode(znak)

        stdscr.addstr(0,0,str(key))


if __name__ == '__main__':
    curses.wrapper(main)
    #print(load_structures_from_directory())