from heuristics import *
from math import inf
from copy import deepcopy


def minimax(state, depth, player=WHITE, alpha=-float(inf), beta=float(inf)):

    if depth == 0 or len(state.legal_moves) == 0:
        return heuristics(state), state

    if player == WHITE:
        value = -100000000
        best_move = None

        for legal_row, legal_column in state.legal_moves:
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, WHITE)

            new_value, new_state = minimax(tmp_board, depth-1, BLACK, alpha, beta)
            value = max(value, new_value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
            if value == new_value:
                best_move = (legal_row, legal_column)
        return value, best_move

    else:
        value = 100000000
        best_move = None

        for legal_row, legal_column in state.legal_moves:
            tmp_board = deepcopy(state)

            tmp_board.insert(legal_row, legal_column, BLACK)
            # print(tmp_board)
            new_value, new_state = minimax(tmp_board, depth-1, WHITE, alpha, beta)
            value = min(value, new_value)
            beta = min(beta, value)
            if beta <= alpha:
                break
            # print(value)
            if value == new_value:
                    best_move = (legal_row, legal_column)
        return value, best_move


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(WINDOW)

state = game.board
# print(state)
game.play(2, 3)
print(state)


mimiMa = minimax(state, 7, WHITE)[1]
row, col = mimiMa
game.play(row, col)
print(state)
print(heuristics(state))
print(state.legal_moves)


state = game.board
# print(state)
game.play(5, 1)
print(state)

mimiMa = minimax(state, 7, WHITE)[1]
row, col = mimiMa
game.play(row, col)
print(state)
print(heuristics(state))
print(state.legal_moves)

state = game.board
# print(state)
game.play(5, 5)
print(state)

mimiMa = minimax(state, 7, WHITE)[1]
row, col = mimiMa
game.play(row, col)
print(state)
print(heuristics(state))
print(state.legal_moves)

# for legal_row, legal_column in state.legal_moves:
#
#
#     tmp_board = deepcopy(state)
#     tmp_board.insert(legal_row, legal_column, WHITE)
#     # print(tmp_board)
#     print("max")
#     print(legal_row, legal_column, heuristics(tmp_board))
#     print("min")
#
#     for legal_row, legal_column in tmp_board.legal_moves:
#         tmp_board = deepcopy(state)
#         tmp_board.insert(legal_row, legal_column, BLACK)
#         print(legal_row, legal_column, heuristics(tmp_board))
#         print("jos min")
#
#         for legal_row, legal_column in tmp_board.legal_moves:
#
#             tmp_board = deepcopy(state)
#             tmp_board.insert(legal_row, legal_column, BLACK)
#             print(legal_row, legal_column, heuristics(tmp_board))
#
#             for legal_row, legal_column in tmp_board.legal_moves:
#
#                 tmp_board = deepcopy(state)
#                 tmp_board.insert(legal_row, legal_column, BLACK)
#                 print(legal_row, legal_column, heuristics(tmp_board))




























# print(game.board)
#
# node = TreeNode(game.board)
# print("START", heuristics(node))
#
# game.play(2, 3)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(4, 2)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(5, 2)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(2, 4)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(4, 5)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(4, 6)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(3, 2)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(1, 2)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(5, 5)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(3, 1)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(2, 2)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
#
# game.play(6, 1)
# node = TreeNode(game.board)
# print("AI", heuristics(node))
#
# game.play(1, 5)
# node = TreeNode(game.board)
# print("JA", heuristics(node))
