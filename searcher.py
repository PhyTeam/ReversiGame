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


class AlplaBetaSearcher(AbstractSearcher):
    __node_visited = 0
    __time_estimate = 0
    __eval_count = 0

    def search(self, node, depth, player):
        # Reset all variable
        self.__eval_count = 0
        self.__node_visited = 0
        self.__time_estimate = 0
        # Swapper function
        result = self.__search(node, depth, -1000, 1000, player)
        print "_________________________________________________"
        print "| Node\t| Depth\t| Eval node\t|"
        print "_________________________________________________"
        print "| ", self.__node_visited, "\t",
        print "| ", depth, "\t",
        print "| ", self.__eval_count, "\t", "|"
        print "_________________________________________________"
        return result

    def __search(self, node, depth, alpha, beta, player):
        """Tim theo giai thuat  minmax"""

        self.__node_visited += 1
        if depth <= 0:
            self.__eval_count += 1
            return self.get_heuristic_value(node), None

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) is 0:
            return self.get_heuristic_value(node), None

        best_value, best_move = -1000, None

        for mov, new_node in valid_moves.iteritems():
            result = self.__search(new_node, depth - 1, -beta, -alpha, -player)
            value = player * result[0]  # Value of this node
            if value > best_value:
                best_value, best_move = value, mov
            alpha = max (value, alpha)
            if alpha >= beta:
                break

        return best_value * player, best_move


class NegamaxSearcher(AbstractSearcher):
    def __init__(self, heuristic):
        AbstractSearcher.__init__(self, heuristic)
        self._transposition_table = {}

    def search(self, node, depth, player):
        # Swapper function
        return self.__search(node, depth, -1000, 1000, player)

    def __search(self, node, depth, alpha, beta, player):
        """Tim theo giai thuat  minmax"""
        alpha_orig = alpha  # Save the original value of Alpha

        tt_entry = self._transposition_table.get(node)  # Looking entry in transposition table

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
            return player * self.get_heuristic_value(node), None

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) is 0:
            return player * self.get_heuristic_value(node), None

        best_value, best_move = -1000, None
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


class AlphaBetaWidthIterativeDeepening(AbstractSearcher):
    def search(self, node, depth, player):
        """Giai thuat alpla-beta cai tien"""
        # TODO: Alpha-beta improve
        pass
