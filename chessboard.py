## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        color_image = np.asanyarray(color_frame.get_data())
        gray_img = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)

        nx = 4
        ny = 3
        ret, corners = cv2.findChessboardCorners(gray_img, (nx, ny), None)
        
        if ret == True:
            cv2.drawChessboardCorners(color_image, (nx, ny), corners, ret)
            corners = cv2.cornerSubPix(gray_img,corners,(nx,ny),(-1,-1),criteria)
            cv2.imwrite('image02.png',color_image)
            np.save('corners02', corners)
            print('Saved!')
            break


        cv2.imshow('RealSense', color_image)
        cv2.waitKey(1)

        # camera_matrix = np.array([[667.496, 0, 472.685],
        #                           [0, 667.496, 268.163],
        #                           [0,       0,    1   ]])
        # dist_coefs = np.array([0,0,0,0,0])
finally:

    # Stop streaming
    pipeline.stop()