import argparse

import cv2
import zmq

from utils import string_to_image

PORT = "8090"


class StreamViewer:
    def __init__(self, port=PORT):
        """
        Binds the computer to a ip address and starts listening for incoming streams.
        :param port: Port which is used for streaming
        """
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.bind('tcp://*:' + port)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, str())
        self.current_frame = None
        self.keep_running = True

    def receive_stream(self, display=True):
        """
        Displays stream in a window if no arguments are passed.
        Keeps updating the 'current_frame' attribute with the most recent "self.current_frame".
        :param display: boolean, If False no stream output will be displayed.
        :return: None
        """
        self.keep_running = True
        while self.footage_socket and self.keep_running:
            try:
                frame = self.footage_socket.recv_string()
                self.current_frame = string_to_image(frame)

                if display:
                    cv2.imshow("Stream", self.current_frame)
                    cv2.waitKey(1)

            except KeyboardInterrupt:
                self.stop_stream()
        print("Streaming Stopped!")

    def stop_stream(self):
        """
        Sets "self.keep_running" to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    port = PORT

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Viewer to use, default'
                             ' is ' + PORT, required=False)

    args = parser.parse_args()
    if args.port:
        port = args.port

    stream_viewer = StreamViewer(port)
    stream_viewer.receive_stream()


if __name__ == '__main__':
    main()
