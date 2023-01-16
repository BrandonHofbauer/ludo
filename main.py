# Description: Program that emulates a game of Ludo. Divided into a player class that contains information on player
#               state, token position, and starting position, and a Game class that handles the logic of initializing
#               the game and moving the tokens based on a priority of movement.

class Player:
    """Player object class. Stores information regarding a chosen position, and a players two tokens when playing
    Ludo. Contains methods for calculating where a given token is, and what space on the board a token occupies."""

    def __init__(self, pos):
        self._pos = pos
        if self._pos == 'A':
            self._start = 1
            self._end = 50
        elif self._pos == 'B':
            self._start = 15
            self._end = 8
        elif self._pos == 'C':
            self._start = 29
            self._end = 22
        elif self._pos == 'D':
            self._start = 43
            self._end = 36
        self._current_pos_p = 'H'
        self._current_pos_q = 'H'
        self._stacked = False
        self._state = 'Playing'

    def get_pos(self):
        """Returns the starting position selected by the player."""
        return self._pos

    def get_current_pos_p(self):
        """Returns the current board position of token p. Can be an int or str."""
        return self._current_pos_p

    def get_current_pos_q(self):
        """Returns the current board position of token q."""
        return self._current_pos_q

    def set_current_pos_p(self, pos):
        """Sets a new position for token p. Can be an int or str"""
        self._current_pos_p = pos

    def set_current_pos_q(self, pos):
        """Sets a new position for token p"""
        self._current_pos_q = pos

    def get_stacked(self):
        """Returns a boolean state representing if a player has stacked token or not."""
        return self._stacked

    def set_stacked(self, boolean):
        """Sets the stacked status"""
        self._stacked = boolean

    def set_completed(self, string):
        """Sets the player status as a string. Default is 'Playing', 'Finished' if they have completed the game."""
        self._state = string

    def get_completed(self):
        """Returns True if a player has finished the game (ie both tokens have a step of 57), and False otherwise."""
        if self._state == 'Finished':
            return True
        else:
            return False

    def get_token_step(self, token):
        """Calculates the total steps taken by the passed token, not by a counter but by its current position
        relative to its start and end point."""
        if token == 'H':
            return -1
        elif token == 'R':
            return 0
        elif token == 'E':
            return 57
        elif isinstance(token, str):
            value = token[1:]
            return 50 + int(value)
        elif token >= self._start:
            return token - self._start + 1
        elif token < self._start:
            difference = 56 - self._start
            return difference + token + 1
        else:
            return False

    def get_token_p_step_count(self):
        """Passes the current position of p to the token step method"""
        return self.get_token_step(self._current_pos_p)

    def get_token_q_step_count(self):
        """Passes the current position of q to the token step method"""
        return self.get_token_step(self._current_pos_q)

    def get_space_name(self, total_steps):
        """This method returns a string that is the name of the current position the token is at. Takes one parameter,
        an integer value that describes its total steps."""
        if total_steps == -1:
            return 'H'
        elif total_steps == 0:
            return 'R'
        elif total_steps == 57:
            return 'E'
        elif total_steps > 50:
            return self._pos + str(total_steps)[1:]
        else:
            space = total_steps + (self._start - 1)
            if space > 56:
                trim = space - 56
                space = trim
            return str(space)


class LudoGame:
    """Represents the game as played. Contains a dictionary of players, with methods to return a player object, move
    tokens on the board (conceptualized, there is currently no implementation for a visual board), and initializing
    the game."""

    def __init__(self):
        self._players = {}

    def get_player_by_position(self, player_pos):
        """Accepts a parameter representing the player's position as a string, and returns the player object."""
        for player in self._players:
            if player == player_pos:
                return self._players[player]
        else:
            return "Player not found!"

    def move_token(self, player_obj, token, steps):
        """Takes the player OBJECT, token name ('p', or 'q'), and steps for the token to take (int). Takes care of
        the movement of a single token, updating the tokens steps / position, kicking opponent tokens, and setting
        the 'stacked' state. Movement algorithm takes into account a total step of the token vs its actual position,
        and looping around the board."""
        # Sets appropriate token states based on which token was passed for movement
        if token == 'p':
            token_current = player_obj.get_current_pos_p
            token_set = player_obj.set_current_pos_p  # needs parameter
            token_step = player_obj.get_token_p_step_count
        elif token == 'q':
            token_current = player_obj.get_current_pos_q
            token_set = player_obj.set_current_pos_q
            token_step = player_obj.get_token_q_step_count
        else:
            return

        # Handles the movement of a token based on 5 situations
        if token_current() == 'E':  # situation 0: the token is finished
            return
        elif steps == 6 and token_current() == 'H':             # situation 1: token is at home with a 6 roll
            token_set('R')
        elif token_current() == 'R':                            # situation 2: is ready to go
            token_set(int(player_obj.get_space_name(steps)))
        elif isinstance(token_current(), str):                  # situation 3: is in home squares
            home_pos = int(token_current()[1:]) + steps
            if home_pos == 7:
                token_set('E')
            elif home_pos > 7:
                rebound = home_pos - 7
                new = 7 - rebound
                token_set(player_obj.get_space_name(50 + new))
            else:
                token_set(player_obj.get_space_name(50 + home_pos))
        elif (token_step() + steps) > 50:                       # situation 4: could enter home squares
            token_set(player_obj.get_space_name(token_step() + steps))
        else:                                                   # situation 5: on board, moving on board
            if token_current() + steps > 56:
                space = 56 - token_current()
                offset = steps - space
                token_set(offset)
            else:
                token_set(int(token_current()) + steps)

        # checks for tokens of opponents at the new current position to kick, and kicks. Removes THEIR stacked status
        for key in self._players:
            if key != player_obj.get_pos():
                if token_current() == self._players[key].get_current_pos_p() and token_current() != 'R':
                    self._players[key].set_current_pos_p('H')
                    self._players[key].set_stacked(False)
                if token_current() == self._players[key].get_current_pos_q() and token_current() != 'R':
                    self._players[key].set_current_pos_q('H')

        # sets stack if applicable
        if player_obj.get_current_pos_p() == player_obj.get_current_pos_q():
            if 0 < player_obj.get_token_p_step_count() < 57:
                player_obj.set_stacked(True)

    def play_game(self, player_list, turns_list):
        """Takes a list of player positions and a list of turns taken. Initializes player objects, and parses
        through the turns list which is a list of tuples, where each tuple represents a player and their roll. This
        method is in charge of priority ruling for movement, updating a tokens position when stacked and player state.
        Returns a list of strings representing the current space of all tokens for each player."""
        for player in player_list:
            self._players[player] = Player(player)

        for turn in turns_list:
            player = self.get_player_by_position(turn[0])

            if player.get_completed():
                continue

            # Priority 1: roll is a 6 with tokens in the home space
            if player.get_token_p_step_count() == -1 and player.get_token_q_step_count() == -1 and turn[1] == 6:
                self.move_token(player, 'p', turn[1])
            elif player.get_token_p_step_count() == -1 and turn[1] == 6:
                self.move_token(player, 'p', turn[1])
            elif player.get_token_q_step_count() == -1 and turn[1] == 6:
                self.move_token(player, 'q', turn[1])

            # Priority 2: a token could finish the game
            elif player.get_token_p_step_count() > 50 and player.get_token_p_step_count() + turn[1] == 57:
                self.move_token(player, 'p', turn[1])
            elif player.get_token_q_step_count() > 50 and player.get_token_q_step_count() + turn[1] == 57:
                self.move_token(player, 'q', turn[1])

            # Priority 3: kicking another token. if both can kick, move the furthest token
            elif -1 < player.get_token_p_step_count() < 57 and -1 < player.get_token_q_step_count() < 57:
                player_p_trounce = False
                player_q_trounce = False
                for key in self._players:
                    if key != player.get_pos():
                        if (player.get_token_p_step_count() + turn[1]) < 51:
                            if (int(player.get_space_name(player.get_token_p_step_count() + turn[1]))) == self._players[
                                key].get_current_pos_p() or (
                            int(player.get_space_name(player.get_token_p_step_count() + turn[1]))) == self._players[
                                key].get_current_pos_q():
                                player_p_trounce = True
                        if (player.get_token_q_step_count() + turn[1]) < 51:
                            if (int(player.get_space_name(player.get_token_q_step_count() + turn[1]))) == self._players[
                                key].get_current_pos_p() or (
                            int(player.get_space_name(player.get_token_q_step_count() + turn[1]))) == self._players[
                                key].get_current_pos_q():
                                player_q_trounce = True
                if player_p_trounce and player_q_trounce:
                    if player.get_token_p_step_count() < player.get_token_q_step_count():
                        self.move_token(player, 'p', turn[1])
                    else:
                        self.move_token(player, 'q', turn[1])
                elif player_p_trounce:
                    self.move_token(player, 'p', turn[1])
                elif player_q_trounce:
                    self.move_token(player, 'q', turn[1])

                # Priority 4: move the furthest token from finishing
                elif player.get_token_p_step_count() < player.get_token_q_step_count():
                    self.move_token(player, 'p', turn[1])
                elif player.get_token_q_step_count() < player.get_token_p_step_count():
                    self.move_token(player, 'q', turn[1])
                elif player.get_token_p_step_count() == player.get_token_q_step_count():
                    if player.get_token_p_step_count() != -1:
                        self.move_token(player, 'p', turn[1])

            # No Priority: Only a single token can move
            else:
                if -1 < player.get_token_p_step_count() < 57:
                    self.move_token(player, 'p', turn[1])
                elif -1 < player.get_token_q_step_count() < 57:
                    self.move_token(player, 'q', turn[1])

            # check stacked, move other token if applicable
            if player.get_stacked():
                player.set_current_pos_q(player.get_current_pos_p())

            # Has the player won?
            if player.get_token_p_step_count() == 57 and player.get_token_q_step_count() == 57:
                player.set_completed('Finished')

        final_pos = []
        for player in self._players:  # add get method for current later
            final_pos.append(str(self._players[player].get_current_pos_p()))
            final_pos.append(str(self._players[player].get_current_pos_q()))

        return final_pos
