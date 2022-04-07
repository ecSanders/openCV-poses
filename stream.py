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

# def calculate_XYZ(self,u,v):
                                      
#         #Solve: From Image Pixels, find World Points

#         uv_1=np.array([[u,v,1]], dtype=np.float32)
#         uv_1=uv_1.T
#         suv_1=self.scalingfactor*uv_1
#         xyz_c=self.inverse_newcam_mtx.dot(suv_1)
#         xyz_c=xyz_c-self.tvec1
#         XYZ=self.inverse_R_mtx.dot(xyz_c)

# return XYZ


# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Attempt conversions
       
       # Image Points
       # Where those points are in the image
        tPoints = np.zeros((4,2),dtype=np.float64)
        tPoints[0,0] = 384.3331
        tPoints[0,1] = 162.23618
        tPoints[1,0] = 385.27521
        tPoints[1,1] = 135.21503
        tPoints[2,0] = 409.36746
        tPoints[2,1] = 165.64435

        # Object Points
        # Need at least four
        # mPoints = np.zeros((4,3),dtype=np.float64)
        # mPoints[0,0] = -88.0
        # mPoints[0,1] = 88.0
        # mPoints[0,2] = 0
        # mPoints[1,0] = -88.0
        # mPoints[1,1] = 0
        # mPoints[1,2] = 0
        # mPoints[2,0] = 88.0
        # mPoints[2,1] = 0
        # mPoints[2,2] = 0
        # mPoints[3,0] = 88.0
        # mPoints[3,1] = 0
        # mPoints[3,2] = 0
        nx = 8
        ny = 7
        ret, corners = cv2.findChessboardCorners(cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY), (nx, ny), None)
        
        if ret == True:
            cv2.drawChessboardCorners(color_image, (nx, ny), corners, ret)
        else:
            print(ret)


        camera_matrix = np.array([[667.496, 0, 472.685],
                                  [0, 667.496, 268.163],
                                  [0,       0,    1   ]])


        dist_coefs = np.array([0,0,0,0,0])

        # found,rvec,tvec = cv2.solvePnP(mPoints, tPoints, camera_matrix, distCoeffs=None)

        # cv2.drawFrameAxes(color_image, camera_matrix, distCoeffs=None, rvec=rvec, tvec=tvec, length=100)


        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()