from sys import maxint
import timeit
from time import clock

class AbstractSearcher:
    """ Lop truu tuong cu cac lop tim kiem"""
    _heuristic = None

    def __init__(self, heuristic):
        """Initialize seacher"""
        self._heuristic = heuristic

    def set_heuristic(self, h):
        self._heuristic = h

    def get_heuristic_value(self, node):
        """
        :param node: a node you want to get its static value
        :return: a real number value
        """
        return self._heuristic.eval(node)

    def search(self, node, depth, player):
        """Find a next best node in a list valid node
            :param: node current state of the game
            :return: next step if there a valid next move
                     Node if there no valid move
        """
        pass


class MinMaxSearcher(AbstractSearcher):
    def search(self, node, depth, player):
        """
        Implementation min-max algorithm
        :param node: Node
        :param depth: Depth of search
        :param player: Current player
        :return: a pair of best node and value
        """

        if depth <= 0:
            return self.get_heuristic_value(node), None

        # Get all node can be of current node
        valid_moves = node.get_all_valid_moves(player)
        lst = [i for i in valid_moves.values()]

        # Get max value of child node
        max, moving = -165, None
        for mov, new_node in valid_moves.iteritems():
            result = self.search(new_node, depth - 1, -player)
            value = player * result[0]  # Value of this node
            if value >= max:
                max, moving = value, mov
        # Get how to move return this node
        return max * player, moving


class AlphaBetaSearcher(AbstractSearcher):
    __node_visited = 0
    __time_estimate = 0
    __eval_count = 0

    def search(self, node, depth, player):
        # Reset all variable
        self.__eval_count = 0
        self.__node_visited = 0
        self.__time_estimate = 0
        # Swapper function
        result = self.__search(node, depth, -maxint, maxint, player)

        return result

    def __search(self, node, depth, alpha, beta, player):
        """Tim theo giai thuat  minmax"""

        self.__node_visited += 1
        if depth <= 0:
            self.__eval_count += 1
            val, parent = player * self.get_heuristic_value(node), None
            return val, parent

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) == 0:
            enemy_valid_moves = node.get_all_valid_moves(-player)
            if len(enemy_valid_moves) == 0:
                return player * self.get_heuristic_value(node), None
            else:
                result = self.__search(node, depth, -beta, -alpha, -player)
                return -result[0], result[1]

        best_value, best_move = -maxint, None

        for mov, new_node in valid_moves.iteritems():
            result = self.__search(new_node, depth - 1, -beta, -alpha, -player)
            value = - result[0]  # Value of this node
            if value > best_value:
                best_value, best_move = value, mov
            alpha = max (value, alpha)
            if alpha >= beta:
                break

        #print depth, best_value * player
        return best_value, best_move


class NegamaxSearcher(AbstractSearcher):
    def __init__(self, heuristic):
        AbstractSearcher.__init__(self, heuristic)
        self._transposition_table = {}

    def search(self, node, depth, player):
        self._transposition_table.clear()
        return self.__search(node, depth, -maxint, maxint, player)

    def __search(self, node, depth, alpha, beta, player):
        alpha_orig = alpha  # Save the original value of Alpha

        try:
            tt_entry = self._transposition_table[node]  # Looking entry in transposition table
        except KeyError:
            tt_entry = None

        if tt_entry is not None and tt_entry[0] >= depth:
            if tt_entry[1] is 0:    # Flag is EXTRACT
                return tt_entry[2], tt_entry[3]
            elif tt_entry[1] is 1:  # Flag is LOWER BOUND
                alpha = max(alpha, tt_entry[2])
            elif tt_entry[1] is 2:  # Flag is UPPER BOUND
                beta = min(beta, tt_entry[2])

        if alpha >= beta:
            return tt_entry[2], tt_entry[3]
        if depth <= 0:
            return self.get_heuristic_value(node), None

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) is 0:
            enemy_valid_moves = node.get_all_valid_moves(-player)
            if len(enemy_valid_moves) is 0:
                return self.get_heuristic_value(node), None
            else:
                result = self.__search(node, depth, -beta, -alpha, -player)
                return -result[0], result[1]

        best_value, best_move = -maxint, None
        for mov, new_node in valid_moves.iteritems():
            result = self.__search(new_node, depth - 1, -beta, -alpha, -player)
            value = -result[0]  # Value of this node
            if value > best_value:
                best_value, best_move = value, mov
            alpha = max(value, alpha)
            if alpha >= beta:
                break

        if best_value <= alpha_orig:    # Set Flag is UPPER BOUND
            flag = 2
        elif best_value >= alpha:       # Set Flag is LOWER Bound
            flag = 1
        else:                           # Set Flag is EXTRACT
            flag = 0

        # Insert entry (including depth, flag, value and move) to transposition table
        self._transposition_table[node] = (depth, flag, best_value, best_move)

        return best_value, best_move


class NegamaxWithDeepeningSearcher(AbstractSearcher):
    schedule = {0: 60 * 1.5, 1: 60 * 1.9, 2: 4, 3: 14, 4: None, 5: None}

    def __init__(self, heuristic):
        AbstractSearcher.__init__(self, heuristic)
        self._is_endgame = False

    def search(self, node, depth, player):
        num_empties_left = 64 - node.get_score(player) - node.get_score(-player)

        if num_empties_left <= self.schedule[3]:
            self._is_endgame = True

        search_depth = self.get_suggested_depth(self.schedule[0], self.schedule[1], self.schedule[3], self.schedule[2], node, player, self.schedule[4], self.schedule[5])

        # print "Previous search time:", self.schedule[4]
        # print "Previous depth counter:", self.schedule[5]

        # print "Next depth is:", search_depth

        depth_counter = self.get_new_depth_counters(search_depth)
        start_time = clock()
        result = self.__search(node, search_depth, -maxint, maxint, player, depth_counter)
        search_time = clock() - start_time
        self.schedule[4] = search_time
        self.schedule[5] = depth_counter
        self.schedule[1] -= search_time
        if num_empties_left > self.schedule[3]:
            self.schedule[0] -= search_time
        # print "Search time is:", search_time
        # print "Remain time:", self.schedule[1]
        # print "Reamin midgame time:", self.schedule[0]
        return result

    def __search(self, node, depth, alpha, beta, player, depth_counters=None):
        if depth_counters is not None:
            depth_counters[depth] += 1

        if depth <= 0:
            if self._is_endgame is True:
                result = node.get_score(player) - node.get_score(-player)
            else:
                result = self.get_heuristic_value(node)
            return player * result, None

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) is 0:
            enemy_valid_moves = node.get_all_valid_moves(-player)
            if len(enemy_valid_moves) is 0:
                if self._is_endgame is True:
                    result = node.get_score(player) - node.get_score(-player)
                else:
                    result = self.get_heuristic_value(node)
                return player * result, None
            else:
                result = self.__search(node, depth, -beta, -alpha, -player, depth_counters)
                return -result[0], result[1]

        best_value, best_move = -maxint, None
        for mov, new_node in valid_moves.iteritems():
            result = self.__search(new_node, depth - 1, -beta, -alpha, -player, depth_counters)
            value = -result[0]  # Value of this node
            if value > best_value:
                best_value, best_move = value, mov
            alpha = max(value, alpha)
            if alpha >= beta:
                break

        return best_value, best_move

    def get_new_depth_counters(self, depth):
        depth_counters = [0] * (depth + 1)
        depth_counters[depth] = 1
        return depth_counters

    def get_average_branching_factors(self, previous_depth_counters):
        depth_counters_len = len(previous_depth_counters)
        player_branching_factor = 0
        player_levels = 0
        opponent_branching_factor = 0
        opponent_levels = 0
        for x in xrange(0, depth_counters_len, 2):
            try:
                player_branching_factor += previous_depth_counters[x] / float(previous_depth_counters[x + 1])
                player_levels += 1
            except:
                pass
        for x in xrange(1, depth_counters_len, 2):
            try:
                opponent_branching_factor += previous_depth_counters[x] / float(previous_depth_counters[x + 1])
                opponent_levels += 1
            except:
                pass
        if player_levels > 0:
            player_branching_factor /= player_levels
        if opponent_levels > 0:
            opponent_branching_factor /= opponent_levels
        return player_branching_factor, opponent_branching_factor

    def get_max_suggested_depth(self, previous_depth_counters, previous_search_time, search_time_limit):
        total_nodes = sum(previous_depth_counters)
        if total_nodes <= 0:
            return 6
        time_per_node = abs(float(previous_search_time) / total_nodes)
        branching_factors = self.get_average_branching_factors(previous_depth_counters)
        suggested_depth = -1
        expected_time = 0
        turn = 0
        current_level_node_count = 1
        for x in xrange(61):
            expected_time += current_level_node_count * time_per_node
            current_level_node_count *= branching_factors[turn]
            if expected_time > search_time_limit:
                suggested_depth -= 1
                break
            else:
                suggested_depth += 1
                turn = 0 if turn else 1
        return max(suggested_depth, 0)

    # How deep should we search to maximize the remaining time?
    def get_suggested_depth(self, mid_game_time_left, game_time_left, end_game_num_empties, min_search_depth, node, player, previous_search_time=None, previous_depth_counters=None):
        num_empties_left = 64 - node.get_score(player) - node.get_score(-player)

        if num_empties_left > end_game_num_empties:  # Still midgame

            if previous_depth_counters == None or previous_depth_counters == None:  # not first search
                test_search_depth = 8
                previous_depth_counters = self.get_new_depth_counters(test_search_depth)
                time_start = clock()
                # Just do a shallow search...
                self.__search(node, test_search_depth, -maxint, maxint, player, previous_depth_counters)
                previous_search_time = clock() - time_start
                mid_game_time_left -= previous_search_time

            num_mid_game_empties_left = num_empties_left - end_game_num_empties
            self_empties_lLeft = num_mid_game_empties_left / 2

            if num_mid_game_empties_left & 1:  # if odd number of empties left in midgame
                self_empties_lLeft += 1

            time_for_search = mid_game_time_left / float(self_empties_lLeft)  # Divide evenly...
            return max(min_search_depth,
                       self.get_max_suggested_depth(previous_depth_counters, previous_search_time, time_for_search))
        else:
            if num_empties_left <= 14:
                return num_empties_left
            else:
                if previous_depth_counters != None and previous_depth_counters != None:
                    # Check if capable of searching to endgame...
                    time_for_search = game_time_left * 0.7  # Assume that end game takes 70% of remaining time
                    max_suggested_depth = self.get_max_suggested_depth(previous_depth_counters, previous_search_time, time_for_search)
                    if max_suggested_depth >= end_game_num_empties:
                        return num_empties_left
                    else:  # Do a pre-end game search
                        return max(min_search_depth,
                                   self.get_max_suggested_depth(previous_depth_counters, previous_search_time, time_for_search * 0.7))
                else:  # We were already confident to proceed with endgame
                    return num_empties_left

class AlphaBetaWidthIterativeDeepening(AbstractSearcher):
    def search(self, node, depth, player):
        """Giai thuat alpla-beta cai tien"""
        # TODO: Alpha-beta improve
        pass
