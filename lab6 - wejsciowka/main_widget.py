from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QMessageBox, QListWidget, QListWidgetItem

from fraction import Fraction


class MainWidget(QWidget):
    def __init__(self):
        super.__init__()
        self.operand = None
        self.setWindowTitle("Kalkulator")

        self.ll = QLineEdit("licznik lewy", self)
        self.ml = QLineEdit("mianownik lewy", self)
        self.lp = QLineEdit("licznik prawy", self)
        self.mp = QLineEdit("mianownik prawy", self)
        self.lw = QLineEdit("licznik wyniku", self)
        self.mw = QLineEdit("mianownik wyniku", self)
        self.operation_list = QListWidget(self)
        self.button = QPushButton(self)

        mult = QListWidgetItem()
        mult.setData(Qt.UserRole, "*")
        div = QListWidgetItem()
        div.setData(Qt.UserRole, "/")
        add = QListWidgetItem()
        add.setData(Qt.UserRole, "+")
        sub = QListWidgetItem()
        sub.setData(Qt.UserRole, "-")
        self.operation_list.addItem(add)
        self.operation_list.addItem(sub)
        self.operation_list.addItem(mult)
        self.operation_list.addItem(div)

        self.button.clicked.connect(self.on_button_clicked)
        self.operation_list.itemClicked.connect(self.on_operation_clicked)

        layout = QGridLayout(self)
        layout.addWidget(self.ll, 0, 0, 1, 1)
        layout.addWidget(self.ml, 1, 0, 1, 1)
        layout.addWidget(self.lp, 0, 2, 1, 1)
        layout.addWidget(self.mp, 1, 2, 1, 1)
        layout.addWidget(self.lw, 0, 4, 1, 1)
        layout.addWidget(self.mw, 1, 4, 1, 1)

        layout.addWidget(self.operation_list, 0, 1, 2, 1)
        layout.addWidget(self.button, 0, 3, 2, 1)

        def on_button_clicked(self):
            lewyl = self.ll.text()
            lewym = self.ml.text()
            f1 = Fraction(lewyl, lewym)
            prawyl = self.lp.text()
            prawym = self.mp.text()
            f2 = Fraction(prawyl, prawym)
            if self.operand == "*":
                try:
                    wynik = f1 * f2
                except (ZeroDivisionError,ValueError) as e:
                    QMessageBox.information(e.)
                self.lw.setText(wynik.__getattribute__("_nominator"))
                self.mw.setText(wynik.__getattribute__("_denominator"))
            elif self.operand == "+":
                wynik = f1 + f2
                self.lw.setText(wynik.__getattribute__("_nominator"))
                self.mw.setText(wynik.__getattribute__("_denominator"))
            elif self.operand == "-":
                wynik = f1 - f2
                self.lw.setText(wynik.__getattribute__("_nominator"))
                self.mw.setText(wynik.__getattribute__("_denominator"))
            elif self.operand == "/":
                wynik = f1 / f2
                self.lw.setText(wynik.__getattribute__("_nominator"))
                self.mw.setText(wynik.__getattribute__("_denominator"))
            else:
                QMessageBox.information("Coś poszło nie tak.")

        def on_operation_clicked(self):
            self.operand = self.operation_list.currentItem()