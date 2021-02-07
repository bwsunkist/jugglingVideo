import cv2
import numpy as np
from hsv_color_picker import nothing
from hsv_color_picker import writeFrameNum

filePath = "./video/IMG_7097.mp4"

# scaling ratio for preview window size
# if window is too large, please adjust this value
imgRatio = 0.5

# setting for indicating frame number
txtFormat = 'frame:'
txtSize = 2
txtColor = (255,255,255)

# the start position of preview 
initialFrameNum = 2000

# TrackBar のstart, end に切り抜きたい範囲を記録しておきましょう

# How to use Video Player
# press esc: end
# press z: back
# press x: reload
# press c: next
# press v: 3 ahead 

if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_width   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if initialFrameNum < 0 or initialFrameNum > allFrameNum:
        raise ValueError("invalid initialFrameNum.")

    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrameNum - 1) 

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('memory_start', 'image', initialFrameNum, allFrameNum, nothing)
    cv2.createTrackbar('memory_end'  , 'image', allFrameNum,     allFrameNum, nothing)
    cv2.createTrackbar('target_num'  , 'image', initialFrameNum, allFrameNum, nothing)
    target_num = initialFrameNum - 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            raise Exception('read video failed.')

        target_num_update = cv2.getTrackbarPos('target_num', 'image')
        memory_start = cv2.getTrackbarPos('memory_start', 'image')
        memory_end   = cv2.getTrackbarPos('memory_end', 'image')

        if target_num != target_num_update:
            # 移動したいframe num (= target_num_update)が指定された場合
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_num_update - 2)
            target_num = target_num_update
            continue

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        frame = cv2.resize(frame, dsize = None, fx = imgRatio, fy = imgRatio)

        txt = txtFormat + str(nowFrameNum)
        writeFrameNum(frame, txt, txtSize, txtColor)

        cv2.imshow('img', frame)

        k = cv2.waitKey(0)
        if k == 27: 
            #press esc: end
            break
        elif k == 122:
            # press z: back
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum - 2)
            continue
        elif k == 120:
            # press x: reload
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum - 1)
            continue
        elif k == 99:
            # press c: next
            continue
        elif k == 118:
            # press v: 3 ahead 
            cap.set(cv2.CAP_PROP_POS_FRAMES, nowFrameNum + 2) 
            continue
        else:
            continue

    print('extract_time = (' + str(memory_start) + ', ' + str(memory_end) + ')' )
    cap.release()
    cv2.destroyAllWindows()
