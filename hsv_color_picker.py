# Copyright (c) 2018 smeschke
# Released under the MIT license
# https://github.com/smeschke/juggling/blob/master/LICENSE

import cv2
import numpy as np

filePath = "./video/IMG_7097.mp4"

# scaling ratio for preview window size
# if window is too large, please adjust this value
imgRatio = 0.5

# setting for indicating frame number
txtFormat = 'frame:'
txtSize = 2
txtColor = (255,255,255)

# the start position of preview 
initialFrameNum = 1000

# initial setting value of color picking
# lower limit (default: 0 = min)
initH = 0
initS = 0
initV = 0
# upper limit (default: 255 = max)
initH1 = 255
initS1 = 255
initV1 = 255

# initial setting value of Morphology transformation kernel size
# 0 - 10
initMorph = 0

# How to use Video Player
# press esc: end
# press z: back
# press x: reload
# press c: next
# press v: 3 ahead 


def nothing(x):
    pass

def colorPick(frame, color_ranges, morph):
    h, s, v, h1, s1, v1 = color_ranges
    hsvLower = np.array([h, s, v])
    hsvUpper = np.array([h1, s1, v1])

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvMask = cv2.inRange(hsvImage, hsvLower, hsvUpper)

    kernel = np.ones((morph, morph), np.uint8)
    hsvMaskOpening = cv2.morphologyEx(hsvMask, cv2.MORPH_OPEN, kernel)

    result = cv2.bitwise_and(hsvImage, hsvImage, mask=hsvMaskOpening)
    return result, hsvMaskOpening

def writeFrameNum(img, txt, size, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, txt, (10,150), font, size, color, 2, cv2.LINE_AA)
    return img


if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if initialFrameNum < 0 or initialFrameNum > allFrameNum:
        raise ValueError("invalid initialFrameNum.")


    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrameNum - 1) 

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('h', 'image', initH, 255, nothing)
    cv2.createTrackbar('s', 'image', initS, 255, nothing)
    cv2.createTrackbar('v', 'image', initV, 255, nothing)
    cv2.createTrackbar('h1', 'image', initH1, 255, nothing)
    cv2.createTrackbar('s1', 'image', initS1, 255, nothing)
    cv2.createTrackbar('v1', 'image', initV1, 255, nothing)
    cv2.createTrackbar('morph', 'image', initMorph, 10, nothing)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
            else:
                raise Exception('read video failed.')

        h  = cv2.getTrackbarPos('h',  'image')
        s  = cv2.getTrackbarPos('s',  'image')
        v  = cv2.getTrackbarPos('v',  'image')
        h1 = cv2.getTrackbarPos('h1', 'image')
        s1 = cv2.getTrackbarPos('s1', 'image')
        v1 = cv2.getTrackbarPos('v1', 'image')
        morph = cv2.getTrackbarPos('morph', 'image')

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        frame = cv2.resize(frame, dsize = None, fx = imgRatio, fy = imgRatio)

        img, mask = colorPick(frame, (h, s, v, h1, s1, v1), morph)
        
        txt = txtFormat + str(nowFrameNum)
        writeFrameNum(img, txt, txtSize, txtColor)
        cv2.imshow('img', img)
        cv2.imshow('image', mask)

        k = cv2.waitKey(0)
        if k == 27: 
            #press esc: end
            break
        elif k == 122:
            # press z: back
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum - 2) 
        elif k == 120:
            # press x: reload
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum - 1) 
        elif k == 99:
            # press c: next
            continue
        elif k == 118:
            # press v: 3 ahead 
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum + 2) 
            continue
        else:
            continue

    print('result: ')
    print('h, s, v, h1, s1, v1 = '+str(h)+', '+str(s)+', '+str(v)+', '+str(h1)+', '+str(s1)+', '+str(v1))
    print('morph = '+str(morph))

    cap.release()
    cv2.destroyAllWindows()
