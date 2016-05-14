from abstract_heuristic import *

class heuristicB():
    __node = None
    __chess_table = 0
    __sum_point = 0
    point_board = [
        [24, -16, 8, 8, 8, 8, -16, 24],
        [-16, -16, 4, 4, 4, 4, -16, -16],
        [8, 4, 4, 8, 8, 4, 4, 8],
        [8, 4, 8, 8, 8, 8, 4, 8],
        [8, 4, 2, 8, 8, 8, 4, 8],
        [8, 4, 4, 8, 8, 4, 4, 8],
        [-16, -16, 4, 4, 4, 4, -16, -16],
        [24, -16, 8, 8, 8, 8, -16, 24]
    ]

    def __init__(self, node):
        __node = node

    def get_checking_path_value(self, node, start_x, start_y, end_x, end_y, roc, player):
        flag = True
        beside = True
        point = 0;
        point_v2 = 0
        if start_x < 0 or start_x >= 8 or start_y < 0 or start_y >= 8:
            return 0
        if roc:
            if start_x == end_x:
                j = start_y
                if end_y == 0:
                    while True:
                        if node.get_at(start_x,j) == 0:
                            end_x = start_x
                            end_y = j
                            break
                        if j - 1 < 0 or node.get_at(start_x,j) == player:
                            flag = False
                            break
                        point += 1
                        j -= 1
                        beside = False
                elif end_y == 7:
                    while True:
                        if node.get_at(start_x,j) == 0:
                            end_x = start_x
                            end_y = j
                            break
                        if j + 1 >= 8 or node.get_at(start_x,j) == player:
                            flag = False
                            break
                        point += 1
                        j += 1
                        beside = False
            elif start_y == end_y:
                i = start_x
                if end_x == 0:
                    while True:
                        if node.get_at(i,start_y) == 0:
                            end_x = i
                            end_y = start_y
                            break
                        if i - 1 < 0 or node.get_at(i,start_y) == player:
                            flag = False
                            break
                        point += 1
                        i -= 1
                        beside = False
                elif end_x == 7:
                    while True:
                        if node.get_at(i,start_y) == 0:
                            end_x = i
                            end_y = start_y
                            break
                        if i + 1 >= 8 or node.get_at(i,start_y) == player:
                            flag = False
                            break
                        point += 1
                        i += 1
                        beside = False
        else:
            x = 0
            y = 0
            if end_x == 0 and end_y == 0:
                x = -1
                y = -1
            elif end_x == 7 and end_y == 0:
                x = 1
                y = -1
            elif end_x == 7 and end_y == 7:
                x = 1
                y = 1
            elif end_x == 0 and end_y == 7:
                x = -1
                y = 1
            else:
                return 0
            i = start_x
            j = start_y

            while True:
                if node.get_at(i,j) == 0:
                    end_x = i
                    end_y = j
                    break
                if (i - 1 < 0 or i + 1 >= 8) or (j - 1 < 0 or j + 1 >= 8) or node.get_at(i,j) == player:
                    flag = False
                    break
                point += 1
                i += x
                j += y
                beside = False

        if flag == True and beside == False:
            return self.point_board[end_x][end_y], point
        else:
            return 0,0

    def if_path_belong_to_player(self, node, player, path_id, curr_player):
        """
        :param node:
        :param player:
        :param path_id:
            == 0 : left
            == 1 : right
            == 2 : bottom
            == 3 : top
        :return:
        """

        #if path_id == 0:



        return 1

    def update_point_board(self, node, player):
        #return sum value of squares that has no
        for i in xrange(8):
            for j in xrange(8):
                if node.get_at(i,j) == player:
                    self.point_board[7-i][7-j] = 0
        return 0

    def get_point_of_a_chessman(self,node,i, j, player):
        point = 0
        # Check PLAYER_1's chessman
        # Check 8 path - left - right - bottom - top and 4 diagonals
        point += self.get_checking_path_value(node, i, j - 1, i, 0, True, player)
        point += self.get_checking_path_value(node, i, j + 1, i, 7, True, player)
        point += self.get_checking_path_value(node, i - 1, j, 0, j, True, player)
        point += self.get_checking_path_value(node, i + 1, j, 7, j, True, player)
        point += self.get_checking_path_value(node, i - 1, j - 1, 0, 0, False, player)
        point += self.get_checking_path_value(node, i - 1, j + 1, 0, 7, False, player)
        point += self.get_checking_path_value(node, i + 1, j + 1, 7, 7, False, player)
        point += self.get_checking_path_value(node, i + 1, j - 1, 7, 0, False, player)
        return point

    def get_number_of_safe_man(self, node, player):
        """
        :return: get the number of safe chessman that's guaranteed not be able to be eaten from the current time to end
        """
        safe_man = 0  # return safe_man
        # start checking at position [0,0]
        x_start = 0
        y_start = 0

        _arrived = [[0 for x in range(8)] for y in range(8)]
        for i in xrange(8):
            for j in xrange(8):
                _arrived[i][j] = False

        _row = 0
        _col = 0
        _max = 8
        if node.get_at(_row,_col) == player:
            while True:
                if _col < 8 and node.get_at(_row,_col) == player:
                    if _arrived[_row][_col] == False:
                        _arrived[_row][_col] = True
                        safe_man += 1
                    # Check on a column
                    while True:
                        _row += 1
                        if _row < _max and node.get_at(_row,_col) == player:
                            if _arrived[_row][_col] == False:
                                _arrived[_row][_col] = True
                                safe_man += 1
                        else:
                            _max = _row - 1
                            #print _max
                            break
                    _row = 0
                    _col += 1;
                else:
                    break
        else:
            flag = True
            count = [False, False, False, False, False, False, False, False]
            for i in xrange(8):
                if node.get_at(_row,i) == 0:
                    flag = False
                    break
                elif node.get_at(_row, i) == player:
                    count[i] = True
            if flag:
                for i in xrange(8):
                    if count[i] and _arrived[_row][i] == False:
                        _arrived[_row][i] = True
                        safe_man += 1


        _row = 7
        _col = 7
        _max = -1
        if node.get_at(_row, _col) == player:
            while True:
                if _col >= 0 and node.get_at(_row,_col)== player:
                    if _arrived[_row][_col] == False:
                        _arrived[_row][_col] = True
                        safe_man += 1
                    # Check on a column
                    while True:
                        _row -= 1
                        if _row > max and node.get_at(_row,_col)== player:
                            if _arrived[_row][_col] == False:
                                _arrived[_row][_col] = True
                                safe_man += 1
                        else:
                            _max = _row + 1
                            break
                    _row = 7
                    _col -= 1;
                else:
                    break
        else:
            flag = True
            count = [False, False, False, False, False, False, False, False]
            for i in xrange(8):
                if node.get_at(_row, 7 - i) == 0:
                    flag = False
                    break
                elif node.get_at(_row, 7 - i) == player:
                    count[i] = True
            if flag:
                for i in xrange(8):
                    if count[i] and _arrived[_row][7 - i] == False:
                        _arrived[_row][7 - i] = True
                        safe_man += 1

        _row = 0
        _col = 7
        _max = -1
        if node.get_at(_row, _col) == player:
            while True:
                if _row < 8 and node.get_at(_row,_col) == player:
                    if _arrived[_row][_col] == False:
                        _arrived[_row][_col] = True
                        safe_man += 1
                    # Check on a column
                    while True:
                        _col -= 1
                        if _col > _max and node.get_at(_row,_col)== player:
                            if _arrived[_row][_col] == False:
                                _arrived[_row][_col] = True
                                safe_man += 1
                        else:
                            _max = _col + 1
                            break
                    _row += 1
                    _col = 7;
                else:
                    break
        else:
            flag = True
            count = [False, False, False, False, False, False, False, False]
            for i in xrange(8):
                if node.get_at(i, _col) == 0:
                    flag = False
                    break
                elif node.get_at(i, _col) == player:
                    count[i] = True
            if flag:
                for i in xrange(8):
                    if count[i] and _arrived[i][_col] == False:
                        _arrived[i][_col] = True
                        safe_man += 1

        _row = 7
        _col = 0
        _max = 8
        if node.get_at(_row, _col) == player:
            while True:
                if _row >= 0 and node.get_at(_row,_col) == player:
                    if _arrived[_row][_col] == False:
                        _arrived[_row][_col] = True
                        safe_man += 1
                    # Check on a column
                    while True:
                        _col += 1
                        if _col < _max and node.get_at(_row,_col) == player:
                            if _arrived[_row][_col] == False:
                                _arrived[_row][_col] = True
                                safe_man += 1
                        else:
                            _max = _col - 1
                            # print _max
                            break
                    _row -= 1
                    _col = 0;
                else:
                    break
        else:
            flag = True
            count = [False, False, False, False, False, False, False, False]
            for i in xrange(8):
                if node.get_at(7 - i, _col) == 0:
                    flag = False
                    break
                elif node.get_at(7 - i, _col) == player:
                    count[i] = True
            if flag:
                for i in xrange(8):
                    if count[i] and _arrived[7 - i][_col] == False:
                        _arrived[7 - i][_col] = True
                        safe_man += 1

        return _arrived

    def __is_Safe(self, node, i , j):
        return False

    def get_value_of_men(self, node, player, reached):
        """Evaluate value of a chessman based on number of opponent's chessman around him [0-8]"""

        point_sum1 = 0
        point_sum2 = 0
        point_sum3 = 0
        #self.update_point_board(node, player)
        safe_man = self.get_number_of_safe_man(node, player)

        for i in xrange(8):
            for j in xrange(8):
                if node.get_at(i,j) == player:
                    #get value of strength
                    point1_1, point1_2 = self.get_point_of_a_chessman(node, i,j, player)
                    point1 = 0
                    if (reached < 20):
                        point1 = point1_1
                    else:
                        point1 = point1_2
                    point3 = self.point_board[i][j]
                    #if i == 0 or j == 0 or i == 7 or j == 7:
                        #point3 = 8
                    #check if it safe until the end. If it is add ... to point2
                    if safe_man[i][j] and point1 == 0:
                        if (i == 0 and j == 0) or (i == 0 and j == 7) or (i == 7 and j == 7) or (i == 7 and j == 0):
                            point2 = 48
                        else:
                            point2 = 32
                    else:
                        point2 = 0
                    # Add point into point_sum
                    point_sum1 += point1; point_sum2+= point2;  point_sum3+= point3
        return point_sum1 + point_sum2 + point_sum3


