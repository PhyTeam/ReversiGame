from abstract_heuristic import *
from node_advance import popcount

class heuristic(AbstractHeuristic):

    def isSafe(self, node, x, y):
        """
        :param:     x,y : position in node board
        :return: False if player at x,y is can be eaten by opponent
                 True if not
        """
        player = node.board[x][y]
        opponent = - player
        # empty position
        if player == 0:
            return True
        # in corner
        if x == 0 and y == 0:
            return True
        if x == 0 and y == 7:
            return True
        if x == 7 and y == 0:
            return True
        if x == 7 and y == 7:
            return True

        # check row
        b_safe = False
        is_opp_in_left = False
        # check left
        for i in range(x - 1, 0, -1):
            if node.board[i][y] != player:
                if node.board[i][y] == opponent: is_opp_in_left = True
                break
            if (i == 0): b_safe = True
        if not b_safe:
            for i in range(x + 1, 7, 1):
                if node.board[i][y] != player:
                    if node.board[i][y] == opponent:
                        if not is_opp_in_left: return False # opponent can eat this if choose in the left
                    if node.board[i][y] == 0:
                        if is_opp_in_left: return False # opponent can eat this if choose in the right
                    break
        # check column
        b_safe = False
        is_opp_in_top = False
        for i in range(y - 1, 0, -1):
            if node.board[x][i] != player:
                if node.board[x][i] == opponent: is_opp_in_top = True
                break
            if i == 0: b_safe = True
        if not b_safe:
            for i in range(y + 1, 7, 1):
                if node.board[x][i] != player:
                    if node.board[x][i] == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left
                    if node.board[x][i] == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right
                    break
        # check the cross left top 2 right down
        la = 0
        ra = 0
        if x < y:
            la = x
            ra = 7 - y
        else:
            la = y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.board[x - i][y - i] != player:
                if node.board[x - i][y - i] == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.board[x + i][y + i] != player:
                    if node.board[x + i][y + i] == opponent:
                        if not is_opp_in_top:
                            return False  # opponent can eat this if choose in the left up
                    if node.board[x + i][y + i] == 0:
                        if is_opp_in_top:
                            return False  # opponent can eat this if choose in the right down
                    break
        # check the cross right top 2 left down
        if x < 7 - y:
            la = x
            ra = y
        else:
            la = 7 - y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.board[x - i][y + i] != player:
                if node.board[x - i][y + i] == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.board[x + i][y - i] != player:
                    if node.board[x + i][y - i] == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left down
                    if node.board[x + i][y - i] == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right up
                    break
        return True

    def eval_early_game(self, node):
        """ return the score of a node in early game"""
        point_board = [[10, 1, 3, 2, 2, 3, 1, 10],
                       [ 1, 1, 2, 2, 2, 2, 1, 1],
                       [ 3, 2, 4, 2, 2, 4, 2, 3],
                       [ 2, 2, 2, 2, 2, 2, 2, 2],
                       [ 2, 2, 2, 2, 2, 2, 2, 2],
                       [ 3, 2, 4, 2, 2, 4, 2, 3],
                       [ 1, 1, 2, 2, 2, 2, 1, 1],
                       [10, 1, 3, 2, 2, 3, 1, 10]]
        res = 0
        for i in range(8):
            for j in range(8):
                res += point_board[i][j]*node.board[i][j]
        return res

    def eval_mid_game(self, node):
        """ return the score of a node in mid game"""
        my_safe = 0
        my_not_safe = 0
        opp_safe = 0
        opp_not_safe = 0
        player = Node.PLAYER_1
        #opponent = Node.PLAYER_2
        # calculate the num of safe-chess, not safe-chess of mine and opponent's
        for i in range(8):
            for j in range(8):
                if node.board[i][j] != 0:
                    if self.isSafe(node, i, j):
                        if node.board[i][j] == player:
                            my_safe += 1  # = my_safe + 1
                        else:
                            opp_safe += 1  # = opp_safe + 1
                    else:
                        if node.board[i][j] == player:
                            my_not_safe += 1  # = my_not_safe + 1
                        else:
                            opp_not_safe += 1  # = opp_not_safe + 1
        res = 2*my_safe + my_not_safe - 2*opp_safe - opp_not_safe
        return res

    def eval_late_game(self, node):
        """ return the score of a node in late game
        We: Player_1
        Opp: Player-2
        """
        return node.get_score(node.PLAYER_1) - node.get_score(node.PLAYER_2)

    def eval(self, node):
        n = node.get_score(node.PLAYER_1) + node.get_score(node.PLAYER_2)
        if n < 30:
            return self.eval_early_game(node)
        elif n < 60:
            return self.eval_mid_game(node)
        else:
            return self.eval_late_game(node)


h10 = 0x8100000000000081
h1 = 0x4263000000006341
h3 = 0x2400810000810024
h4 = 0x0000240000240000
h2 = h10 | h1 | h3 | h4
h2 = ~ h2

class HeuristicAdvance(AbstractHeuristic):
    def is_safe(self, node, x, y):
        """"""

        player = node.get_at(x, y)
        opponent = - player
        # empty position
        if player == 0:
            return True
        if x == 0 and y == 0:
        # in corner
            return True
        if x == 0 and y == 7:
            return True
        if x == 7 and y == 0:
            return True
        if x == 7 and y == 7:
            return True

        # check row
        b_safe = False
        is_opp_in_left = False
        # check left
        for i in range(x - 1, 0, -1):
            if node.get_at(x, y) != player:
                if node.get_at(x, y) == opponent: is_opp_in_left = True
                break
            if (i == 0): b_safe = True
        if not b_safe:
            for i in range(x + 1, 7, 1):
                if node.get_at(x, y) != player:
                    if node.get_at(x, y) == opponent:
                        if not is_opp_in_left: return False  # opponent can eat this if choose in the left
                    if node.get_at(x, y) == 0:
                        if is_opp_in_left: return False  # opponent can eat this if choose in the right
                    break
        # check column
        b_safe = False
        is_opp_in_top = False
        for i in range(y - 1, 0, -1):
            if node.get_at(x, y) != player:
                if node.get_at(x, y) == opponent: is_opp_in_top = True
                break
            if i == 0: b_safe = True
        if not b_safe:
            for i in range(y + 1, 7, 1):
                if node.get_at(x, y) != player:
                    if node.get_at(x, y) == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left
                    if node.get_at(x, y) == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right
                    break
        # check the cross left top 2 right down
        la = 0
        ra = 0
        if x < y:
            la = x
            ra = 7 - y
        else:
            la = y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.get_at(x - i, y - i) != player:
                if node.get_at(x - i, y - i) == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.get_at(x + i, y + i) != player:
                    if node.get_at(x + i, y + i) == opponent:
                        if not is_opp_in_top:
                            return False  # opponent can eat this if choose in the left up
                    if node.get_at(x + i, y + i) == 0:
                        if is_opp_in_top:
                            return False  # opponent can eat this if choose in the right down
                    break
        # check the cross right top 2 left down
        if x < 7 - y:
            la = x
            ra = y
        else:
            la = 7 - y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.get_at(x - i, y + i) != player:
                if node.get_at(x - i, y + i) == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.get_at(x + i, y - i) != player:
                    if node.get_at(x + i, y - i) == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left down
                    if node.get_at(x + i, y - i) == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right up
                    break
        return True

    def eval_early_game(self, node):
        """"""
        """point_board = [[10, 1, 3, 2, 2, 3, 1, 10],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [3, 2, 4, 2, 2, 4, 2, 3],
                       [2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2],
                       [3, 2, 4, 2, 2, 4, 2, 3],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [10, 1, 3, 2, 2, 3, 1, 10]] """

        res = 0
        p10 = popcount(h10 & node.bitboard[1])
        p1 = popcount(h1 & node.bitboard[1])
        p2 = popcount(h2 & node.bitboard[1])
        p3 = popcount(h3 & node.bitboard[1])
        p4 = popcount(h4 & node.bitboard[1])

        o10 = popcount(h10 & node.bitboard[-1])
        o1 = popcount(h1 & node.bitboard[-1])
        o2 = popcount(h2 & node.bitboard[-1])
        o3 = popcount(h3 & node.bitboard[-1])
        o4 = popcount(h4 & node.bitboard[-1])

        res = 10*(p10 - o10) + (p1 - o1) + 2*(p2 - o2) + 3*(p3 - o3) + 4*(p4 - o4)
        """for i in range(8):
            for j in range(8):
                res += point_board[i][j] * node.get_at(i,j)"""
        return res

    def eval_mid_game(self, node):
        """"""
        my_safe = 0
        my_not_safe = 0
        opp_safe = 0
        opp_not_safe = 0
        player = Node.PLAYER_1
        # opponent = Node.PLAYER_2
        # calculate the num of safe-chess, not safe-chess of mine and opponent's
        for i in range(8):
            for j in range(8):
                if node.get_at(i, j) != 0:
                    if self.is_safe(node, i, j):
                        if node.get_at(i, j) == player:
                            my_safe += 2  # = my_safe + 1
                        else:
                            opp_safe += 2  # = opp_safe + 1
                    else:
                        if node.get_at(i, j) == player:
                            my_not_safe += 1  # = my_not_safe + 1
                        else:
                            opp_not_safe += 1  # = opp_not_safe + 1
        res = my_safe + my_not_safe - opp_safe - opp_not_safe
        return res

    def eval_late_game(self, node):
        """"""
        return node.get_score(1) - node.get_score(-1)

    def eval(self, node):
        """"""
        n = node.get_score(1) + node.get_score(-1)
        if n < 30:
            return self.eval_early_game(node)
        elif n < 60:
            return self.eval_mid_game(node)
        else:
            return self.eval_late_game(node)