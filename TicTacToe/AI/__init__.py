from random import choice
# from copy import deepcopy
from math import inf

class Dummie:

    def __init__(self):
        self.grid = None

    def setGrid(self, grid : dict):
        self.grid = grid.copy()

    def move(self):
        choices = list()
        for key, item in self.grid.items():
            if item == ' ':
                choices.append(key)
        return choice(choices)

class MinMax:

    def __init__(self):
        self.grid = None

    def setGrid(self, grid : dict):
        self.grid = grid.copy()

    def checkStates(self, board : dict):
        draw = True
        vert_horiz = [
            ['a1', 'a2', 'a3'], ['b1', 'b2', 'b3'], ['c1', 'c2', 'c3'],
            ['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'], ['a3', 'b3', 'c3'],
        ]
        diagonal = [['a1', 'b2', 'c3'], ['a3', 'b2', 'c1']]

        for value in board.values():
            if value == ' ':
                draw = False
        if draw:
            return None, 'Draw'

        for cond in vert_horiz:
            if board[cond[0]] == board[cond[1]] and board[cond[1]] == board[cond[2]] and board[cond[0]] is not ' ':
                return board[cond[0]], 'Done'
        for cond in diagonal:
            if board[cond[0]] == board[cond[1]] and board[cond[1]] == board[cond[2]] and board[cond[0]] is not ' ':
                return board[cond[1]], 'Done'
        return None, 'Not Done'

    def move(self):
        print(self.grid)
        num = self.__move()
        #print(f'{str(int((num-1)/3))} - {str(int(((num-1) % 3) + 1))}')
        col = str(int((num-1)/3))
        row = str(int(((num-1) % 3) + 1))
        col = col.replace('0', 'a').replace('1', 'b').replace('2', 'c')
        #print(col+row)
        return col+row

    def __move(self, board = None, turn = 'o'):
        if board is None:
            board = self.grid

        win_lose, isdone = self.checkStates(board)

        if isdone == 'Done' and win_lose == 'o':
            return 1
        elif isdone == 'Done' and win_lose == 'x':
            return -1
        elif isdone == 'Draw':
            return 0
        
        moves, empty_fields, empty_cells = list(), list(), list()

        for key, value in board.items():
            if value == ' ':
                #print(key)
                v = key
                v = v.replace('1', '0').replace('2', '1').replace('3', '2')
                v = v.replace('a', '0').replace('b', '1').replace('c', '2')
                empty_fields.append(int(v[0])*int(v[1]))
                empty_cells.append(key)

        for field, cell in zip(empty_fields, empty_cells):
            actual_move = {}

            actual_move['index'] = field
            new_board = board.copy()
            new_board[cell] = turn

            if turn == 'o':
                result = self.__move(new_board, 'x')
                actual_move['score'] = result
            else:
                result = self.__move(new_board, 'o')
                actual_move['score'] = result

            moves.append(actual_move)

        best_move = None
        if turn == 'o':
            best = -inf
            for m in moves:
                if m['score'] > best:
                    best = m['score']
                    best_move = m['index']
        else:
            best = inf
            for m in moves:
                if m['score'] < best:
                    best = m['score']
                    best_move = m['index']
        return best_move