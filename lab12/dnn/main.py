import cv2
import numpy as np

# opencv dnn (deep neural network)

# Co robi funkcja obraz():
# Wczytuje model detekcji obiektów (np. MobileNet-SSD).
# Przetwarza obraz wejściowy i wykrywa obiekty.
# Wyświetla wykryte obiekty z podpisami, jeśli ich pewność > 66%.
def obraz():
    net = cv2.dnn.readNet("dnn/coco/model.pbtxt", "dnn/coco/weights.pb") # Wczytanie sieci neuronowej z pliku konfiguracyjnego i wag
    img = cv2.imread("obraz.jpg") # Wczytanie obrazu z pliku
    out_img = img.copy() # kopia obrazu do rysowania wyników
    blob = cv2.dnn.blobFromImage( # Tworzenie "blobu" - czyli przeskalowanego, przetworzonego obrazu do wejścia sieci
        img, 1.0/127.5, size=(300, 300),
        mean=(127.5, 127.5, 127.5), swapRB=True, crop=False)

    net.setInput(blob) # ustawiamy blob jako wejście do sieci
    result = net.forward() # wykonujemy forward pass - sieć przetwarza obraz

    with open("coco/labels.txt") as file:  # Wczytanie etykiet klas z pliku tekstowego
        labels = [label.strip() for label in file.readlines()]

    for entry in result[0, 0, :, :]: # Iteracja po wykrytych obiektach w wynikach sieci
        try:
            label_index = int(entry[1]) # indeks etykiety
            print(labels[label_index], entry[2]) # nazwa klasy i prawdopodobieństwo
            if entry[2] > 0.66: # jeśli pewność wykrycia jest > 66%
                cols, rows, _ = img.shape # rozmiary obrazu
                # Wyznaczenie prostokąta: przeskalowanie współrzędnych z zakresu 0-1 do pikseli
                x,y,w,h = int(cols*entry[3]),int(rows*entry[4]),int(cols*entry[5]),int(rows*entry[6])
                cv2.rectangle(out_img, (x, y), (x+w, y+h), (255, 0, 0),1,1) # rysowanie prostokąta
        except IndexError:
            print(f"Błąd: indeks {label_index} poza zakresem listy 'labels'")
        except Exception as e:
            print(f"Inny błąd: {e}")

    cv2.imshow("img", out_img) # Wyświetlenie obrazu z narysowanymi prostokątami
    cv2.waitKey(0)

def kamera():
    net = cv2.dnn.readNet("dnn/coco/model.pbtxt", "dnn/coco/weights.pb") # Wczytanie modelu sieci neuronowej
    camera = cv2.VideoCapture(2) # Inicjalizacja kamery
    while True:
        _, frame = camera.read() # Odczyt pojedynczej klatki z kamery

        blob = cv2.dnn.blobFromImage( # Przekształcenie obrazu na blob (czyli odpowiedni format wejścia do sieci)
            frame, 1.0 / 127.5, size=(300, 300),
            mean=(127.5, 127.5, 127.5), swapRB=True,crop=False)
        net.setInput(blob) # ustawienie blobu jako wejścia do sieci
        detections = net.forward() # wykonanie prognozy (forward pass)
        conf_threshold = 0.66 # próg pewności wykrycia obiektu
        with open("coco/labels.txt") as file: # Wczytanie etykiet klas
            class_names = [label.strip() for label in file.readlines()]
        h, w = frame.shape[:2] # wysokość i szerokość obrazu
        for i in range(detections.shape[2]): # Iteracja po wszystkich wykryciach
            confidence = float(detections[0, 0, i, 2]) # pewność wykrycia
            if confidence > conf_threshold:
                class_id = int(detections[0, 0, i, 1]) # numer klasy
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h]) # przeliczenie współrzędnych na piksele
                (x1, y1, x2, y2) = box.astype('int') # konwersja na liczby całkowite
                label = f"{class_names[class_id - 1]}: {confidence * 100:.1f}%" # Przygotowanie tekstu z nazwą klasy i procentową pewnością
                # Rysowanie prostokąta i napisu na klatce
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Wyświetlenie przetworzonej klatki
        cv2.imshow("img", frame)
        if cv2.waitKey(1) == ord('q'): # Przerwanie pętli po wciśnięciu klawisza 'q'
            break;

if __name__ == '__main__':
    obraz()