from AI import *
from time import time


def play_console(game, hash_map, game_tree):

    while game.game_on():

        if game.turn == BLACK:
            moves = game._legal_moves
            for move in moves:
                print(moves.index(move), "-", move, end="\t")
            my_move = -1
            while my_move not in range(len(moves)):
                my_move = int(input("\nInput move from above: "))
            row, column = moves[my_move]
            moved = game.play(row, column)
            if moved:
                for child in game_tree.current.children:
                    if child.data == game.board:
                        game_tree.current = child
                else:
                    new_node = TreeNode(deepcopy(game.board))
                    game_tree.current.add_child(new_node)
                    game_tree.current = new_node

        if game.turn == WHITE:
            start = time()
            row, col, depth = ai_play(game.board, hash_map, game_tree.current)
            elapsed_time = time() - start
            moved = game.play(row, col, depth, elapsed_time)
            if moved:
                for child in game_tree.current.children:
                    if child.data == game.board:
                        game_tree.current = child
                else:
                    new_node = TreeNode(deepcopy(game.board))
                    game_tree.current.add_child(new_node)
                    game_tree.current = new_node


def main_GUI(mode, game, hash_map, game_tree, WINDOW):
    if mode == 2:
        pygame.init()

        FPS = 200
        pygame.display.set_caption("Othello")
        font = pygame.font.Font('freesansbold.ttf', 15)
        GUI_play(game, hash_map, game_tree, WINDOW, FPS, font)


def nortifications(WINDOW, font=None, black=2, white=2, last_played="", time=0.00):
    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(0, 700, 700, 30))
    text = font.render(f'      '
                       f'Black: {black}          '
                       f'White: {white}               '
                       f'Elapsed time for the last {last_played} move: {time: .2f} s     ',
                       True, BLACK, WHITE)
    textbox = text.get_rect()
    textbox.center = (700 // 2, 715)

    return text, textbox


def mouse_action(position):

    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE

    return row, column


def GUI_play(game, hash_map, game_tree, WINDOW, FPS, font):

    clock = pygame.time.Clock()
    start = time()
    run = True
    text, textbox = nortifications(WINDOW, font)
    winner = None

    game.update()

    while run:
        clock.tick(FPS)
        WINDOW.blit(text, textbox)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == BLACK:
                    position = pygame.mouse.get_pos()
                    row, column = mouse_action(position)
                    moved = game.play(row, column)
                    if moved:
                        elapsed_time = time() - start
                        text, textbox = nortifications(WINDOW, font, game.black, game.white, "black", elapsed_time)

                        for child in game_tree.current.children:
                            if child.data == game.board:
                                game_tree.current = child
                        else:
                            new_node = TreeNode(deepcopy(game.board))
                            game_tree.current.add_child(new_node)
                            game_tree.current = new_node
                        game.update()
                        WINDOW.blit(text, textbox)

        winner = game.winner()
        if winner is not None:
            WINDOW.blit(font.render(f"      "
                                    f"Black: {game.black}          "
                                    f"White: {game.white}                          "
                                    f"Game over !      "
                                    f"{winner} won !                  ", True, BLACK, WHITE), textbox)
        pygame.display.update()

        if game.turn == WHITE:
            start = time()
            row, col, depth = ai_play(game.board, hash_map, game_tree.current)
            elapsed_time = time() - start
            moved = game.play(row, col, depth, elapsed_time)
            if moved:
                text, textbox = nortifications(WINDOW, font, game.black, game.white, "white", elapsed_time)

                for child in game_tree.current.children:
                    if child.data == game.board:
                        game_tree.current = child
                else:
                    new_node = TreeNode(deepcopy(game.board))
                    game_tree.current.add_child(new_node)
                    game_tree.current = new_node
                game.update()
                WINDOW.blit(text, textbox)
                start = time()

        pygame.display.update()

    print(winner, "WON ! ")
    pygame.quit()

