from math import gcd

class Fraction:

    def __init__(self, nominator, denominator):             # konstruktor ustawiający wartości
        if denominator == 0:                                # jeśli mianownik == 0
            raise ValueError("Denominator = 0")             # raise służy do zgłaszania wyjątków
        self.nominator = nominator
        self.denominator = denominator
        if nominator != 0:
            self.__reduce()

    def is_integer(self):                                   # metoda do sprawdzenia, czy ułamek jest liczbą całkowitą
        return self.nominator % self.denominator == 0

    # def to_string(self):
    #     return f"{self.nominator}/{self.denominator}"
    # równolegle, ale z innym wywołaniem:

    def __str__(self):                                      # metoda __str__ odpowiada za tekstową reprezentację ułamka
        return f"{self.nominator}/{self.denominator}"

    def __float__(self):                                    # zwraca ułamek dziesiętny
        return float(self.nominator/self.denominator)

    def __reduce(self):                                     # __nazwa - metoda prywatna do skracania ułamka
        gcd_value = gcd(self.nominator,self.denominator)
        self.nominator //= gcd_value
        self.denominator //= gcd_value

    def __mul__(self, other):
        # if other.__class__.__name__ == Fraction.__name__:
        if isinstance(other, Fraction):                     # mnożenie dwóch ułamków
            nominator = self.nominator * other.nominator
            denominator = self.denominator * other.denominator
            return Fraction(nominator,denominator)
        elif isinstance(other, int):                        # mnożenie przez liczbę całkowitą
            return Fraction(self.nominator * other, self.denominator)
        else:
            return NotImplemented

    def __rmul__(self, other):                              # mnożenie z lewej strony (np. 3 * Fraction) - int nie wie, jak pomnożyć Fraction
        return self.__mul__(other)                          # ta metoda służy, żeby mnożenie działało niezależnie od kolejności argumentów

    def __imul__(self, other):                              # definicja operatora *=
        self.nominator = self.nominator * other.nominator
        self.denominator = self.denominator * other.denominator
        return self

    def __truediv__(self, other):                           # mnożenie przez odwrotność drugiego ułamka ze sprawdzeniem dzielenia przez 0
        if other.nominator == 0:
            raise ZeroDivisionError("Dzielenie przez 0")
        return self.__mul__(Fraction(other.denominator,other.nominator))

    def __add__(self, other):
        return self.__operation(other,lambda a,b: a+b)

    def __sub__(self, other):
        return self.__operation(other, lambda a,b: a-b)

    def __operation(self, other, operand):
        return self.__class__(operand(self.nominator * other.denominator, other.nominator * self.denominator),
                        self.denominator * other.denominator)               # oblicza wspólny mianownik
                                                                            # wykonuje przekazaną operację
                                                                            # tworzy nowy obiekt