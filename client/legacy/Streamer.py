import argparse

import zmq
import mss
import numpy as np

from utils import image_to_string


SERVER_ADDRESS = "localhost"
PORT = "8090"


class Streamer:

    def __init__(self, server_address=SERVER_ADDRESS, port=PORT):
        """
        Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.

        :param server_address: Address of the computer on which the StreamViewer is running, default is `localhost`
        :param port: Port which will be used for sending the stream
        """

        print("Connecting to ", server_address, "at", port)
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect('tcp://' + server_address + ':' + port)
        self.keep_running = False

    def start(self):
        """
        Starts sending the stream to the Viewer.
        Creates a camera, takes a image frame converts the frame to string and sends the string across the network
        :return: None
        """
        with mss.mss() as sct:
            self.keep_running = True
            print("Streaming Started...")
            while self.footage_socket and self.keep_running:
                # noinspection PyTypeChecker
                frame = np.array(sct.grab(sct.monitors[1]))  # grab the current frame
                image_as_string = image_to_string(frame)
                self.footage_socket.send(image_as_string)

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    port = PORT
    server_address = SERVER_ADDRESS

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        help='IP Address of the server which you want to connect to, default'
                             ' is ' + SERVER_ADDRESS,
                        required=True)
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Server to use, default'
                             ' is ' + PORT, required=False)

    args = parser.parse_args()

    if args.port:
        port = args.port
    if args.server:
        server_address = args.server

    streamer = Streamer(server_address, port)
    streamer.start()


if __name__ == '__main__':
    main()
