import pygame as pg
from pygame.locals import *
from random import choice
from AI import Dummie

show = f'a1 | b1 | c1\n'\
'------------\n'\
'a2 | b2 | c2\n'\
'------------\n'\
'a3 | b3 | c3\n'

class Engine:
    def __init__(self, AI_list : list):
        self.__grid = {'a1' : ' ', 'b1' : ' ','c1' : ' ',
        'a2' : ' ','b2' : ' ', 'c2' : ' ',
        'a3' : ' ','b3' : ' ','c3' : ' ' }
        self.__actual_turn = 'p' #choice(['c', 'p'])
        self.AI_list = AI_list
        self.AI = AI_list[1] #choice(AI_list)
        self.__winner = False

    def changeAI(self):
        print(type(self.AI))
        print(self.AI_list)
        index = self.AI_list.index(self.AI)
        if index == len(self.AI_list) - 1:
            index = 0
        else:
            index += 1
        self.AI = self.AI_list[index]

    def getTurn(self) -> str:
        return self.__actual_turn

    def changeTurn(self, turn : str):
        self.__actual_turn = turn

    def getGrid(self) -> dict:
        return self.__grid

    def __str__(self) -> str:
        return self.printGrid()

    def ifWinner(self) -> bool:
        return self.__winner

    def checkField(self,field):
        return self.getGrid()[field] == ' '

    def printGrid(self) -> str:
        string = ''
        for key,value in self.getGrid().items():
            if 'c' not in key:
                string += f'{value} | '
            elif 'c' in key:
                string += f'{value}\n'
            if 'c' in key and key != 'c3':
                string += f'---------\n'
        return string

    def updateGrid(self, move : str, which : str) -> str:
        if which == 'c':
            self.getGrid()[move] = 'o'
            self.changeTurn('p')
        elif which == 'p':
            self.getGrid()[move] = 'x'
            self.changeTurn('c')
        return self.checkCondition()

    def checkCondition(self) -> str:
        winning_conditions = [
            ['a1', 'a2', 'a3'],['b1', 'b2', 'b3'],['c1', 'c2', 'c3'],
            ['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'],['a3', 'b3', 'c3'],
            ['a1', 'b2', 'c3'], ['a3', 'b2', 'c1']
        ]

        player, computer = list(), list()
        for key, value in self.getGrid().items():
            if value == 'x':
                player.append(key)
            elif value == 'o':
                computer.append(key)
        if len(player) + len(computer) == len(self.getGrid()):
            return 'Remis'
        for cond in winning_conditions:
            if all(value in player for value in cond):
                self.__winner = True
                return 'Player win'
            if all(value in computer for value in cond):
                self.__winner = True
                return 'Computer win'
        return ''

    def computerMove(self, move):
        print(f'here: {move}')
        self.updateGrid(move, 'c')


class TextUI():

    def __init__(self, Engine : 'Engine'):
        self.engine = Engine

    def __str__(self) -> str:
        return self.engine.printGrid()

    def playerMove(self) ->str:
        print(self.engine.printGrid())
        move = ''
        while move not in [key for key in self.engine.getGrid().keys()]:
            move = input(f'{show}Podaj numer pola:\n> ')
            if self.engine.getGrid()[move] != ' ':
                print('Pole jest zajete!')
                move = ''
        return self.engine.updateGrid(move, 'p')
        
    def game(self):
        choice = ''
        while not self.engine.ifWinner():
            while choice not in ['z', 'k', 'g'] and not self.engine.ifWinner():
                choice = input('z - zmiana interface\nk - zmiana AI\ng - dalsza gra bez zmian\n> ')

                if choice == 'g':
                    msg = self.playerMove()
                    if msg: 
                        print(msg)
                        break
                    self.engine.AI.setGrid(self.engine.getGrid())
                    msg = self.engine.computerMove(self.engine.AI.move())
                    if msg: print(msg)
                    else: print(self.engine.printGrid())
                elif choice == 'k':
                    self.engine.changeAI()
                    print(type(self.engine.AI))
                elif choice == 'z':
                    pass
                choice = ''
        return 'koniec'


class GraphicalUI:

    def __init__(self, Engine):
        self.engine = Engine
        
    def prepare(self):
        pg.init()
        self.CLOCK = pg.time.Clock()
        self.width = 400
        self.height = 400
        line_color = (10,10,10)
        white = (255, 255, 255)
        self.screen = pg.display.set_mode((self.width, self.height + 100),0,32)
        pg.display.set_caption('Tic Tac Toe!')
        self.x_img = pg.image.load('interface\\images\\x.png')
        self.o_img = pg.image.load('interface\\images\\o.png')
        self.x_img = pg.transform.scale(self.x_img, (80, 80))
        self.o_img = pg.transform.scale(self.o_img, (80, 80))
        self.screen.fill(white)

        pg.draw.line(self.screen,line_color,(self.width/3,0),(self.width/3, self.height),7)
        pg.draw.line(self.screen,line_color,(self.width/3*2,0),(self.width/3*2, self.height),7)

        pg.draw.line(self.screen,line_color,(0,self.height/3),(self.width, self.height/3),7)
        pg.draw.line(self.screen,line_color,(0,self.height/3*2),(self.width, self.height/3*2),7)

        for key, item in self.engine.getGrid().items():
            if item == 'x':
                self.drawMove(key, 'p')
            if item == 'o':
                self.drawMove(key, 'c')

    def game(self):
        self.prepare()
        while True:
            if self.engine.getTurn() == 'p':
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                    elif event.type is MOUSEBUTTONDOWN:
                        self.userClick()
            elif self.engine.getTurn() == 'c':
                self.engine.AI.setGrid(self.engine.getGrid())
                move = self.engine.AI.move()
                self.drawMove(move,'c')
                self.engine.computerMove(move)
            pg.display.update()
            self.CLOCK.tick()

    def drawMove(self, move, which):
        if '1' in move:
            posx = 30
        elif '2' in move:
            posx = self.width / 3 + 30
        else:
            posx = self.width / 3*2 + 30

        if 'a' in move:
            posy = 30
        elif 'b' in move:
            posy = self.height / 3 + 30
        else:
            posy = self.height / 3*2 + 30

        if which == 'c':
            self.screen.blit(self.o_img, (posy, posx))
        elif which == 'p':
            self.screen.blit(self.x_img, (posy, posx))
            self.engine.updateGrid(move, which)
        pg.display.update()

    def userClick(self):
        x,y = pg.mouse.get_pos()

        if x < self.width / 3:
            pos = 'a'
        elif x < self.width / 3*2:
            pos = 'b'
        elif x < self.width:
            pos = 'c'
        else:
            pos = None
        if pos:
            if y < self.height / 3:
                pos += '1'
            elif y < self.height / 3*2:
                pos += '2'
            elif y < self.height:
                pos += '3'
            else:
                pos = None
        else:
            pos = None

        if self.engine.checkField(pos):
            self.drawMove(pos, 'p')


