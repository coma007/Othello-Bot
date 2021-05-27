from gameplay import *
from data_structures.HashMap import *
from data_structures.GameTree import *


def select_mode():

    mode = -1
    print("GAME MODE: ", "\n 1 - console\n 2 - gui")
    while mode not in ["1", "2"]:
        mode = input("Select game mode: ")

    return int(mode)


def init_game():

    mode = select_mode()

    game = Game(mode)
    hash_map = HashMap()

    game_root = TreeNode(deepcopy(game.board))
    game_tree = Tree(game_root)
    for row, col in game.board.legal_moves:
        tmp_board = deepcopy(game.board)
        tmp_board.insert(row, col, BLACK)
        game_root.add_child(TreeNode(tmp_board))

    return game, hash_map, game_tree, mode


def begin():

    game, hash_map, game_tree, mode = init_game()

    if mode == 1:
        try:
            pygame.quit()
        except Exception:
            pass
        play_console(game, hash_map, game_tree)

    elif mode == 2:
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        game.window = WINDOW
        main_GUI(mode, game, hash_map, WINDOW, game_tree)


if __name__ == '__main__':

    begin()
