from abstract_heuristic import *

class heuristicB():
    __node = None
    __chess_table = 0
    __sum_point = 0
    point_board = [
        [10, 1, 3, 2, 2, 3, 1, 10],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [3, 2, 4, 2, 2, 4, 2, 3],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [3, 2, 4, 2, 2, 4, 2, 3],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [10, 1, 3, 2, 2, 3, 1, 10]
    ]

    def __init__(self, node):
        __node = node

    def get_checking_path_value(self, node, start_x, start_y, end_x, end_y, roc, player):
        flag = True
        beside = True
        point = 1;
        if start_x < 0 or start_x >= 8 or start_y < 0 or start_y >= 8:
            return 0
        if roc:
            if start_x == end_x:
                j = start_y
                if end_y == 0:
                    while True:
                        if node.get_at(start_x,j) == 0:
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
                    break
                if (i - 1 < 0 or i + 1 >= 8) or (j - 1 < 0 or j + 1 >= 8) or node.get_at(i,j) == player:
                    flag = False
                    break
                point += 1
                i += x
                j += y
                beside = False

        if flag == True and beside == False:
            return point
        else:
            return 0

    def count_value_of_chess_table(self):
        #return sum value of squares that has no
        return 0;

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

    def get_number_of_safe(self, node, player):
        """
        :return: get the number of safe chessman that's guaranteed not be able to be eaten from the current time to end
        """
        safe_man = 0 #return safe_man
        #start checking at position [0,0]
        x_start = 0
        y_start = 0

        while True: #check on each of line of board (start at row = 0)
            columns_safe = [True, True, True, True, True, True, True, True]
            for i in xrange(8):
                return  0


        return 0

    def __is_Safe(self, node, i , j):
        return False

    def get_value_of_men(self, node, player):
        """Evaluate value of a chessman based on number of opponent's chessman around him [0-8]"""

        point_sum = 0

        for i in xrange(8):
            for j in xrange(8):
                if node.get_at(i,j) == player:
                    #get value of strength
                    point = self.get_point_of_a_chessman(node, i,j, player)
                    #check if it safe to the end. If it is add ... to point2
                    #isSafe = self.__is_Safe(node, i, j)
                    #if isSafe:
                        #point += 0
                    # Add point into point_sum
                    point_sum += point
        return point_sum