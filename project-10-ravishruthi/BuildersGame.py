# Author: Shruthi Ravi
# Date: 12/01/2020
# Description: BuildersGame represents a board that allows two players to move
#              their builders around the board and take turns adding levels to
#              each square. The first player to move one of their builders on top
#              of a 3-level tower wins the game.
#

class BuildersGame:
    """
        Represents a BuildersGame that has a board (5x5 grid), current state, turn and is_Valid
        (checks to see both players have made their initial placements. It has a get method to
        get the current status of the game. A method, initial_placement, that places both players
        builders on the board. A method, make_move, takes 6 parameters, row and col for current
        builder's location, row and col to where the player wants to move that builder, and row
        and col that the player wants to add a level to. It then records it, update the current
        status of the game and changes the player.
    """

    def __init__(self):
        """ Creates a new BuildersGame. """
        self._board = [[['', 0], ['', 0], ['', 0], ['', 0], ['', 0]],  # row1
                       [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]],  # row2
                       [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]],  # row3
                       [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]],  # row4
                       [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]]  # row5
        self._current_state = "UNFINISHED"
        self._turn = 'x'
        self._is_Valid = True  # to check validity of initial placement being called

    def get_current_state(self):
        """ Returns the current state. """
        return self._current_state

    def initial_placement(self, row_b1, col_b1, row_b2, col_b2, player):
        """
            Places the player's two builders on the board.
            :param row_b1: The row to place builder one.
            :param col_b1: The col to place builder one.
            :param row_b2: The row to place builder two.
            :param col_b2: The col to place builder two.
            :param player: The player
            :return: True or False
        """
        if ((self._turn != player) or (self._is_Valid == False)):
            return False
        for row in self._board:
            if (row == row_b1 or row == row_b2):
                for col in row:
                    if (col == col_b1 or col == col_b2):
                        if (col[0] != ''):
                            return False
                        col[0] = player
        if (player == 'x'):
            self._board[row_b1][col_b1][0] = self._turn
            self._board[row_b2][col_b2][0] = self._turn
            self._turn = 'o'
        else:
            self._board[row_b1][col_b1][0] = self._turn
            self._board[row_b2][col_b2][0] = self._turn
            self._turn = 'x'
            self._is_Valid = False
        return True

    def make_move(self, row_piece, col_piece, row_movingTo, col_movingTo, row_build, col_build):
        """
            Records the current player's move, updates the current state, and returns True.
            If it's not the player's turn, or if the move is invalid, or if the game has ended,
            it returns False.
            :param row_piece: The current row of a builder.
            :param col_piece: The current col of a builder.
            :param row_movingTo: The row where the player wants to move the builder.
            :param col_movingTo: The col where the player wants to move the builder.
            :param row_build: The row where the player wants to build a level.
            :param col_build: The col where the player wants to build a level.
            :return: True or False
        """
        if (self._current_state != "UNFINISHED"):
            return False
        # player being moved is not the same as the player who's turn it is
        elif (self._turn != self._board[row_piece][col_piece][0]):
            return False
        # the square being moved to is already occupied by a builder
        elif (self._board[row_movingTo][col_movingTo][0] != ''):
            return False
        # trying to move more than 1 level up
        elif (((self._board[row_movingTo][col_movingTo][1]) -
               (self._board[row_piece][col_piece][1])) > 1):
            return False
        # the square being built on is already occupied by a builder
        elif (self._board[row_build][col_build][0] != ''):
            return False
        # the square being built on has 4 levels already
        elif (self._board[row_build][col_build][1] == 4):
            return False
        # the square being built on is an adjacent square
        elif (self._is_adjacent_square(row_movingTo, col_movingTo, row_build, col_build) == False):
            return False
        # one or both players haven't made their initial placements
        elif (self._is_Valid):
            return False
        # current player moves builder on top of a 3-story tower, they win
        elif (self._board[row_movingTo][col_movingTo][1] == 3):
            if (self._turn == 'x'):
                self._current_state = "X_WON"
            else:
                self._current_state = "O_WON"
            return False
        # if opponent is 'o', and they have no legal moves, 'x' wins
        elif (self._turn == 'x' and self._legal_move_available('o') == False):
            self._current_state = "X_WON"
            return False
        # if opponent is 'x', and they have no legal moves, 'o' wins
        elif (self._turn == 'o' and self._legal_move_available('x') == False):
            self._current_state = "O_WON"
            return False

        else:
            self._board[row_piece][col_piece][0] = ''
            self._board[row_movingTo][col_movingTo][0] = self._turn
            self._board[row_build][col_build][1] += 1
            if (self._turn == 'x'):
                self._turn = 'o'
            else:
                self._turn = 'x'
        return True

    def _legal_move_available(self, opponent):
        """
            If the opponent has no possible, legal move left, the current
            player wins, current status is updated and it returns True. If
            a legal move is available, it returns False.
            :param opponent: The player whose turn it is NOT.
            :return: True or False
        """
        opponent_level = []
        for row in self._board:  # Get current square levels for both builders
            for col in row:
                if (col[0] == opponent):
                    opponent_level.append(col[1])
        for row in self._board:  # Check if player has legal move available
            for col in row:
                if (col[0] == ''):
                    if ((col[1] - opponent_level[0] <= 1) or (col[1] - opponent_level[1] <= 1)):
                        return True
        return False

    # Checks if level is being added to an adjacent square
    def _is_adjacent_square(self, row_movingTo, col_movingTo, row_build, col_build):
        """
            Checks to see if the players is building a level on an adjacent square.
            If the player is, it returns True, else it returns False.
            :param :param row_movingTo: The row where the player wants to move the builder.
            :param col_movingTo: The col where the player wants to move the builder.
            :param row_build: The row where the player wants to build a level.
            :param col_build: The col where the player wants to build a level.
            :return: True or False
        """
        if ((row_movingTo == 0 and col_movingTo == 0)):
            if ((row_build == row_movingTo and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo + 1)):
                return True
        elif ((row_movingTo == 1 and col_movingTo == 0) or
              (row_movingTo == 2 and col_movingTo == 0) or
              (row_movingTo == 3 and col_movingTo == 0)):
            if ((row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo)):
                return True
        elif ((row_movingTo == 4 and col_movingTo == 0)):
            if ((row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo and col_build == col_movingTo + 1)):
                return True
        elif ((row_movingTo == 0 and col_movingTo == 1) or
              (row_movingTo == 0 and col_movingTo == 2) or
              (row_movingTo == 0 and col_movingTo == 3)):  # l1
            if ((row_build == row_movingTo and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo and col_build == col_movingTo + 1)):
                return True
        elif ((row_movingTo == 1 and col_movingTo == 1) or
              (row_movingTo == 1 and col_movingTo == 2) or
              (row_movingTo == 1 and col_movingTo == 3) or
              (row_movingTo == 2 and col_movingTo == 1) or
              (row_movingTo == 2 and col_movingTo == 2) or
              (row_movingTo == 2 and col_movingTo == 3) or
              (row_movingTo == 3 and col_movingTo == 1) or
              (row_movingTo == 3 and col_movingTo == 2) or
              (row_movingTo == 3 and col_movingTo == 3)):
            if ((row_build == row_movingTo - 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo + 1)):
                return True
        elif ((row_movingTo == 4 and col_movingTo == 1) or
              (row_movingTo == 4 and col_movingTo == 2) or
              (row_movingTo == 4 and col_movingTo == 3)):
            if ((row_build == row_movingTo and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo + 1) or
                    (row_build == row_movingTo and col_build == col_movingTo + 1)):
                return True
        elif ((row_movingTo == 4 and col_movingTo == 0)):
            if ((row_build == row_movingTo and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo)):
                return True
        elif ((row_movingTo == 1 and col_movingTo == 4) or
              (row_movingTo == 2 and col_movingTo == 4) or
              (row_movingTo == 3 and col_movingTo == 4)):
            if ((row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo + 1 and col_build == col_movingTo)):
                return True
        elif ((row_movingTo == 4 and col_movingTo == 4)):
            if ((row_build == row_movingTo - 1 and col_build == col_movingTo - 1) or
                    (row_build == row_movingTo - 1 and col_build == col_movingTo) or
                    (row_build == row_movingTo and col_build == col_movingTo - 1)):
                return True
        return False
