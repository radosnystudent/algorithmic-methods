from fraction import Fraction
from copy import deepcopy


def generate(n : int):
    for i in range(1, n + 1):
        if n % i == 0:
            yield i
            yield -i


class Polynomial:

    def __init__(self, coeff : list):
        self.__coefficients = coeff

    def __repr__(self) -> str:
        result = str()
        for power,c in enumerate(self.getCoefficients()):
            if power == 0:
                result += f'{c}'
            else:
                if c < 0:
                    result += f' {c}x^{power}'
                else:
                    result += f' + {c}x^{power}'
        return result

    def __removeLastZero(self):
        self.__coefficients = self.__coefficients[0:]

    def __updateCoefficient(self, coeff : list):
        self.__coefficients = deepcopy(coeff)

    def getCoefficients(self) -> list:
        return self.__coefficients

    def __presumedRoots(self) -> list:
        an = abs(self.getCoefficients()[-1])
        a0 = abs(self.getCoefficients()[0])
        p,q = list(generate(a0)), list(generate(an))
        factors = list()
        for num in p:
            for denum in q:
                if Fraction(num,denum) not in factors:
                    factors.append(Fraction(num,denum))
        return factors

    def __findRoots(self) -> list:
        roots = list()
        if self.getCoefficients()[0] == 0:
            roots.append(Fraction(0,1))
            self.__removeLastZero()
        result = Fraction(0,1)
        coeff = deepcopy(self.getCoefficients())
        rootsToCheck = self.__presumedRoots()
        
        for root in rootsToCheck:
            for power,c in enumerate(coeff):
                result += Fraction(c, 1) * root**power
            if result == Fraction(0,1):
                roots.append(root)
            result = Fraction(0,1)

        return roots

    def __derivative(self) -> list:
        coeff = deepcopy(self.getCoefficients())
        return [coeff[i] * i for i in range(1,len(coeff))]

    def findMultipleRoots(self) -> list:
        result = dict()
        notDerivative = True
        if not self.__findRoots():
            return result

        while len(self.getCoefficients()) > 1:
            roots = self.__findRoots()
            for r in roots:
                if r in result :
                    result[r] += 1
                elif r not in result and notDerivative:
                    result[r] = 1
            self.__updateCoefficient(self.__derivative())
            notDerivative = False
        return result
