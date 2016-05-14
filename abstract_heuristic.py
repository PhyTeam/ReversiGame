from node import *
from heuristicB import *

class AbstractHeuristic:
    def __init__(self):
        """Contuctor method"""
    """def eval_early_game(self,node):

        pass
    def eval_mid_game(self,node):

        pass
    def eval_late_game(self,node):

        pass
    """
    def eval(self, node):
        """Return value f(b)"""
        pass


class DummyHeuristic(AbstractHeuristic):
    def eval(self, node):
        my_index = Node.PLAYER_1

        enemy_index = Node.PLAYER_2
        return node.get_score(my_index) - node.get_score(enemy_index)

class BestHeuristic(AbstractHeuristic):
    def eval(self, node):
        evalHeu = heuristicB(node)
        my_index = Node.PLAYER_1
        enemy_index = Node.PLAYER_2

        # normalize
        good_1 = float(node.get_score(my_index))
        good_2 = float(node.get_score(enemy_index))

        if good_1 == 0 and good_2 == 0:
            return 0
        elif good_2 == 0:
            return 1000
        elif good_1 == 0:
            return -1000

        reached = good_1 + good_2
        #if good_2/good_1 > 5:
        #    return -500
        #elif good_1/good_2 > 5:
        #    return 500

        strong_1 = float(evalHeu.get_value_of_men(node, my_index, reached) / good_1)
        strong_2 = float(evalHeu.get_value_of_men(node, enemy_index, reached) / good_2)
        if strong_1 + strong_2 == 0 or good_1 + good_2 == 0:
            return 0
        _value =  (strong_1-strong_2)# / (strong_1 + strong_2) * (128 - reached) + (good_1 - good_2)/(good_1 + good_2) * reached

        #if reached < 18 and _length_moves > 0 :
            #return _length_moves
        #else:
            #return _value
        return strong_1 - strong_2
        # return  strong_1/good_1 - strong_2/good_2
        # return node.get_score(my_index) - node.get_score(enemy_index)


