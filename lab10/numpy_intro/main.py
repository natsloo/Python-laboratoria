import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def ex1():
    array = np.array([1,2,3,4],dtype=np.uint8)      # tworzymy tablice z listy o typie uint8
    array2 = np.array([[1,2,3,4,5],[1,2,3,4,5]])
    print(array,array.shape,array.dtype)            # wyswietlamy tablice, jej wymiary i typ
    print(array2, array2.shape, array2.dtype)

def ex2():
    img = np.zeros((100,100),dtype=np.uint8)        # robimy tablicę 100 x 100 wypelniona zerami (czarno-bialy, jednokanalowy obraz, 0 = czarny)
    img[50,50] = 255                                # ustawiamy srodkowy piksel na 255, czyli bialy
    plt.imshow(img, cmap="Spectral_r")              # wyswietlamy obrazek z uzyciem mapy barw
    plt.show()

def ex3():
    img = np.random.randint(0,256,(100,100),dtype=np.uint8) # obraz (szum) 100 x 100, kazdy piksel ma losowa wartosc z przedzialu 0-255
    plt.imshow(img)
    plt.show()

def ex4():
    img1 = np.random.normal(loc=0,scale=50,size=(100,100)) # obraz 100×100, w którym wartości są losowo pobierane z rozkładu normalnego (Gaussa)
    # średnia loc=0 (czyli wartości skupione wokół zera),
    # odchylenie standardowe scale=50 (określa rozrzut wartości wokół średniej),
    #fig, (ax1,ax2) = plt.subplots(1,2)
    img = np.random.randint(0, 256, (512,512), dtype=np.uint8) # # obraz (szum) 100 x 100, kazdy piksel ma losowa wartosc z przedzialu 0-255
    #ax1.imshow(img1)
    #ax2.imshow(img)
    #plt.imshow(img, cmap="gray")
    #plt.show()
    return (img,img1)

def ex5(img, bri, con):
    fig, (ax1,ax2) = plt.subplots(1,2)      # tworzymy 1 wiersz i 2 kolumny wykresów
    img2 = np.clip(img.astype(np.float32)*con + bri, 0, 255).astype(np.uint8)   # modyfikujemy jasność i kontrast + przycinamy wartości
    ax1.imshow(img)
    ax2.imshow(img2)
    #matplotlib.colors.Normalize(vmin=0, vmax=255)
    plt.show()

def ex6(img, x, y, w, h):
    result = img.copy()                     # tworzymy kopię obrazu, żeby nie modyfikować oryginału
    result[y:y+h, x:x+w] = 255              # ustawiamy piksele na biale, tak zeby powstal prostokat
    plt.imshow(result)
    plt.show()
    return result

def ex8(img):
    img = img.copy()
    img = 255 - img                     # negatyw - czarne(0) stają się biale(255) i na odwrot
    plt.imshow(img)
    plt.show()

def ex9():
    line = np.linspace(0,255,100,dtype=np.uint8) # tworzymy 1-wymiarową tablicę line z 100 wartościami równomiernie rozłożonymi od 0 do 255
    img = np.tile(line,(100,1)) # powielamy ten wiersz 100 razy w pionie, tworząc obraz 100×100 pikseli
    # – każdy wiersz jest identyczny: gradient od czarnego do białego (lewa → prawa strona)
    plt.imshow(img)
    plt.show()

def ex7(img):
    img = img.copy()
    threshold = 150
    img[img > threshold] = 255 # jesli piksele maja wartosc > progu, to sa max
    img[img < 50] = 0          # jesli ponizej 50 - min
    plt.imshow(img)
    plt.show()
    return img

def ex10(freq):
    x = np.linspace(0,2*np.pi*freq,100) # 100 punktów od 0 do 2π * freq
    y = np.sin(x)                       # obliczamy wartość funkcji sinus dla każdego x
    plt.figure()
    plt.plot(x, y)                      # rysujemy sinus
    plt.show()

def ex11(freq):
    x = np.linspace(0,2*np.pi*freq,100) # generujemy 100 punktów od 0 do 2π * freq, czyli fragment osi X zawierający freq pełnych okresów sinusa.
    xx,_ = np.meshgrid(x,x) # tworzy dwie siatki 2D z wektora x: xx: każdy wiersz to x (zmienia się poziomo), _: (nieważna tutaj), odpowiadająca osi Y, ale nie jest używana
    img = np.sin(xx) # oblicza wartość sinusa dla każdej wartości w xx, czyli fale poziome (wartosci w pionie sie zmieniaja)
    plt.imshow(img)
    plt.show()

def ex12(freq):         # jak wyzej, tylko w druga strone
    x = np.linspace(0,2*np.pi*freq,100)
    _,xx = np.meshgrid(x,x)
    img = np.sin(xx)
    plt.imshow(img)
    plt.show()

def ex13(freq):     # dwuwymiarowy wzór fal sinusoidalnych w poziomie i pionie, czyli siatkę fal (tzw. wzór interferencyjny)
    x = np.linspace(0,2*np.pi*freq,512)
    xx,yy = np.meshgrid(x,x)

    img = np.sin(xx) + np.sin(yy)
    plt.imshow(img, cmap="gray")
    plt.show()

def ex14(img, mask): # zamienia obraz i maskę na typ float32, by uniknąć błędów zaokrągleń lub przepełnienia.
    img = img.astype(np.float32) * mask.astype(np.float32)
    plt.imshow(img)
    plt.show()

if __name__ == '__main__':
    # ex1()
    # ex2()
    # ex3()
    # (img1, img2) = ex4()
    # #ex5(img1, 0, 1.2)
    #
    # img3 = ex6(img1,60,50,20,45)
    #
    # ex5(img1,0,1.2)
    # ex8(img3)
    # ex9()
    # ex7(img1)
    # ex10(5)
    ex11(5)
    ex12(5)
    ex13(32)
    #ex14(img1, ex13(5))