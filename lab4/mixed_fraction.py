from fraction import Fraction

class MixedFraction(Fraction):                                  # klasa dziedziczy po Fraction
    def __str__(self):                                          # metoda do wypisywania ułamka
        whole = self.nominator//self.denominator                # dzielenie całkowite, żeby wyznaczyć całość
        nominator_rest = self.nominator % self.denominator      # reszta z dzielenia
        if nominator_rest == 0:                                 # jeśli reszta == 0, metoda zwraca tylko całość
            return str(whole)
        elif whole == 0:                                        # jeśli ułamek < 1, metoda wywołuje metodę __str__ klasy bazowej
            return super().__str__()
        else:                                                   # zwraca liczbę mieszaną
            return f"{whole} {nominator_rest}/{self.denominator}"