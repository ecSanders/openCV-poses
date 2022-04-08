import cv2
import numpy as np

rect = cv2.imread('data/rect01.png')

x=230
y=376

image = cv2.circle(rect, (x,y), radius=0, color=(0, 0, 255), thickness=-1)
cv2.imshow('Rectangle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_points = np.array([[179,244],
                       [293,200],
                       [370,284],
                       [378,312],
                       [219,347],
                       [230,376]])
                       
np.save('rect.npy',img_points)