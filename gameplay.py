from AI import *
from time import time


def play_player(game, hash_map, game_tree, player, row, column, start):

    if player == WHITE:
        row, col, depth = ai_play(game.board, hash_map, game_tree.current)
        elapsed_time = time() - start
        moved = game.play(row, col, depth, elapsed_time)
    else:
        moved = game.play(row, column)
    if moved:
        for child in game_tree.current.children:
            if game.board == child.data:
                game_tree.current = child
                break
        else:
            new_node = TreeNode(deepcopy(game.board))
            game_tree.current.add_child(new_node)
            game_tree.current = new_node

    return time(), moved


def play_console(game, hash_map, game_tree):

    start = time()

    while game.game_on():

        if game.turn == BLACK:
            moves = game.board.legal_moves
            for move in moves:
                print(moves.index(move), "-", move, end="\t")
            my_move = -1
            while my_move not in range(len(moves)):
                my_move = int(input("\nInput move from above: "))
            row, column = moves[my_move]
            start, moved = play_player(game, hash_map, game_tree, BLACK, row, column, None)

        if game.turn == WHITE:
            play_player(game, hash_map, game_tree, WHITE, None, None, start)

    winner = game.winner()
    if winner != "TIE":
        print(f"Game over ! {winner} WON !")
    else:
        print(f"Game over ! TIE !")


def GUI_play(game, hash_map, WINDOW, FPS, font, game_tree):

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
                    end, moved = play_player(game, hash_map, game_tree, BLACK, row, column, None)
                    if moved:
                        elapsed_time = end - start
                        text, textbox = nortifications(WINDOW, font, game.black, game.white, "black", elapsed_time)
                        game.update()
                        WINDOW.blit(text, textbox)

        winner = game.winner()
        if winner is not None:
            if winner == "TIE":
                winner_text = "    TIE !        "
            else:
                winner_text = f"{winner} won !"
            WINDOW.blit(font.render(f"      "
                                    f"Black: {game.black}          "
                                    f"White: {game.white}                          "
                                    f"Game over !      "
                                    f"{winner_text}                  ", True, BLACK, WHITE), textbox)
        pygame.display.update()

        if game.turn == WHITE:
            start = time()
            end, moved = play_player(game, hash_map, game_tree, WHITE, None, None, start)

            if moved:
                elapsed_time = end - start
                text, textbox = nortifications(WINDOW, font, game.black, game.white, "white", elapsed_time)
                game.update()
                WINDOW.blit(text, textbox)
                start = end

        pygame.display.update()

    print(winner, "WON ! ")
    pygame.quit()


def main_GUI(mode, game, hash_map, WINDOW,  game_tree):
    if mode == 2:
        pygame.init()

        FPS = 200
        pygame.display.set_caption("Othello")
        font = pygame.font.Font('freesansbold.ttf', 15)
        GUI_play(game, hash_map, WINDOW, FPS, font, game_tree)


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
