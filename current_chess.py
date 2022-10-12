
#%%

from array import array
import pygame as pyg

pyg.init()

window_size = (600, 600)

# draws main screen
board_screen = pyg.display.set_mode(size=window_size)
pyg.display.set_caption('Chess')
board_screen.fill((255, 255, 255))

"""
Making a dictionary of squares as keys and square indexes (0-63) as their values
"""

num_coords = [number for number in range(1, 9)]
let_coords = [chr(letter) for letter in range(ord('a'), ord('a') + 8)]

sq_names = [] # list of all square names

for j in num_coords:
    for i in let_coords:
        sq_names.append(i+str(j))

square_size = window_size[0] // 8

images = {} # loads images at init so fetching them is more efficient 

fen_to_name = {n: 'w' + n if n.islower() else 'b' + n.lower() for n in "rnbqkpPRNBQK" }

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

print(sq_names)

class Piece(object):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

class Pawn(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class King(Piece):
    pass

class Queen(Piece):
    pass

class GeneratePiece():

    #TODO
    """subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._piece_type] = cls"""


    @classmethod
    def create(cls, name):
        #return cls.subclasses[name]
        piece = None
        if name == 'P':
            piece = Pawn('bp')
        elif name == 'p':
            piece = Pawn('wp')
        elif name == ('N'):
            piece = Knight('bn')
        elif name == ('n'):
            piece = Knight('wn')
        elif name == ('B'):
            piece = Bishop('bb')
        elif name == ('b'):
            piece = Bishop('wb')
        elif name == ('R'):
            piece = Rook('br')
        elif name == ('r'):
            piece = Rook('wr')
        elif name == ('Q'):
            piece = Queen('bq')
        elif name == ('q'):
            piece = Queen('wq') 
        elif name == ('K'):
            piece = King('bk') 
        elif name == ('k'):
            piece = King('wk')

        return piece           
        
        

class Square(object):
    def __init__(self, name, piece = None):
        self.height = int(window_size[0] / 8)
        self.width = int(window_size[1] / 8)
        self.square = pyg.Surface((self.width, self.height))
        self.name = name
        self.index = sq_names.index(name)
        self.piece = piece

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)

    def colour(self):
        return 'w' if (((self.index // 8)%2) - (self.index % 2) == 0) else 'b'

    def coords(self):
        return (ord(self.name[0])-ord('a'), int(self.name[1]))

    def draw(self):
        
        if self.colour() == 'w':
            self.square.fill((255, 255, 255))

        else:
            self.square.fill((150, 160, 160))

        if self.piece is not None:
            self.square.blit(images[self.piece.name], pyg.Rect(0, 0, square_size, square_size))

        return self.square


class ChessBoard(object):

    def __init__(self):
        pass

    board_array = []
    for i in range(8):
        row = sq_names[i*8 : i*8 + 8]
        row = [Square(x) for x in row]
        board_array.append(row)

    def draw(self):

        for i, rows in enumerate(self.board_array):
            for j, squares in enumerate(rows):
    
                board_screen.blit(squares.draw(), (i*square_size, j*square_size)) #TODO

    def fen_to_board(self, fen) -> array:

        i = 0
        j = 0
        for row in fen.split('/'):
            for c in row:
                temp_sq = self.board_array[j%8][7-i]
                
                if c == ' ':
                    
                    break
                elif c in '12345678':
                    
                    j += int(c)-1

                else:
                    temp_sq.piece = GeneratePiece.create(c)
                j += 1
            i += 1

            



def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb','wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (square_size, square_size))



def main():

    gameExit = False
    load_images()
    game_board = ChessBoard()
    game_board.fen_to_board(starting_fen)

    while not gameExit:
        for event in pyg.event.get():

            
            game_board.draw()
            pyg.display.flip()


            if event.type == pyg.QUIT:
                gameExit = True


if __name__ == "__main__":
    main()

               
