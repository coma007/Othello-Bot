from heuristics import *
from math import inf
from copy import deepcopy
from random import randint


def init_table():

    table = []

    for i in range(8):
        column = []
        for j in range(8):
            numbers = []
            for k in range(2):
                numbers.append(randint(0, 255))
            column.append(numbers)
        table.append(column)

    return table


def hash_formula(board, table):

    hashed = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            field = table[i][j]
            if piece != 0:
                if piece.color == WHITE:
                    color = 0
                else:
                    color = 1
                table_value = field[color]
                hashed ^= table_value

    return hashed


def variable_depth(state):
    oldest_children = len(state.legal_moves)
    if oldest_children > 9:
        return 2
    elif oldest_children > 7:
        return 3
    elif oldest_children > 5:
        return 4
    else:
        return 5


def minimax(state, depth, table, hash_map, player=WHITE, alpha=-float(inf), beta=float(inf)):

    if depth == 0 or len(state.legal_moves) == 0:

        future_legal_moves = 0
        if len(state.legal_moves) != 0:
            for legal_row, legal_column in state.legal_moves:
                tmp_board = deepcopy(state)
                color = WHITE
                if tmp_board.playing == WHITE:
                    color = BLACK
                tmp_board.insert(legal_row, legal_column, color)
                future_legal_moves = max(future_legal_moves, len(tmp_board.legal_moves))

        hash = hash_formula(state.state, table)

        if hash not in hash_map.keys():
            value = heuristics(state)
            value += mobility_heuristics(len(state.legal_moves), future_legal_moves)
            hash_map[hash] = value
        else:
            value = hash_map[hash]
        return value, state, future_legal_moves

    if player == WHITE:
        value = -100000000
        best_move = None
        now_legal_moves = 0

        for legal_row, legal_column in state.legal_moves:
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, WHITE)
            tmp_legal_moves = len(tmp_board.legal_moves)

            hash = hash_formula(tmp_board.state, table)

            if hash not in hash_map.keys():
                value = heuristics(state)
                hash_map[hash] = value
            else:
                value = hash_map[hash]

            new_value, new_state, future_legal_moves = minimax(tmp_board, depth-1, table, hash_map,  BLACK, alpha, beta)

            new_value += mobility_heuristics(tmp_legal_moves, future_legal_moves)
            value = max(value, new_value)
            alpha = max(alpha, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]
        return value, best_move, now_legal_moves

    else:
        value = 100000000
        best_move = None
        now_legal_moves = 0

        for legal_row, legal_column in state.legal_moves:
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, BLACK)
            tmp_legal_moves = len(tmp_board.legal_moves)

            hash = hash_formula(tmp_board.state, table)
            if hash not in hash_map.keys():
                value = heuristics(state)
                hash_map[hash] = value
            else:
                value = hash_map[hash]

            new_value, new_state, future_legal_moves = minimax(tmp_board, depth-1, table, hash_map, WHITE, alpha, beta)

            new_value += mobility_heuristics(tmp_legal_moves, future_legal_moves)

            value = min(value, new_value)
            beta = min(beta, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]
        return value, best_move, now_legal_moves



def ai_play(board, table, hash_map):

    depth = variable_depth(board)
    row, col = minimax(board, depth, table, hash_map)[1]

    return row, col
