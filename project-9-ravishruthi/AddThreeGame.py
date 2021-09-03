# Author: Shruthi Ravi
# Date: 11/25/2020
# Description: This program defines a class AddThreeGame, which has 4 private data members
#              (first player, second player, current status, turn), 1 get method, to return
#              the current status, and a method, make_move, that records the current player's
#              move and updates the status of the game. If at any point 3 of the current player's
#              numbers add up to 15, the current status changes and that player wins the game.
#

class AddThreeGame:
    """
        Represents an AddThreeGame that has a first player, second player,
        current status and turn. It has a get method to get the current status
        of the game. A method, make_move, takes two parameters, a string indicating
        which player is making the move and the player's number choice, and will
        record the move of the player and update the current status of the game.
    """
    def __init__(self):
        """ Creates a new AddThreeGame game. """
        self._first_player = []
        self._second_player = []
        self._current_state = "UNFINISHED"
        self._turn = "first"

    def get_current_state(self):
        """ Returns the current state. """
        return self._current_state

    def make_move(self, player, int_choice):
        """
            Records the current player's move, updates the current state, and returns True.
            If it's not the player's turn, or if integer is not between 1-9 (or has already
            been chosen), or if the game has ended, it returns False.
        """
        if ((self._turn != player) or
                ((int_choice < 1) or (int_choice > 9)) or
                ((int_choice in self._first_player) or (int_choice in self._second_player)) or
                (self._current_state != "UNFINISHED")):
            return False
        else:
            if (self._turn == "first"):  # If player one, append chosen number and update current state
                self._first_player.append(int_choice)
                if (len(self._first_player) >= 3):  # Checks all possible combos of 3 within player one's list of numbers
                    lists = self._combos_of_three(self._first_player)
                    for sublist in lists:  # Loop through the list of combos
                        sum = 0
                        for num in sublist:  # Loop through a subset (list of 3 nums, within the list)
                            sum += num
                        if (sum == 15):  # If combo of 3 adds up to 15, change current status accordingly
                            self._current_state = "FIRST_WON"
                            return True
                self._turn = "second"  # Else, it is player two's turn
            else:  # If player two, append chosen number and update current state
                self._second_player.append(int_choice)
                if (len(self._second_player) >= 3):  # Checks all possible combos of 3 within player two's list of numbers
                    lists = self._combos_of_three(self._second_player)
                    for sublist in lists:  # Loop through the list of combos
                        sum = 0
                        for num in sublist:  # Loop through a subset (list of 3 nums, within the list)
                            sum += num
                        if (sum == 15):  # If combo of 3 adds up to 15, change current status accordingly
                            self._current_state = "SECOND_WON"
                            return True
                self._turn = "first"  # Else, it is player one's turn
        return True

    def _combos_of_three(self, player_lst):
        """
            Computes the possible various combos, of size 3, based on the number
            of elements in player_lst. It appends these various subsets to a list
            and returns the list.
        """
        lst_of_subsets = []
        for i in range(0, len(player_lst)):
            for j in range(i + 1, len(player_lst)):
                for k in range(j + 1, len(player_lst)):
                    subset = [player_lst[i]] + [player_lst[j]] + [player_lst[k]]
                    lst_of_subsets.append(subset)
        return lst_of_subsets
