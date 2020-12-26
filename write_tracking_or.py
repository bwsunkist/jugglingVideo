#色抽出した結果の二値画像を利用して、動画に軌道を書き込む
import cv2
import numpy as np
import os

#元動画
video = cv2.VideoCapture("./IMG_6859_wo_audio.mp4")

inputBaseDir = "./IMG6859s/"
outputBaseDir = "./IMG6859s/"
outputImageBaseName = "writeTrack2_"
#軌道を書くフレーム数指定
trackNum = 4

print("baseframe: " + str(0) + "/tracking:" + str(0))

frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(frameCount)):
    print("write frames... " + str(i) + "/" + str(int(frameCount)))
    img = cv2.imread(inputBaseDir + "frame" + str(i) +".png", -1)
    width = img.shape[0]
    height = img.shape[1]

    base = np.zeros((width, height), dtype=int)
    loopFirstFlg = True
    #色抽出部分の合計
    for idx in range(i-trackNum, i):
        if idx < 0:
            continue
        print("  baseframe: " + str(i) + "/tracking:" + str(idx))
        if loopFirstFlg:
            base = cv2.imread(inputBaseDir + "colorPick" + str(idx) +".png")
            base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
            loopFirstFlg = False

        #色抽出画像の読み込み
        pickImg = cv2.imread(inputBaseDir + "colorPick" + str(idx) +".png")
        pickImgExt = cv2.cvtColor(pickImg, cv2.COLOR_BGR2GRAY)
        base = cv2.bitwise_or(base, pickImgExt)

    # --- 元画像に書き込む
    for w in range(width):
        for h in range(height):
            val = base[w][h]
            if val>0:
                img[w][h][0] = 0
                img[w][h][1] = 255
                img[w][h][2] = 0

    cv2.imwrite(outputBaseDir + outputImageBaseName + str(i) + '.png', img)
