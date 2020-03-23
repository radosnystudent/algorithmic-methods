from fraction import Fraction
import re

def generate(n):
    for i in range(1, n + 1):
        if n % i == 0:
            yield i
            yield -i

class Polynomial:

    def __init__(self, coeff : list):
        self.__coefficients = coeff

    def __repr__(self) -> str:
        result = str()
        power = len(self.getCoefficients()) - 1
        for c in self.getCoefficients():
            if power != 0:
                result += f'{c}x^{power} + '
            else:
                result += f'{c}\n'
            power -= 1
        return result


    def getCoefficients(self) -> list:
        return self.__coefficients


    def __presumedRoots(self) -> list:
        an = abs(self.getCoefficients()[0])
        a0 = abs(self.getCoefficients()[-1])
        p,q = list(generate(a0)), list(generate(an))

        factors = list()
        for num in p:
            for denum in q:
                if Fraction(num,denum) not in factors:
                    factors.append(Fraction(num,denum))
        return factors

    def findRoots(self):
        rootsToCheck = self.__presumedRoots()
        roots = list()
        result = Fraction(0,1)
        coeff = self.getCoefficients()
        coeff.reverse()

        #print(coeff)
        for root in rootsToCheck:
            for power,c in enumerate(coeff):
                #print(f'root: {root}, c: {c}, power: {power}')
                result += Fraction(c, 1) * root**power
                #print(f'{result} += {Fraction(c, 1)} * {root**power}')
            #print(f'{root} -> {result}')
            if result == Fraction(0,1):
                roots.append(root)
            result = Fraction(0,1)

        return roots
