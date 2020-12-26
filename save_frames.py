import cv2
import numpy as np
import os

# Capture the webcam (or enter path to video)
cap = cv2.VideoCapture("./IMG_6859_wo_audio.mp4")
folderPath = "./IMG6859s/"

fileBaseName = 'frame'
frameNum = 0

def nothing(arg): pass

#main loop of the program
while True:

    #read image from the video
    _, img = cap.read()
    if _ == False:
        break
    cv2.imwrite(folderPath + fileBaseName + str(frameNum) + '.png', img)
    print(str(frameNum) + ' done.')
    frameNum = frameNum + 1
    k=cv2.waitKey(300)
    if k==27: break

#release the video to avoid memory leaks, and close the window
cap.release()
cv2.destroyAllWindows()
