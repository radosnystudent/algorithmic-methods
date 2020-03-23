
class Fraction:

    def __reduce(self, nom : int, denom : int, sign : int) -> tuple:
        n = abs(nom)
        d = abs(denom)
        while n % d != 0:
            n, d = d, n % d
        return (abs(nom)//d*sign, abs(denom)//d)

    def __init__(self, numerator : int, denominator : int):
        if not isinstance(numerator,int) or not isinstance(denominator,int):
            raise TypeError('licznik i mianownik musza byc liczbami calkowitymi')
        if denominator == 0:
            raise ZeroDivisionError('mianownik nie może być zerem')
        if numerator == 0:
            self.__numerator = 0
            self.__denominator = 1
            pass
        else:
            if (numerator < 0 and denominator >=0) or (numerator >= 0 and denominator < 0):
                sign = -1
            else:
                sign = 1
            (self.__numerator, self.__denominator) = self.__reduce(numerator, denominator, sign)

    def __hash__(self):
        return hash((self.__numerator, self.__denominator))

    def __repr__(self) -> str:
        return f'{self.__numerator}/{self.__denominator}'

    def getNumerator(self) -> bool:
        return self.__numerator

    def getDenominator(self) -> bool:
        return self.__denominator

    def __eq__(self, rhs : 'Fraction') -> bool:
        return self.getNumerator() == rhs.getNumerator() and self.getDenominator() == rhs.getDenominator()

    def __ne__(self, rhs : 'Fraction') -> bool:
        return not self == rhs

    def __lt__(self, rhs : 'Fraction') -> bool:
        return self.getNumerator() * rhs.getDenominator() < self.getDenominator() * rhs.getNumerator()

    def __le__(self, rhs : 'Fraction') -> bool:
        return not rhs < self

    def __gt__(self, rhs : 'Fraction') -> bool:
        return rhs < self

    def __ge__(self, rhs : 'Fraction') -> bool:
        return not rhs > self

    def __add__(self, rhs : 'Fraction') -> 'Fraction':
        num = self.getNumerator() * rhs.getDenominator() + rhs.getNumerator() * self.getDenominator()
        denom = self.getDenominator() * rhs.getDenominator()
        return Fraction(num, denom)

    def __sub__(self, rhs : 'Fraction') -> 'Fraction':
        num = self.getNumerator() * rhs.getDenominator() - rhs.getNumerator() * self.getDenominator()
        denom = self.getDenominator() * rhs.getDenominator()
        return Fraction(num, denom)

    def __mul__(self, rhs : 'Fraction') -> 'Fraction':
        num = self.getNumerator() * rhs.getNumerator()
        denom = self.getDenominator() * rhs.getDenominator()
        return Fraction(num, denom)

    def __truediv__(self, rhs : 'Fraction') -> 'Fraction':
        num = self.getNumerator() * rhs.getDenominator()
        denom = self.getDenominator() * rhs.getNumerator()
        return Fraction(num, denom)

    def __pow__(self, a : int) -> 'Fraction':
        if a == 0:
            return Fraction(1, 1)
        result = self
        for _ in range(a-1):
            result *= self
        return result
