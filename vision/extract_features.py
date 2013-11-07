'''
Properties of cv2.KeyPoint:

pt – coordinates of the keypoint
size – diameter of the meaningful keypoint neighborhood
angle – computed orientation of the keypoint. range [0,360) degrees.
response - the response by which the most strong keypoints have been selected. Can be used for further sorting or subsampling
octave - octave (pyramid layer) from which the keypoint has been extracted
'''

import cv2
import numpy as np

img = cv2.imread('images/sidewalk2.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
kp, des = sift.detectAndCompute(gray,None)

print kp[0].pt, kp[0].size, kp[0].angle, kp[0].response, kp[0].octave
print '*' * 10
print des[0]

img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('images/sift_keypoints.jpg',img)
