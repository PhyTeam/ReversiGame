from node import Node

# Declare const
C_PLAYER1, C_PLAYER2 = 1, -1
shift_left_mask = -9187201950435737472
shift_right_mask = 72340172838076673

inv_slm = ~shift_left_mask
inv_srm = ~shift_right_mask

# Types and constants used in the functions below

m1 = 0x5555555555555555  # binary: 0101...
m2 = 0x3333333333333333  # binary: 00110011..
m4 = 0x0f0f0f0f0f0f0f0f  # binary:  4 zeros,  4 ones ...
m8 = 0x00ff00ff00ff00ff  # binary:  8 zeros,  8 ones ...
m16 = 0x0000ffff0000ffff  # binary: 16 zeros, 16 ones ...
m32 = 0x00000000ffffffff  # binary: 32 zeros, 32 ones
hff = 0xffffffffffffffff  # binary: all ones
h01 = 0x0101010101010101  # the sum of 256 to the power of 0,1,2,3...

index64 = [
    0, 47, 1, 56, 48, 27, 2, 60,
    57, 49, 41, 37, 28, 16, 3, 61,
    54, 58, 35, 52, 50, 42, 21, 44,
    38, 32, 29, 23, 17, 11, 4, 62,
    46, 55, 26, 59, 40, 36, 15, 53,
    34, 51, 20, 43, 31, 22, 10, 45,
    25, 39, 14, 33, 19, 30, 9, 24,
    13, 18, 8, 12, 7, 6, 5, 63
]


def bitScanForward(bb):
    """
    Using de Bruijn Sequences to Index a 1 in a Computer Word
    :param bb: bb bitboard to scan
    :precondition bb != 0
    :return: index (0..63) of least significant one bit
    """
    debruijn64 = 0x03f79d71b4cb0a89
    return index64[((bb ^ (bb - 1)) * debruijn64) >> 58]

def popcount(x):
    """
    Efficient methods for counting the on-bits in an integer
    It uses 17 arithmetic operations.
    """
    x -= (x >> 1) & m1  # put count of each 2 bits into those 2 bits
    x = (x & m2) + ((x >> 2) & m2)  # put count of each 4 bits into those 4 bits
    x = (x + (x >> 4)) & m4  # put count of each 8 bits into those 8 bits
    x += x >> 8  # put count of each 16 bits into their lowest 8 bits
    x += x >> 16  # put count of each 32 bits into their lowest 8 bits
    x += x >> 32  # put count of each 64 bits into their lowest 8 bits
    return x & 0x7f

def shift_left(position):
    return (position >> 1) & inv_slm


def shift_right(position):
    return (position << 1) & inv_srm


def shift_down(position):
    return position >> 8


def shift_up(position):
    return position << 8


def shift_left_up(position):
    return ((position >> 1) & inv_slm) << 8


def shift_left_down(position):
    return ((position >> 1) & inv_slm) >> 8


def shift_right_up(position):
    return ((position << 1) & inv_srm) << 8


def shift_right_down(position):
    return ((position << 1) & inv_srm) >> 8


direction = {
    'UPP': shift_up,
    'DOW': shift_down,
    'LEF': shift_left,
    'RIG': shift_right,
    'LUP': shift_left_up,
    'LDO': shift_left_down,
    'RUP': shift_right_up,
    'RDO': shift_right_down
}

inv_direction = {
    'UPP': shift_down,
    'DOW': shift_up,
    'LEF': shift_right,
    'RIG': shift_left,
    'LUP': shift_right_down,
    'LDO': shift_right_up,
    'RUP': shift_left_down,
    'RDO': shift_left_up
}


def dilation(bits, d=None, is_inverted=False):
    if d is not None:
        if is_inverted:
            return inv_direction[d](bits)
        else:
            return direction[d](bits)
    else:
        return bits | shift_up(bits) | shift_down(bits) | \
               shift_left(bits) | shift_right(bits) | \
               shift_left_down(bits) | shift_left_up(bits) | \
               shift_right_up(bits) | shift_right_down(bits)


class BitBoard(Node):
    bitboard = {
        # 0x00\00\00\08\10\00\00\00
        C_PLAYER1: 0x0000000810000000,
        C_PLAYER2: 0x0000001008000000
    }

    def __position(self, row, col):
        return 1 << (row * 8 + col)

    def __set_at(self, pos, player):
        self.bitboard[player] = (self.bitboard[player] & ~pos) | pos

    def __get_at(self, pos, player):
        return self.bitboard[player] & pos

    def one_bits(self, bits):
        """
        Calculate index of 1s bit in bitstring
        :param bits: bb
        :return: List index of
        """
        if bits == 0:
            return []
        else:
            bb = bits
            result = []
            while bb != 0:
                index = bitScanForward(bb)
                result.append(index)
                bb &= ~(1 << index)
            return result


    def __to_x_y(self, board):

        to_x_y = []
        for i in xrange(0, 64, 8):
            temp = board >> i & 0xFF
            if temp != 0:
                for j in xrange(8):
                    valid = temp & 1
                    temp >>= 1
                    if valid != 0:
                        to_x_y.append((i / 8, j))
        return to_x_y

    def __generate_flipped_squares(self, move, dir, player):
        flipped_bit = move
        is_end = 0xFFFFFFFFFFFFFFFF
        while is_end != 0:
            move = dilation(move, dir, True)
            is_end = move & self.bitboard[player]
            flipped_bit |= move
        return flipped_bit

    def __gererate_new_board(self, flipped_squares, player):
        new_board = {C_PLAYER1: self.bitboard[C_PLAYER1], C_PLAYER2: self.bitboard[C_PLAYER2]}

        # Add to player bitboard
        new_board[player] |= flipped_squares
        # Clear opponent
        new_board[-player] &= ~flipped_squares
        return new_board

    def __str__(self):
        tostring = ""
        for i in xrange(8):
            for j in xrange(8):
                pos = self.__position(i, j)
                if self.__get_at(pos, C_PLAYER1) | self.__get_at(pos, C_PLAYER2) != 0:
                    tostring += '1'
                else:
                    tostring += '0'
            tostring += '\n'
        return tostring

    def __init__(self, board):
        super(BitBoard, self).__init__(board)

    def get_all_valid_moves(self, player):
        moves = {}
        empty = ~(self.bitboard[C_PLAYER1] | self.bitboard[C_PLAYER2])
        for d in direction.keys():
            dmove = 0
            candidates = self.bitboard[-player] & dilation(self.bitboard[player], d)
            while candidates != 0:
                dmove |= empty & dilation(candidates, d)
                candidates = self.bitboard[-player] & dilation(candidates, d)
            moves[d] = dmove
        all_candidate_moves = {}
        for keys, values in moves.iteritems():
            if values != 0:
                # Select a random valid move
                # Try
                bit2xy = self.__to_x_y(values)
                for valid_move in bit2xy:
                    x, y = valid_move[0], valid_move[1]
                    flipped_square = self.__generate_flipped_squares(1 << (x * 8 + y), keys, player)
                    bstr = self.__gererate_new_board(flipped_square, player)
                    new_board = BitBoard(None)
                    new_board.bitboard = bstr
                    all_candidate_moves[(x, y)] = new_board

        return all_candidate_moves

    def __hash__(self):
        h1 = self.bitboard[C_PLAYER1] & 0xFFFFFFFF
        h1 |= (self.bitboard[C_PLAYER1] >> 32) & 0xFFFFFFFF

        h2 = self.bitboard[C_PLAYER2] & 0xFFFFFFFF
        h2 |= (self.bitboard[C_PLAYER2] >> 32) & 0xFFFFFFFF

        return h1 | h2

    def __eq__(self, other):
        return other.bitboard[1] == self.bitboard[1] and other.bitboard[-1] == self.bitboard[-1]

    def get_at(self, row, colunm):
        """
        This is a method to get a square in bit board
        Please note that this is LOW PERFORMANCE method
        """
        pos = self.__position(row, colunm)
        p1, p2 = self.__get_at(pos, C_PLAYER1), self.__get_at(pos, C_PLAYER2)
        if p1 == 0 and p2 == 0:
            return 0
        elif p1 != 0:
            return C_PLAYER1
        else:
            return C_PLAYER2

    def get_score(self, player):
        """ Return score if a player """
        return popcount(self.bitboard[player])




def bitboard_tostring(bits):
    seq = '\n'
    tostring = seq.join(["{0:08b}".format(bits >> (i * 8) & 0xFF) for i in range(8)])
    return tostring


save_board = []

from multiprocessing import *
def anlysis(node, depth, player):
    print depth
    if depth <= 0:
        #save_board.append(node)
        return

    lst = node.get_all_valid_moves(player)
    p = Pool(len(lst))

    def f(x):
        anlysis(x, depth - 1, -player)
        return 0

    p.map(f, lst.values())
    # for k, v in lst.iteritems():
    #    # print k
    #    anlysis(v, depth - 1, -player)


if __name__ == "__main__":
    print "Unit test for bitboard"
    bb = BitBoard(None)
    print "Player 1", bb.get_score(C_PLAYER1)
    print "Player 2", bb.get_score(C_PLAYER2)
    print bitboard_tostring(bb.bitboard[C_PLAYER1])
    print bb.get_at(4, 4)
    for i in xrange(100000):
        if i != 0:
            bb.one_bits(0b100000000000000)

    # print bb
"""
    nb = Node.create()
    start_time = 0
    for i in xrange(9,12):
        start_time = time()
        if i <= 7:
            anlysis(nb, i, 1)
        end_time = time()
        estimate1 = end_time - start_time
        start_time = time()
        anlysis(bb, i, 1)
        end_time = time()
        estimate2 = end_time - start_time
        print 'Depth = ', i, '\t', estimate1, '---------------------\t', estimate2
    if bb.bitboard[1] == bb.bitboard[1] and \
                    bb.bitboard[-1] == bb.bitboard[-1]:
        print 'OK'

"""

"""
    anlysis(bb, 6, 1)

    dup = 0
    check = {}
    for i in xrange(len(save_board)):
        c = 0
        for j in xrange(i+1, len(save_board)):
            if save_board[i].bitboard[1] == save_board[j].bitboard[1] and \
                save_board[i].bitboard[-1] == save_board[j].bitboard[-1] and not check.has_key(j):
                check[j] = 1
                dup +=1
"""
