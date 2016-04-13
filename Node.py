from copy import copy, deepcopy


class Node(object):
    """ This is class declare a state of game Reversi """

    __player1 = 0
    __player2 = 0
    __is_player1_turn = True

    def __init__(self, board, parent=None):
        """ Constructor for node class """
        self.board = deepcopy(board)
        self.parent = parent

    def __eq__(self, other):
        """ Implement fast compare two state is equal or not """
        return self.board == other.board

    def __hash__(self):
        """ Hash function """
        hash = [0] * 8
        hashcode = 0
        for i in range(7):
            current = 0
            for j in range(7):
                current |= self.board[i][j] << 4 * j
            hash[i] = current
            hashcode |= hash[i] << 4 * i

        return hashcode

    def __str__(self):
        tostring = "\n".join([str(i) for i in self.board])
        return tostring

    def is_valid_move(self, player, x, y):
        """
        Check if given move is valid or not
        :param player: move of @player
        :param x: x-position of given move
        :param y: y-position of given move
        :return: True if (x, y) is a valid move
        """

        def check_direction(x, y, i, j):
            """
            Iterating along direction defined by (i, j)
            :param x: x-position of given move
            :param y: y-position of given move
            :param i: increase x by i
            :param j: increase y by j
            :return: True if (x, y) is a valid move
            """

            x += i
            y += j
            if x in range(8) and y in range(8) and self.board[x][y] and self.board[x][y] != player:
                x += i
                y += j
                while x in range(8) and y in range(8):
                    if self.board[(x)][y] == 0:
                        break
                    elif self.board[x][y] != player:
                        x += i
                        y += j
                    else:
                        return True
            return False

        # Check over 8 direction by change (i, j) value
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (i or j) and check_direction(x, y, i, j):
                    return True
        return False

    def get_move(self, player, x, y):
        """
        Get the Node state if given move is valid
        :param player: move of @player
        :param x: x-position of given move
        :param y: y-position of given move
        :return: Node if given move is valid, False if move is invalid
        """

        def check_direction(x, y, i, j):
            """
            Iterating along direction defined by (i, j)
            :param x: x-position of given move
            :param y: y-position of given move
            :param i: increase x by i
            :param j: increase y by j
            :return: True if (x, y) is a valid move
            """
            x_orig = x
            y_orig = y
            x += i
            y += j
            if x in range(8) and y in range(8) and self.board[x][y] and self.board[x][y] != player:
                x += i
                y += j
                while x in range(8) and y in range(8):
                    if self.board[(x)][y] == 0:
                        break
                    elif self.board[x][y] != player:
                        x += i
                        y += j
                    else:
                        board = deepcopy(self.board)
                        board[x_orig][y_orig] = player
                        while x != x_orig or y != y_orig:
                            board[x][y] = player
                            x -= i
                            y -= j
                        return Node(board, self)
            return False

        # Check over 8 direction by change (i, j) value
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i or j:
                    result = check_direction(x, y, i, j)
                    if result:
                        return result
        return False

    def get_all_valid_moves(self, player):
        """
        Get all valid moves of player
        :param player: ID of player
        :return: a list of Node contains all valid moves
        """
        move_lists = []
        for i in range(8):
            for j in range(8):
                result = self.get_move(player, i, j)
                if self.board[i][j] == 0 and result:
                    move_lists.append(result)
        return move_lists

    def get_number_valid_moves(self):
        # No need, use length of list returned by get_all_valid_moves func
        pass

    def get_score(self, player):
        """
        :param player: ID of player
        :return: score of player
        """
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player:
                    score += 1
        return score

    def get_turn(self):
        if self.__is_player1_turn:
            return 1
        else:
            return 2

    @staticmethod
    def create():
        """Create begin board value
        """
        board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        init_node = Node(board)

        return init_node
