import cv2

# Klasa bazowa do wyświetlania i przetwarzania obrazu z kamery z suwakiem (trackbarem)
class Viewer:
    def __init__(self, slider_name, current_value, end_value):
        self.slider_name = slider_name
        self.start_value = current_value # wartość początkowa suwaka
        self.end_value = end_value
        self.cam = cv2.VideoCapture(1) # otwieranie strumienia wideo - kamery (liczba) lub pliku wideo (nazwa pliku)
        if self.cam is not None and self.cam.isOpened(): # sprawdzamy, czy kamera zostala poprawnie otwarta
            cv2.namedWindow("okno") # tworzymy i nazywamy okno
            cv2.createTrackbar(slider_name, "okno", current_value, end_value, lambda x:x) # dodajemy do okna suwak do zmieniania wartosci do sterowania paramterami obrazu

    def get_slider_value(self):
        # Pobiera bieżącą wartość z trackbara (suwaka)
        return cv2.getTrackbarPos(self.slider_name, "okno")

    def process_frame(self, frame, value):
        # Przetwarza pojedynczą klatkę obrazu (metoda do nadpisania w klasach dziedziczących)
        return frame

    def run(self):
        value = 0
        while True:
            ok, frame = self.cam.read() # czytamy kolejną klatkę z kamery
            if not ok:
                break
            cv2.flip(frame, 1, frame) # odbicie lustrzane obrazu (flip w poziomie)
            value = self.get_slider_value() # pobranie aktualnej wartości suwaka
            frame = self.process_frame(frame,value)  # przetwarzanie klatki na podstawie wartości suwaka
            cv2.imshow("okno", frame) # wyświetlenie przetworzonej klatki
            if cv2.waitKey(1) == ord('q'): # wyjście z pętli po wciśnięciu 'q'
                break

# Klasa dziedzicząca – regulacja jasności obrazu
class BrightnessViewer(Viewer):
    def __init__(self):
        super().__init__("jasnosc", 256, 256*2-1) # ustawienie suwaka od 0 do 511

    def get_slider_value(self):
        return super().get_slider_value() - 256 # przesunięcie wartości suwaka, by mieć zakres od -256 do +255

    def process_frame(self, frame, value):
        return cv2.add(frame, value) # zwiększamy lub zmniejszamy jasność każdej klatki

# Klasa dziedzicząca – filtr rozmycia Gaussa
class GaussianViewer(Viewer):
    def __init__(self):
        super().__init__("gauss",0,50) # suwak od 0 do 50

    def get_slider_value(self):
        return super().get_slider_value()*2+1 # zamiana na nieparzystą liczbę (wymóg kernela Gaussa)

    def process_frame(self, frame, value):
        slider_value = self.get_slider_value()
        return cv2.GaussianBlur(frame,(slider_value,slider_value),0) # zastosowanie rozmycia Gaussa

# Klasa dziedzicząca – filtr medianowy
class MedianViewer(Viewer):
    def __init__(self):
        super().__init__("median",0,50) # suwak od 0 do 50

    def get_slider_value(self):
        return super().get_slider_value()*2+1 # tylko nieparzyste wartości dla rozmiaru kernela

    def process_frame(self, frame, value):
        return cv2.medianBlur(frame,self.get_slider_value()) # zastosowanie medianowego rozmycia

# Klasa dziedzicząca – modyfikacja składowej H (odcień) w przestrzeni HSV
class HSVViewer(Viewer):
    def __init__(self):
        super().__init__("HSV",0,180) # zakres H w przestrzeni HSV to 0–179

    def process_frame(self, frame, value):
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # konwersja do przestrzeni HSV (hue, saturation, value)
        hue = frame[:,:,0] # wyodrębnienie kanału H (odcień); dostawanie sie do innych kanalow przez zwiekszenie ostatniej wartosci
        # frame[y, x, c]
        # to oznacza:
        # y – wiersz (wysokość obrazu, czyli oś pionowa),
        # x – kolumna (szerokość obrazu, czyli oś pozioma),
        # c – kanał koloru (np. 0 – niebieski w BGR, 0 – odcień w HSV itd.).
        frame[:,:,0] = (hue + super().get_slider_value()) % 180 # przesunięcie odcienia i zawinięcie modulo 180
        return cv2.cvtColor(frame, cv2.COLOR_HSV2BGR) # konwersja z powrotem do BGR

# pokazanie statycznego obrazu
def ex1():
    img = cv2.imread("img.png") # wczytanie obrazu z pliku
    cv2.imshow("okno", img) # wyświetlenie obrazu
    cv2.waitKey(0) # oczekiwanie na dowolny klawisz

# ręczna obsługa kamery z suwakiem do regulacji jasności (bez klas)
def ex2():
    cam = cv2.VideoCapture(0)
    if cam is not None and cam.isOpened():
        cv2.namedWindow("okno")
        brightness = 0
        slider = cv2.createTrackbar("jasnosc", "okno", 256, 256*2-1, lambda x:x)
        while True:
            ok, frame = cam.read()
            if not ok:
                break
            cv2.flip(frame, 1, frame)
            brightness = cv2.getTrackbarPos("jasnosc", "okno") - 256
            frame = cv2.add(frame, brightness)
            cv2.imshow("okno", frame)
            if cv2.waitKey(1) == ord('q'):
                break


def main():
    # viewer = Viewer("slider",0,255)
    # viewer = BrightnessViewer()
    # viewer = GaussianViewer()
    # viewer = MedianViewer()
    viewer = HSVViewer()
    viewer.run()


if __name__ == '__main__':
    main()