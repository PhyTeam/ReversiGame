from copy import copy

from heuristic import *
from reversi_client import *
from searcher import *

class ReversiClient(PlayReversi):
    map_function = {
        -1: 0,
        2: -1,
        1: 1
    }

    _searcher = None
    _player = 1

    def __init__(self, searcher, player):
        """
        Constructor of revesi client
        :param searcher: searcher
        :param player: 1 if you are first player, 2 otherwise
        """
        super(ReversiClient, self).__init__()
        self._searcher = searcher
        self._player = player

        if self._player == 2:
            self._player = -1

    def make_bit_board(self, board):
        """
        Get bitboard of current state
        :param board: recv from server
        :return: a bitboard
        """
        board = copy(board)
        black, white = 0, 0
        for i in xrange(8):
            for j in xrange(8):
                temp = board[i][j]
                board[i][j] = self.map_function[temp]
                # Calculate bitboard
                if board[i][j] == 1:
                    black |= 1 << (i * 8 + j)
                elif board[i][j] == -1:
                    white |= 1 << (i * 8 + j)
        # Create a bitboard node
        bit_board = BitBoard(None)
        bit_board.bitboard[1] = black
        bit_board.bitboard[-1] = white
        return bit_board

    def make_a_move(self, updated_board):
        board = copy(updated_board)
        # current_node = Node(board)

        # Generate a bitboard node
        current_node = self.make_bit_board(board)
        # current_node = Node(updated_board)
        #heuristic, move = self._searcher.search(current_node, 4, self._player)
        heuristic, move = self._searcher.search(current_node, self._player)
        return {'X': move[1], 'Y': move[0]}

    def update_board(self, updated_board):
        print (updated_board.__str__())
        super(ReversiClient, self).update_board(updated_board)


from node_advance import *
if __name__ == "__main__":
    heuristic = BestHeuristic()
    # heuristic = HeuristicAdvance()
    begin = BitBoard(None)
    #begin = Node.create()
    searcher = NegamaxWithDeepeningSearcher(heuristic)
    turn = int(raw_input("Enter your turn: "))
    #searcher.search(begin, 10, turn)
    handler = ReversiClient(searcher, turn)
    play(handler)
