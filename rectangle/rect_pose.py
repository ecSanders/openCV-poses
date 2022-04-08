import cv2
import numpy as np

img = cv2.imread('data/rect01.png')
imgp = np.load('data/rect.npy')

objp = np.zeros((6,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:1].T.reshape(-1,2)
print(objp)

camera_matrix = np.array([[667.496, 0, 472.685],
                          [0, 667.496, 268.163],
                          [0,       0,    1   ]])

dist_coefs = np.array([0,0,0,0,0])

found,rvec,tvec = cv2.solvePnP(objp, imgp, camera_matrix, distCoeffs=None)

cv2.drawFrameAxes(img, camera_matrix, distCoeffs=None, rvec=rvec, tvec=tvec, length=5)

cv2.imshow('Pose', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
