import curses
#moduł curses, który służy do tworzenia interaktywnych aplikacji tekstowych w terminalu

def main(stdscr):
    curses.curs_set(0)
    # funkcja do ustawiania stanu kursora: 0 - niewidoczny, 1 - normalny, 2 - bardzo widoczny

    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    # ustawienie eventów myszy, które mają być obługiwane/śledzone/raportowane:
    # ALL_MOUSE_EVENTS - wszystkie zmiany przycisków myszy
    # REPORT_MOUSE_POSITION - pozycja kursora myszy

    height, width = stdscr.getmaxyx()
    # pobranie rozmiaru okna terminala:
    # height - liczba wierszy, width - liczba kolumn

    stdscr.clear()
    # wyczyszczenie ekranu

    stdscr.addstr(5, 10, f"* {height}x{width} *")
    # zapisanie stringa z przeciego argumentu na kordach (10, 5)
    # x i y są w curses zawsze zamienione!
    # funkcja nadpisuje wszystko, co było wcześniej w danym miejscu

    stdscr.refresh()
    # natychmiastowe odświeżenie i synchronizacja ekranu, żeby zawierał wprowadzone
    # i jeszcze niewyświetlone zmiany

    stdscr.getch()
    # oczekuje na naciśnięcie dowolnego klawisza przez użytkownika

if __name__ == '__main__':
    curses.wrapper(main)

    # tutaj wrapper przygotowuje terminal, tworzy obiekt całego okna stdscr, który
    # jest tworzony przez curses i przekazuje ten obiekt do wywoływanej przez wrapper
    # funkcji main, która może z niego korzystać, a potem, gdy funkcja się zakończy,
    # wrapper przywraca terminal do defaultowych ustawień żeby nie było z nim problemów
    # (np. brak kursora czy wypisywania inputu)
    # podsumowując: wrapper = "osłonka" dla funkcji