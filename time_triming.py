import cv2
import numpy as np
from hsv_color_picker import nothing
from hsv_color_picker import writeFrameNum

filePath = "./video/IMG_7097.mp4"
outputPath = "./video/IMG_7097_time_trim.mp4"

# paste result of 'time_triming_checker.py'
extract_time = (3931, 4978)


if __name__ == '__main__':
    cap = cv2.VideoCapture(filePath)
    if not cap.isOpened():
        raise Exception('read video failed.')

    allFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_width   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_fps     = cap.get(cv2.CAP_PROP_FPS)


    if extract_time[0] < 0 or extract_time[0] > allFrameNum:
        raise ValueError("invalid extract_time[0].")

    if extract_time[1] < 0 or extract_time[1] > allFrameNum:
        raise ValueError("invalid extract_time[1].")

    cap.set(cv2.CAP_PROP_POS_FRAMES, extract_time[0]) 

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    newClip = cv2.VideoWriter(outputPath, fourcc, cap_fps, (cap_width, cap_height))
    if not newClip.isOpened():
        raise Exception('read newClip failed.')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
            else:
                raise Exception('read video failed.')

        nowFrameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if extract_time[1] == nowFrameNum:
            break

        newClip.write(frame)

    print('complete.' )
    cap.release()
    newClip.release()
