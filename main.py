from GUI import *
from data_structures.HashMap import *
from data_structures.GameTree import *

if __name__ == '__main__':

    # Inicijalizacija igre

    mode = 0
    print("GAME MODE: ", "\n 1 - console\n 2 - gui")
    while mode not in ["1", "2"]:
        mode = input("Select game mode: ")

    mode = int(mode)
    if mode == 1:
        game = Game(mode)
        hash_map = HashMap()

        game_root = TreeNode(deepcopy(game.board))
        for legal_row, legal_column in game.board.legal_moves:
            tmp_board = deepcopy(game.board)
            tmp_board.insert(legal_row, legal_column, BLACK)
            new_node = TreeNode(tmp_board)
            game_root.add_child(new_node)
        game_tree = Tree(game_root)

        try:
            pygame.quit()
        except Exception:
            pass

        play_console(game, hash_map, game_tree)

    if mode == 2:

        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

        game = Game(mode, WINDOW)
        hash_map = HashMap()

        game_root = TreeNode(deepcopy(game.board))
        for legal_row, legal_column in game.board.legal_moves:
            tmp_board = deepcopy(game.board)
            tmp_board.insert(legal_row, legal_column, BLACK)
            new_node = TreeNode(tmp_board)
            game_root.add_child(new_node)
        game_tree = Tree(game_root)
        main_GUI(mode, game, hash_map, game_tree, WINDOW)
