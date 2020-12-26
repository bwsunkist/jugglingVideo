#連番画像から動画を生成する
import cv2
import numpy as np
import os

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
newClip = cv2.VideoWriter('./IMG6859s/video.mp4',fourcc, 30.0, (1280, 720))

if not newClip.isOpened():
    print("video open failed.")
    sys.exit()

finalFrame = 335
for i in range(0, finalFrame):
    img = cv2.imread("./IMG6859s/writeTrack" + str(i) + ".png")

    if img is None:
        print("img open failed.")
        break

    newClip.write(img)
    print(str(i) + "/" + str(finalFrame))

newClip.release()
print('complete.')
