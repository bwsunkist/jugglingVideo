# Copyright (c) 2018 smeschke
# Released under the MIT license
# https://github.com/smeschke/juggling/blob/master/LICENSE

import cv2
import numpy as np
from hsv_color_picker import colorPick

filePath = "./video/IMG_7097.mp4"
outputPath = "./video/IMG_7097_write_all_track.mp4"

# paste result of 'hsv_color_picker.py'
h, s, v, h1, s1, v1 = 113, 52, 69, 169, 188, 255
#h, s, v, h1, s1, v1 = 0, 0, 0, 255, 255, 255
morph = 0

# the start position of preview ( > 0)
initialFrameNum = 2000

# scaling ratio for preview window size
# if window is too large, please adjust this value
imgRatio = 0.5

# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# newClip = cv2.VideoWriter(outputPath, fourcc, cap_fps, (cap_width, cap_height))
# if not newClip.isOpened():
#     raise Exception('read newClip failed.')

def getFrame(cap):
    ret, frame = cap.read()
    if not ret:
        raise Exception('read video failed.')
    return frame

def getColorPickedBinary(frame):
    img, mask = colorPick(frame, (h, s, v, h1, s1, v1), morph)

    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    threshold = 100
    # 二値化(閾値100を超えた画素を255にする。)
    ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    if not ret:
        raise Exception('read video failed.')
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if initialFrameNum <= 0 or initialFrameNum > allFrameNum:
        raise ValueError("invalid initialFrameNum.")

    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrameNum -1)

    baseFrm = getFrame(cap)
    baseImg = getColorPickedBinary(baseFrm)
    baseImg = cv2.resize(baseImg, dsize = None, fx = imgRatio, fy = imgRatio)

    while cap.isOpened():
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break
        frame = getFrame(cap)
        img = getColorPickedBinary(frame)
        img = cv2.resize(img, dsize = None, fx = imgRatio, fy = imgRatio)

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        img = cv2.bitwise_or(img, baseImg)
        cv2.imshow('img', img)
        baseImg = img

        k = cv2.waitKey(0)
        if k == 27: 
            #press esc: end
            break
        else:
            continue

    cap.release()
    cv2.destroyAllWindows()
