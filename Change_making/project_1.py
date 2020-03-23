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

        if to_return == 0:
            return result
        return None

    def _recursion(self, to_return : int, index : int, count : int, array : list, min_count : any) -> dict:
        if to_return == 0:
            if min_count is None or min_count > count:
                min_count = count
                return dict(), min_count

        if index >= len(array):
            return None, min_count
            
        best_change = None
        coin = array[index]
        
        taking = min(to_return // coin, self.__cash[coin])

        for c in range(taking, -1, -1):
            change, min_count = self._recursion(to_return - coin * c, index + 1, count + c, array, min_count)
            if change is not None:
                if c:
                    change.update({coin : c})
                best_change = change
        return best_change, min_count

    def _not_greedy(self, to_return : int) -> dict:
        array = list()
        for key in self.__cash.keys():
            array.append(key)
        #result, _  = self.recursion(to_return, 0, 0, array, None)
        return self._recursion(to_return, 0, 0, array, None)[0]

    def calculate(self, to_pay : float, given_money: float):
        to_return = int((given_money - to_pay) * 100)
        if self._check_cash():
            result = self._greedy_algorithm(to_return)
        else:
            result = self._not_greedy(to_return)

        if result is not None:
            self._update(result)
            final_value = float(0)
            for index, value in result.items():
                print(f'{round(float(index/100), 3)}zł - {value}')
                final_value += float(index/100) * value
            print(f'Wydana reszta - {round(final_value,3)}zł:')
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
