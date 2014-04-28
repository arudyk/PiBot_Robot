import io
import socket
import struct
import time
import picamera

from argparse import ArgumentParser


class CameraClient:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def connect(self):
        client_socket = socket.socket()
        client_socket.connect((server, port))
        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)

                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)

                # Note the start time and construct a stream to hold image data
                # temporarily (we could write it directly to connection but in this
                # case we want to find out the size of each capture first to keep
                # our protocol simple)
                start = time.time()
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg'):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()

                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())

                    # If we've been capturing for more than 30 seconds, quit
                    if time.time() - start > 30:
                        break

                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            client_socket.close()


def main():
    arg_parser = ArgumentParser(prog='./camera_client <server address> <port>',
                                description='Sends pycam pictures to server',
                                epilog='PyCam client')
    arg_parser.add_argument('server', metavar='S', type=str,
                            help='server ip address')
    arg_parser.add_argument('port', metavar='P', type=int,
                            help='server port number')
    args = arg_parser.parse_args()
    client = CameraClient(args.server, args.port)
    client.connect()

if __name__ == '__main__':
    main()
