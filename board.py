import pygame as pyg
import engine

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
test_fen = "3k4/2n2B2/1KP5/2B2p2/5b1p/7P/8/8 b - - 0 0"


def diagonals(move_list, x, y, n, board, col):
    vs = [(1, 1),
          (1, -1), 
          (-1, 1), 
          (-1, -1)]
    for i in vs:
        try: obstruction_restriction(move_list, x, y, i[0], i[1], n, board, col)
        except IndexError: continue

def rank_file(move_list, x, y, n, board, col):
    vs =[(1, 0), 
         (0, 1), 
         (-1, 0), 
         (0, -1)]
    for i in vs:
        try: obstruction_restriction(move_list, x, y, i[0], i[1], n, board, col)
        except IndexError: continue
        
def obstruction_restriction(move_list, x, y, xp, yp, n, board, col):
    if isinstance(board, ChessBoard):
        for i in range(1, n):
            targ = board.board_array[y + i*yp][x + i*xp]
            if targ.piece is None: move_list.append((x + i*xp, y + i*yp))
            elif targ.piece.colour == col: break
            else:
                move_list.append((x + i*xp, y + i*yp))
                break

def on_board(los):
    # coords witihin board boundaries
    return [co for co in los if 
            all(0 <= elem <= 7 for elem in co)]

class Piece(object):
    def __init__(self, name, square):
        self.name = name
        self.colour = name[0]
        self.square = square

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

    def image(self):
        return images[self.name]


class Pawn(Piece):
    moved = False
    en_passant = False

    def attacking_squares(self, square):
        if self.colour == 'w': i = 1
        else: i = -1
        x, y = square.coords()  
        return on_board([(x+1, y+i), (x-1, y+i)])

    def capturable_squares(self, square, board):
        c_squares = []
        for x, y in self.attacking_squares(square):
            try:
                if board.board_array[y][x].piece.colour != self.colour:
                    c_squares.append((x, y))
            except (AttributeError): pass
        return c_squares
            
    def line_of_sight(self, square=None, board=None):
        if square is None: square = self.square
        x, y = square.coords()
        los = []
        if self.colour == 'w': i = 1
        else: i = -1
        if not self.moved and board.board_array[y + 2*i][x].piece is None and board.board_array[y + 1*i][x].piece is None:
            los.append((x, y + 2*i))
        if board.board_array[y + 1*i][x].piece is None:
            los.append((x, y + 1*i))
        los.extend(self.capturable_squares(square, board))
        return on_board(los)

    def promotion(self):
        x, y = self.square.coords()
        if y == 0 or y == 7: return True
    

class Knight(Piece):
    def line_of_sight(self, square = None, board = None):
        if square is None: square = self.square
        x,y = square.coords()
        los = [(x+2, y+1),
               (x+2, y-1),
               (x-2, y+1),
               (x-2, y-1),
               (x+1, y-2),
               (x-1, y-2),
               (x+1, y+2),
               (x-1, y+2)]
        los = on_board(los)
        tlist = []
        for i in los:
            if board.board_array[i[1]][i[0]].piece is not None:
                if board.board_array[i[1]][i[0]].piece.colour == self.colour: pass
                else: tlist.append(i)
            else: tlist.append(i)
        return tlist


class Bishop(Piece):
    def line_of_sight(self, square=None, board = None):
        if square is None: square = self.square
        x,y = square.coords()
        los = []
        diagonals(los, x, y, 8, board, self.colour)
        return on_board(los)
    

class Rook(Piece):
    moved = False
    def line_of_sight(self, square=None, board = None):
        if square is None: square = self.square
        x,y = square.coords()
        los = []
        rank_file(los, x, y, 8, board, self.colour)
        return on_board(los)


class King(Piece):
    moved = False
    check = False

    def castle(self, board):
        x, y = self.square.coords()
        k_rook_sq = board.board_array[y][x + 3]
        q_rook_sq = board.board_array[y][x - 4]

        # shortside
        if isinstance(k_rook_sq.piece, Rook) and not k_rook_sq.piece.moved:
            short_cas = True
            # check way is clear
            for i in board.board_array[y][ x+1: x+3]:
                if i.piece is not None:
                    short_cas = False
                    break
            # relevant squares not in check
            for i in board.board_array[y][ x: x+3]:
                if not movable(Move(self.square, i), board):
                    short_cas = False
                    break
        
        # longside
        if isinstance(q_rook_sq.piece, Rook) and not q_rook_sq.piece.moved:
            long_cas = True
            for i in board.board_array[y][ x-3: x]:
                if i.piece is not None:
                    long_cas = False
                    break
            for i in board.board_array[y][ x-2: x+1]:
                if not movable(Move(self.square, i), board):
                    long_cas = False
                    break
        return([long_cas, short_cas])

    def line_of_sight(self, square=None, board = None):
        if square is None: square = self.square
        x,y= square.coords()
        los = []
        diagonals(los, x, y, 2, board, self.colour)
        rank_file(los, x, y, 2, board, self.colour)
        return on_board(los)


class Queen(Piece):
    def line_of_sight(self, square=None, board = None):
        if square is None: square = self.square
        x, y = square.coords()
        los = []
        diagonals(los, x, y, 8, board, self.colour)
        rank_file(los, x, y, 8, board, self.colour) 
        return on_board(los)


class GeneratePiece():
    #TODO make this class sleeker.
    """subclasses = {}
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._piece_type] = cls"""

    # generates an instance of each piece class
    # at squares, according to fen string.
    @classmethod
    def create(cls, name, square):
        #return cls.subclasses[name]
        piece = None
        if name == 'P':
            piece = Pawn('bp', square)
        elif name == 'p':
            piece = Pawn('wp', square)
        elif name == ('N'):
            piece = Knight('bn', square)
        elif name == ('n'):
            piece = Knight('wn', square)
        elif name == ('B'):
            piece = Bishop('bb', square)
        elif name == ('b'):
            piece = Bishop('wb', square)
        elif name == ('R'):
            piece = Rook('br', square)
        elif name == ('r'):
            piece = Rook('wr', square)
        elif name == ('Q'):
            piece = Queen('bq', square)
        elif name == ('q'):
            piece = Queen('wq', square) 
        elif name == ('K'):
            piece = King('bk', square) 
        elif name == ('k'):
            piece = King('wk', square)

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
        # Pieces are drawn onto individual square surfaces        
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
    turn = 'w'

    # Main internal game board
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
                    temp_sq.piece = GeneratePiece.create(c, temp_sq)
                j += 1
            i += 1

    def count_piece(self, piece):
        return [i.piece.name for row in self.board_array for i in row
                if i.piece is not None].count(piece)


class Move():
    castle = False
    en_passant = False
    promotion = False

    def __init__(self, from_sq, to_sq, piece=None):
        if piece == None: self.piece = from_sq.piece
        else: self.piece = piece
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.captures = to_sq.piece

    def __str__(self) -> str:
        return "({}, {} to {})".format(self.piece, self.from_sq, self.to_sq)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Move): return NotImplemented
        return self.from_sq == __o.from_sq and self.to_sq == __o.to_sq and self.piece == __o.piece




def all_opp_los(board):
    # determine all squares in opponent's line of sight
    coords = set()
    for row in board.board_array:
        for i in row:
            if i.piece is not None:
                if i.piece.colour != board.turn and isinstance(i.piece, Pawn):
                    coords.update(i.piece.attacking_squares(i.piece.square))
                elif i.piece.colour != board.turn:
                    coords.update(i.piece.line_of_sight(i.piece.square, board))
    return list(coords)

def check_if_check(board) -> bool:
    # if self king in opp los, turn player in check
    coords = all_opp_los(board)
    for m in coords:
        x, y = m
        if isinstance(board.board_array[y][x].piece, King) and board.board_array[y][x].piece.colour == board.turn:
            return True
        else: pass
    return False


def movable(move, board) -> bool:
    # if a move results in check on self king (illegal)
    movable = False
    old_piece = move.captures
    move.to_sq.piece = move.piece
    move.from_sq.piece = None
    if not check_if_check(board): movable = True
    move.from_sq.piece = move.piece
    move.to_sq.piece = old_piece
    return movable

def legal_moves(piece, board):
    # all pseudolegals that don't result in check (legal)
    moves = [Move(piece.square, board.board_array[y][x]) for x, y in piece.line_of_sight(piece.square, board)]
    tlegal = []
    for move in moves:
        if movable(move, board):
            tlegal.append(move)
    return tlegal

def actions(board):
    # all legal moves available for turn player
    moves = []
    for row in board.board_array:
        for piece in (x.piece for x in row if x.piece is not None and x.piece.colour == board.turn):
            moves.extend(legal_moves(piece, board))
    return moves

def any_moves(game_board):
    if actions(game_board): return True
    else: return False


images = {} 
def load_images():
    # helps efficiency
    pieces = ['wp', 'wr', 'wn', 'wb','wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (square_size, square_size))

def get_mouse_square(board = None):
    # returns square cursor hovers over
    mouse_pos = pyg.Vector2(pyg.mouse.get_pos())
    x = int(mouse_pos[0] // square_size)
    y = 7-int(mouse_pos[1] // square_size)
    try: 
        if x >= 0 and y >= 0:
            if board is None: return (x, y)
            else: return ((x, y), board.board_array[y][x])
    except IndexError: pass
    return None, None, None

def make_move(move, board):
    xo, yo = move.from_sq.coords()
    x, y = move.to_sq.coords()
    
    if move.castle: 
        if x - xo > 0:
            board.board_array[y][xo+1].piece = board.board_array[y][xo+3].piece
            board.board_array[y][xo+3].piece = None
        else:
            board.board_array[y][xo-1].piece = board.board_array[y][xo-4].piece
            board.board_array[y][xo-4].piece = None

    if move.en_passant:
        if board.turn == 'w': i = -1
        else: i = 1
        board.board_array[y+i][x].piece = None

    # remove en passant possibility from all pawns
    for row in board.board_array:
        for i in row:
            if isinstance(i, Pawn): i.en_passant = False  

    if isinstance(move.piece, Pawn) and abs(y-yo) == 2:
        move.piece.en_passant = True
        
    move.to_sq.piece = move.piece
    move.to_sq.piece.square = move.to_sq
    

    if isinstance(move.piece, (Pawn, King, Rook)):
        move.piece.moved = True

    if move.promotion:
        move.piece = Queen('{}q'.format(board.turn), move.to_sq)
    
    
    
def main():
    gameExit = False
    load_images()
    clock = pyg.time.Clock()
    game_board = ChessBoard()
    game_board.fen_to_board(starting_fen) #choose starting position
    selected_piece = None
    down = False #click-drag
    en_pass_pawn = None

    while not gameExit:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                gameExit = True
                mate = False

            if event.type == pyg.MOUSEBUTTONDOWN:
                old_coord, old_square = get_mouse_square(game_board)
                if old_square.piece is not None and old_square.piece.colour == game_board.turn:
                    legal = old_square.piece.line_of_sight(old_square, game_board)
                    selected_piece = old_square.piece
                    xo, yo = old_coord
                    legal = legal_moves(selected_piece, game_board)

                    #castling
                    if isinstance(selected_piece, King) and not selected_piece.moved and not check_if_check(game_board):
                        if selected_piece.castle(game_board)[0]:
                            short_castle = Move(old_square, game_board.board_array[yo][xo - 2])
                            short_castle.castle = True
                            legal.append(short_castle)
                        if selected_piece.castle(game_board)[1]: 
                            long_castle = Move(old_square, game_board.board_array[yo][xo + 2])
                            long_castle.castle = True
                            legal.append(long_castle)
    
                    # en passant
                    if isinstance(selected_piece, Pawn):
                        for i in [-1, 1]:
                            try:
                                adjacent = game_board.board_array[yo][xo + i].piece
                            except IndexError: continue
                            if isinstance(adjacent, Pawn) and adjacent.en_passant:
                                if game_board.turn == 'w': j = 1
                                else: j = -1
                                capture = Move(old_square, game_board.board_array[yo + j][xo + i])
                                capture.en_passant = True
                                legal.append(capture)
                                
                    down = True
                    old_square.piece = None
                else:
                    old_coord = None
                    old_square = None

            if event.type == pyg.MOUSEBUTTONUP:
                if old_square is not None:
                    _, new_sq = get_mouse_square(game_board)
                    match = [x for x in legal if x.to_sq == new_sq and selected_piece == x.piece]
                    if match: new_move = match[0]
                    else: new_move = None
                    if selected_piece is not None and new_move is not None:
                        # make move
                        make_move(new_move, game_board)
                        print(engine.naive_eval(game_board))

                        

                        # change turns
                        if game_board.turn == 'w': game_board.turn = 'b'
                        else: game_board.turn = 'w' 
                    
                    # no legal square was selected
                    else: old_square.piece = selected_piece

                    # Checkmate check
                    if check_if_check(game_board):
                        mate = not any_moves(game_board)
                        if mate: gameExit = True 
                    down = False
            game_board.draw()

            if down == True and selected_piece is not None:
                # draws legal moves
                for i in legal:
                    x, y = i.to_sq.coords()
                    x = (x*square_size) + int(square_size/2)
                    y = ((7-y)*square_size) + int(square_size/2)
                    pyg.draw.circle(board_screen, (150, 0, 0), (x, y), square_size/10)
                # blits piece under cursor when dragging
                image = selected_piece.image()
                image_rect = image.get_rect()
                image_rect.center = pyg.Vector2(pyg.mouse.get_pos())
                board_screen.blit(image,image_rect)

            pyg.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    main()

               
