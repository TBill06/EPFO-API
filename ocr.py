import cv2
import pytesseract
import numpy as np

img = cv2.imread("t.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(gray,(3,3),0)
ret,th3 = cv2.threshold(gray,110,255,cv2.THRESH_BINARY)
inv = cv2.bitwise_not(th3)
vpp = np.sum(inv,axis=0)
index = []
f = []
for i in range(0,len(vpp)):
    if(i+1 < len(vpp)):
        if (vpp[i] == 0):
            if(vpp[i+1] != 0):
                index.append(i+1)
        else:
            if(vpp[i+1] == 0):
                index.append(i)
ocr = ''
for i in range(0,len(index),2):
    letter = inv[:,index[i]:index[i+1]]
    print(pytesseract.image_to_string(letter,config="--psm 7"))
    cv2.imshow("win",letter)
    cv2.waitKey()
