import cv2
import zmq
import argparse
import numpy as np

args = argparse.ArgumentParser()
args.add_argument("-i", "--ip", type=str, default="192.168.1.99",
                  help="ip address of the server to which the client will connect")

args.add_argument("-p", "--port", type=str, default="5555",
                  help="port number of the server to which the client will connect")

args = vars(args.parse_args())

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://' + args["ip"] + ':' + args["port"])
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode_(''))

while True:
    try:
        frame = footage_socket.recv()
        npimg = np.frombuffer(frame, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break
