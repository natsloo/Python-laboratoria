from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QMessageBox, QListWidget, QListWidgetItem
import requests

class MainWidget(QWidget):                  # dziedziczenie po QWidget
    def __init__(self):                     # konstruktor
        super().__init__()                  # wywołujemy konstruktor klasy nadrzędnej
        self.setWindowTitle("Weather")      # ustawiamy nazwę okna
        
        # self refers to the current object instance, it is essential for accessing attributes and methods within the class
        
        # tworzymy atrybuty - elementy gui
        self.label = QLabel(self)               # "etykieta" z temperaturą
        self.button = QPushButton(self)         # przycisk
        self.edit = QLineEdit("Lublin", self)   # okienko na wpisanie nazwy miasta
        self.city_list = QListWidget(self)      # lista wyszukiwań

        self.button.clicked.connect(self._on_button_clicked)        # po kliknięciu przycisku wywołujemy metodę _on_button_clicked() - connect przyjmuje metodę bez ()
        self.city_list.itemClicked.connect(self._on_city_clicked)   # po kliknięciu na miasto z listy wyników wywołujemy metodę _on_city_clicked()

        layout = QGridLayout(self)              # tworzymy interfejs i jego układ
        layout.addWidget(self.edit, 0, 0, 1, 1)     # addWidget(element, row, column, rowSpan, columnSpan[, alignment=0])
        layout.addWidget(self.button, 0, 1, 1, 1)
        layout.addWidget(self.city_list, 1, 0, 1, 2)
        layout.addWidget(self.label, 2, 0, 1, 2)

    # metoda do wyszukiwania miasta
    def _on_button_clicked(self):
        text = self.edit.text()     # pobieramy tekst z okienka
        #self.label.setText(text)
        response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={text}')  # wysyłamy zapytanie do api pogodowego
        #print(response.json())
        json = response.json()              # tworzymy słownik
        if "results" not in json.keys():    # jeśli nie ma wyników
            QMessageBox.information(self, "Błąd", "Nie ma takiej miejscowości.") # wyskakuje okienko z informacją o błędzie
            return

        # jeśli są wyniki
        results = json["results"]           # podpisujemy tylko wyniki pod zmienną
        self.city_list.clear()              # czyścimy listę wyników  
        for city in results:                                    # dla każdego miasta w wynikach
            item = QListWidgetItem(city["name"])                # pobieramy nazwę
            latitude = city["latitude"]                         # i współrzędne
            longitude = city["longitude"]
            item.setData(Qt.UserRole, (latitude,longitude))     # ustawia w elemencie listy dane o współrzędnych
            self.city_list.addItem(item)                        # dodaje do listy
        #print(latitude, longitude)

    # metoda do zwracania wyników dla danego miasta
    def _on_city_clicked(self):
        latitude, longitude = self.city_list.currentItem().data(Qt.UserRole)    # pobieramy dane z aktualnie wybranego elementu
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m') # wysyłamy zapytanie do api z pobranymi współrzędnymi
        json = response.json()                                                  # tworzymy słownik 
        self.label.setText(f"{json["current"]["temperature_2m"]} stopni C")     # pobieramy z sekcji current temperaturę i wyświetlamy