import pygame as pyg

pyg.init()
window_size = (400, 400)
board_screen = pyg.display.set_mode(size=window_size)# Draws main screen.
pyg.display.set_caption('Chess')
board_screen.fill((255, 255, 255))

# Making a dictionary of squares as keys
# and square indexes (0-63) as their values.

num_coords = [number for number in range(1, 9)]
let_coords = [chr(letter) for letter in range(ord('a'), ord('a') + 8)]
sq_names = [] # list of all square names
for j in num_coords:
    for i in let_coords:
        sq_names.append(i+str(j))
square_size = window_size[0] // 8

# Part of fen conversion, converts to image name format.
# Used in ChessBoard method, fen_to_board().
fen_to_name = {n: 'w' + n if n.islower() 
                else 'b' + n.lower() for n in "rnbqkpPRNBQK" }
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def on_board(legal_coords):
    # Returns the sublist of the input that
    # is actually on the board.
    legal = [co for co in legal_coords if 
            all(0 <= elem <= 7 for elem in co)]
    return legal

def diagonals(move_list, x, y, n, board, col):

    vs = [
        (1, 1),
        (1, -1), 
        (-1, 1), 
        (-1, -1)
    ]
    for i in vs:
        try:
            obstruction_restriction(move_list, x, y, i[0], i[1], n, board, col)
        except IndexError: continue


def rank_file(move_list, x, y, n, board, col):

    vs = [
        (1, 0), 
        (0, 1), 
        (-1, 0), 
        (0, -1)
    ]

    for i in vs:
        try:
            obstruction_restriction(move_list, x, y, i[0], i[1], n, board, col)
        except IndexError: continue
        

def obstruction_restriction(move_list, x, y, xp, yp, n, board, col):
    for i in range(1, n):
        if board.board_array[y + i*yp][x + i*xp].piece is None:
            move_list.append((x + i*xp, y + i*yp))
        elif board.board_array[y + i*yp][x + i*xp].piece.colour == col:
            break
        elif board.board_array[y + i*yp][x + i*xp].piece.colour != col:
            move_list.append((x + i*xp, y + i*yp))
            break



class Piece(object):
    def __init__(self, name):
        self.name = name
        self.colour = name[0]

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

    def image(self):
        return images[self.name]


class Pawn(Piece):
    moved = False

    def legal_moves(self, square, board = None):
        x, y = square.coords()
        legal_coords = []

        def capturable_squares(x, y, board, col):
            if board is not None:
                    try:
                        if board.board_array[y][x].piece.colour == col:
                            legal_coords.append((x, y))
                    except (AttributeError, IndexError) as e:
                        pass

        if self.colour == 'w':
            legal_coords.append((x, y+1))
            if not self.moved:
                legal_coords.append((x, y+2))
            capturable_squares(x+1, y+1, board, 'b')
            capturable_squares(x-1, y+1, board, 'b')
            
        else:
            legal_coords.append((x, y-1))
            if not self.moved:
                legal_coords.append((x, y-2))
            capturable_squares(x+1, y-1, board, 'w')
            capturable_squares(x-1, y-1, board, 'w')            
        
        return on_board(legal_coords)
    

class Knight(Piece):
    def legal_moves(self, square, board = None):
        x,y = square.coords()
        legal_coords = [
            (x+2, y+1),
            (x+2, y-1),
            (x-2, y+1),
            (x-2, y-1),
            (x+1, y-2),
            (x-1, y-2),
            (x+1, y+2),
            (x-1, y+2)
        ]
        legal_coords = on_board(legal_coords)
        tlist = []
        for i in legal_coords:
            if board.board_array[i[1]][i[0]].piece is not None:
                if board.board_array[i[1]][i[0]].piece.colour == self.colour:
                    pass
                else:
                    tlist.append(i)
            else:
                tlist.append(i)
        return tlist


class Bishop(Piece):
    def legal_moves(self, square, board = None):
        x,y = square.coords()
        legal_coords = []
        diagonals(legal_coords, x, y, 8, board, self.colour)
        return on_board(legal_coords)
    

class Rook(Piece):
    def legal_moves(self, square, board = None):
        x,y = square.coords()
        legal_coords = []
        rank_file(legal_coords, x, y, 8, board, self.colour)
        return on_board(legal_coords)


class King(Piece):
    moved = False
    def legal_moves(self, square, board = None):
        x,y= square.coords()
        legal_coords = []
        diagonals(legal_coords, x, y, 2, board, self.colour)
        rank_file(legal_coords, x, y, 2, board, self.colour)
        return on_board(legal_coords)


class Queen(Piece):
    def legal_moves(self, square, board = None):
        x, y = square.coords()
        legal_coords = []
        diagonals(legal_coords, x, y, 8, board, self.colour)
        rank_file(legal_coords, x, y, 8, board, self.colour) 
        return on_board(legal_coords)


class GeneratePiece():
    #TODO make this class sleeker.
    """subclasses = {}
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._piece_type] = cls"""

    # generates an instance of each piece class
    # at squares, according to fen string.
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
        self.selected = False

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)

    def colour(self):
        return 'w' if (((self.index // 8)%2) - (self.index % 2) == 0) else 'b'

    def coords(self):
        return (ord(self.name[0])-ord('a'), int(self.name[1])-1)

    def draw(self):
        # Pieces are drawn onto individual square 
        # surfaces, depending on Square.piece attr,
        # and ChessBoard.draw() blits each square.
        #
        # Squares will have to be redrawn upon 
        # piece Movement.
        
        if self.colour() == 'w':
            self.square.fill((255, 255, 255))
        else:
            self.square.fill((150, 160, 160))
        if get_mouse_square() == self.coords():
            pyg.draw.rect(self.square, (170, 0, 0), (0, 0, square_size, square_size), 4)
        if self.piece is not None:
            self.square.blit(images[self.piece.name], pyg.Rect(0, 0, square_size, square_size))

        return self.square


class ChessBoard(object):
    def __init__(self):
        pass
    # generates the board,
    # 8x8 Squares() with correct
    # indexing.
    board_array = []
    for i in range(8):
        row = sq_names[i*8 : i*8 + 8]
        row = [Square(x) for x in row]
        board_array.append(row)

    def draw(self):
        for i, rows in enumerate(self.board_array):
            for j, squares in enumerate(rows):
                board_screen.blit(squares.draw(), ((j)*square_size, (7-i)*square_size))
                
    def fen_to_board(self, fen):
        # Generates pieces directly onto
        # the board_array according to fen
        # string.
        i = 0
        j = 0
        for row in fen.split('/'):
            for c in row:
                temp_sq = self.board_array[i][(j%8)]
                if c == ' ':
                    break
                elif c in '12345678':
                    j += int(c)-1
                else:
                    temp_sq.piece = GeneratePiece.create(c)
                j += 1
            i += 1


# loads images at init so fetching them is more efficient 
images = {} 
def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb','wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (square_size, square_size))

def get_mouse_square(board = None):
    mouse_pos = pyg.Vector2(pyg.mouse.get_pos())
    x = int(mouse_pos[0] // square_size)
    y = 7-int(mouse_pos[1] // square_size)
    try: 
        if x >= 0 and y >= 0:
            if board is None: return (x, y)
            else: return ((x, y), board.board_array[y][x])
    except IndexError: pass
    return None, None, None

def main():
    # Main game logic
    gameExit = False
    load_images()
    clock = pyg.time.Clock()
    game_board = ChessBoard()
    game_board.fen_to_board(starting_fen)
    selected_piece = None
    down = False
    turn = 'w'
    legal = []


    while not gameExit:
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                gameExit = True

            if event.type == pyg.MOUSEBUTTONDOWN:
                old_coord, old_square = get_mouse_square(game_board)

                if old_square.piece is not None and old_square.piece.colour == turn:
                    legal = old_square.piece.legal_moves(old_square, game_board)
                    selected_piece = old_square.piece
                    down = True
                    old_square.piece = None
                else:
                    old_coord = None
                    old_square = None

            if event.type == pyg.MOUSEBUTTONUP:
                if old_square is not None:
                    new_coord, new_sq = get_mouse_square(game_board)
                    if selected_piece is not None and new_coord in legal:
                        new_sq.piece = selected_piece
                        if isinstance(selected_piece, Pawn) or isinstance(selected_piece, King):
                            selected_piece.moved = True
                        if turn == 'w':
                            turn = 'b'
                        else:
                            turn = 'w' 
                    else:
                        old_square.piece = selected_piece

                    
                legal = []
                selected_piece = None
                down = False
                



            game_board.draw()
            if down == True and selected_piece is not None:

                for i in legal:
                    x = (i[0]*square_size) + int(square_size/2)
                    y = ((7-i[1])*square_size) + int(square_size/2)
                    pyg.draw.circle(board_screen, (150, 0, 0), (x, y), square_size/10)

                image = selected_piece.image()
                image_rect = image.get_rect()
                image_rect.center = pyg.Vector2(pyg.mouse.get_pos())
                board_screen.blit(image,image_rect)

                

            
            pyg.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    main()

               
