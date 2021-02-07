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

# initial setting value of triming
# aspect ratio (horizontal:x, vertical:y)
initAspectX = 16
initAspectY = 9
# vertival:x length (horizontal length will be auto-calicurated)
initLengthX = 255
# trimint start position
initTrimingX = 255
initTrimingY = 255

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

    if initAspectX < 0 or initAspectY < 0:
        raise ValueError("invalid initAspect ratio.")

    if initLengthX < 0 or initLengthX > cap_width:
        raise ValueError("invalid initLengthX.")

    if initTrimingX > cap_width or initTrimingY > cap_height:
        raise ValueError("invalid initTriming X, Y.")

    if initialFrameNum < 0 or initialFrameNum > allFrameNum:
        raise ValueError("invalid initialFrameNum.")

    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrameNum - 1) 

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('aspect_x', 'image', initAspectX, 20, nothing)
    cv2.createTrackbar('aspect_y', 'image', initAspectY, 20, nothing)
    cv2.createTrackbar('x_length', 'image', initLengthX, cap_width, nothing)
    cv2.createTrackbar('trim_x', 'image', initTrimingX, cap_width, nothing)
    cv2.createTrackbar('trim_y', 'image', initTrimingY, cap_height, nothing)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            raise Exception('read video failed.')

        aspect_x  = cv2.getTrackbarPos('aspect_x', 'image')
        aspect_y  = cv2.getTrackbarPos('aspect_y', 'image')
        x_length  = cv2.getTrackbarPos('x_length',  'image')
        trim_x    = cv2.getTrackbarPos('trim_x', 'image')
        trim_y    = cv2.getTrackbarPos('trim_y', 'image')
        
        box_x_len = x_length
        box_y_len = x_length / aspect_x * aspect_y

        resized_box_x_len = box_x_len * imgRatio
        resized_box_y_len = box_y_len * imgRatio
        resized_trim_x_from = trim_x * imgRatio
        resized_trim_y_from = trim_y * imgRatio
        xy_from = (int(resized_trim_x_from), int(resized_trim_y_from))
        resized_trim_x_to   = trim_x * imgRatio + resized_box_x_len
        resized_trim_y_to   = trim_y * imgRatio + resized_box_y_len
        xy_to   = (int(resized_trim_x_to), int(resized_trim_y_to))

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        frame = cv2.resize(frame, dsize = None, fx = imgRatio, fy = imgRatio)

        color_green = (0,255,0)
        img = cv2.rectangle(frame, xy_from, xy_to, color_green, 3)

        txt = txtFormat + str(nowFrameNum)
        writeFrameNum(img, txt, txtSize, txtColor)

        cv2.imshow('img', img)

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

    print('** Result: ')
    print('aspect_x =', aspect_x)
    print('aspect_y =', aspect_y)
    print('x_length =', x_length)
    print('trim_x =',   trim_x)
    print('trim_y =',   trim_y)

    cap.release()
    cv2.destroyAllWindows()
