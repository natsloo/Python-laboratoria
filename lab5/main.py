from PySide6.QtWidgets import QApplication, QWidget

from main_widget import MainWidget


def main ():
    app = QApplication()    # tworzymy instancję aplikacji QApplication
    widget = MainWidget()   # tworzymy obiekt MainWidget, który jest głównym oknem aplikacji
    widget.show()           # wyświetlamy okno, bo domyślnie jest ukryte
    return app.exec()       # uruchamia główną pętlę zdarzeń

if __name__ == '__main__':
    main()