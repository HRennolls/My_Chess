
#%%

from array import array
import pygame as pyg

pyg.init()

window_size = (800, 800)

board_screen = pyg.display.set_mode(size=window_size)
pyg.display.set_caption('Chess')
board_screen.fill((255, 255, 255))

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

fen_to_name = {n: 'w' + n if n.islower() else 'b' + n.lower() for n in "rnbqkpPRNBQK" }

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

print(fen_to_name)



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
    """subclasses = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._piece_type] = cls"""


    @classmethod
    def create(cls, name):
        #return cls.subclasses[name]
        piece = None
        if name == 'p':
            piece = Pawn('bp')
        elif name == 'P':
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
        sq_draw = pyg.Surface((square_size, square_size))
        if self.colour() == 'w':
            
            sq_draw.fill((255, 255, 255))
        else:
            
            sq_draw.fill((150, 160, 160))

        if self.piece is not None:
            sq_draw.blit(images[self.piece], pyg.Rect(0, 0, square_size, square_size))

        return sq_draw


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
        for i, row in enumerate(fen.split('/')):
            
            for j, c in enumerate(row):
                temp_sq = self.board_array[i][j]

                if c == ' ':
                    break
                elif c in '12345678':
                    
                    #brow.extend( ['--'] * int(c) )
                    pass

                else:
                    temp_sq.piece = GeneratePiece.create(c)

            



def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb','wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (square_size, square_size))




def draw_pieces(screen, board):
    for r in range(window_size[0]):
        for c in range(window_size[0]):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pyg.Rect(c*square_size, r*square_size, square_size, square_size))

def main():

    gameExit = False
    load_images()

    game_board = ChessBoard()


    while not gameExit:
        for event in pyg.event.get():
            game_board.draw()
            pyg.display.flip()


            if event.type == pyg.QUIT:
                gameExit = True


if __name__ == "__main__":
    main()

               
