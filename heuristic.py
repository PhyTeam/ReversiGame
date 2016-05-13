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


def packA1A8(X):
    return ((((X) & 0x0101010101010101) * 0x0102040810204080) >> 56)


def packH1H8(X):
    return ((((X) & 0x8080808080808080) * 0x0002040810204081) >> 56)

class HeuristicAdvance(AbstractHeuristic):
    score_lookup_table = []

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

    def precompute(self):
        point_board = \
            [[10, 1, 3, 2, 2, 3, 1, 10],
             [1, 1, 2, 2, 2, 2, 1, 1],
             [3, 2, 4, 2, 2, 4, 2, 3],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [3, 2, 4, 2, 2, 4, 2, 3],
             [1, 1, 2, 2, 2, 2, 1, 1],
             [10, 1, 3, 2, 2, 3, 1, 10]]
        precompute_table_lookup = []
        for row in xrange(4):
            table = {}
            for i in xrange(2 ** 8):
                value = 0
                for j in xrange(8):
                    value += ((i >> j) & 1) * point_board[0][j]
                table[i] = value
            precompute_table_lookup[row] = table

        return precompute_table_lookup

    def score_table_heuristic(self, node):
        player = node.bitboard[1]
        opponent = node.bitboard[-1]
        score = 0
        for row in xrange(8):
            score += self.score_lookup_table[row % 4][(player >> 8) & 0xFF]
        return score

    def eval_early_game(self, node):
        """Fast implement """
        return self.score_table_heuristic(node)

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

X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
v20 = 0x8100000000000081
v_3 = 0x4281001818008142
v11 = 0x2400810000810024
v8 = 0x1800008181000018
v_7 = 0x0042000000004200
v_4 = 0x0024420000422400
v1 = 0x0018004242001800
v2 = 0x00003C24243C0000


class HeuristicNam(AbstractHeuristic):
    def eval(self, node):
        """"""
        p20 = popcount(v20 & node.bitboard[1])
        p_3 = popcount(v_3 & node.bitboard[1])
        p11 = popcount(v11 & node.bitboard[1])
        p8 = popcount(v8 & node.bitboard[1])
        p_7 = popcount(v_7 & node.bitboard[1])
        p_4 = popcount(v_4 & node.bitboard[1])
        p1 = popcount(v1 & node.bitboard[1])
        p2 = popcount(v2 & node.bitboard[1])

        o20 = popcount(v20 & node.bitboard[-1])
        o_3 = popcount(v_3 & node.bitboard[-1])
        o11 = popcount(v11 & node.bitboard[-1])
        o8 = popcount(v8 & node.bitboard[-1])
        o_7 = popcount(v_7 & node.bitboard[-1])
        o_4 = popcount(v_4 & node.bitboard[-1])
        o1 = popcount(v1 & node.bitboard[-1])
        o2 = popcount(v2 & node.bitboard[-1])
        
        d = 20*(p20 - o20) - 3*(p_3 - o_3) + 11*(p11 - o11) + 8*(p8 - o8) -7*(p_7 - o_7) -4*(p_4 - o_4) + p1 - o1 + 2*(p2 - o2)

        my_f_tiles = 0
        opp_f_tiles = 0

        for i in xrange(8):
            for j in xrange(8):
                if node.get_at(i, j) != 0:
                    for k in xrange(8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if (x >= 0) and (x < 8) and (y >= 0) and (y < 8) and node.get_at(x, y) == 0:
                            if node.get_at(i, j) == 1:
                                my_f_tiles += 1
                            else:
                                opp_f_tiles += 1
                            break
        my_tiles = node.get_score(1)
        opp_tiles = node.get_score(-1)

        p = 0

        if my_tiles > opp_tiles:
            p = my_tiles/(my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -opp_tiles / (my_tiles + opp_tiles)

        f = 0

        if my_f_tiles > opp_f_tiles:
            f = -my_f_tiles/(my_f_tiles + opp_f_tiles)
        elif my_f_tiles < opp_f_tiles:
            f = opp_f_tiles/(my_f_tiles + opp_f_tiles)

        # Corner occupancy
        c = 0
        c += node.get_at(0, 0) + node.get_at(0, 7) + node.get_at(7, 0) + node.get_at(7, 7)

        # Corner closeness
        l = 0
        le_up = 0x40C0000000000000
        ri_up = 0x0203000000000000
        le_do = 0x000000000000C040
        ri_do = 0x0000000000000302
        if node.get_at(0, 0) == 0:
            l += popcount(node.bitboard[1] & le_up) - popcount(node.bitboard[-1] & le_up)
        if node.get_at(0, 7) == 0:
            l += popcount(node.bitboard[1] & ri_up) - popcount(node.bitboard[-1] & ri_up)
        if node.get_at(7, 0) == 0:
            l += popcount(node.bitboard[1] & le_do) - popcount(node.bitboard[-1] & le_do)
        if node.get_at(7, 7) == 0:
            l += popcount(node.bitboard[1] & ri_do) - popcount(node.bitboard[-1] & ri_do)

        # Mobility
        my_mo = node.get_mobility(1) 
        opp_mo = node.get_mobility(-1)
        m = 0
        if my_mo > opp_mo:
            m = my_mo / (my_mo + opp_mo)
        elif my_mo < opp_mo:
            m = -opp_mo / (my_mo + opp_mo)
        

        # final weight

        score = (1000 * p) + (20043.1 * c) - 4775.325 * l + (7892.2 * m) + (7439.6 * f) + (10 * d)
        return score
