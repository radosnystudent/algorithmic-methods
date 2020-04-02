import pygame as pg
from pygame.locals import *
from random import choice
from AI import Dummie

show = f'1 | 2 | 3\n'\
'------------\n'\
'4 | 5 | 6\n'\
'------------\n'\
'7 | 8 | 9\n'

class Engine:
    def __init__(self, AI_list : list):
        """self.__grid = {'a1' : ' ', 'b1' : ' ','c1' : ' ',
        'a2' : ' ','b2' : ' ', 'c2' : ' ',
        'a3' : ' ','b3' : ' ','c3' : ' ' } """

        #self.__grid = {'a1' : ' ', 'b1' : 'x','c1' : 'o',
        #'a2' : 'o','b2' : ' ', 'c2' : 'o',
        #'a3' : ' ','b3' : ' ','c3' : 'x' }

        self.__grid = [
                    [' ',' ',' '],
                    [' ',' ',' '],
                    [' ',' ',' ']
        ]
        self.__actual_turn = 'p' #choice(['c', 'p'])
        self.AI_list = AI_list
        self.AI = AI_list[1] #choice(AI_list)
        self.__winner = False

    def changeAI(self):
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

    def getGrid(self) -> list:
        return self.__grid

    def __str__(self) -> str:
        return self.printGrid()

    def setWinner(self):
        self.__winner = True

    def ifWinner(self) -> bool:
        return self.__winner

    def printGrid(self) -> str:
        string = ''
        string += f' {self.getGrid()[0][0]} | {self.getGrid()[0][1]} | {self.getGrid()[0][2]}\n'
        string += '------------\n'
        string += f' {self.getGrid()[1][0]} | {self.getGrid()[1][1]} | {self.getGrid()[1][2]}\n'
        string += '------------\n'
        string += f' {self.getGrid()[2][0]} | {self.getGrid()[2][1]} | {self.getGrid()[2][2]}\n'
        return string

    def checkField(self, x : int, y : int) -> bool:
        return True if self.getGrid()[x][y] == ' ' else False

    def updateGrid(self, x : int, y : int, which : str) -> str:
        if which == 'c':
            self.getGrid()[x][y] = 'o'
            self.changeTurn('p')
        elif which == 'p':
            self.getGrid()[x][y] = 'x'
            self.changeTurn('c')

        return self.checkCondition()

    def checkCondition(self) -> str:
        draw = True
        for row in self.getGrid():
            for value in row:
                if value is ' ':
                    draw = False
        if draw:
            return "Remis"
        
        if self.getGrid()[0][0] == self.getGrid()[0][1] and self.getGrid()[0][1] == self.getGrid()[0][2] and self.getGrid()[0][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[0][0] is 'x' else 'Wygral komputer'
        if self.getGrid()[1][0] == self.getGrid()[1][1] and self.getGrid()[1][1] == self.getGrid()[1][2] and self.getGrid()[1][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[1][0] is 'x' else 'Wygral komputer'
        if self.getGrid()[2][0] == self.getGrid()[2][1] and self.getGrid()[2][1] == self.getGrid()[2][2] and self.getGrid()[2][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[2][0] is 'x' else 'Wygral komputer'
        
        if self.getGrid()[0][0] == self.getGrid()[1][0] and self.getGrid()[1][0] == self.getGrid()[2][0] and self.getGrid()[0][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[0][0] is 'x' else 'Wygral komputer'
        if self.getGrid()[0][1] == self.getGrid()[1][1] and self.getGrid()[1][1] == self.getGrid()[2][1] and self.getGrid()[0][1] is not ' ':
            return 'Wygral gracz' if self.getGrid()[0][1] is 'x' else 'Wygral komputer'
        if self.getGrid()[0][2] == self.getGrid()[1][2] and self.getGrid()[1][2] == self.getGrid()[2][2] and self.getGrid()[0][2] is not ' ':
            return 'Wygral gracz' if self.getGrid()[0][2] is 'x' else 'Wygral komputer'
        
        if self.getGrid()[0][0] == self.getGrid()[1][1] and self.getGrid()[1][1] == self.getGrid()[2][2] and self.getGrid()[0][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[1][1] is 'x' else 'Wygral komputer'
        if self.getGrid()[2][0] == self.getGrid()[1][1] and self.getGrid()[1][1] == self.getGrid()[0][2] and self.getGrid()[2][0] is not ' ':
            return 'Wygral gracz' if self.getGrid()[1][1] is 'x' else 'Wygral komputer'
        return ''

    def computerMove(self, move : list):
        x,y = move
        self.updateGrid(x, y, 'c')


class TextUI():

    def __init__(self, Engine : 'Engine'):
        self.engine = Engine

    def __str__(self) -> str:
        return self.engine.printGrid()

    def playerMove(self) ->str:
        print(self.engine.printGrid())
        move = int(0)
        grids = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
        fields = [1,2,3,4,5,6,7,8,9]
        while move not in fields:
            move = int(input(f'{show}Podaj numer pola (od 1-9):\n> '))
            x,y = grids[fields.index(move)]
            if self.engine.getGrid()[x][y] != ' ':
                print('Pole jest zajete!')
                move = int(0)
        return self.engine.updateGrid(x,y, 'p')
        
    def game(self):
        choice = ''
        while not self.engine.ifWinner():
            while choice not in ['i', 'a', 'g'] and not self.engine.ifWinner():
                choice = input('z - zmiana interface\'u\na - zmiana AI\ng - dalsza gra bez zmian\n> ')

                if choice == 'g':
                    msg = self.playerMove()
                    if msg: 
                        print(msg)
                        self.engine.setWinner()
                        break
                    self.engine.AI.setGrid(self.engine.getGrid())
                    msg = self.engine.computerMove(self.engine.AI.move())
                    if msg: 
                        print(msg)
                        self.engine.setWinner()
                        break
                    else: print(self.engine.printGrid())
                elif choice == 'a':
                    self.engine.changeAI()
                elif choice == 'i':
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
        self.screen = pg.display.set_mode((self.width, self.height + 200),0,32)
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

        for x,row in enumerate(self.engine.getGrid()):
            for y, cell in enumerate(row):
                if cell == 'x':
                    self.drawMove(x,y, 'p')
                if cell == 'o':
                    self.drawMove(x,y, 'c')

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
                self.drawMove(move[0], move[1],'c')
                self.engine.computerMove(move)
            pg.display.update()
            self.CLOCK.tick()

    def drawMove(self, x,y, which):
        if x == 0:
            posx = 30
        elif x == 1:
            posx = self.width / 3 + 30
        else:
            posx = self.width / 3*2 + 30

        if y == 0:
            posy = 30
        elif y == 1:
            posy = self.height / 3 + 30
        else:
            posy = self.height / 3*2 + 30

        if which == 'c':
            self.screen.blit(self.o_img, (posy, posx))
        elif which == 'p':
            self.screen.blit(self.x_img, (posy, posx))
            self.engine.updateGrid(x, y, which)
        pg.display.update()

    def userClick(self):
        y,x = pg.mouse.get_pos()
        if x < self.width / 3:
            posx = 0
        elif x < self.width / 3*2:
            posx = 1
        elif x < self.width:
            posx = 2
        else:
            posx = None
        if y < self.height / 3:
            posy = 0
        elif y < self.height / 3*2:
            posy = 1
        elif y < self.height:
            posy = 2
        else:
            posy = None

        if self.engine.checkField(posx, posy):
            self.drawMove(posx, posy, 'p')
