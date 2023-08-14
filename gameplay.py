"""
Module with basic game flow functions.
"""

from bot_logic.bot import *
from time import time


def play_player(game, hash_map, game_tree, player, row=None, column=None, start=None):
    """
    Helper function for determining a player's move.

    :param game: Game instance.
    :type game: Game
    :param hash_map: Hash map.
    :type hash_map: data_structures.HashMap.HashMap
    :param game_tree: Game tree.
    :type game_tree: data_structures.GameTree.Tree
    :param player: Current player.
    :type player: tuple[int, int, int]
    :param row: Chosen row (for the black player).
    :type row: int or NoneType
    :param column: Chosen column (for the black player).
    :type column: int or NoneType
    :param start: Start time of the move.
    :type start: float or NoneType

    :return: End time of the move and whether the move was successful.
    :rtype: tuple[float, bool]
    """

    if player == WHITE:
        row, col, depth = bot_play(game.board, hash_map, game_tree.current)
        elapsed_time = time() - start
        moved = game.play(row, col, depth, elapsed_time)
    else:
        moved = game.play(row, column)
    if moved:
        for current_child in game_tree.current.children:
            if game.board == current_child.data:
                game_tree.current = current_child
                break
        else:
            new_node = TreeNode(deepcopy(game.board))
            game_tree.current.add_child(new_node)
            game_tree.current = new_node
    return time(), moved


def play_console(game, hash_map, game_tree):
    """
    Main function for playing in console mode.

    :param game: Game instance.
    :type game: Game
    :param hash_map: Hash map.
    :type hash_map: HashMap
    :param game_tree: Game tree.
    :type game_tree: Tree
    """

    start = time()
    while game.game_on():
        if game.turn == BLACK:
            moves = game.board.legal_moves
            print()
            for move in moves:
                print(moves.index(move), "->", move, end="\t\t")
            my_move = -1
            while my_move not in range(len(moves)):
                try:
                    my_move = int(input("\nInput one of the moves above: "))
                except Exception:
                    continue
            row, column = moves[my_move]
            start, moved = play_player(game, hash_map, game_tree, BLACK, row, column, None)
        if game.turn == WHITE:
            play_player(game, hash_map, game_tree, WHITE, None, None, start)
    winner = game.winner()
    if winner != "TIE":
        print(f"Game over! {winner} WON!")
    else:
        print("Game over! TIE!")


def play_gui(game, hash_map, window, fps, font, game_tree):
    """
    Main function for playing in GUI mode.

    :param game: Game instance.
    :type game: Game
    :param hash_map: Hash map.
    :type hash_map: data_structures.HashMap.HashMap
    :param window: Window in which the game is displayed.
    :type window: pygame.Surface
    :param fps: Frames per second.
    :type fps: int
    :param font: Text font in the window.
    :type font: pygame.font.Font
    :param game_tree: Game tree.
    :type game_tree: Tree
    """

    clock = pygame.time.Clock()
    start = time()
    run = True
    text, textbox = nortifications(window, font)
    winner = None
    game.update()
    while run:
        clock.tick(fps)
        window.blit(text, textbox)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == BLACK:
                    position = pygame.mouse.get_pos()
                    row, column = mouse_action(position)
                    end, moved = play_player(game, hash_map, game_tree, BLACK, row, column, None)
                    if moved:
                        elapsed_time = end - start
                        text, textbox = nortifications(window, font, game.black, game.white, "black", elapsed_time)
                        game.update()
                        window.blit(text, textbox)
        winner = game.winner()
        if winner is not None:
            if winner == "TIE":
                winner_text = "       TIE!        "
            else:
                winner_text = f"{winner} won!"
            window.blit(font.render(f"      "
                                    f"Black: {game.black}          "
                                    f"White: {game.white}                          "
                                    f"Game over!      "
                                    f"{winner_text}                  ", True, BLACK, WHITE), textbox)
        pygame.display.update()
        if game.turn == WHITE:
            start = time()
            end, moved = play_player(game, hash_map, game_tree, WHITE, None, None, start)
            if moved:
                elapsed_time = end - start
                text, textbox = nortifications(window, font, game.black, game.white, "white", elapsed_time)
                game.update()
                window.blit(text, textbox)
                start = end
        pygame.display.update()
    print(f"{winner} WON!")
    pygame.quit()


def main_gui(mode, game, hash_map, window, game_tree):
    """
    Initialization of parameters needed for GUI mode.

    :param mode: Mode.
    :type mode: int
    :param game: Game instance.
    :type game: Game
    :param hash_map: Hash map.
    :type hash_map: data_structures.HashMap.HashMap
    :param window: Window in which the game is displayed.
    :type window: pygame.Surface
    :param game_tree: Game tree.
    :type game_tree: Tree
    """

    if mode == 2:
        pygame.init()
        FPS = 60
        pygame.display.set_caption("Othello")
        font = pygame.font.Font('freesansbold.ttf', 15)
        play_gui(game, hash_map, window, FPS, font, game_tree)


def nortifications(window, font=None, black=2, white=2, last_played="", elapsed_time=0.00):
    """
    Helper function for displaying notifications in GUI mode.

    :param window: Window in which the game is displayed.
    :type window: pygame.Surface
    :param font: Text font in the window.
    :type font: pygame.font.Font
    :param black: Number of black pieces on the board.
    :type black: int
    :param white: Number of white pieces on the board.
    :type white: int
    :param last_played: Player who just made a move.
    :type last_played: str
    :param elapsed_time: Duration of the last played move.
    :type elapsed_time: float

    :return: Text and text box area to be displayed in the window.
    :rtype: tuple[pygame.Surface, pygame.Rect]
    """

    pygame.draw.rect(window, WHITE, pygame.Rect(0, 700, 700, 30))
    text = font.render(f'      '
                       f'Black: {black}          '
                       f'White: {white}               '
                       f'Elapsed time for the last {last_played} move: {elapsed_time: .2f} s     ',
                       True, BLACK, WHITE)
    textbox = text.get_rect()
    textbox.center = (700 // 2, 715)
    return text, textbox


def mouse_action(position):
    """
    Helper function for calculating the selected field's coordinates in GUI mode based on mouse action.

    :param position: Coordinates recorded during mouse action.
    :type position: tuple[int, int]

    :return: Row and column of the selected field on the board.
    :rtype: tuple[int, int]
    """

    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column
