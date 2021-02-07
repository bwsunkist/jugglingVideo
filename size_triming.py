import cv2
import numpy as np
from hsv_color_picker import nothing
from hsv_color_picker import writeFrameNum
import os

filePath = "./video/IMG_7097.mp4"
outputPath = "./video/IMG_7097_size_trim.mp4"

# paste result of 'size_triming_checker.py'
aspect_x = 16
aspect_y = 9
x_length = 1623
trim_x = 63
trim_y = 75


if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_width   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_fps     = cap.get(cv2.CAP_PROP_FPS)

    if aspect_x < 0 or aspect_y < 0:
        raise ValueError("invalid initAspect ratio.")

    if x_length < 0 or x_length > cap_width:
        raise ValueError("invalid initLengthX.")

    if trim_x > cap_width or trim_y > cap_height:
        raise ValueError("invalid initTriming X, Y.")

    output_w = x_length
    output_h = int(x_length / aspect_x * aspect_y)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    newClip = cv2.VideoWriter(outputPath, fourcc, cap_fps, (output_w, output_h))

    if not newClip.isOpened():
        raise Exception('newClip open failed.')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
            else:
                raise Exception('read video failed.')

        # print(str(cap.get(cv2.CAP_PROP_POS_FRAMES)) + "/" + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        print(frame.shape)

        x_from = trim_x
        y_from = trim_y
        x_to   = trim_x + x_length
        y_to   = trim_y + int(x_length / aspect_x * aspect_y)

        img = frame[y_from : y_to, x_from : x_to, :]
        newClip.write(img)

    newClip.release()
    cap.release()
    print('complete.')
