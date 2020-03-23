from polynomial import Polynomial

def unpack(d : dict) -> str:
    result = ''
    for key,value in d.items():
        result += f'{key} jest pierwiastkiem {value}-krotnym\n'
    return result

if __name__ == "__main__":
    data = input('Podaj kolejne, wymierne wspolczynniki wielomianu zaczynajac od najwyzszej potegi i oddzielając je spacją:\n> ')
    l = list(map(int, data.split()))
    l.reverse()
    p = Polynomial(l)
    print(f'Wielomian w(x): {p}')
    print(f'Pierwiastki wielomianu w(x): {unpack(p.findMultipleRoots())}')
