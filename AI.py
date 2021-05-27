from heuristics import *
from math import inf
from copy import deepcopy
from data_structures.GameTree import *
from time import time


def variable_depth(state, elapsed_time):

    oldest_children = len(state.legal_moves)
    if elapsed_time > 2.5:
        return 1
    if oldest_children > 8:
        return 2
    elif oldest_children > 5:
        return 3
    else:
        return 4


def minimax(state, depth, hash_map, elapsed_time, current_node, player=WHITE, alpha=-float(inf), beta=float(inf)):

    if depth == 0 or len(state.legal_moves) == 0:
        start = time()

        future_legal_moves = 0
        if len(state.legal_moves) != 0:
            for legal_row, legal_column in state.legal_moves:
                tmp_board = deepcopy(state)
                color = WHITE
                if tmp_board.playing == WHITE:
                    color = BLACK
                tmp_board.insert(legal_row, legal_column, color)
                future_legal_moves = max(future_legal_moves, len(tmp_board.legal_moves))

        try:
            value = hash_map[state.state]
        except KeyError:
            value = heuristics(state)
            value += mobility_heuristics(len(state.legal_moves), future_legal_moves)
            hash_map[state.state] = value

        return value, state, future_legal_moves, time() - start

    if player == WHITE:
        value = -100000000
        best_move = None
        now_legal_moves = 0
        start = elapsed_time

        for legal_row, legal_column in state.legal_moves:
            if elapsed_time > 2.5:
                break
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, WHITE)
            tmp_legal_moves = len(tmp_board.legal_moves)
            new_node = None
            for child in current_node.children:
                if tmp_board == child.data:
                    new_node = child
                    break
            else:
                new_node = TreeNode(deepcopy(tmp_board))
                current_node.add_child(new_node)
            if (legal_row, legal_column) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                best_move = (legal_row, legal_column)
                break
            # new_depth = variable_depth(tmp_board, elapsed_time)
            # if new_depth <= depth:
            #     depth = new_depth
            new_value, new_state, future_legal_moves, new_time = minimax(tmp_board, depth - 1, hash_map, elapsed_time, new_node, BLACK, alpha, beta)
            elapsed_time += new_time
            if elapsed_time > 2:
                break

            try:
                current_value = hash_map[state.state]
            except KeyError:
                current_value = heuristics(state)
                current_value += mobility_heuristics(len(state.legal_moves), future_legal_moves)
                hash_map[state.state] = current_value

            value = max(value, new_value)
            alpha = max(alpha, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]
        return value, best_move, now_legal_moves, elapsed_time - start

    else:
        value = 100000000
        best_move = None
        now_legal_moves = 0
        start = elapsed_time

        for legal_row, legal_column in state.legal_moves:
            if elapsed_time > 2.5:
                break
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, BLACK)
            # new_node = TreeNode(tmp_board)
            tmp_legal_moves = len(tmp_board.legal_moves)
            new_node = None
            for child in current_node.children:
                if tmp_board == child.data:
                    new_node = child
                    break
            else:
                new_node = TreeNode(deepcopy(tmp_board))
                current_node.add_child(new_node)

            # new_depth = variable_depth(tmp_board, elapsed_time)
            # if new_depth < depth - 1:
            #     depth = new_depth
            new_value, new_state, future_legal_moves, new_time = minimax(tmp_board, depth - 1, hash_map, elapsed_time, new_node, WHITE, alpha, beta)

            elapsed_time += new_time
            if elapsed_time > 2:
                break

            try:
                current_value = hash_map[state.state]
            except KeyError:
                current_value = heuristics(state)
                current_value += mobility_heuristics(len(state.legal_moves), future_legal_moves)
                hash_map[state.state] = current_value

            value = min(value, new_value)
            beta = min(beta, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]

        return value, best_move, now_legal_moves, elapsed_time - start


def ai_play(board, hash_map, current_node):

    elapsed_time = time() - time()
    depth = variable_depth(board, elapsed_time)
    row, col = minimax(board, depth, hash_map, elapsed_time, current_node)[1]

    return row, col, depth

