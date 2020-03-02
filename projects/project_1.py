"""
input:
product price
given cash
output:
give the change
"""

class CashRegister:

    def __init__(self):
        self.__cash = dict()

    def __str__(self) -> str:
        string = ''
        for index, value in self.__cash.items():
            string += f'{round(float(index/100), 2)}zł : {value}\n'
        return string

    def prepare(self):
        with open('data1.txt', 'r') as file:
            for line in file:
                index,value = list(map(int,line.split()))
                self.__cash[index] = value

    def _check_cash(self) -> bool:
        for index, value in self.__cash.items():
            if index <= 5000 and value < 5:
                return False
            if index > 5000 and value == 0:
                return False
        return True

    def _update(self, result : dict):
        for ind, val in result.items():
            self.__cash[ind] -= val

    def _greedy_algorithm(self, to_return : int) -> dict:
        result = dict()
        for index, value in self.__cash.items():
            if index <= to_return:
                result[index] = 0
                for _ in range(value):
                    if to_return - index >= 0:
                        to_return -= index
                        result[index] += 1

        return result

    def _dynamic_programming(self, to_return : int) -> dict:
        min_count = None
        array = list()

        for key in self.__cash.keys():
            array.append(key)

        def recursion(to_return : int, index : int, count : int) -> dict:
            nonlocal min_count
            nonlocal array

            if to_return == 0:
                if min_count is None or count < min_count:
                    min_count = count
                    return dict()

            if index >= len(array):
                return None
                
            best_change = None
            coin = array[index]
            
            taking = min(to_return // coin, self.__cash[coin])

            for c in range(taking, -1, -1):
                change = recursion(to_return - coin * c, index + 1, count + c)
                if change is not None:
                    if c:
                        change._update({coin : c})
                    best_change = change
            return best_change
        return recursion(to_return, 0, 0)


    def calculate(self, to_pay : float, given_money: float):
        to_return = int((given_money - to_pay) * 100)
        if self._check_cash():
            result = self._greedy_algorithm(to_return)
        else:
            result = self._dynamic_programming(to_return)

        final_value = float(0)
        for ind, val in result.items():
            final_value += float(ind/100) * val

        self._update(result)

        if float(to_return/100) == round(final_value,3):
            print(f'Wydana reszta - {round(final_value,3)}zł:')
            for index, value in result.items():
                print(f'{round(float(index/100), 2)}zł - {value}')
        else:
            print('Nie można wydać reszty.')
        print('\n\n')


def menu():
    C = CashRegister()
    C.prepare()
    while True:
        choice = -1
        while (choice > 2 or choice < 0):
            choice = int(input('1. Nastepny towar\n2. Stan kasy\n0. Zamknij program\n> '))
        if choice == 1:
            to_pay = float(input('Podaj cene\n> '))
            given_money = float(input('Ile placisz\n> '))
            if given_money >= to_pay:
                C.calculate(to_pay, given_money)
            else:
                print('Błędne dane\n')
        elif choice == 2:
            print(C)
        elif choice == 0:
            break   


if __name__ == '__main__':
    menu()
