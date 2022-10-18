import board as b_

# basic evaluation function
def naive_eval(board):
    material = 200 * (board.count_piece('wk')-board.count_piece('bk'))\
        + 9 * (board.count_piece('wq')-board.count_piece('bq'))\
        + 5 * (board.count_piece('wr')-board.count_piece('br'))\
        + 3 * (board.count_piece('wn')-board.count_piece('bn'))\
        + 3 * (board.count_piece('wb')-board.count_piece('bb'))\
        + 1 * (board.count_piece('wp')-board.count_piece('bp'))
    mobility = 0.1 * (len(b_.actions(board)) - len(b_.actions(board)))
    if board.turn == 'w': t=1
    else: t=-1
    return (material + mobility) * t


    