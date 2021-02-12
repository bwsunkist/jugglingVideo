import cv2
import numpy as np
from hsv_color_picker import colorPick

filePath = "./video/IMG_7097.mp4"
outputPath = "./video/IMG_7097_write_all_track.mp4"

# paste result of 'hsv_color_picker.py'
h, s, v, h1, s1, v1 = 77, 52, 46, 169, 189, 255
#h, s, v, h1, s1, v1 = 0, 0, 0, 255, 255, 255
morph = 10

# the start position of preview ( > 0)
initialFrameNum = 2200

# scaling ratio for preview window size
# if window is too large, please adjust this value
imgRatio = 0.5

threshold = 50

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

    # 二値化(閾値を超えた画素を255にする。)
    ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    if not ret:
        raise Exception('read video failed.')
    return img

def contourArr2CenterOfGravityArr(contourArr):
    cogArr = []
    for contour in contourArr:
        moment = cv2.moments(contour)
        if moment['m00'] == 0:
            continue
        cogX = int(moment['m10']/moment['m00'])
        cogY = int(moment['m01']/moment['m00'])
        cogArr.append((cogX, cogY))
    return cogArr

def contourArr2AreaArr(contourArr):
    cogArr = []
    for contour in contourArr:
        cogArr.append(cv2.contourArea(contour))
    return cogArr


if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if initialFrameNum <= 0 or initialFrameNum > allFrameNum:
        raise ValueError("invalid initialFrameNum.")

    cap_width   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.set(cv2.CAP_PROP_POS_FRAMES, initialFrameNum -1)

    bluesq_detect_count = 0
    bluesq_detect_count_before = 0
    blue_ball_count = 0
    blue_ball_count_before = 0
    blue_display_count = 0

    redsq_detect_count = 0
    redsq_detect_count_before = 0
    red_ball_count = 0
    red_ball_count_before = 0
    red_display_count = 0

    
    while cap.isOpened():
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break
        frame = getFrame(cap)
        img = getColorPickedBinary(frame)

        # 基本の四角書く
        color_green = (0,255,0)
        color_blue  = (255,0,0)
        color_red   = (0,0,255)
        color_white   = (255,255,255)
        square_blue_xyfrom = (0, 5)
        square_blue_xyto   = (int(cap_width / 2) - 5, int(cap_height / 2) -1)
        square_blue_xyfrom_knock = (10, 10)
        square_blue_xyto_knock   = (int(cap_width / 2) - 10, int(cap_height / 2) - 5)
        frame = cv2.rectangle(frame, square_blue_xyfrom, square_blue_xyto, color_blue, 10)
        square_red_xyfrom = (int(cap_width / 2) + 5, 5)
        square_red_xyto   = (cap_width, int(cap_height / 2) -1)
        square_red_xyfrom_knock = (int(cap_width / 2) + 20, 20)
        square_red_xyto_knock   = (cap_width, int(cap_height / 2) -1)
        frame = cv2.rectangle(frame, square_red_xyfrom, square_red_xyto, color_red, 10)

        # ボール検出
        # # コントア確認
        contours, hierarchy = cv2.findContours(img, 1, 2)
        # frame = cv2.drawContours(frame, contours, -1, (0,255,0), 3)

        # 四角範囲に位置するもののなかで大きい方から2領域 & ある程度以上の大きさのもの抽出
        cogArr = contourArr2CenterOfGravityArr(contours)
        areaArr = contourArr2AreaArr(contours)
        len_arr = len(cogArr)
        allArrBase = []
        for lenarri in range(len_arr):
            if int(cap_height / 2) < cogArr[lenarri][1]:
                continue
            allArrBase.append((cogArr[lenarri], areaArr[lenarri]))
        allArr = sorted(allArrBase, key=lambda x:x[1], reverse=True)
        allArr = allArr[0:3]

        for arr in allArr:
            if arr[1] < 13.0:
                continue
            # cv2.putText(frame, str(arr[1]), (arr[0][0]+50, arr[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color_blue, 2, cv2.LINE_AA)
            if arr[0][0] < square_blue_xyto[0] and arr[0][1] < square_blue_xyto[1]:
                bluesq_detect_count = bluesq_detect_count + 1
                cv2.circle(frame, arr[0], 15, color_blue, thickness=-1)
            if arr[0][0] > square_red_xyfrom[0] and arr[0][1] < square_red_xyto[1]:
                redsq_detect_count = redsq_detect_count + 1
                cv2.circle(frame, arr[0], 15, color_red, thickness=-1)

        blue_ball_count = bluesq_detect_count - bluesq_detect_count_before
        red_ball_count  = redsq_detect_count - redsq_detect_count_before

        blue_fluctuation = blue_ball_count - blue_ball_count_before
        red_fluctuation  = red_ball_count  - red_ball_count_before

        if blue_fluctuation > 0:
            blue_display_count = blue_display_count + 5
        if red_fluctuation > 0:
            red_display_count  = red_display_count  + 5
        
        if blue_display_count > 0:
            frame = cv2.rectangle(frame, square_blue_xyfrom_knock, square_blue_xyto_knock, color_blue, 30)
            blue_display_count = blue_display_count -1

        if red_display_count > 0:
            frame = cv2.rectangle(frame, square_red_xyfrom_knock, square_red_xyto_knock, color_red, 30)
            red_display_count = red_display_count -1

        bluesq_detect_count_before = bluesq_detect_count
        redsq_detect_count_before  = redsq_detect_count

        blue_ball_count_before = blue_ball_count
        red_ball_count_before  = red_ball_count

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        img = cv2.resize(img, dsize = None, fx = imgRatio, fy = imgRatio)
        frame = cv2.resize(frame, dsize = None, fx = imgRatio, fy = imgRatio)

        cv2.imshow('img', frame)

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


    cap.release()
    cv2.destroyAllWindows()
