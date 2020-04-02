from interface import Engine, TextUI, GraphicalUI
from AI import Dummie, MinMax
import random

class Game:

    def __init__(self):
        self.E = Engine([Dummie(), MinMax()])
        self.T_UI = TextUI(self.E)
        self.G_UI = GraphicalUI(self.E)
        self.UI = [self.T_UI, self.G_UI]

    def run(self):
        actual_UI = random.choice(self.UI)
        max_ind = len(self.UI)
        while True:
            msg = actual_UI.game()
            if msg == 'zmiana':
                ind = self.UI.index(actual_UI)
                if ind == max_ind - 1:
                    ind = 0
                else:
                    ind += 1
                actual_UI = self.UI[ind]
            elif msg == 'koniec':
                break

g = Game()
g.run()
