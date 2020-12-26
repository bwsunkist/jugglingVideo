#画像をインプットに色抽出し、取得したコントアを重ねが着して表示する
import cv2
import numpy as np
import os

def contourArr2CenterOfGravityArr(contourArr):
    cogArr = []
    for contour in contourArr:
        moment = cv2.moments(contour)
        cogX = int(moment['m10']/moment['m00'])
        cogY = int(moment['m01']/moment['m00'])
        cogArr.append((cogX, cogY))
    return cogArr

#色抽出画像の読み込み
img = cv2.imread("./IMG6859s/colorPick93.png", -1)
climg = cv2.imread("./IMG6859s/frame93.png", -1)

ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
cogArr = contourArr2CenterOfGravityArr(contours)
print(cogArr)

#drow cog
for cog in cogArr:
    cogx, cogy = cog
    climg[cogy][cogx][0] = 255
    climg[cogy][cogx][1] = 0
    climg[cogy][cogx][2] = 0
    cv2.line(climg, (436, cogy), (cogx, cogy), (0,255,0), 3)

#draw contour
climg = cv2.drawContours(climg, contours, -1, (0,255,0), 3)
cv2.imshow('res', climg)
cv2.waitKey(0)
cv2.destroyAllWindows()