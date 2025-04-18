from PySide6.QtWidgets import QApplication, QWidget

from main_widget import MainWidget

def main():
    app = QApplication()
    widget = QWidget()
    widget.show()
    return app.exec()

if __name__ == '__main__':
    main()