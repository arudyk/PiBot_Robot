#!/usr/bin/env python2

"""
Andriy Rudyk
Tim Sizemore

Camera operation module

"""

import picamera
from time import sleep
import os
import io
import cv2

PICTURE_NAME = 'capture'
WIDTH = 1024
HEIGHT = 768


def take_picture(filename, width, height):
    """
    Takes a picture width x height and saves us filename.
    """
    picamera.resolution = (width, height)
    # According to API camera needs 0.2 seconds warm up at start.
    time.sleep(0.2)
    camera.capture(filename)


def ocv_object():
    """
    Takes a picture then converts that data to an array that Open CV can use.
    """
    stream = io.BytesIO()
    with picamera.PiCamera() as cam
    cam.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')

    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)
    image = image[:, :, ::-1]


def remove_picture(filename):
    """
    Removes filename
    """
    os.remove(filename)


def timelapse(filename):
    """
    Takes a timelapse sequence of pictures.
    """
    with picamera.PiCamera() as cam:
        cam.start_preview()
        time.sleep(2)
        for filename in cam.capture_continuous('img{counter:03d}.jpg'):
            print('Captured %s' % filename)
            time.sleep(60)


def video(height, width):
    """
    Captures a video of specified height and width
    """
    with picamera.PiCamera() as cam:
        cam.resolution = (height, width)
        cam.start_recording('video.h264')
        cam.wait_recording(60)
        cam.stop_recording()


def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img


def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite(PICTURE_NAME, img)


def main():
    take_picture(PICTURE_NAME, WIDTH, HEIGHT)
    rects, img = detect(PICTURE_NAME + '_DETECTED')
    box(rects, img)


if __name__ == '__main__':
    main()
