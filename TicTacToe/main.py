from interface import Engine, TextUI, GraphicalUI
from AI import Dummie, MinMax
import random

class Game:

    def __init__(self):
        self.E = Engine([Dummie(), MinMax()])
        self.T_UI = TextUI(self.E)
        self.G_UI = GraphicalUI(self.E)

    def run(self):
        while True:
            #msg = self.T_UI.game()
            self.G_UI.game()
            #self.
            if msg == 'koniec':
                break
g = Game()
g.run()
