def heuristics(board, move, color):

    row1 = [ 10, -10, 5, 5, 5, 5, -10,  10]
    row2 = [-10, -10, 5, 5, 5, 5, -10, -10]
    row3 = [  5,   5, 7, 7, 7, 7,   5,   5]
    row4 = [  5,   5, 7, 0, 0, 7,   5,   5]
    row5 = [  5,   5, 7, 0, 0, 7,   5,   5]
    row6 = [  5,   5, 7, 7, 7, 7,   5,   5]
    row7 = [-10, -10, 5, 5, 5, 5, -10, -10]
    row8 = [ 10, -10, 5, 5, 5, 5, -10,  10]

    board_heuristics = [row1, row2, row3, row4, row5, row6, row7, row8]

    black = board.black
    white = board.white
