from fraction import Fraction
from mixed_fraction import MixedFraction

def main():
    f = Fraction(4, 0)
    # f.nominator = 7
    # f.denominator = 7
    # f.reduce()
    nf = Fraction(45, 81)
    # nf.nominator = 45
    # nf.denominator = 81
    # nf.reduce()
    print(f"{f.nominator}/{f.denominator} czy integer: ", f.is_integer())
    print(f"{nf.nominator}/{nf.denominator} czy integer: ", nf.is_integer())
    # print(f"{f.to_string()}")
    print(f"{f}")
    print(float(f), float(nf))
    print(f * nf)
    for _ in range(3):
        f *= nf
    print(f)
    print(5*f)
    try:
        ff = Fraction(4, 0)
        print(Fraction(1, 2) / ff)
    except (ZeroDivisionError, ValueError) as e:
        print(e)
    # except ZeroDivisionError as e:
    #     print(str(e))
    # except ValueError as e:
    #     print(e)
    print(MixedFraction(1,2) + MixedFraction(3,4))
    print(Fraction(1,2) - Fraction(3,4))
    print(MixedFraction(4,3))

if __name__ == '__main__':
    main()