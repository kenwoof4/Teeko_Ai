import random
import copy
import time


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.depth = 4

    def succ(self, state, piece):
        drop_phase = True
        count = 0
        succs = []
        new_state = copy.deepcopy(state)

        for row in range(5):
            for column in range(5):
                if state[row][column] == 'r' or state[row][column] == 'b':
                    count += 1
        if count >= 8:
            drop_phase = False

        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if new_state[row][col] == ' ':
                        new_state[row][col] = piece
                        succs.append(new_state)
                        new_state = copy.deepcopy(state)
        else:
            for row in range(5):
                for column in range(5):
                    if state[row][column] == piece:
                        m_row = row - 1
                        p_row = row + 1
                        m_column = column - 1
                        p_column = column + 1
                        # top left
                        if m_row >= 0 and m_column >= 0:
                            if state[m_row][m_column] == ' ':
                                new_state[m_row][m_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)

                        # left
                        if m_column >= 0:
                            if state[row][m_column] == ' ':
                                new_state[row][m_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)

                        # top
                        if m_row >= 0:
                            if state[m_row][column] == ' ':
                                new_state[m_row][column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)

                        # bottom right
                        if p_row < 5 and p_column < 5:
                            if state[p_row][p_column] == ' ':
                                new_state[p_row][p_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)
                                
                        # right
                        if p_column < 5:
                            if state[row][p_column] == ' ':
                                new_state[row][p_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)

                        # bottom
                        if p_row < 5:
                            if state[p_row][column] == ' ':
                                new_state[p_row][column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)
                                
                        # bottom left
                        if p_row < 5 and m_column >= 0:
                            if state[p_row][m_column] == ' ':
                                new_state[p_row][m_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)

                        # top right
                        if m_row >= 0 and p_column < 5:
                            if state[m_row][p_column] == ' ':
                                new_state[m_row][p_column] = piece
                                new_state[row][column] = ' '
                                succs.append(new_state)
                                new_state = copy.deepcopy(state)
        return succs

    def heuristic_game_value(self, state, piece):
        factor = 1 if piece == self.my_piece else -1
        if self.game_value(state) != 0:
            return self.game_value(state)

        max_row_score = 0
        for row in state:
            for i in range(2):
                row_score = 0
                if row[i] == piece:
                    row_score += 0.25
                elif row[i] != ' ':
                    row_score -= 0.05

                if row[i+1] == piece:
                    row_score += 0.25
                elif row[i+1] != ' ':
                    row_score -= 0.05

                if row[i+2] == piece:
                    row_score += 0.25
                elif row[i+2] != ' ':
                    row_score -= 0.05

                if row[i+3] == piece:
                    row_score += 0.25
                elif row[i+3] != ' ':
                    row_score -= 0.05

                if row_score > max_row_score:
                    max_row_score = row_score

        max_col_score = 0
        for col in range(5):
            for i in range(2):
                col_score = 0
                if state[i][col] == piece:
                    col_score += 0.25
                elif state[i][col] != ' ':
                    col_score -= 0.05

                if state[i+1][col] == piece:
                    col_score += 0.25
                elif state[i+1][col] != ' ':
                    col_score -= 0.05

                if state[i+2][col] == piece:
                    col_score += 0.25
                elif state[i+2][col] != ' ':
                    col_score -= 0.05

                if state[i+3][col] == piece:
                    col_score += 0.25
                elif state[i+3][col] != ' ':
                    col_score -= 0.05

                if col_score > max_col_score:
                    max_col_score = col_score

        max_diag1_score = 0
        for row in range(2):
            for col in range(2):
                diag1_score = 0
                if state[row][col] == piece:
                    diag1_score += 0.25
                elif state[row][col] != ' ':
                    diag1_score -= 0.04

                if state[row+1][col+1] == piece:
                    diag1_score += 0.25
                elif state[row+1][col+1] != ' ':
                    diag1_score -= 0.04

                if state[row+2][col+2] == piece:
                    diag1_score += 0.25
                elif state[row+2][col+2] != ' ':
                    diag1_score -= 0.04

                if state[row+3][col+3] == piece:
                    diag1_score += 0.25
                elif state[row+3][col+3] != ' ':
                    diag1_score -= 0.04

            if diag1_score > max_diag1_score:
                max_diag1_score = diag1_score

        max_diag2_score = 0
        for row in range(2):
            for col in range(3, 5):
                diag2_score = 0
                if state[row][col] == piece:
                    diag2_score += 0.25
                elif state[row][col] != ' ':
                    diag2_score -= 0.04

                if state[row+1][col-1] == piece:
                    diag2_score += 0.25
                elif state[row+1][col-1] != ' ':
                    diag2_score -= 0.04

                if state[row+2][col-2] == piece:
                    diag2_score += 0.25
                elif state[row+2][col-2] != ' ':
                    diag2_score -= 0.04

                if state[row+3][col-3] == piece:
                    diag2_score += 0.25
                elif state[row+3][col-3] != ' ':
                    diag2_score -= 0.04

            if diag2_score > max_diag2_score:
                max_diag2_score = diag2_score

        # Change to 2x2 squares
        max_square_score = 0
        for row in range(3):
            for col in range(3):
                square_score = 0
                if state[row][col] == piece:
                    square_score += 0.25

                if state[row][col+1] == piece:
                    square_score += 0.25

                if state[row+1][col] == piece:
                    square_score += 0.25

                if state[row+1][col+1] == piece:
                    square_score += 0.25

                if square_score > max_square_score:
                    max_square_score = square_score

        max_row_score += random.uniform(-0.02, 0.02)
        max_col_score += random.uniform(-0.02, 0.02)
        max_diag1_score += random.uniform(-0.02, 0.02)
        max_diag2_score += random.uniform(-0.02, 0.02)
        max_square_score += random.uniform(-0.02, 0.02)

        hval = max(max_row_score, max_col_score, max_diag1_score,
                   max_diag2_score, max_square_score)
        return factor * hval

    def max_value(self, alpha, beta, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)

        if depth >= self.depth:
            return self.heuristic_game_value(state, self.my_piece)

        for successor in self.succ(state, self.my_piece):
            alpha = max(alpha, self.min_value(
                alpha, beta, successor, depth + 1))
            if alpha >= beta:
                return beta
        return alpha

    def min_value(self, alpha, beta, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth >= self.depth:
            return self.heuristic_game_value(state, self.opp)
        
        for successor in self.succ(state, self.opp):
            beta = min(beta, self.max_value(alpha, beta, successor, depth + 1))
            if alpha >= beta:
                return beta
        return beta

    def make_move(self, state):
        start = time.time()
        drop_phase = True
        count = 0
        
        best_value = float("-inf")
        best_state = None
        for successor in self.succ(state, self.my_piece):
            current_value = self.min_value(
                float("-inf"), float("inf"), successor, 1)
            if current_value > best_value:
                best_value = current_value
                best_state = successor

        for row in range(5):
            for column in range(5):
                if state[row][column] == 'r' or state[row][column] == 'b':
                    count += 1
        if count >= 8:
            drop_phase = False

        move = []
        if not drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] != ' ' and state[i][j] != best_state[i][j]:
                        (source_row, source_col) = (i, j)
                        move.append((source_row, source_col))

        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ' and state[i][j] != best_state[i][j]:
                    (row, col) = (i, j)
                    # ensure the destination (row,col) tuple is at the beginning of the move list
                    move.insert(0, (row, col))

        stop = time.time()
        print(f'Move made in {(stop - start):.3f} seconds.\n')
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception(
                    'Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):

        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # check / diagonal wins
        for row in range(2):
            for col in range(3, 5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # check 2x2 square  wins
        for row in range(3):
            for col in range(3):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row+1][col] == state[row+1][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " +
                  chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move(
                        [(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " +
                  chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
