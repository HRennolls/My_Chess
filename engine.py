import board as b_

# basic evaluation function
def naive_eval(board):
    material = 200 * (board.count_piece('wk')-board.count_piece('bk'))\
        + 9 * (board.count_piece('wq')-board.count_piece('bq'))\
        + 5 * (board.count_piece('wr')-board.count_piece('br'))\
        + 3 * (board.count_piece('wn')-board.count_piece('bn'))\
        + 3 * (board.count_piece('wb')-board.count_piece('bb'))\
        + 1 * (board.count_piece('wp')-board.count_piece('bp'))

    if board.turn == 'w':
        t=1
        board.turn = 'b'
        opp_mobility = len(b_.actions(board))
        board.turn = 'w'
    else: 
        t=-1
        board.turn = 'w'
        opp_mobility = len(b_.actions(board))
        board.turn = 'b'
    
    mobility = 0.1 * (len(b_.actions(board)) - opp_mobility)
    return (material + mobility) * t

def checkmate(board):
    if not b_.any_moves(board):
        if board.turn == 'w': return 'b'
        else: return 'w'
    else: return None



def negamax(board, depth=2, root = True):
    if depth == 0:
        return naive_eval(board)
    
    max_eval = float('-infinity')
    move_list = b_.actions(board)
    for move in move_list:
        b_.make_move(move, board)
        current_eval = -negamax(board, depth-1, False)
        b_.unmake_move(move, board)

        if current_eval > max_eval:
            max_eval = current_eval

    return max_eval

def negamaxroot(board, depth=2):
    if depth == 0:
        return naive_eval(board)
    
    max_eval = float('-infinity')
    
    move_list = b_.actions(board)
    best_move = move_list[0]
    for move in move_list:
        b_.make_move(move, board)
        current_eval = -negamax(board, depth-1, False)
        b_.unmake_move(move, board)

        if current_eval > max_eval:
            max_eval = current_eval
            best_move = move

    return best_move, max_eval
    