#色抽出した結果の二値画像を保存する（動画の全フレーム数分ファイル生成）
import cv2
import numpy as np
import os

#設定
video = cv2.VideoCapture("./IMG_6859_wo_audio.mp4")
inputBaseDir = "./IMG6859s/"
outputBaseDir = "./IMG6859s/"
outputImageBaseName = "colorPick"

frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(frameCount)):
    print("write frames... " + str(i) + "/" + str(frameCount))
    img = cv2.imread(inputBaseDir + "frame" + str(i) +".png", -1)


    colorVal = (0,0,242,255,35,255)
    morph = 5
    h,s,v,h1,s1,v1 = colorVal
    frameNum = 0


    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower = np.array([h,s,v])
    upper = np.array([h1,s1,v1])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    #define kernel size (for touching up the image)
    kernel = np.ones((morph, morph),np.uint8)
    #touch up
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask= mask)
    img = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 二値化 ---
    threshold = 100
    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    cv2.imwrite(outputBaseDir + outputImageBaseName + str(i) + '.png', img_thresh)

