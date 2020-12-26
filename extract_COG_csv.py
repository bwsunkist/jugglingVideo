#画像をインプットに色抽出し、取得したコントアの重心を導出する
#出力CSV: フレーム数, 検出オブジェクト数、オブジェクトそれぞれの座標
import cv2
import numpy as np
import os
import csv

def contourArr2CenterOfGravityArr(contourArr):
    cogArr = []
    for contour in contourArr:
        moment = cv2.moments(contour)
        cogX = int(moment['m10']/moment['m00'])
        cogY = int(moment['m01']/moment['m00'])
        cogArr.append((cogX, cogY))
    return cogArr

def contourArr2AreaArr(contourArr):
    cogArr = []
    for contour in contourArr:
        cogArr.append(cv2.contourArea(contour))
    return cogArr

#元動画読み込み
video = cv2.VideoCapture("./IMG_6859_wo_audio.mp4")
filePath = "./IMG6859s/"

outputAllFile = "./IMG6859_All.csv"
outputCogFile = "./IMG6859_Cog.csv"
outputAreaFile = "./IMG6859_Area.csv"

outputCog = []
outputArea = []

frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(frameCount)):
    #色抽出画像の読み込み,コントアの取得
    img = cv2.imread(filePath + "colorPick" + str(i) + ".png", -1)
    ret,thresh = cv2.threshold(img,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)
    cogArr = contourArr2CenterOfGravityArr(contours)
    areaArr = contourArr2AreaArr(contours)

    # 面積でフィルタリング. 大きい順３つのみ保存
    len_arr = len(cogArr)
    allArrBase = []
    for lenarri in range(len_arr):
        allArrBase.append((cogArr[lenarri], areaArr[lenarri]))
    allArr = sorted(allArrBase, key=lambda x:x[1], reverse=True)
    allArr = allArr[0:3]
    print(allArr)
    if len_arr > 3:
        len_arr = 3

    with open(outputAllFile, 'a') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([i, len_arr, allArr])

    #drow cog
    climg = cv2.imread("./IMG6859s/frame" + str(i) + ".png", -1)
    for all in allArr:
        cogx, cogy = all[0]
        climg[cogy][cogx][0] = 255
        climg[cogy][cogx][1] = 0
        climg[cogy][cogx][2] = 0
        cv2.line(climg, (436, cogy), (cogx, cogy), (0,255,0), 3)
    #draw contour
    climg = cv2.drawContours(climg, contours, -1, (0,255,0), 3)
    cv2.imshow('res', climg)
    k = cv2.waitKey(0)
    if k==27: break

cv2.destroyAllWindows()
