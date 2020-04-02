from random import choices
from math import inf
from copy import deepcopy

class Dummie:

    def __init__(self):
        self.grid = list()

    def __repr__(self):
        return 'Dummie!'

    def setGrid(self, grid : list):
        self.grid = [[grid[i][j] for j in range(len(grid[0]))] for i in range(len(grid))]

    def move(self):
        while True:
            x,y = choices([0,1,2], k=2)
            if self.grid[x][y] == ' ':
                return [x, y]

class MinMax:

    def __init__(self):
        self.grid = list()

    def __repr__(self):
        return 'MiniMax!'

    def setGrid(self, grid : list):
        self.grid = [[grid[i][j] for j in range(len(grid[0]))] for i in range(len(grid))] 

    def move(self) -> list:
        pos = self.MinMax(self.grid, sum(x == ' ' for row in self.grid for x in row), 'o')
        x, y, _ = pos
        return [x,y]

    def checkConditions(self, board : list, turn : str) -> bool:
        winning_conditions = [
            #horizontal
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            #vertical
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            #diagonal
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        
        return True if [turn, turn, turn] in winning_conditions else False


    def MinMax(self, board : list, depth : int, turn : str) -> list:
        
        def evaluateScore(board : list) -> int:
            if self.checkConditions(board, 'o'):
                return 1 
            elif self.checkConditions(board, 'x'):
                return -1
            else:
                return 0

        best = [inf, inf, -inf] if turn == 'o' else [inf, inf, inf]

        if depth == 0 or (self.checkConditions(board, 'x') or self.checkConditions(board, 'o')):
            return [-1, -1, evaluateScore(board)]

        for cell in [[x,y] for x,row in enumerate(board) for y,cell in enumerate(row) if cell == ' ']:
            x, y = cell
            board[x][y] = turn
            if turn == 'o':
                score = self.MinMax(board, depth - 1, 'x')
            else:
                score = self.MinMax(board, depth - 1, 'o')

            board[x][y] = ' '
            score = [x,y,score[2]]

            if turn == 'o':
                if score[2] > best[2]:
                    best = score[:]
            else:
                if score[2] < best[2]:
                    best = score[:]

        return best
