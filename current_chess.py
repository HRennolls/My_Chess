
#%%

import pygame as pyg

pyg.init()

window_size = (800, 800)
board_screen = pyg.display.set_mode(size=window_size)

pyg.display.set_caption('Chess')


"""
Making a dictionary of squares as keys and square indexes (0-63) as their values
"""
num_coords = [number for number in range(1, 9)]
let_coords = [chr(letter) for letter in range(ord('a'), ord('a') + 8)]

sq_names = [] #list of all square names

for j in num_coords[::-1]:
    for i in let_coords:
        sq_names.append(i+str(j))

square_size = window_size[0] // 8
images = {}

board_screen.fill((255, 255, 255))


class Square(object):
    def __init__(self, name):
        self.height = int(window_size[0] / 8)
        self.width = int(window_size[1] / 8)
        self.square = pyg.Surface((self.width, self.height))

        self.name = name
        self.index = sq_names.index(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)

    def colour(self):
        return 'w' if (((self.index // 8)%2) - (self.index % 2) == 0) else 'b'

    def coords(self):
        return (ord(self.name[0])-ord('a'), int(self.name[1]))



class ChessBoard(object):

    def __init__(self):
        pass

    board_array = []
    for i in range(8):
        row = sq_names[i*8 : i*8 + 8]
        row = [Square(x) for x in row]
        board_array.append(row)

            

    def draw(self):
        board = pyg.Surface(window_size)

        for i, rows in enumerate(self.board_array):
            for j, squares in enumerate(rows):
                if squares.colour() == 'w':
                    pyg.draw.rect(board, (255, 255, 255), (i*square_size, j*square_size, square_size, square_size))
                else:
                    pyg.draw.rect(board, (0, 0, 0), (i*square_size, j*square_size, square_size, square_size))

        return board

                
gameExit = False
new = ChessBoard()

while not gameExit:
    for event in pyg.event.get():
        board_screen.blit(new.draw(), (0, 0))
        pyg.display.flip()


        if event.type == pyg.QUIT:
            gameExit = True

            
