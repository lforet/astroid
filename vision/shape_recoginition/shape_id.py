import numpy as np
import cv, cv2
import time

img = cv2.imread('shapes.png')
gray = cv2.imread('shapes.png',0)

ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

contours,h = cv2.findContours(th2,cv.CV_RETR_TREE ,cv.CV_CHAIN_APPROX_NONE)
print "number of contours found:", len(contours)

for cnt in contours:
    print
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    cv2.drawContours(img,[cnt],0, (0,0,0),  thickness=3)
    cv2.imshow('img',img)
    cv2.waitKey(10)
    

    print len(approx), cv2.isContourConvex(cnt)
    if len(approx)==5:
        print "pentagon"
    if len(approx)==3:
        print "triangle"
    if len(approx)==4:
        print "square"
    if len(approx) >= 9:
        print "half-circle"
    if len(approx) >= 12:
        print "circle"
    time.sleep(1.5)
#cv2.drawContours(img, contours, -1, (0,0,255),  thickness=3)

cv2.imshow('img',img)
cv2.imshow('img2',th2)
cv2.imshow('img3',th3)
cv2.waitKey(0)
cv2.destroyAllWindows()
