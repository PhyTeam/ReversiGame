from socketIO_client import SocketIO, BaseNamespace


class PlayReversi(object):
    def __init__(self):
        self.board = []

    def make_a_move(self, updated_board):
        self.board = updated_board
        return {'X': 4, 'Y': 5}

    def update_board(self, updated_board):
        self.board = updated_board


class ReversiNamespace(BaseNamespace):
    def on_updated(self, data):
        """ Response to updated event
        """
        print('updated triggered')
        board = data['board']
        play_reversi.update_board(board)

    def on_yourturn(self, data):
        """ Response to yourturn event
        """
        print('yourturn triggered')
        board = data['board']
        move = play_reversi.make_a_move(board)
        print(board)
        self.emit('mymove', {'rowIdx': move['Y'], 'colIdx': move['X']})

    def on_errormessage(self, data):
        """ Response to errormessage event
        """
        print(data)

    def on_end(self, data):
        """ Response to end event
        """
        print('The winner is ' + str(data['winner']))
        print('P1 count: ' + str(data['player1']))
        print('P2 count: ' + str(data['player2']))


global play_reversi


def play(handler):
    token = raw_input('Enter your token: ')
    global play_reversi
    play_reversi = handler
    # Use socketio with defined Namespace
    # socketIO = SocketIO('localhost', 8100, params={'token': token})
    # gameplay = socketIO.define(ReversiNamespace, '/play')
    socketIO = SocketIO('localhost', 8100, ReversiNamespace, params={'token': token})
    socketIO.wait()


if __name__ == '__main__':
    play(None)
