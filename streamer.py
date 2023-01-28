import cv2
import zmq
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", type=int, default=5555,
                help="port number")
ap.add_argument("-i", "--ip", type=str, default='192.168.1.99',
                help="ip address")
ap.add_argument("-c", "--camera", type=int, default=0,
                help="camera number")

args = vars(ap.parse_args())

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://{}:{}'.format(args["ip"], args["port"]))

camera = cv2.VideoCapture(args["camera"])  # init the camera

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
#        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        # jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(buffer)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break
