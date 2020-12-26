#色抽出と、元画像への描画を行う
import cv2
import numpy as np
import os

# Capture the webcam (or enter path to video)
img = cv2.imread("./IMG6859s/frame135.png", -1)
outputBaseImg = cv2.imread("./IMG6859s/frame135.png", -1)

width = img.shape[0]
height = img.shape[1]
colorVal = (0,0,242,255,35,255)
morph = 5

h,s,v,h1,s1,v1 = colorVal
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

# --- 元画像に赤で書き込む
for w in range(width):
    for h in range(height):
        val = img_thresh[w][h]
        if val>0:
            outputBaseImg[w][h][0] = 0
            outputBaseImg[w][h][1] = 255
            outputBaseImg[w][h][2] = 0

# 表示
cv2.imshow("img_th", outputBaseImg)
cv2.waitKey()
cv2.destroyAllWindows()

print(outputBaseImg)
