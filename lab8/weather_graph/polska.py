import math
from datetime import datetime, timedelta

import geopandas as gpd
import matplotlib.pyplot as plt
import requests

cities = [                              # lista miast z koordami
    ("Warszawa", 52.2297, 21.0122),
    ("Kraków" ,50.0647, 19.9450),
    ("Łódź" ,51.7592, 19.4560),
    ("Wrocław", 51.1079, 17.0385),
    ("Poznań", 52.4064, 16.9252),
    ("Gdańsk", 54.3520, 18.6466),
    ("Szczecin", 53.4285, 14.5528),
    ("Bydgoszcz", 53.1235, 18.0084),
    ("Lublin",51.2465, 22.5684),
    ("Katowice",50.2649, 19.0238),
    ("Białystok",53.1325, 23.1688),
    ("Rzeszów",50.0413, 21.9990),
    ("Olsztyn",53.7784, 20.4801),
    ("Kielce",50.8661, 20.6286),
    ("Opole",50.6751, 17.9213),
    ("Zielona Góra",51.9355, 15.5062)
]

class PolandMap:
    def __init__(self, shapefile_url='ne_50m_admin_0_countries.zip'):
        #default_url = 'https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip'
        self.shapefile_url = shapefile_url #or default_url                  # wczytanie danych geograficznych świata z pliku
        self._world = gpd.read_file(self.shapefile_url)
        self.poland = self._world[self._world['ADMIN'] == 'Poland']         # wybranie tylko danych dla polski
        self.active_index = 0                                               # indeks aktywnego miasta do wykresu temperatury (0 = Warszawa)

    # główna metoda do rysowania wykresów
    def draw(self):
        fig, (map_ax, temp_ax) = plt.subplots(2, 1, figsize=(8,12))         # metoda subplots zwraca fig(obiekt główny) i wykres lub tablicę wykresów, którą można rozpakować jako krotkę
        self.fig = fig                                                      # subplots(nr_rows,nr_cols)
        self.temp_ax = temp_ax
        self.map_ax = map_ax
        self.poland.plot(ax=map_ax, color='lightgrey', edgecolor='black')   # narysowanie mapy Polski
        self.data = self.get_data()                                         # pobranie danych z api
        self.draw_cities(map_ax, self.data, fig)                            # zaznaczenie kropek miast na mapie
        self.draw_cities_labels(map_ax, self.data)                          # narysowanie etykiet miast
        self.draw_temperature_plot(temp_ax, self.data)
        plt.tight_layout()                                                  # zmiana marginesów na ścisłe
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)    # reakcja na kliknięcie myszą

    # metoda do zaznaczania kropek miast
    def draw_cities(self, ax, data, fig):
        x = [city[2] for city in cities]                                    # tworzenie lisy długości i szerokości geograficznych dla wszystkich miast
        y = [city[1] for city in cities]
        c = [entry["hourly"]["temperature_2m"][0] for entry in data]        # pobranie temperatury dla danego miasta
        plot = ax.scatter(x, y, c=c, cmap="Spectral_r")                     # metoda scatter tworzy wykres punktowy i mapuje temperatury na kolor punktów
        fig.colorbar(plot, ax=ax, label="C")                                # legenda kolorów

    # metoda do rysowania etykiet z nazwą miasta i temperaturą
    def draw_cities_labels(self, ax, data):
        for city, entry in zip(cities, data):                               # łącznie nazwy miasta i danych o temperaturze
            label = f"{city[0]}\n{entry["hourly"]["temperature_2m"][0]}"    # odpowiedni format stringa etykiety
            ax.text(city[2], city[1], label, ha="center", bbox=dict(boxstyle="Round,pad=0.2", fc="white", alpha=0.2))   # narysowanie etykiety na wykresie

    # metoda do pobierania danych z Open-Meteo API
    def get_data(self):
        start_date = datetime.now().date()                                  # wybór przedziału czasu do zapytania
        end_date = start_date + timedelta(days=7)

        latitude = ",".join([str(city[1]) for city in cities])              # tworzy ciągi z szerokościami i długościami geograficznymi wszystkich miast (oddzielone przecinkami)
        longitude = ",".join([str(city[2]) for city in cities])

        url = (                                                             # format urla z parametrami
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&hourly=temperature_2m"
            f"&start_date={start_date}&end_date={end_date}"
            f"&timezone=Europe/Warsaw"
        )

        response = requests.get(url)                                        # wysłanie zapytania pod podany url
        data = response.json()                                              # konwertuje odpowiedź z JSON na słownik Pythona
        for i in range(len(cities)):                                        # wyświetlenie w konsoli danych
            print(cities[i][0], data[i]["hourly"]["temperature_2m"][0])
        return data                                                         # zwrot danych

    # metoda do rysowania wykresu godzinowego temperatury dla wybranego miasta
    def draw_temperature_plot(self, ax, data):
        format = "%Y-%m-%dT%H:%M"                                           # ustalenie formatu daty i czasu z danych z API do wykresu
        hourly = data[self.active_index]["hourly"]                          # pobranie danych godzinowych temperatury dla aktualnie wybranego miasta (active_index)
        hours = [datetime.strptime(i, format) for i in hourly["time"]]      # konwersja ciągów znaków z godzinami na obiekty datetime dla osi X wykresu
        ax.plot(hours, hourly["temperature_2m"], label="temperatura", color="red")      # rysowanie wykresu temperatury w czasie
        ax.tick_params(axis="x",labelrotation = 45)                         # obrót etykiet na osi x o 45 stopni
        ax.grid(True)                                                       # dodatnie siatki do wykresu
        self.fig.canvas.draw()                                              # odświeżenie wykresu po jego aktualizacji (związane chyba z klikaniem na kropki - nie działa?)

    # metoda do obsługi kliknięć na mapie
    def onclick(self, event):
        if event.inaxes == self.map_ax:                                     # sprawdzenie, czy kliknięcie nastąpiło w obrębie mapy
            for i, city in enumerate(cities):                               # iteracja po wszystkich miastach, by sprawdzić, czy kliknięto w obrębie któregoś z nich
                print(city[0], math.hypot(city[2] - event.xdata, city[1] - event.ydata))
                if math.hypot(city[2] - event.xdata, city[1] - event.ydata) < 0.25:     # obliczenie odległości między punktem kliknięcia a pozycją miasta
                    self.fig.set_label(city[0])                             # ustawienie etykiety wykresu na nazwę miasta
                    self.active_index = i                                   # aktywny indeks = kliknięte miasto
                    self.draw_temperature_plot(self.temp_ax, self.data)     # ponowne rysowanie nowego wykresu temperatury
                print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %   # wypisanie danych do kliknięciu do konsoli
                      ('double' if event.dblclick else 'single', event.button,
                       event.x, event.y, event.xdata, event.ydata))


if __name__ == '__main__':
    poland = PolandMap()
    poland.draw()
    plt.show()