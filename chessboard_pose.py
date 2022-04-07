from cv2 import imshow
import numpy as np
import cv2

img01 = cv2.imread('image01.png')
img02 = cv2.imread('image02.png')

arr01 = np.load('corners01.npy')
arr02 = np.load('corners02.npy')

objp = np.zeros((3*4,3), np.float32)
objp[:,:2] = np.mgrid[0:4,0:3].T.reshape(-1,2)
print(objp)

camera_matrix = np.array([[667.496, 0, 472.685],
                          [0, 667.496, 268.163],
                          [0,       0,    1   ]])

dist_coefs = np.array([0,0,0,0,0])


found,rvec,tvec = cv2.solvePnP(objp, arr02, camera_matrix, distCoeffs=None)

cv2.drawFrameAxes(img02, camera_matrix, distCoeffs=None, rvec=rvec, tvec=tvec, length=5)

cv2.imshow('Pose', img02)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('pose02.png',img02)