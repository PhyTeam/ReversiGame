import websocket

import websocket
import thread
import time
import json


def on_message(ws, message):
    print message


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    token = raw_input("Input your token")
    jheader = json.dumps({'query': 'token=' + token.__str__()})
    ws = websocket.WebSocketApp("ws://localhost:8100/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=jheader)
    ws.on_open = on_open
    ws.run_forever()
